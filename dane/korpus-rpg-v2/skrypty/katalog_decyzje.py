"""Stosuje progi z preregistracja.json ('katalog_i_listy') do pełnego przebiegu detektora. Liczy test negatywny (1000 losowych wierszy fikcji, nowe ziarno).
Argumenty: wejscie.parquet katalog_k wyjscie_decyzje.json."""
import collections
import json
import os
import random
import sys

import pyarrow.parquet as pq

P, K, WY = sys.argv[1], sys.argv[2], sys.argv[3]
w = []
for f in sorted(os.listdir(K)):
    if f.startswith("k_"):
        w += json.load(open(f"{K}/{f}", encoding="utf-8"))
pf = pq.ParquetFile(P)
if len(w) != pf.metadata.num_rows:
    raise SystemExit(f"niepełny przebieg detektora: {len(w)} != {pf.metadata.num_rows}")
meta = {}
for g in range(pf.num_row_groups):
    for i, a in enumerate(pf.read_row_group(g, columns=["tokeny", "atrybucja"]).to_pylist()):
        meta[(g, i)] = (a["tokeny"], json.loads(a["atrybucja"]).get("kategoria"))


def flagi(x):
    p = []
    if x["zr"] != "gutenberg":
        return p
    if x["kat2_frac"] >= 0.2:
        p.append("katalog")
    if x["idx_frac"] >= 0.7:
        p.append("indeks")
    if x["lnum_zn"] >= 0.4 and x["linii"] >= 10:
        p.append("spis")
    if x["tab_frac"] >= 0.5:
        p.append("tabela")
    return p


ozn = [(x, flagi(x)) for x in w]
ozn = [t for t in ozn if t[1]]
licz = collections.Counter()
tok = collections.Counter()
for x, kl in ozn:
    for k in kl:
        licz[k] += 1
    pierwsza = kl[0]
    tok[pierwsza] += meta[(x["rg"], x["i"])][0]
fik = [x for x in w if x["zr"] == "gutenberg" and meta[(x["rg"], x["i"])][1] == "fikcja"]
rng = random.Random(20261121)
prob = rng.sample(fik, 1000)
neg = [(x["id"], flagi(x)) for x in prob if flagi(x)]
wyj = {"wiersze": [{"rg": x["rg"], "i": x["i"], "id": x["id"], "zrodlo": x["zr"], "klasy": kl} for x, kl in ozn],
       "liczby": {"wiersze_z_klasa": dict(licz), "wiersze_razem": len(ozn), "tokeny_wg_pierwszej_klasy": dict(tok)},
       "test_negatywny_pelny_przebieg": {"probka": "1000 losowych wierszy fikcji z pełnego korpusu, ziarno 20261121", "oznaczone": len(neg), "przyklady": neg[:20]},
       "pozytyw_51718_cz10": [flagi(x) for x in w if x["id"] == "51718/cz10"]}
json.dump(wyj, open(WY, "w", encoding="utf-8"), ensure_ascii=False)
print(json.dumps({k: wyj[k] for k in ("liczby", "test_negatywny_pelny_przebieg", "pozytyw_51718_cz10")}, ensure_ascii=False))
