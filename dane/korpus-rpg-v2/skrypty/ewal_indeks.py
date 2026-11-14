"""Buduje indeks 13-gramów i krótkich napisów (<13 słów) z pobranych zbiorów ewaluacyjnych.
Argumenty: pobrania_ewal status_pobran.json wyjscie."""
import csv
import json
import os
import re
import sys

import numpy as np
import pyarrow.parquet as pq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rdzen as r  # noqa: E402

D, ST, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(OUT, exist_ok=True)
MAKS = 12
POMIN = re.compile(r"^(id|_id|idx|index|qid|uid|pairid|linguistics_term|field|label|labels|answerkey|answer_key|ans|gold|gold_index|ind|url|split|split_type|activity_label|source|domain|subject|category|tags?|date|timestamp|meta|phenomenon|lang|language)$", re.I)


def wypisz(o, k=None, w_liscie=False, skal=None, lst=None):
    if isinstance(o, str):
        if k is None or not POMIN.match(k):
            (lst if w_liscie else skal).append(o)
    elif isinstance(o, dict):
        for kk, v in o.items():
            wypisz(v, kk, w_liscie, skal, lst)
    elif isinstance(o, (list, tuple)):
        for v in o:
            wypisz(v, k, True, skal, lst)


def teksty_wiersza(w):
    skal, lst = [], []
    wypisz(w, None, False, skal, lst)
    s = [x for x in skal if x and x.strip()]
    e = [x for x in lst if x and x.strip()]
    out = list(s) + list(e)
    for a, b in zip(s, s[1:]):
        out.append(a + " " + b)
    if len(s) > 2:
        out.append(" ".join(s))
    for a in s:
        if len(a) < 20000:
            for b in e:
                out.append(a + " " + b)
    if isinstance(w.get("sentence"), str) and "_" in w["sentence"]:
        for o in ("option1", "option2"):
            if isinstance(w.get(o), str):
                out.append(w["sentence"].replace("_", w[o]))
    return out


def czytaj_wiersze(tid, wpis):
    for p in wpis["pliki"]:
        pelna = f"{D}/{tid}/{p['plik']}"
        if p.get("format") == "tsv":
            with open(pelna, encoding="utf-8", newline="") as f:
                yield from csv.DictReader(f, delimiter="\t")
        elif p.get("format") == "jsonl":
            with open(pelna, encoding="utf-8") as f:
                for x in f:
                    if x.strip():
                        yield json.loads(x)
        else:
            pf = pq.ParquetFile(pelna)
            for batch in pf.iter_batches(batch_size=512):
                yield from batch.to_pylist()


status = json.load(open(ST, encoding="utf-8"))
wyn = {}
wsz13 = []
wsz_kr = {n: [] for n in range(1, MAKS + 1)}
for tid, wpis in sorted(status.items()):
    if wpis.get("status") != "OK":
        wyn[tid] = {"status": "BLOCKED", "powod": wpis.get("powod") or wpis.get("powod_blocked")}
        continue
    n13 = []
    kr = {n: set() for n in range(1, MAKS + 1)}
    wier, teks = 0, 0
    try:
        for w in czytaj_wiersze(tid, wpis):
            wier += 1
            for t in teksty_wiersza(w):
                teks += 1
                h = r.hasze_slow(r.norm_slowa(t))
                if len(h) >= r.N_EVAL:
                    n13.append(np.unique(r.ngramy(h, r.N_EVAL)))
                elif 1 <= len(h) <= MAKS:
                    kr[len(h)].add(int(r.ngramy(h, len(h))[0]))
    except Exception as e:  # noqa: BLE001
        wyn[tid] = {"status": "BLOCKED", "powod": f"{type(e).__name__}: {str(e)[:300]}"}
        continue
    x = np.unique(np.concatenate(n13)) if n13 else np.zeros(0, dtype=np.uint64)
    np.save(f"{OUT}/{tid}__13.npy", x)
    kraw = {f"n{n}": np.array(sorted(v), dtype=np.uint64) for n, v in kr.items()}
    np.savez(f"{OUT}/{tid}__krotkie.npz", **kraw)
    wyn[tid] = {"status": "OK", "wierszy": wier, "tekstow": teks, "ngramow_13": int(len(x)), "krotkich": {k: int(len(v)) for k, v in kraw.items()}, "repo": wpis.get("repo"), "rewizja": wpis.get("rewizja"), "pliki": len(wpis["pliki"]), "zrodlo": wpis.get("zrodlo")}
    wsz13.append(x)
    for n in range(1, MAKS + 1):
        wsz_kr[n].append(kraw[f"n{n}"])
    print(tid, wier, teks, len(x), flush=True)
wsz = np.unique(np.concatenate(wsz13))
np.save(f"{OUT}/wszystkie_13.npy", wsz)
np.savez(f"{OUT}/wszystkie_krotkie.npz", **{f"n{n}": np.unique(np.concatenate(v)) if v else np.zeros(0, dtype=np.uint64) for n, v in wsz_kr.items()})
json.dump(wyn, open(f"{OUT}/status_indeks.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ogolem", len(wsz), {k: int(len(v)) for k, v in np.load(f"{OUT}/wszystkie_krotkie.npz").items()}, flush=True)
print("KONIEC", flush=True)
