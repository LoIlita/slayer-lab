"""Kalibracja progów na próbce: rozkłady, negatywna próba losowych wierszy fikcji, odczyt fragmentów. Argumenty: wejscie.parquet katalog_k wyjscie_md."""
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
gut = [x for x in w if x["zr"] == "gutenberg"]
pf = pq.ParquetFile(P)
rej = {}
tok = {}
for g in sorted({x["rg"] for x in gut}):
    t = pf.read_row_group(g, columns=["atrybucja", "tokeny", "id_zrodla"]).to_pylist()
    for i, a in enumerate(t):
        rej[(g, i)] = json.loads(a["atrybucja"]).get("kategoria")
        tok[(g, i)] = a["tokeny"]


def flaga(x, pk, pi, pl, pt):
    p = []
    if x["kat2_frac"] >= pk:
        p.append("katalog")
    if x["idx_frac"] >= pi:
        p.append("indeks")
    if x["lnum_zn"] >= pl and x["linii"] >= 10:
        p.append("spis")
    if x["tab_frac"] >= pt:
        p.append("tabela")
    return p


linie = []
for pk in (0.1, 0.2, 0.3):
    c = collections.Counter()
    tk = collections.Counter()
    for x in gut:
        for p in flaga(x, pk, 0.7, 0.4, 0.5):
            c[p] += 1
            tk[p] += tok[(x["rg"], x["i"])]
    linie.append(f"progi kat2={pk} idx=0.5 lnum=0.5 tab=0.5: {dict(c)} tokeny {dict(tk)}")
print("\n".join(linie))
print("pozytyw 51718/cz10:", [(x["kat2_frac"], x["kat_k4"]) for x in gut if x["id"] == "51718/cz10"])

rng = random.Random(20261110)
fik = [x for x in gut if rej[(x["rg"], x["i"])] == "fikcja"]
neg = rng.sample(fik, 300)
trafione = [(x, flaga(x, 0.2, 0.7, 0.4, 0.5)) for x in neg]
print("wszystkie wg progu w próbce:", collections.Counter(p for x in gut for p in flaga(x, 0.2, 0.7, 0.4, 0.5)))
print("spis (idx<0.7) do oka:", [(x["id"], x["lnum_zn"], x["idx_frac"]) for x in gut if x["lnum_zn"] >= 0.4 and x["linii"] >= 10 and x["idx_frac"] < 0.7][:25])
trafione = [t for t in trafione if t[1]]
print("negatywna: 300 losowych wierszy fikcji; oznaczone:", len(trafione), [(t[0]["id"], t[1], round(t[0]["kat2_frac"], 2)) for t in trafione])


def tekst(g, i):
    return pf.read_row_group(g, columns=["text"]).column(0)[i].as_py()


with open(WY, "w", encoding="utf-8") as f:
    f.write(f"## Rozkłady\n{chr(10).join(linie)}\n\n## Negatywna: oznaczone wśród 300 losowych wierszy fikcji\n")
    for x, pr in trafione:
        t = tekst(x["rg"], x["i"])
        f.write(f"- {x['id']} {pr} k2={x['kat2_frac']:.2f} idx={x['idx_frac']:.2f} lnum={x['lnum_udz']:.2f} tab={x['tab_frac']:.2f} | {t[:300]!r}\n")
    f.write("\n## Oznaczone katalogiem kat2>=0.2 z niskim k4 (typ okładkowy), do oka\n")
    gr = sorted([x for x in gut if 0.2 <= x["kat2_frac"] < 0.35], key=lambda x: x["kat2_frac"])
    for x in rng.sample(gr, min(25, len(gr))):
        t = tekst(x["rg"], x["i"])
        f.write(f"- {x['id']} k2={x['kat2_frac']:.2f} k4={x['kat_k4']:.2f} zn={x['zn']} | {t[-280:]!r}\n")
    f.write("\n## Proza z kwotami (powinna nie być w katalogu): top wg ceny, kat2<0.2\n")
    pr = sorted([x for x in gut if x["kat2_frac"] < 0.2], key=lambda x: -x["ceny"])[:15]
    for x in pr:
        f.write(f"- {x['id']} ceny={x['ceny']} k2={x['kat2_frac']:.2f} k4={x['kat_k4']:.2f}\n")
