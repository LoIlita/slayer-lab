"""Dzieli wybór do eksportu (wybor.json z agreguj_mat.py) na kolejne części po ok. `cel` tokenów v6, w kolejności puli.

Po co: shard.write i check.py repo zgłoszeń trzymają cały zbiór w pamięci (lista wierszy, table.to_pylist()), a pełne pule
części 2 to po kilka mld tokenów (kilkadziesiąt GB tekstu) przy 48 GB RAM. Każda część to osobny klucz <klucz>_pNN.
Tokeny dokumentów z przebiegu (ntok w u_NNNN.npz), więc bez ponownego czytania tekstów.
Użycie: python czesci.py <wybor.json> <katalog_przebiegu> <cel_tokenow_v6> <katalog_wyjscia>
Wyjście: <katalog_wyjscia>/wybor_pNN.json (format wybor.json) i czesci.json (dokumenty i tokeny na część)."""
import json
import os
import sys

import numpy as np

WYB, PRZ, CEL, OUT = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
w = json.load(open(WYB, encoding="utf-8"))
jed = json.load(open(f"{PRZ}/jednostki.json"))
ntok = np.concatenate([np.load(f"{PRZ}/u_{k:04d}.npz")["ntok"] for k in range(len(jed))])
g = np.asarray(w["dokumenty_globalne"], np.int64)
assert len(ntok) == w["poczatki"][-1], "przebieg i wybor z różnych pul"
narast = np.cumsum(ntok[g])
n = max(1, int(round(narast[-1] / CEL)))  # równe części, każda blisko celu
granice = np.searchsorted(narast, narast[-1] * np.arange(1, n) / n, "right")
os.makedirs(OUT, exist_ok=True)
opis = []
for i, kawalek in enumerate(np.split(g, granice), 1):
    json.dump({**w, "dokumenty_globalne": kawalek.tolist(), "czesc": i, "czesci": n},
              open(f"{OUT}/wybor_p{i:02d}.json", "w", encoding="utf-8"))
    opis.append({"czesc": i, "dokumenty": int(len(kawalek)), "tokeny_v6": int(ntok[kawalek].sum())})
json.dump({"wybor": WYB, "cel_tokenow_v6": CEL, "czesci": opis, "dokumenty": int(len(g)), "tokeny_v6": int(narast[-1])},
          open(f"{OUT}/czesci.json", "w", encoding="utf-8"), indent=1)
print(json.dumps(opis))
