"""Re-export of an already exported part with the prose mask of obfuscated e-mails (slayer-lab: annex
`aneks_2026_11_27_zaciemnione_proza` in the source's preregistration, pattern list EMAIL_PROSE_OBF in mat_wybor.py).

The pool of the part is not rebuilt (the local copies of the web sources were deleted): rows are read from the previous export
of the part (same ids, same order, every row field unchanged), the text goes through mat_wybor.premask_emails(prose_obf=True)
and shard.write runs again, so the language gate, dedup, token counts and stats are those of a normal export. shard.write
cannot see the rows the previous export dropped nor the e-mails it masked before, so those counters of the previous
stats.json are added to the new one (stats stay cumulative over the pool of the part).

Usage: python src/reexport_masked.py <previous.parquet> <previous.stats.json> <key>"""
import json
import sys
from pathlib import Path

import pyarrow.parquet as pq

import mat_wybor
import shard

OLD, OLD_STATS, KEY = sys.argv[1:4]


def build():
    for b in pq.ParquetFile(OLD).iter_batches(batch_size=20000, columns=list(shard.ROW_FIELDS)):
        for r in b.to_pylist():
            r["text"] = mat_wybor.premask_emails(r["text"], prose_obf=True)
            yield r


if __name__ == "__main__":
    old = json.loads(Path(OLD_STATS).read_text(encoding="utf-8"))
    mat_wybor.no_masking(emails=True)
    stats = shard.write(KEY, build())
    for reason, n in old["dropped"].items():
        stats["dropped"][reason] += n
    stats["pii"]["counts"]["pii"] += old["pii"]["counts"]["pii"]
    stats["pii"]["masked_in_this_reexport"] = mat_wybor.MASKED["pii"]
    out = shard.ROOT / "data" / KEY / f"{KEY}.stats.json"
    out.write_text(json.dumps(stats, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(stats)
