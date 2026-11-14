"""Przebieg dnia 1 po próbce DCLM, tekst niezmieniany. Per dokument: tokeny v6, domena testu, PII, mojibake, 13-gramy i krótkie
napisy testów, hasz tekstu, podpis MinHash, dedup wobec 1.07 EN (indeks RPG v2), hasz url; dodatkowe indeksy z indeksy.py
(walidacja, ivme) podane jako nazwa=katalog.
Wyjście: u_NNNN.npz + u_NNNN.json na jednostkę (grupa 5000 wierszy lokalnej kopii z pobierz.py). Metoda i progi: preregistracja.json.
Argumenty: probka_pliki.json katalog_ewal katalog_idx_107 tokenizer.json wyjscie procesy [nazwa=katalog ...]."""
import collections
import json
import multiprocessing as mp
import os
import re
import sys
import time

os.environ["TOKENIZERS_PARALLELISM"] = "false"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np  # noqa: E402
import pyarrow.parquet as pq  # noqa: E402
from tokenizers import Tokenizer  # noqa: E402

import wspolne as w  # noqa: E402
from wspolne import r, r2  # noqa: E402

PROBKA, EW, IDX, TOK, OUT, PROC = sys.argv[1:7]
PROC = int(PROC)
DODATKOWE = dict(a.split("=", 1) for a in sys.argv[7:])
A, B = r.perm_param(128)
BANDY, WIERSZE = 32, 4
RX_SCISLE = re.compile(r"Ã[\x80-\xBF]|â€|Â[\x80-\xBF]|ï»¿|�|Ä[\x80-\xBF]|Å[\x80-\xBF]|Ã[¡-¿]")
UE13 = np.load(f"{EW}/wszystkie_13.npy", mmap_mode="r")
_KR = np.load(f"{EW}/wszystkie_krotkie.npz")
UK = {n: _KR[f"n{n}"] for n in range(1, 13)}
TESTY_13 = {p[:-8]: np.load(f"{EW}/{p}", mmap_mode="r") for p in sorted(os.listdir(EW)) if p.endswith("__13.npy") and not p.startswith("wszystkie")}
BAZY = {"slayer_107_en": tuple(np.load(f"{IDX}/idx_slayer_107_en_{x}.npy", mmap_mode="r") for x in ("szkic", "sig", "kl", "dok"))}
for nz, kat in DODATKOWE.items():
    BAZY[nz] = tuple(np.load(f"{kat}/idx_{nz}_{x}.npy", mmap_mode="r") for x in ("szkic", "sig", "kl", "dok"))
TK = None


def init():
    global TK
    TK = Tokenizer.from_file(TOK)


def wiersz_baza(s, x, baza):
    szk, sig, kl, dok = baza
    u = r.udzial(x, szk)
    est = None
    if s is not None and len(kl):
        kand = set()
        for k in r2.klucze_band(s[None, :], BANDY, WIERSZE).ravel():
            a, e = np.searchsorted(kl, k, "left"), np.searchsorted(kl, k, "right")
            if e > a:
                kand.update(np.asarray(dok[a:min(e, a + 500)]).tolist())
        if kand:
            est = float((np.asarray(sig[sorted(kand)]) == s).mean(axis=1).max())
    return u, est


def jednostka(a):
    k, sciezka, g = a
    t = pq.ParquetFile(sciezka).read_row_group(g, columns=["text", "url", "id"])
    tx, ur, ids = t.column("text").to_pylist(), t.column("url").to_pylist(), t.column("id").to_pylist()
    n = len(tx)
    ntok = np.zeros(n, np.int64)
    id0 = np.zeros(n, bool)
    for i, e in enumerate(TK.encode_batch(tx, add_special_tokens=False)):
        ntok[i] = len(e.ids) + 1
        id0[i] = 0 in e.ids
    dom = np.zeros(n, np.int8)
    piim = np.zeros(n, np.int8)
    moj = np.zeros(n, np.int32)
    ew = np.zeros(n, bool)
    hx = np.zeros(n, np.uint64)
    hu = np.zeros(n, np.uint64)
    sig = np.zeros((n, 128), np.uint64)
    ma_sig = np.zeros(n, bool)
    bz = {nz: np.full((n, 2), np.nan) for nz in BAZY}
    ew_testy = {}
    kr_dok = collections.Counter()
    for i, s in enumerate(tx):
        d = w.domena_testu(ur[i])
        dom[i] = 0 if d is None else 1 + w.DOMENY_TESTOW.index(d)
        for kl in w.pii(s):
            piim[i] |= {"email": 1, "telefon": 2, "ip": 4}[kl]
        moj[i] = len(RX_SCISLE.findall(s))
        sl = r.norm_slowa(s)
        hx[i] = w.h64(" ".join(sl))
        hu[i] = w.h64(w.norm_url(ur[i]))
        h = r.hasze_slow(sl)
        n13 = np.unique(r.ngramy(h, r.N_EVAL))
        if r.ma_trafienie(n13, UE13):
            ew[i] = True
            ew_testy[i] = [nz for nz, ind in TESTY_13.items() if r.ma_trafienie(n13, ind)]
        for m, arr in UK.items():
            if len(arr) == 0 or len(h) < m:
                continue
            gm = np.unique(r.ngramy(h, m))
            j = np.minimum(np.searchsorted(arr, gm), len(arr) - 1)
            if np.any(arr[j] == gm):
                kr_dok[m] += 1
        x = n13[n13 % np.uint64(r.PROBKA) == 0]
        p = r.podpis(np.unique(r.ngramy(h, 5)), A, B)
        if p is not None:
            sig[i] = p
            ma_sig[i] = True
        for nz, baza in BAZY.items():
            u, est = wiersz_baza(p, x, baza)
            bz[nz][i] = (np.nan if u is None else u, np.nan if est is None else est)
    np.savez(f"{OUT}/.u_{k:04d}.npz", ntok=ntok, id0=id0, dom=dom, pii=piim, moj=moj, ew=ew, hx=hx, hu=hu, sig=sig, ma_sig=ma_sig,
             **{f"bz_{nz}": v for nz, v in bz.items()})
    os.replace(f"{OUT}/.u_{k:04d}.npz", f"{OUT}/u_{k:04d}.npz")
    json.dump({"k": k, "plik": sciezka, "rg": g, "ids": ids, "urls": ur, "ew_testy": {str(i): v for i, v in ew_testy.items()},
               "kr_dok": dict(kr_dok)}, open(f"{OUT}/u_{k:04d}.json", "w", encoding="utf-8"))
    return k, n


def main():
    os.makedirs(OUT, exist_ok=True)
    pl = json.load(open(PROBKA, encoding="utf-8"))["pliki"]
    wsad, k = [], 0
    for p in pl:
        for g in range(pq.ParquetFile(p["lokalnie"]).metadata.num_row_groups):
            wsad.append((k, p["lokalnie"], g))
            k += 1
    json.dump([x[1:] for x in wsad], open(f"{OUT}/jednostki.json", "w"))
    do = [x for x in wsad if not os.path.exists(f"{OUT}/u_{x[0]:04d}.npz")]
    print("jednostek", len(wsad), "do zrobienia", len(do), flush=True)
    t0 = time.time()
    with mp.get_context("fork").Pool(PROC, initializer=init) as pool:
        for j, (k, n) in enumerate(pool.imap_unordered(jednostka, do, chunksize=1), 1):
            print(j, "/", len(do), "u", k, n, f"{time.time() - t0:.0f}s", flush=True)
    print("KONIEC", f"{time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
