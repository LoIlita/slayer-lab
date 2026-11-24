"""Pomiar przed aneksem 24.11d: dokumenty wybrane do eksportu CraneMath, które nadal pasują do regex_tekst reguły suma40 (bo
tekst przed przepisaniem zawiera gdzieś liczbę 40), i ile z nich ma w oryginale samo zadanie o sumie do 40.
Argumenty: wybor.json przebieg_oryg/jednostki.json preregistracja.json wyjscie.json"""
import json
import re
import sys

import pyarrow.parquet as pq

WYB, JO, PRE, OUT = sys.argv[1:5]
w = json.load(open(WYB, encoding="utf-8"))
jo = json.load(open(JO, encoding="utf-8"))
p = json.load(open(PRE, encoding="utf-8"))["aneks_2026_11_24c"]["suma40"]
rx_t = re.compile(p["regex_tekst"])
rx_zad = re.compile(r"(?i)(1\s*(to|through|-|–|\.\.\.?|…)\s*40\b|1\s*\+\s*2\s*\+.{0,20}\+\s*40\b|first\s+40\s+(natural|positive|counting)?\s*(numbers|integers))")
sel = set(w["dokumenty_globalne"])
traf, z_zad, przyk = 0, 0, []
for u, ((pt, g), (po, go)) in enumerate(zip(w["jednostki"], jo)):
    t = pq.ParquetFile(pt).read_row_group(g, columns=["text"]).column(0).to_pylist()
    o = pq.ParquetFile(po).read_row_group(go, columns=["text"]).column(0).to_pylist()
    for j, (a, b) in enumerate(zip(t, o)):
        gi = w["poczatki"][u] + j
        if gi in sel and rx_t.search(a or ""):
            traf += 1
            ma = bool(rx_zad.search(b or ""))
            z_zad += ma
            if len(przyk) < 15:
                m = rx_zad.search(b or "")
                przyk.append({"nr": gi, "oryginal_ma_zadanie": ma, "fragment": (b or "")[max(0, m.start() - 60):m.end() + 60] if m else None})
wyn = {"wybrane_pasujace_do_regex_tekst": traf, "z_zadaniem_w_oryginale": z_zad, "bez_zadania": traf - z_zad, "regex_zadanie": rx_zad.pattern,
       "przyklady": przyk}
json.dump(wyn, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print({k: v for k, v in wyn.items() if k != "przyklady"})
