"""Porównanie nowego eksportu części z poprzednim (po aneksie maskowania): te same id w tej samej kolejności (nowy może
nie mieć wierszy, które po masce odrzuciła bramka języka albo dedup shard.write — lista 'usuniete'), a tekst nowy = tekst
poprzedni po masce z flagą (code_obf: EMAIL_CODE_OBF, Stack-Edu; prose_obf: EMAIL_PROSE_OBF, źródła stron, aneks
zaciemnione_proza; obie przez mat_wybor._mask_emails, czyli razem z EMAIL i EMAIL_AT); pozostałe kolumny bez zmian, a
token_count zmienia się tylko w wierszach ze zmienionym tekstem.
Użycie: python porownaj_eksporty.py <stary.parquet> <nowy.parquet> [code_obf|prose_obf] [wynik.json]"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "eksport", "src"))
sys.modules["pii"] = type(sys)("pii")
import mat_wybor as m  # noqa: E402
import pyarrow.parquet as pq  # noqa: E402

A, B = pq.ParquetFile(sys.argv[1]), pq.ParquetFile(sys.argv[2])
FLAGA = sys.argv[3] if len(sys.argv) > 3 else "code_obf"
assert FLAGA in ("code_obf", "prose_obf"), FLAGA
KOL = A.schema_arrow.names
assert KOL == B.schema_arrow.names, (KOL, B.schema_arrow.names)
wyn = {"flaga": FLAGA, "wiersze_stary": A.metadata.num_rows, "wiersze_nowy": B.metadata.num_rows, "tekst_zmieniony": 0,
       "usuniete": [], "niezgodne": 0, "przyklady_niezgodne": [], "token_count_zmieniony_poza_zmienionym_tekstem": 0}


def wiersze(f):
    for b in f.iter_batches(batch_size=20000, columns=KOL):
        yield from b.to_pylist()


ib = wiersze(B)
y = next(ib, None)
for x in wiersze(A):
    if y is None or x["id"] != y["id"]:
        wyn["usuniete"].append(x["id"])
        continue
    zgodny = m._mask_emails(x["text"], **{FLAGA: True})[0] == y["text"] and all(
        x[k] == y[k] for k in KOL if k not in ("text", "token_count"))
    wyn["tekst_zmieniony"] += x["text"] != y["text"]
    if x["text"] == y["text"] and x["token_count"] != y["token_count"]:
        wyn["token_count_zmieniony_poza_zmienionym_tekstem"] += 1
    if not zgodny:
        wyn["niezgodne"] += 1
        if len(wyn["przyklady_niezgodne"]) < 5:
            wyn["przyklady_niezgodne"].append(x["id"])
    y = next(ib, None)
assert y is None, "nowy eksport ma wiersze spoza starego"
print(json.dumps(wyn, ensure_ascii=False))
if len(sys.argv) > 4:
    json.dump(wyn, open(sys.argv[4], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
