"""Próbka kontrolna (aneks 24.11c, pole probka_kontrolna): n zachowanych z końcowego wyboru do eksportu, numpy default_rng(seed+2),
podzielona na wycinki po 100 dla recenzentów; pliki zostają w robocze/ (pełne teksty). Część 2 (preregistracja czesc_2.probka
i nowe źródła): PRZESUNIECIE=3 -> default_rng(seed+3).
Argumenty: wybor.json preregistracja.json n katalog_wycinkow [przebieg_oryg_jednostki.json dla cranemath]"""
import json
import os
import sys

import numpy as np
import pyarrow.parquet as pq

WYB, PRE, N, KAT = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
ORYG = sys.argv[5] if len(sys.argv) > 5 else None
w = json.load(open(WYB, encoding="utf-8"))
seed = json.load(open(PRE, encoding="utf-8"))["seed"]
jed, pocz = w["jednostki"], w["poczatki"]
jed_o = json.load(open(ORYG, encoding="utf-8")) if ORYG else None
wyb = np.sort(np.random.default_rng(seed + int(os.environ.get("PRZESUNIECIE", "2"))).choice(np.array(w["dokumenty_globalne"]), N, replace=False))


def kol(jd, i, nazwa):
    j = int(np.searchsorted(pocz, i, "right") - 1)
    return pq.ParquetFile(jd[j][0]).read_row_group(jd[j][1], columns=[nazwa]).column(0)[int(i - pocz[j])].as_py()


os.makedirs(KAT, exist_ok=True)
poz = []
for i in wyb.tolist():
    o = {"nr": i, "grupa": "zachowany", "powod": None, "url": kol(jed, i, "url"), "tekst": kol(jed, i, "text")[:3000]}
    if jed_o is not None and len(poz) < 100:
        o["tekst_oryginalny"] = kol(jed_o, i, "text")[:3000]
    poz.append(o)
for a in range(0, len(poz), 100):
    with open(f"{KAT}/kontr_{a // 100:02d}.jsonl", "w", encoding="utf-8") as f:
        for o in poz[a:a + 100]:
            f.write(json.dumps(o, ensure_ascii=False) + "\n")
print("pozycji", len(poz), "seed", seed + int(os.environ.get("PRZESUNIECIE", "2")))
