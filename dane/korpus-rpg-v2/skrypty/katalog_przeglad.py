"""Przegląd próbki detektora katalogów: najgorsze wiersze z fragmentem najgęstszego okna; próba negatywna fikcji przy zadanych progach.
Argumenty: wejscie.parquet katalog_k tryb [progi_json]. tryb=przeglad: wyjście na stdout. tryb=negatywna: 300 losowych wierszy fikcji z próbki, ile przekracza progi."""
import json
import os
import random
import re
import sys

import pyarrow.parquet as pq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

P, K, TRYB = sys.argv[1], sys.argv[2], sys.argv[3]
sys.argv = [sys.argv[0], P, "/tmp/x", "1", "sample"]
import katalog as kt  # noqa: E402

w = []
for f in sorted(os.listdir(K)):
    if f.startswith("k_"):
        w += json.load(open(f"{K}/{f}", encoding="utf-8"))
pf = pq.ParquetFile(P)


def tekst(g, i):
    return pf.read_row_group(g, columns=["text"]).column(0)[i].as_py()


def fragment(t, n=260):
    pos = sorted([m.start() for m in kt.CENA.finditer(t)] + [m.start() for m in kt.FORMAT.finditer(t)] + [m.start() for m in kt.IDX.finditer(t)])
    best, bs = 0, -1
    for x in pos:
        c = sum(1 for p in pos if x <= p < x + 1000)
        if c > bs:
            bs, best = c, x
    return t[max(0, best - 20):best + n].replace("\n", " ⏎ ")


def wydruk(lista, tyt, klucz):
    print(f"\n=== {tyt} (n={len(lista)}) ===")
    for j, x in enumerate(lista):
        t = tekst(x["rg"], x["i"])
        print(f"{j:3d} {x['zr'][:3]} {x['id']:28s} k4={x['kat_k4']:.2f} k6={x['kat_k6']:.2f} kmax={x['kat_max']:.0f} ceny={x['ceny']} fmt={x['format']} idx={x['idx_frac']:.2f} lnum={x['lnum_udz']:.2f} tab={x['tab_frac']:.2f} zn={x['zn']} | {fragment(t)}")


gut = [x for x in w if x["zr"] == "gutenberg"]
print("wierszy w próbce", len(w), "gutenberg", len(gut), "pozytyw", [(x["id"], x["kat_k4"], x["kat_max"]) for x in gut if x["id"] == "51718/cz10"])
if TRYB == "przeglad":
    for pole, n in (("kat_k4", 100), ("idx_frac", 30), ("lnum_udz", 30), ("tab_frac", 30)):
        wydruk(sorted(gut, key=lambda x: -x[pole])[:n], "najgorsze wg " + pole, pole)
else:
    progi = json.loads(sys.argv[4]) if False else json.load(open(sys.argv[4])) if False else None
    print("użyj negatywna przez katalog_negatywna.py")
