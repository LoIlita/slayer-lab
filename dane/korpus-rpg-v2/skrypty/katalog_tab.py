"""Podgląd wierszy z tab_frac/lnum wysokim bez wysokiego idx_frac: czy to tabele i spisy, czy proza. Argumenty: wejscie.parquet katalog_k."""
import json
import os
import random
import sys

import pyarrow.parquet as pq

P, K = sys.argv[1], sys.argv[2]
w = []
for f in sorted(os.listdir(K)):
    if f.startswith("k_"):
        w += json.load(open(f"{K}/{f}", encoding="utf-8"))
g = [x for x in w if x["zr"] == "gutenberg"]
pf = pq.ParquetFile(P)


def tekst(x, a, n=200):
    t = pf.read_row_group(x["rg"], columns=["text"]).column(0)[x["i"]].as_py()
    s = int(a * len(t))
    return t[s:s + n].replace("\n", " ⏎ ")


rng = random.Random(1)
for tyt, lst in (("TABELA tab>=.5 idx<.5", [x for x in g if x["tab_frac"] >= 0.5 and x["idx_frac"] < 0.5]), ("SPIS lnum_zn>=.4 idx<.7", [x for x in g if x["lnum_zn"] >= 0.4 and x["linii"] >= 10 and x["idx_frac"] < 0.7]),
                 ("INDEKS idx>=.7", [x for x in g if x["idx_frac"] >= 0.7])):
    print("###", tyt, len(lst))
    for x in rng.sample(lst, min(18, len(lst))):
        print(f"{x['id']} tab={x['tab_frac']:.2f} lnum={x['lnum_udz']:.2f} idx={x['idx_frac']:.2f} zn={x['zn']} | {tekst(x, 0.5)}")
