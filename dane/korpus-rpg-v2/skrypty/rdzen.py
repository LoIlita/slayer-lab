"""Wspólne funkcje korpusu: normalizacja, stabilne hasze n-gramów, MinHash, szkice, akapity.

Hasze są stabilne między procesami i przebiegami (blake2b + wielomian mod 2^64), w odróżnieniu od hash()
z dane_ramion.py, które pod `python -I` nie dostaje PYTHONHASHSEED. Definicja słowa ta sama: \\w+ po lower().
"""
import hashlib
import re
import unicodedata

import numpy as np

SLOWO = re.compile(r"\w+", re.UNICODE)
N_EVAL = 13
P = 0x100000001B3
P_INV = pow(P, -1, 2 ** 64)
PROBKA = 16
PROG_ZAWIERANIA = 0.5
MIN_PROBEK = 4
_CACHE = {}


def norm_slowa(tekst):
    """Normalizacja do porównań: NFKC, małe litery, _ jako spacja, sklejenie n't, słowa \\w+."""
    t = unicodedata.normalize("NFKC", tekst).replace("_", " ").replace("’", "'").lower()
    t = re.sub(r"\s+n't\b", "n't", t)
    return SLOWO.findall(t)


def norm_tekst(tekst):
    return " ".join(norm_slowa(tekst))


def _h(w):
    v = _CACHE.get(w)
    if v is None:
        v = int.from_bytes(hashlib.blake2b(w.encode("utf-8", "surrogatepass"), digest_size=8).digest(), "little")
        if len(_CACHE) < 5_000_000:
            _CACHE[w] = v
    return v


def hasze_slow(slowa):
    return np.fromiter((_h(w) for w in slowa), dtype=np.uint64, count=len(slowa))


def ngramy(w, n):
    """Hasze n-gramów z tablicy haszy słów; wynik zależy tylko od kolejnych n słów."""
    m = len(w) - n + 1
    if m <= 0:
        return np.zeros(0, dtype=np.uint64)
    pw = np.full(len(w), P, dtype=np.uint64)
    pw[0] = 1
    pw = np.cumprod(pw, dtype=np.uint64)
    ipw = np.full(m, P_INV, dtype=np.uint64)
    ipw[0] = 1
    ipw = np.cumprod(ipw, dtype=np.uint64)
    s = np.cumsum(w * pw, dtype=np.uint64)
    okno = s[n - 1:].copy()
    okno[1:] -= s[:m - 1]
    x = okno * ipw
    x ^= x >> np.uint64(29)
    x *= np.uint64(0xBF58476D1CE4E5B9)
    x ^= x >> np.uint64(32)
    return x


def ngramy_tekstu(tekst, n):
    return ngramy(hasze_slow(norm_slowa(tekst)), n)


def szkic(tekst):
    x = np.unique(ngramy_tekstu(tekst, N_EVAL))
    return x[x % np.uint64(PROBKA) == 0]


def ma_trafienie(x, indeks):
    if len(indeks) == 0 or len(x) == 0:
        return False
    return bool(np.any(indeks[np.minimum(np.searchsorted(indeks, x), len(indeks) - 1)] == x))


def udzial(x, indeks):
    """Ułamek próbek x obecnych w posortowanym indeksie; None gdy próbek < MIN_PROBEK."""
    if len(x) < MIN_PROBEK:
        return None
    if len(indeks) == 0:
        return 0.0
    return float(np.mean(indeks[np.minimum(np.searchsorted(indeks, x), len(indeks) - 1)] == x))


# ------------------------------------------------------------------ MinHash

def perm_param(n=128, seed=20261110):
    g = np.random.default_rng(seed)
    a = g.integers(1, 2 ** 63, size=n, dtype=np.uint64) * np.uint64(2) + np.uint64(1)
    b = g.integers(0, 2 ** 63, size=n, dtype=np.uint64)
    return a, b


def podpis(x, a, b, porcja=16):
    """MinHash zbioru haszy x (np.uint64, unikalne): 128 wartości; pusty zbiór = None."""
    if len(x) == 0:
        return None
    out = []
    for i in range(0, len(a), porcja):
        aa = a[i:i + porcja][:, None]
        bb = b[i:i + porcja][:, None]
        out.append((aa * x[None, :] + bb).min(axis=1))
    return np.concatenate(out)


def jaccard(x, y):
    if len(x) == 0 or len(y) == 0:
        return 0.0
    w = len(np.intersect1d(x, y, assume_unique=True))
    return w / (len(x) + len(y) - w)


class Scalanie:
    """Union-find po indeksach dokumentów."""

    def __init__(self, n):
        self.p = list(range(n))

    def znajdz(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def polacz(self, a, b):
        ra, rb = self.znajdz(a), self.znajdz(b)
        if ra != rb:
            self.p[rb] = ra


# ------------------------------------------------------------------ akapity

def akapity(tekst):
    return [a.strip() for a in re.split(r"\n\s*\n", tekst) if a.strip()]


def h_akapitu(a):
    return int.from_bytes(hashlib.blake2b(norm_tekst(a).encode("utf-8"), digest_size=8).digest(), "little")


def powtarzalnosc(dok_akapity):
    """dok_akapity: iterowalne listy haszy akapitów (po dokumencie). Zwraca liczniki i odsetek."""
    h, d = [], []
    for i, lst in enumerate(dok_akapity):
        if lst:
            h.append(np.asarray(lst, dtype=np.uint64))
            d.append(np.full(len(lst), i, dtype=np.int64))
    if not h:
        return {"akapity": 0, "w_wielu_dok": 0, "odsetek": 0.0}
    h, d = np.concatenate(h), np.concatenate(d)
    para = np.unique(np.stack([h, d.astype(np.uint64)], axis=1), axis=0)
    wart, ile = np.unique(para[:, 0], return_counts=True)
    multi = wart[ile > 1]
    n_w_wielu = int(np.isin(h, multi, assume_unique=False).sum())
    return {"akapity": int(len(h)), "w_wielu_dok": n_w_wielu, "odsetek": round(100.0 * n_w_wielu / len(h), 4),
            "akapitow_roznych_w_wielu_dok": int(len(multi))}


# ------------------------------------------------------------------ jakość

MOJIBAKE = re.compile(r"Ã[\x80-\xBF¡-¿]|â€|Â[ -¿]|ï»¿|�|Ä[\x80-\xBF]|Å[\x80-\xBF]")
PL_ZNAKI = set("ąćęłńśźżĄĆĘŁŃŚŹŻ")
PL_SLOWA = set("i w nie się na że jest to do z o jak co ale po tak za od czy przez dla być ich jego jej".split())
EN_SLOWA = set("the of and to in that was he it is his with had as for you at on not".split())


def jezyk(tekst):
    """Heurystyka: 'pl' gdy słowa funkcyjne PL dominują i są polskie znaki. Zwraca (etykieta, udział PL, udział EN)."""
    pr = norm_slowa(tekst[:20000])
    if not pr:
        return "brak", 0.0, 0.0
    pl = sum(1 for w in pr if w in PL_SLOWA) / len(pr)
    en = sum(1 for w in pr if w in EN_SLOWA) / len(pr)
    zn = sum(1 for c in tekst[:20000] if c in PL_ZNAKI) / max(1, len(tekst[:20000]))
    if pl > en and zn > 0.01:
        return "pl", pl, en
    if en >= 0.08:
        return "en", pl, en
    return "inny", pl, en
