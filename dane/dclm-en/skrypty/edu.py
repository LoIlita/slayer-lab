"""Ocena klasyfikatora FineWeb-Edu na losowej podpróbce dokumentów próbki (preregistracja.json -> fineweb_edu_klasyfikator).
Kolejność dokumentów globalnych = kolejność jednostek przebiegu (jednostki.json). Python z torch i transformers.
Argumenty: jednostki.json wyjscie.npz liczba urzadzenie [limit_czasu_s]"""
import json
import os
import sys
import time

import numpy as np
import pyarrow.parquet as pq
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

JED, OUT, ILE, DEV = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
LIMIT = float(sys.argv[5]) if len(sys.argv) > 5 else 1e9
MODEL, REW = "HuggingFaceFW/fineweb-edu-classifier", "284663cbb2dabf9bda30d8f8cc49601251ee1631"
SEED = 20261114
torch.set_num_threads(int(os.environ.get("EDU_WATKI", "4")))
jed = json.load(open(JED))
rozm = [pq.ParquetFile(p).metadata.row_group(g).num_rows for p, g in jed]
pocz = np.concatenate([[0], np.cumsum(rozm)])
N = int(pocz[-1])
wyb = np.sort(np.random.default_rng(SEED).choice(N, min(ILE, N), replace=False))
tok = AutoTokenizer.from_pretrained(MODEL, revision=REW)
mod = AutoModelForSequenceClassification.from_pretrained(MODEL, revision=REW, torch_dtype=torch.float16 if DEV == "mps" else torch.float32).to(DEV).eval()
wyn = np.full(len(wyb), np.nan, dtype=np.float32)
t0 = time.time()
k = 0
for j, (p, g) in enumerate(jed):
    w = wyb[(wyb >= pocz[j]) & (wyb < pocz[j + 1])] - pocz[j]
    if not len(w):
        continue
    tx = pq.ParquetFile(p).read_row_group(g, columns=["text"]).column(0).to_pylist()
    tx = [tx[i] for i in w]
    for b in range(0, len(tx), 64):
        x = tok(tx[b:b + 64], return_tensors="pt", padding="longest", truncation=True, max_length=512).to(DEV)
        with torch.no_grad():
            s = mod(**x).logits.squeeze(-1).float().cpu().numpy()
        wyn[k:k + len(s)] = s
        k += len(s)
    print(j, k, f"{time.time() - t0:.0f}s", flush=True)
    if time.time() - t0 > LIMIT:
        print("LIMIT CZASU", flush=True)
        break
ok = ~np.isnan(wyn)
np.savez(OUT, idx=wyb[ok], score=wyn[ok], int_score=np.clip(np.round(wyn[ok]), 0, 5).astype(np.int8))
print("KONIEC", int(ok.sum()), f"{time.time() - t0:.0f}s", flush=True)
