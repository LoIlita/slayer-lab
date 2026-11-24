"""Helpers for the slayer-lab maths sources (finemath_4plus_en, cranemath_en, stack_edu_python).

Rows come from the filtered pool built in slayer-lab (dane/<set>/skrypty/odtworz.sh: pula, przebieg, agreguj): `wybor.json`
lists the global row numbers kept after every filter and chosen up to the export token target, and the pool units
(parquet path, row group) they live in. The text is passed to shard.write unchanged.

`parallel_pii(processes)` runs pii.mask in worker processes on slices of the input. It calls the same pii.mask on each
slice, so the masked text and the counts are the same as one call; only the wall time changes."""
import json
import multiprocessing as mp
from collections import Counter

import pyarrow.parquet as pq

import pii


def rows(wybor_path: str, columns: list[str]):
    """Kept pool rows in pool order, as dicts with the requested columns."""
    w = json.load(open(wybor_path, encoding="utf-8"))
    starts, units = w["poczatki"], w["jednostki"]
    by_unit: dict[int, list[int]] = {}
    u = 0
    for g in w["dokumenty_globalne"]:
        while starts[u + 1] <= g:
            u += 1
        by_unit.setdefault(u, []).append(g - starts[u])
    for u in sorted(by_unit):
        path, rg = units[u]
        t = pq.ParquetFile(path).read_row_group(rg, columns=columns).to_pylist()
        for i in by_unit[u]:
            yield t[i]


_serial_mask = pii.mask


def _mask_slice(args):
    texts, language, names = args
    return _serial_mask(texts, language, names=names)


def parallel_pii(processes: int, slice_size: int = 500) -> None:
    def mask(texts, language, *, names=False):
        if len(texts) <= slice_size:
            return _serial_mask(texts, language, names=names)
        parts = [(texts[a:a + slice_size], language, names) for a in range(0, len(texts), slice_size)]
        out, counts = [], Counter()
        with mp.get_context("fork").Pool(processes) as pool:
            for masked, c in pool.imap(_mask_slice, parts, chunksize=1):
                out.extend(masked)
                counts.update(c)
        return out, dict(counts)

    pii.mask = mask
