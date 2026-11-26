"""Fragmenty trafień detektorów pii i mojibake dla pozycji próbki przeglądu, których tekst w próbce jest ucięty.

Po co: próbka pokazuje 3000 pierwszych znaków, a pełna praca arXiv ma medianę 25 tys. tokenów, więc telefon, adres IP
albo zepsute kodowanie leżą zwykle dalej (przegląd 26.11: 79/96 ocen pii i 16/17 mojibake 'watpliwy' z braku trafienia).
Dla pozycji z powodem pii albo mojibake czyta pełny tekst z puli (wybor.json: jednostki, poczatki) i dopisuje pole
`trafienia_fragmenty`: do 5 trafień tych samych wzorców co przebieg (wspolne.RX_TEL/RX_IP z tymi samymi wyjątkami,
przebieg.RX_SCISLE), każde z kontekstem ±300 znaków. Pozostałe pozycje bez zmian.
Użycie: python trafienia_probki.py <probka.jsonl> <wybor.json> <wyjscie.jsonl>"""
import json
import os
import re
import sys

import pyarrow.parquet as pq

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "dclm-en", "skrypty"))
from wspolne import RX_IP, RX_TEL  # noqa: E402

RX_SCISLE = re.compile(r"Ã[\x80-\xBF]|â€|Â[\x80-\xBF]|ï»¿|�|Ä[\x80-\xBF]|Å[\x80-\xBF]|Ã[¡-¿]")  # = przebieg.RX_SCISLE
KONTEKST, MAKS = 300, 5


def trafienia_pii(t):
    for m in RX_TEL.finditer(t):
        if m.group(0).startswith("+") and sum(c.isdigit() for c in m.group(0)) < 9:
            continue
        yield "telefon", m
    for m in RX_IP.finditer(t):
        o = [int(x) for x in m.groups()]
        if max(o) > 255 or o[0] in (0, 10, 127) or o == [255, 255, 255, 255] or (o[0] == 192 and o[1] == 168):
            continue
        yield "ip", m


def trafienia_moj(t):
    for m in RX_SCISLE.finditer(t):
        yield "mojibake", m


PROBKA, WYB, OUT = sys.argv[1:4]
w = json.load(open(WYB, encoding="utf-8"))
starts, units = w["poczatki"], w["jednostki"]
poz = [json.loads(x) for x in open(PROBKA, encoding="utf-8")]


def jednostka(nr):
    return next(i for i in range(len(units)) if starts[i] <= nr < starts[i + 1])


cele = sorted((o for o in poz if o.get("powod") in ("pii", "mojibake")), key=lambda o: o["nr"])
cache = {}
n = 0
for o in cele:
    u = jednostka(o["nr"])
    if u not in cache:
        cache.clear()
        cache[u] = pq.ParquetFile(units[u][0]).read_row_group(units[u][1], columns=["text"]).column(0).to_pylist()
    t = cache[u][o["nr"] - starts[u]]
    assert t.startswith(o["tekst"][:200]), f"nr {o['nr']}: tekst puli nie zgadza się z próbką"
    gen = trafienia_pii(t) if o["powod"] == "pii" else trafienia_moj(t)
    fr = []
    for klasa, m in gen:
        if len(fr) == MAKS:
            break
        fr.append({"klasa": klasa, "trafienie": m.group(0), "pozycja": m.start(),
                   "kontekst": t[max(0, m.start() - KONTEKST):m.end() + KONTEKST]})
    o["trafienia_fragmenty"] = fr
    o["dlugosc_pelnego_tekstu"] = len(t)
    n += 1
with open(OUT, "w", encoding="utf-8") as f:
    for o in poz:
        f.write(json.dumps(o, ensure_ascii=False) + "\n")
print("pozycji z fragmentami", n)
