"""Buduje parquet kontroli dodatnich (preregistracja.json -> kontrole_dodatnie) i probka_kontrola.json dla przebieg.py.
Kawałki testów brane z pobranych plików ewaluacji RPG v2, kopia z 1.07 EN dekodowana z train.bin.
Argumenty: katalog_pobran_ewal_rpg katalog_slayer107 tokenizer.json probka.parquet(do duplikatu) wyjscie_katalog
[walidacja.parquet katalog_pobran_ivme]"""
import json
import os
import sys

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
from tokenizers import Tokenizer

EW, S107, TOK, PROB, OUT = sys.argv[1:6]
os.makedirs(OUT, exist_ok=True)
TLO = ("The town council met on Tuesday to discuss the new library schedule and the budget for road repairs. "
       "Residents asked questions about parking near the school and the summer program for children. ") * 6


def pierwszy(katalog, pole):
    for f in sorted(os.listdir(katalog)):
        if f.endswith(".parquet") and ("test" in f or "valid" in f):
            w = pq.read_table(os.path.join(katalog, f)).slice(0, 1).to_pylist()[0]
            return w[pole] if isinstance(pole, str) else pole(w)
    raise SystemExit("brak pliku testu w " + katalog)


hs = pierwszy(f"{EW}/T05_hellaswag", lambda w: w["ctx"] + " " + w["endings"][0])
pi = pierwszy(f"{EW}/T06_piqa", lambda w: w["goal"] + " " + w["sol1"])
ar = pierwszy(f"{EW}/T02_arc_challenge", lambda w: w["question"] + " " + " ".join(w["choices"]["text"]))
wg = pierwszy(f"{EW}/T07_winogrande", lambda w: w["sentence"].replace("_", w["option1"]))
ends = np.fromfile(f"{S107}/en_fineweb_edu/docs.idx", dtype=np.uint64)
ids = np.memmap(f"{S107}/en_fineweb_edu/train.bin", dtype=np.uint16, mode="r")
kopia107 = Tokenizer.from_file(TOK).decode(ids[int(ends[999]):int(ends[1000])].tolist(), skip_special_tokens=True)
dup = pq.ParquetFile(PROB).read_row_group(0, columns=["text"]).column(0).to_pylist()[7]
wiersze = [
    ("K_email", "https://news.example-town.org/a", TLO + " Contact John at john.miller84@gmail.com for details."),
    ("K_telefon", "https://news.example-town.org/b", TLO + " Call the office at (415) 555-0132 after noon."),
    ("K_ip", "https://news.example-town.org/c", TLO + " The server at 84.23.117.9 went down overnight."),
    ("K_domena", "https://www.wikihow.com/Fold-a-Shirt", TLO),
    ("K_hellaswag", "https://blog.example-town.org/h", TLO + " " + hs),
    ("K_piqa", "https://blog.example-town.org/p", TLO + " " + pi),
    ("K_arc_c", "https://blog.example-town.org/a", TLO + " " + ar),
    ("K_winogrande", "https://blog.example-town.org/w", TLO + " " + wg),
    ("K_kopia_107", "https://copy.example-town.org/1", kopia107),
    ("K_dup_a", "https://dup.example-town.org/1", dup),
    ("K_dup_b", "https://dup.example-town.org/2", dup),
    ("K_czysty", "https://news.example-town.org/z", TLO),
]
if len(sys.argv) > 6:
    wal = pq.read_table(sys.argv[6]).slice(100, 1).to_pylist()[0]["text"]
    wiersze.append(("K_walidacja", "https://copy.example-town.org/2", wal))
if len(sys.argv) > 7:
    iv = sys.argv[7]
    e = np.load(f"{iv}/train-batches/train-dclm-000000/shard-00000.bin.ends.npy")
    x = np.fromfile(f"{iv}/train-batches/train-dclm-000000/shard-00000.bin", dtype=np.uint16)
    tiv = Tokenizer.from_file(f"{iv}/metadata/tokenizer.json")
    wiersze.append(("K_ivme", "https://copy.example-town.org/3", tiv.decode(x[int(e[49]):int(e[50])].tolist(), skip_special_tokens=True)))
t = pa.table({"text": [x[2] for x in wiersze], "url": [x[1] for x in wiersze], "id": [x[0] for x in wiersze]})
p = f"{OUT}/kontrola.parquet"
pq.write_table(t, p, row_group_size=5000)
json.dump({"pliki": [{"lokalnie": p}]}, open(f"{OUT}/probka_kontrola.json", "w"))
print(json.dumps({"wierszy": len(wiersze), "winogrande": wg[:80], "hellaswag": hs[:80]}, ensure_ascii=False))
