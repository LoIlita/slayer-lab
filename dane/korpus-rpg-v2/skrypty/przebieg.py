"""Główny przebieg po korpusie, niezmieniający tekstu: flagi jakości (znak PG, język, mojibake), 13-gramy i krótkie napisy
ewaluacji, dedup wobec baz (MinHash + szkic 13-gramów). Wyjście: g_NNNN.pkl per grupa wierszy.
Argumenty: wejscie.parquet katalog_ewal katalog_idx wyjscie procesy."""
import collections
import json
import multiprocessing as mp
import os
import pickle
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np  # noqa: E402
import pyarrow.parquet as pq  # noqa: E402

import rdzen as r  # noqa: E402
import rdzen2 as r2  # noqa: E402

PLIK, EW, IDX, OUT, PROC = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5])
PREREG = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "preregistracja.json"), encoding="utf-8"))
A, B = r.perm_param(128)
BANDY, WIERSZE = 32, 4
RX_PG = re.compile(PREREG["znak_pg"]["regex"])
RX_SCISLE = re.compile(r"Ã[\x80-\xBF]|â€|Â[\x80-\xBF]|ï»¿|�|Ä[\x80-\xBF]|Å[\x80-\xBF]|Ã[¡-¿]")
STOP = {
    "fr": "le la les de des du un une et est dans que qui pour pas sur au avec il elle".split(),
    "de": "der die das und ist nicht ein eine mit zu von den im für auf des sich dem sie er".split(),
    "es": "el la los las de del que y en un una es por con para no se su al lo".split(),
    "it": "il lo la gli le di che e un una per con non è del della dei in sono si".split(),
    "la": "et in est non ad quod cum qui ut sed de per si hic ab ex sunt ego tu nos".split(),
    "pt": "o a os as de do da que e em um uma para com não por se no na mais".split(),
    "nl": "de het een en van is dat in op te zijn met niet voor aan er om hij ze bij".split(),
}
STOP = {k: set(v) for k, v in STOP.items()}
ZEW = {}
UE13 = np.load(f"{EW}/wszystkie_13.npy", mmap_mode="r")
_KR = np.load(f"{EW}/wszystkie_krotkie.npz")
UK = {n: _KR[f"n{n}"] for n in range(1, 13)}
TESTY_13 = {p[:-8]: np.load(f"{EW}/{p}", mmap_mode="r") for p in sorted(os.listdir(EW)) if p.endswith("__13.npy") and not p.startswith("wszystkie")}
BAZY = {}
for nazwa in ("slayer_107_en", "technika_i_nauka"):
    BAZY[nazwa] = tuple(np.load(f"{IDX}/idx_{nazwa}_{x}.npy", mmap_mode="r") for x in ("szkic", "sig", "kl", "dok"))


def jezyk_metryki(t):
    sl = r.norm_slowa(t)
    if not sl:
        return {"en": 0.0, "obcy": 0.0, "obcy_jezyk": None, "nielat": 0.0, "slow": 0}
    n = len(sl)
    en = sum(1 for w in sl if w in r.EN_SLOWA) / n
    ob = {k: sum(1 for w in sl if w in v) / n for k, v in STOP.items()}
    kj = max(ob, key=ob.get)
    lit = sum(1 for c in t if c.isalpha())
    nl = sum(1 for c in t if c.isalpha() and not ("a" <= c.lower() <= "z" or "LATIN" in __import__("unicodedata").name(c, "")))
    return {"en": en, "obcy": ob[kj], "obcy_jezyk": kj, "nielat": nl / max(1, lit), "slow": n}


def wiersz_baza(s, x, baza):
    szk, sig, kl, dok = baza
    u = r.udzial(x, szk)
    est = None
    if s is not None and len(kl):
        klucze = r2.klucze_band(s[None, :], BANDY, WIERSZE).ravel()
        kand = set()
        for k in klucze:
            a, e = np.searchsorted(kl, k, "left"), np.searchsorted(kl, k, "right")
            if e > a:
                kand.update(np.asarray(dok[a:min(e, a + 500)]).tolist())
        if kand:
            est = float((np.asarray(sig[sorted(kand)]) == s).mean(axis=1).max())
    return u, est


def grupa(rg):
    t = pq.ParquetFile(PLIK).read_row_group(rg, columns=["text", "zrodlo", "id_zrodla"])
    tx, zr, idz = t.column("text").to_pylist(), t.column("zrodlo").to_pylist(), t.column("id_zrodla").to_pylist()
    flagi, ile = [], 0
    kr_dok = collections.Counter()
    kr_traf = {n: [] for n in UK}
    for i, s in enumerate(tx):
        ile += 1
        f = {}
        if RX_PG.search(s):
            f["pg"] = True
        et = r.jezyk(s)[0]
        if et == "inny":
            f["jezyk"] = jezyk_metryki(s)
        if r.MOJIBAKE.search(s):
            f["mojibake"] = len(RX_SCISLE.findall(s))
        w = r.hasze_slow(r.norm_slowa(s))
        n13 = np.unique(r.ngramy(w, r.N_EVAL))
        if r.ma_trafienie(n13, UE13):
            hity = [nz for nz, ind in TESTY_13.items() if r.ma_trafienie(n13, ind)]
            f["ewal"] = hity
        for n, arr in UK.items():
            if len(arr) == 0 or len(w) < n:
                continue
            g = np.unique(r.ngramy(w, n))
            idx = np.searchsorted(arr, g)
            idx[idx >= len(arr)] = len(arr) - 1
            h = g[arr[idx] == g]
            if len(h):
                kr_dok[n] += 1
                kr_traf[n].append(h)
        x = n13[n13 % np.uint64(r.PROBKA) == 0]
        sh = np.unique(r.ngramy(w, 5))
        podp = r.podpis(sh, A, B)
        bz = {}
        for nazwa, baza in BAZY.items():
            u, est = wiersz_baza(podp, x, baza)
            bz[nazwa] = (u, est)
            if (u is not None and u >= r.PROG_ZAWIERANIA) or (est is not None and est >= 0.8):
                f.setdefault("baza", {})[nazwa] = (u, est)
        if len(x) < r.MIN_PROBEK:
            f["krotki_szkic"] = True
        if f:
            f["rg"], f["i"], f["id"], f["zrodlo"] = rg, i, idz[i], zr[i]
            flagi.append(f)
    wyj = {"rg": rg, "ile": ile, "flagi": flagi, "kr_dok": dict(kr_dok), "kr_traf": {n: (np.unique(np.concatenate(v)) if v else np.zeros(0, dtype=np.uint64)) for n, v in kr_traf.items()}}
    with open(f"{OUT}/g_{rg:04d}.pkl.tmp", "wb") as f:
        pickle.dump(wyj, f)
    os.replace(f"{OUT}/g_{rg:04d}.pkl.tmp", f"{OUT}/g_{rg:04d}.pkl")
    return rg, ile, len(flagi)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    pf = pq.ParquetFile(PLIK)
    gr = [g for g in range(pf.metadata.num_row_groups) if not os.path.exists(f"{OUT}/g_{g:04d}.pkl")]
    t0 = time.time()
    with mp.get_context("fork").Pool(PROC) as p:
        for k, (rg, ile, fl) in enumerate(p.imap_unordered(grupa, gr)):
            print(k + 1, "/", len(gr), "rg", rg, "flagi", fl, f"{time.time() - t0:.0f}s", flush=True)
    print("KONIEC", flush=True)
