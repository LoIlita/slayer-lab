"""Niezależna kontrola paczki: rozmiary, rosnące offsety, EOT=0 na każdym końcu i nigdzie indziej, id w słowniku, długość każdego dokumentu równa n_tokens z shardów
w kolejności shardów, suma tokenów równa liczbom budowy, ponowne kodowanie pierwszego i ostatniego dokumentu. Kod wyjścia != 0 przy błędzie.
Argumenty: katalog_paczki katalog_korpusu tokenizer.json liczby_budowy.json|- wyjscie.json [limit_wierszy]."""
import hashlib
import json
import os
import sys

import numpy as np
import pyarrow.parquet as pq
from tokenizers import Tokenizer

PA, KOR, TOK, LB, WY = sys.argv[1:6]
LIMIT = int(sys.argv[6]) if len(sys.argv) > 6 else None
bl = []
b = f"{PA}/train.bin"
idx = np.fromfile(f"{PA}/docs.idx", dtype="<u8")
dane = np.memmap(b, dtype="<u2", mode="r")
if os.path.getsize(b) % 2:
    bl.append("nieparzysty rozmiar bin")
if len(idx) == 0 or int(idx[-1]) != len(dane):
    bl.append(f"ostatni offset {idx[-1] if len(idx) else None} != tokenów w bin {len(dane)}")
if len(idx) > 1 and not np.all(np.diff(idx.astype(np.int64)) > 0):
    bl.append("offsety nie rosną")
if not np.all(dane[idx.astype(np.int64) - 1] == 0):
    bl.append("brak EOT na końcu dokumentu")
tk = Tokenizer.from_file(TOK)
voc = tk.get_vocab_size(with_added_tokens=True)
zera, mx = 0, 0
for s in range(0, len(dane), 1 << 26):
    c = np.asarray(dane[s:s + (1 << 26)])
    zera += int((c == 0).sum())
    mx = max(mx, int(c.max()))
if zera != len(idx):
    bl.append(f"zer w bin {zera} != dokumentów {len(idx)}")
if mx >= voc:
    bl.append(f"max id {mx} >= słownik {voc}")
k = f"{KOR}/data/default"
pliki = sorted(f"{k}/{p}" for p in os.listdir(k) if p.startswith("train-"))
n = []
pierwszy = ostatni = None
for p in pliki:
    pf = pq.ParquetFile(p)
    for g in range(pf.num_row_groups):
        t = pf.read_row_group(g, columns=["text", "n_tokens"]).to_pylist()
        if pierwszy is None:
            pierwszy = t[0]["text"]
        n += [x["n_tokens"] for x in t]
        if LIMIT is None:
            ostatni = t[-1]["text"]
        elif len(n) >= LIMIT:
            ostatni = t[LIMIT - 1 - (len(n) - len(t))]["text"]
            break
    if LIMIT is not None and len(n) >= LIMIT:
        break
if LIMIT is not None:
    n = n[:LIMIT]
n = np.asarray(n, dtype=np.int64)
dl = np.diff(np.concatenate([[0], idx.astype(np.int64)]))
if len(dl) != len(n):
    bl.append(f"dokumentów {len(dl)} != wierszy {len(n)}")
elif not np.array_equal(dl, n):
    bl.append(f"długości różne od n_tokens w {int((dl != n).sum())} dokumentach")
if LIMIT is None and LB != "-":
    oczek = json.load(open(LB, encoding="utf-8"))["default/train"]
    if oczek["tokeny"] != len(dane):
        bl.append(f"tokeny bin {len(dane)} != liczby budowy {oczek['tokeny']}")
    if oczek["wierszy"] != len(idx):
        bl.append(f"dokumenty {len(idx)} != liczby budowy {oczek['wierszy']}")
for nazwa, tekst, od, do in (("pierwszy", pierwszy, 0, int(idx[0])), ("ostatni", ostatni, int(idx[-2]) if len(idx) > 1 else 0, int(idx[-1]))):
    if tk.encode(tekst, add_special_tokens=False).ids + [0] != dane[od:do].tolist():
        bl.append(f"dokument {nazwa}: kodowanie różne od bin")
hb = hashlib.sha256()
with open(b, "rb") as f:
    for c in iter(lambda: f.read(1 << 24), b""):
        hb.update(c)
wyn = {"status": "PASS" if not bl else "FAIL", "bledy": bl, "dokumentow": len(idx), "tokenow_z_eot": len(dane), "zer_w_bin": zera, "max_id": mx, "rozmiar_slownika": voc,
       "tokenizer_sha256": hashlib.sha256(open(TOK, "rb").read()).hexdigest(), "train_bin_sha256": hb.hexdigest(), "format": "train.bin uint16 LE, docs.idx uint64 LE (końcowe offsety), EOT=0 po każdym dokumencie", "pliki": ["paczka-slayera/train.bin", "paczka-slayera/docs.idx", "paczka-slayera/tokenizer.json", "paczka-slayera/train.meta.json"]}
json.dump(wyn, open(WY, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(wyn, ensure_ascii=False))
sys.exit(0 if not bl else 1)
