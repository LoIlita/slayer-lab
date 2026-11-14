"""Paczka treningowa Slayera: dla jednego splitu configu default tworzy <split>.bin (uint16 LE) i <split>.idx (uint64 LE, końcowe offsety) z EOT=0 po każdym dokumencie.
Argumenty: katalog_korpusu tokenizer.json config split katalog_wyjscia procesy [limit w WIERSZACH].
Uruchamiać dopiero po rozstrzygnięciu, który tokenizer jest właściwy (sprawdzenie sha i rozmiaru słownika na początku)."""
import hashlib
import json
import multiprocessing as mp
import os
import sys

os.environ["TOKENIZERS_PARALLELISM"] = "false"
import numpy as np  # noqa: E402
import pyarrow.parquet as pq  # noqa: E402
from tokenizers import Tokenizer  # noqa: E402

KOR, TOK, CFG, SPLIT, OUT, PROC = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], int(sys.argv[6])
LIMIT = int(sys.argv[7]) if len(sys.argv) > 7 else None
TK = None


def init():
    global TK
    TK = Tokenizer.from_file(TOK)


def grupa(a):
    p, g = a
    t = pq.ParquetFile(p).read_row_group(g, columns=["text"]).column(0).to_pylist()
    wyj = [e.ids for e in TK.encode_batch(t, add_special_tokens=False)]
    return wyj


def main():
    os.makedirs(OUT, exist_ok=True)
    tk = Tokenizer.from_file(TOK)
    sha = hashlib.sha256(open(TOK, "rb").read()).hexdigest()
    voc = tk.get_vocab_size(with_added_tokens=True)
    if tk.id_to_token(0) != "<|endoftext|>":
        raise SystemExit("token 0 to nie <|endoftext|>: " + str(tk.id_to_token(0)))
    pliki = sorted(f"{KOR}/data/{CFG}/{p}" for p in os.listdir(f"{KOR}/data/{CFG}") if p.startswith(SPLIT + "-") and p.endswith(".parquet"))
    wsad = []
    w_wsadzie = 0
    for p in pliki:
        md = pq.ParquetFile(p).metadata
        for g in range(md.num_row_groups):
            if LIMIT is None or w_wsadzie < LIMIT:
                wsad.append((p, g))
                w_wsadzie += md.row_group(g).num_rows
    binp = f"{OUT}/{SPLIT}.bin"
    idx = f"{OUT}/docs.idx" if SPLIT == "train" else f"{OUT}/{SPLIT}.idx"
    koniec, dok, max_id = 0, 0, 0
    with open(binp, "wb") as fb, open(idx, "wb") as fi, mp.get_context("fork").Pool(PROC, initializer=init) as p:
        for lista in p.imap(grupa, wsad, chunksize=1):
            for ids in lista:
                if LIMIT is not None and dok >= LIMIT:
                    break
                a = np.asarray(ids + [0], dtype=np.uint16)
                if len(ids) and max(ids) >= 65536:
                    raise SystemExit("id poza uint16")
                max_id = max(max_id, int(a.max()))
                a.tofile(fb)
                koniec += len(a)
                np.asarray([koniec], dtype=np.uint64).tofile(fi)
                dok += 1
    meta = {"config": CFG, "split": SPLIT, "dokumentow": dok, "tokenow_z_eot": koniec, "max_id": max_id, "tokenizer_sha256": sha, "rozmiar_slownika": voc, "format": "uint16 LE + uint64 LE, EOT=0 po każdym dokumencie"}
    json.dump(meta, open(f"{OUT}/{SPLIT}.meta.json", "w", encoding="utf-8"), indent=1)
    print(json.dumps(meta, ensure_ascii=False))


if __name__ == "__main__":
    main()
