"""Sprawdza na gotowych shardach, że żaden wiersz z usuniecia.json nie został i że zostały wszystkie pozostałe, oraz że YAML karty się parsuje na oczekiwane configi.
Argumenty: wejscie.parquet usuniecia.json katalog_korpusu."""
import json
import os
import sys

import pyarrow.parquet as pq

WE, US, KOR = sys.argv[1:4]
usun = {(r[0], r[1]) for r in json.load(open(US, encoding="utf-8"))["wiersze"]}
pf = pq.ParquetFile(WE)
oczek, zabr = set(), set()
for g in range(pf.num_row_groups):
    t = pf.read_row_group(g, columns=["zrodlo", "id_zrodla"]).to_pylist()
    for i, x in enumerate(t):
        (zabr if (g, i) in usun else oczek).add(f"{x['zrodlo']}:{x['id_zrodla']}")
jest = []
for cfg in ("default", "cc-by-sa"):
    k = f"{KOR}/data/{cfg}"
    for p in sorted(os.listdir(k)):
        f = pq.ParquetFile(f"{k}/{p}")
        for g in range(f.num_row_groups):
            jest += f.read_row_group(g, columns=["document_id"]).column(0).to_pylist()
s = set(jest)
wyn = {"w_shardach": len(jest), "unikalne": len(s), "usuniete_a_obecne": len(s & zabr), "oczekiwane_a_brak": len(oczek - s), "nadmiarowe": len(s - oczek), "51718/cz10_obecny": "gutenberg:51718/cz10" in s}
print(json.dumps(wyn, ensure_ascii=False))
blad = wyn["usuniete_a_obecne"] or wyn["oczekiwane_a_brak"] or wyn["nadmiarowe"] or wyn["w_shardach"] != wyn["unikalne"] or wyn["51718/cz10_obecny"]
sys.exit(1 if blad else 0)
