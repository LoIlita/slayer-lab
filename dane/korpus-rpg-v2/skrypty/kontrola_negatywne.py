"""Pokazuje fragmenty wierszy oznaczonych w teście negatywnym detektora i liczy wiersze 'inny', które zostały mimo przewagi obcych słów funkcyjnych.
Argumenty: wejscie.parquet katalog_k katalog_decyzje.json katalog_przebieg wyjscie_json."""
import json
import os
import pickle
import sys

import pyarrow.parquet as pq

P, K, D, PR, WY = sys.argv[1:6]
dec = json.load(open(D, encoding="utf-8"))
ids = [x[0] for x in dec["test_negatywny_pelny_przebieg"]["przyklady"]]
w = {}
for f in sorted(os.listdir(K)):
    if f.startswith("k_"):
        for x in json.load(open(f"{K}/{f}", encoding="utf-8")):
            if x["id"] in ids:
                w[x["id"]] = x
pf = pq.ParquetFile(P)
for i in ids:
    x = w[i]
    r = pf.read_row_group(x["rg"], columns=["text", "atrybucja"]).to_pylist()[x["i"]]
    t = r["text"]
    a = json.loads(r["atrybucja"])
    print("###", i, {k: a.get(k) for k in ("tytul", "title", "kategoria")}, {k: round(x[k], 3) for k in ("kat2_frac", "idx_frac", "lnum_zn", "tab_frac")}, "znaki", len(t))
    for frac in (0.1, 0.5, 0.9):
        s = int(frac * len(t))
        print(f"[{frac}]", t[s:s + 350].replace("\n", " / "))


def regula(m):
    return (m["en"] < 0.05 and m["obcy"] >= m["en"] + 0.05) or (m["en"] < 0.03 and m["obcy"] >= m["en"]) or (m["nielat"] >= 0.30 and m["en"] < 0.05)


zost = bez = 0
for p in sorted(os.listdir(PR)):
    if p.endswith(".pkl"):
        for f in pickle.load(open(f"{PR}/{p}", "rb"))["flagi"]:
            m = f.get("jezyk")
            if m and not regula(m):
                zost += 1
                if m["obcy"] > m["en"]:
                    bez += 1
wyn = {"inny_zostawione": zost, "zostawione_z_obcy_wiekszym_niz_en": bez}
json.dump(wyn, open(WY, "w", encoding="utf-8"))
print(wyn)
