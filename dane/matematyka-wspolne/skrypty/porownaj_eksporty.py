"""Porównanie nowego eksportu części z poprzednim (po aneksie maskowania): te same id w tej samej kolejności (nowy może
nie mieć wierszy, które po masce odrzuciła bramka języka shard.write — lista 'usuniete'), a tekst nowy = tekst
poprzedni po nowych wzorcach (EMAIL_CODE_OBF); pozostałe kolumny bez zmian poza token_count.
Użycie: python porownaj_eksporty.py <stary.parquet> <nowy.parquet>"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "eksport", "src"))
sys.modules["pii"] = type(sys)("pii")
import mat_wybor as m  # noqa: E402
import pyarrow.parquet as pq  # noqa: E402

A, B = pq.ParquetFile(sys.argv[1]), pq.ParquetFile(sys.argv[2])
KOL = ["id", "text", "license", "author", "created"]
wyn = {"wiersze_stary": A.metadata.num_rows, "wiersze_nowy": B.metadata.num_rows, "tekst_zmieniony": 0, "usuniete": [],
       "niezgodne": 0, "przyklady_niezgodne": []}


def wiersze(f):
    for b in f.iter_batches(batch_size=20000, columns=KOL):
        yield from b.to_pylist()


def maska(t):
    for rx in m.EMAIL_CODE_OBF:
        t = rx.sub(lambda q: q.group(0) if q.lastindex and q.group(1).lower() in m.EXAMPLE_DOMAINS else "[PII]", t)
    return t


ib = wiersze(B)
y = next(ib, None)
for x in wiersze(A):
    if y is None or x["id"] != y["id"]:
        wyn["usuniete"].append(x["id"])
        continue
    zgodny = maska(x["text"]) == y["text"] and all(x[k] == y[k] for k in KOL if k != "text")
    wyn["tekst_zmieniony"] += x["text"] != y["text"]
    if not zgodny:
        wyn["niezgodne"] += 1
        if len(wyn["przyklady_niezgodne"]) < 5:
            wyn["przyklady_niezgodne"].append(x["id"])
    y = next(ib, None)
assert y is None, "nowy eksport ma wiersze spoza starego"
print(json.dumps(wyn, ensure_ascii=False))
