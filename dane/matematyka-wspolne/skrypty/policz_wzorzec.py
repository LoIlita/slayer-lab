"""Pomiar częstości wzorca w puli (przed decyzją o regule): ile dokumentów puli i ile wybranych do eksportu pasuje do regexu.
Argumenty: wybor.json regex wyjscie.json [maks_przykladow]"""
import json
import re
import sys

import pyarrow.parquet as pq

WYB, RX, OUT = sys.argv[1:4]
MAKS = int(sys.argv[4]) if len(sys.argv) > 4 else 20
w = json.load(open(WYB, encoding="utf-8"))
sel = set(w["dokumenty_globalne"])
rx = re.compile(RX)
n = traf = traf_sel = 0
przyklady = []
for u, (p, g) in enumerate(w["jednostki"]):
    for j, t in enumerate(pq.ParquetFile(p).read_row_group(g, columns=["text"]).column(0).to_pylist()):
        gi = w["poczatki"][u] + j
        n += 1
        m = rx.search(t or "")
        if m:
            traf += 1
            traf_sel += gi in sel
            if len(przyklady) < MAKS:
                przyklady.append({"nr": gi, "fragment": (t or "")[max(0, m.start() - 80):m.end() + 80]})
wyn = {"regex": RX, "pula": n, "trafienia_pula": traf, "wybrane": len(sel), "trafienia_wybrane": traf_sel,
       "proc_wybranych": round(100 * traf_sel / len(sel), 3), "przyklady": przyklady}
json.dump(wyn, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in wyn.items() if k != "przyklady"}, ensure_ascii=False))
