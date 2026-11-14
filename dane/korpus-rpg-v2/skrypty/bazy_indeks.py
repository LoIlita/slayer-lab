"""Indeksy baz do dedupu: szkice 13-gramów (hash%16==0) i MinHash 128 z kluczami LSH 32x4 (ta sama metoda co indeks_krzyzowy.py).
slayer_107_en: bin uint16 + docs.idx, dekodowane tokenizerem z karty 1.07. technika_i_nauka: parquet.
Argumenty: pobrania tokenizer_107.json wyjscie procesy."""
import json
import multiprocessing as mp
import os
import sys
import time

os.environ["TOKENIZERS_PARALLELISM"] = "false"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np  # noqa: E402
import pyarrow.parquet as pq  # noqa: E402
from tokenizers import Tokenizer  # noqa: E402

import rdzen as r  # noqa: E402
import rdzen2 as r2  # noqa: E402

D, TOK, OUT, PROC = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
A, B = r.perm_param(128)
BANDY, WIERSZE, SH = 32, 4, 5
PACZKA = 4000
TK = None


def init():
    global TK
    TK = Tokenizer.from_file(TOK)


def licz_teksty(teksty):
    szk, sig = [], []
    for x in teksty:
        if not x:
            continue
        w = r.hasze_slow(r.norm_slowa(x))
        n13 = np.unique(r.ngramy(w, r.N_EVAL))
        szk.append(n13[n13 % np.uint64(r.PROBKA) == 0])
        s = r.podpis(np.unique(r.ngramy(w, SH)), A, B)
        if s is not None:
            sig.append(s)
    return (np.unique(np.concatenate(szk)) if szk else np.zeros(0, dtype=np.uint64), np.vstack(sig) if sig else np.zeros((0, 128), dtype=np.uint64), len(teksty))


def grupa_bin(a):
    b, i0, i1 = a
    ends = np.fromfile(f"{D}/slayer107/{b}/docs.idx", dtype=np.uint64)
    ids = np.memmap(f"{D}/slayer107/{b}/train.bin", dtype=np.uint16, mode="r")
    pocz = 0 if i0 == 0 else int(ends[i0 - 1])
    dok = []
    for i in range(i0, i1):
        k = int(ends[i])
        s = ids[pocz:k].tolist()
        pocz = k
        dok.append(s)
    t = TK.decode_batch(dok, skip_special_tokens=True)
    return licz_teksty(t)


def grupa_parquet(a):
    sciezka, g = a
    return licz_teksty(pq.ParquetFile(sciezka).read_row_group(g, columns=["text"]).column(0).to_pylist())


def zapisz(nazwa, wyniki):
    cz, sg, dok = [], [], 0
    for h, s, d in wyniki:
        cz.append(h)
        sg.append(s)
        dok += d
    x = np.unique(np.concatenate(cz))
    S = np.vstack(sg)
    kl = r2.klucze_band(S, BANDY, WIERSZE).ravel()
    dk = np.repeat(np.arange(S.shape[0], dtype=np.int64), BANDY)
    por = np.argsort(kl, kind="stable")
    np.save(f"{OUT}/idx_{nazwa}_szkic.npy", x)
    np.save(f"{OUT}/idx_{nazwa}_sig.npy", S)
    np.save(f"{OUT}/idx_{nazwa}_kl.npy", kl[por])
    np.save(f"{OUT}/idx_{nazwa}_dok.npy", dk[por])
    return {"dokumentow": dok, "probek_szkicu": int(len(x)), "podpisow": int(S.shape[0])}


def main():
    os.makedirs(OUT, exist_ok=True)
    wyn = {}
    t0 = time.time()
    with mp.get_context("spawn").Pool(PROC, initializer=init) as p:
        wsad = []
        for b in ("en_mix", "en_fineweb_edu"):
            n = int(os.path.getsize(f"{D}/slayer107/{b}/docs.idx") // 8)
            wsad += [(b, i, min(i + PACZKA, n)) for i in range(0, n, PACZKA)]
        print("paczki", len(wsad), flush=True)
        wy = []
        for i, w in enumerate(p.imap_unordered(grupa_bin, wsad, chunksize=1)):
            wy.append(w)
            if i % 50 == 0:
                print(i, f"{time.time() - t0:.0f}s", flush=True)
        wyn["slayer_107_en"] = zapisz("slayer_107_en", wy)
        print(wyn, flush=True)
        wy = []
        wsad = []
        for f in ("train", "validation", "test"):
            s = f"{D}/technika/{f}.parquet"
            wsad += [(s, g) for g in range(pq.ParquetFile(s).num_row_groups)]
        for w in p.imap_unordered(grupa_parquet, wsad, chunksize=1):
            wy.append(w)
        wyn["technika_i_nauka"] = zapisz("technika_i_nauka", wy)
    wyn["tokenizer_sha_oczekiwany_karta_107"] = "0640d3bd3674d7a6e59c540d945a2ad275a12e1bcaeb6007c37a90751f9815dd"
    json.dump(wyn, open(f"{OUT}/liczby_indeks.json", "w", encoding="utf-8"), indent=1)
    print(wyn, flush=True)
    print("KONIEC", f"{time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
