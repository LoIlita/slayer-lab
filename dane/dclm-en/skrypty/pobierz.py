"""Losuje i pobiera shardy próbki DCLM (repo parquet), zapisuje sha256 oryginału i lokalną kopię z grupami po 5000 wierszy
(tekst niezmieniony, ta sama kolejność wierszy). Wybór: preregistracja.json -> probka.
Argumenty: katalog_pobran wyniki/probka_pliki.json docelowe_wiersze wykluczone.json"""
import hashlib
import json
import os
import sys

import numpy as np
import pyarrow.parquet as pq
from huggingface_hub import HfApi, hf_hub_download

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wspolne as w  # noqa: E402

CEL, WYN, DOCEL, WYKL = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
REPO, REW = "mlfoundations/dclm-baseline-1.0-parquet", "817d6752765f6a41261085171dd546b104f60626"
PREF = "filtered/OH_eli5_vs_rw_v2_bigram_200k_train/fasttext_openhermes_reddit_eli5_vs_rw_v2_bigram_200k_train/processed_data/"
api = HfApi()
wsz = sorted(f for f in api.list_repo_files(REPO, repo_type="dataset", revision=REW) if f.endswith(".parquet"))
wykl = set(json.load(open(WYKL, encoding="utf-8"))["pliki"])
kand = [f for f in wsz if f[len(PREF):].replace(".parquet", "") not in wykl]
kolej = np.random.default_rng(w.SEED).permutation(len(kand)).tolist()
os.makedirs(CEL, exist_ok=True)
out, suma = [], 0
for i in kolej:
    f = kand[i]
    p = hf_hub_download(REPO, f, repo_type="dataset", revision=REW, local_dir=CEL)
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 24), b""):
            h.update(b)
    t = pq.read_table(p)
    lok = p.replace(".parquet", ".rg5000.parquet")
    pq.write_table(t, lok, row_group_size=5000)
    out.append({"plik": f, "shard": f[len(PREF):].replace(".parquet", ""), "rozmiar": os.path.getsize(p), "sha256": h.hexdigest(),
                "wiersze": t.num_rows, "lokalnie": lok})
    suma += t.num_rows
    print(f, t.num_rows, suma, flush=True)
    if suma >= DOCEL:
        break
json.dump({"repo": REPO, "rewizja": REW, "plikow_w_repo": len(wsz), "wykluczonych": len(wsz) - len(kand), "seed": w.SEED,
           "wiersze": suma, "pliki": out}, open(WYN, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("KONIEC", suma, flush=True)
