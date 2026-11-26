"""Wersja stokenizowana części zbioru z repo HF (obok tekstu), w formacie trenera Slayera (wygaszanie/dane.py, flaga
--dtype uint16): płaski plik uint16, przed każdym dokumentem token 0 (<|endoftext|>), dokumenty w kolejności wierszy
parquetu (bez tasowania; trener losuje okna). Tekst w data/ zostaje źródłem prawdy: inny tokenizer = ponowne uruchomienie.

Dla każdej części data/<klucz>/<klucz>.parquet: pobranie, tokenizacja strumieniowo po grupach wierszy, zapis
tokenized/<nazwa_tokenizera>/<klucz>.bin + <klucz>.json (dokumenty, tokeny, sha256 .bin i źródłowego parquetu, sha256
tokenizera), wysyłka do tego samego repo, usunięcie plików lokalnych. Wznawialne: część z istniejącym .json na HF
jest pomijana.
Użycie: python tokenizuj_hf.py <repo> <tokenizer.json> <nazwa_tokenizera> <katalog_roboczy> [klucz ...]"""
import hashlib
import json
import os
import sys

import numpy as np
import pyarrow.parquet as pq
from huggingface_hub import HfApi, hf_hub_download
from tokenizers import Tokenizer

REPO, TOKP, NAZWA, KAT = sys.argv[1:5]
TYLKO = set(sys.argv[5:])
api = HfApi()
tok = Tokenizer.from_file(TOKP)
EOT = tok.token_to_id("<|endoftext|>")
assert EOT == 0 and tok.get_vocab_size() <= 65536, "format trenera: <|endoftext|> = 0, słownik mieści się w uint16"


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 24), b""):
            h.update(b)
    return h.hexdigest()


TOK_SHA = sha(TOKP)
pliki = api.list_repo_files(REPO, repo_type="dataset")
czesci = sorted(p.split("/")[1] for p in pliki if p.startswith("data/") and p.endswith(".parquet"))
gotowe = {p.split("/")[-1][:-5] for p in pliki if p.startswith(f"tokenized/{NAZWA}/") and p.endswith(".json")}
os.makedirs(KAT, exist_ok=True)
for k in czesci:
    if (TYLKO and k not in TYLKO) or k in gotowe:
        continue
    src = hf_hub_download(REPO, f"data/{k}/{k}.parquet", repo_type="dataset", local_dir=KAT)
    out = os.path.join(KAT, f"{k}.bin")
    pf = pq.ParquetFile(src)
    docs = ntok = 0
    with open(out, "wb") as f:
        for g in range(pf.num_row_groups):
            teksty = pf.read_row_group(g, columns=["text"]).column(0).to_pylist()
            for a in range(0, len(teksty), 256):  # 256 dok.: pełne prace arXiv to ~33 tys. tokenów na dokument (OOM 26.11)
                enc = tok.encode_batch(teksty[a:a + 256], add_special_tokens=False)
                arr = np.concatenate([np.asarray([EOT] + e.ids, dtype=np.uint16) for e in enc])
                arr.tofile(f)
                docs += len(enc)
                ntok += len(arr)
    meta = {"zrodlo": f"data/{k}/{k}.parquet", "zrodlo_sha256": sha(src), "dokumenty": docs, "tokeny": ntok,
            "bin_sha256": sha(out), "dtype": "uint16", "format": "płaski uint16; token 0 <|endoftext|> przed każdym dokumentem; "
            "kolejność wierszy parquetu", "tokenizer": NAZWA, "tokenizer_sha256": TOK_SHA, "slownik": tok.get_vocab_size()}
    assert docs == pf.metadata.num_rows and os.path.getsize(out) == 2 * ntok
    mp_ = os.path.join(KAT, f"{k}.json")
    json.dump(meta, open(mp_, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    api.upload_file(path_or_fileobj=out, path_in_repo=f"tokenized/{NAZWA}/{k}.bin", repo_id=REPO, repo_type="dataset",
                    commit_message=f"tokenized/{NAZWA}: {k}")
    api.upload_file(path_or_fileobj=mp_, path_in_repo=f"tokenized/{NAZWA}/{k}.json", repo_id=REPO, repo_type="dataset",
                    commit_message=f"tokenized/{NAZWA}: {k} (metadane)")
    for p in (out, mp_, src):
        os.remove(p)
    print(k, docs, ntok, meta["bin_sha256"][:12], flush=True)
print("KONIEC", flush=True)
