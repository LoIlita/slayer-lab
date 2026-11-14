"""Detektor części katalogowych (reklamy książek, listy wydawców) oraz spisów treści, indeksów i tabel w całych częściach.
Metryki na oknach 1000 znaków (krok 500); wynik dla każdego wiersza Gutenberga (wiersze SCP i RPG też policzone, bez reguły).
Argumenty: wejscie.parquet wyjscie procesy tryb(sample|all)."""
import json
import multiprocessing as mp
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np  # noqa: E402
import pyarrow.parquet as pq  # noqa: E402

PLIK, OUT, PROC, TRYB = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
OKNO, KROK = 1000, 500

CENA = re.compile(r"\b\d{1,3}s\.(?:\s*\d{1,2}d\.)?|\b\d{1,2}d\.(?=[\s,;)])|\b\d{1,3}s\s+\d{1,2}d\b|\$\s?\d+(?:\.\d{2})?\b|£\s?\d|\b\d+\s*cents\b|\bPRICE\b|\bPrice\b")
FORMAT = re.compile(r"(?i)\b(?:crown|demy|imperial|post|fcap\.?|foolscap|royal)\s+\d{1,2}(?:vo|mo)\b|\b\d{1,2}(?:vo|mo)\b|\boctavo\b")
SLABE = re.compile(r"(?i),\s*cloth\b|\bcloth,\s|\bnew\s+(?:and\s+\w+\s+)?edition\b|\bnow\s+ready\b|\bin\s+the\s+press\b|\bby\s+the\s+same\s+author\b|\bpost\s+free\b|\bpublishers?\b|\bsold\s+by\b")
DITTO = re.compile(r"(?m)^\s*[-—_]{2,}\s*[A-Z]")
IDX = re.compile(r",\s*\d{1,4}(?:\s*[,;–—-]\s*\d{1,4})*\s*(?:[;.\n]|$)")
LINIA_NUM = re.compile(r"(?m)^.{3,90}?[\s.…_-](\d{1,4})\s*$")
LICZBA = re.compile(r"\b\d[\d,.]*\b")
SLOWO = re.compile(r"\S+")


def okna_licz(poz, n):
    """Liczba trafień w oknach [i, i+OKNO) przesuwanych co KROK; poz posortowane."""
    gr = np.arange(0, max(1, n - OKNO + 1) + 0, KROK)
    if len(gr) == 0:
        gr = np.array([0])
    return np.searchsorted(poz, gr + OKNO) - np.searchsorted(poz, gr)


def metryki(t):
    n = len(t)
    cena = np.fromiter((m.start() for m in CENA.finditer(t)), dtype=np.int64)
    forma = np.fromiter((m.start() for m in FORMAT.finditer(t)), dtype=np.int64)
    slabe = np.fromiter((m.start() for m in SLABE.finditer(t)), dtype=np.int64)
    ditto = np.fromiter((m.start() for m in DITTO.finditer(t)), dtype=np.int64)
    idx = np.fromiter((m.start() for m in IDX.finditer(t)), dtype=np.int64)
    trafione_linie = [m.group(0) for m in LINIA_NUM.finditer(t)]
    linie_num = len(trafione_linie)
    linii = t.count("\n") + 1
    lnum_zn = sum(len(x) for x in trafione_linie) / max(1, n)
    licz = np.fromiter((m.start() for m in LICZBA.finditer(t)), dtype=np.int64)
    slow = np.fromiter((m.start() for m in SLOWO.finditer(t)), dtype=np.int64)
    scena, sforma, sslabe, sditto, sidx, sliczb, sslow = [okna_licz(x, n) for x in (cena, forma, slabe, ditto, idx, licz, slow)]
    wynik_k = scena + sforma + 0.5 * sslabe + sditto
    frakcje = {f"kat_k{k}": float((wynik_k >= k).mean()) for k in (3, 4, 6, 8, 12)}
    # okno katalogowe: wynik >= 4 ORAZ dowód formatu książki (format + słabe znaczniki >= 2); same kwoty pieniędzy w prozie nie wystarczą
    frakcje["kat2_frac"] = float(((wynik_k >= 4) & ((sforma + sslabe) >= 2)).mean())
    return dict(frakcje, zn=n, sl=int(len(slow)), kat_max=float(wynik_k.max()), kat_sred=float(wynik_k.mean()), ceny=int(len(cena)), format=int(len(forma)),
                idx_frac=float((sidx >= 5).mean()), idx_sred=float(sidx.mean()), lnum_udz=round(linie_num / linii, 4), lnum_zn=round(lnum_zn, 4), linii=linii,
                tab_frac=float(((sliczb / np.maximum(sslow, 1)) >= 0.35).mean()))


def grupa(rg):
    t = pq.ParquetFile(PLIK).read_row_group(rg, columns=["text", "zrodlo", "id_zrodla"])
    tx, zr, idz = t.column("text").to_pylist(), t.column("zrodlo").to_pylist(), t.column("id_zrodla").to_pylist()
    out = []
    for i, s in enumerate(tx):
        m = metryki(s)
        m.update({"rg": rg, "i": i, "id": idz[i], "zr": zr[i]})
        out.append(m)
    with open(f"{OUT}/k_{rg:04d}.json.tmp", "w", encoding="utf-8") as f:
        json.dump(out, f)
    os.replace(f"{OUT}/k_{rg:04d}.json.tmp", f"{OUT}/k_{rg:04d}.json")
    return rg


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    pf = pq.ParquetFile(PLIK)
    n = pf.metadata.num_row_groups
    if TRYB == "sample":
        wyb = {g for g in range(n) if g % 8 == 0}
        for g in range(n):
            ids = pf.read_row_group(g, columns=["id_zrodla"]).column(0).to_pylist()
            if "51718/cz10" in ids:
                wyb.add(g)
                print("pozytywny przypadek 51718/cz10 w grupie", g, flush=True)
                break
        gr = sorted(wyb)
    else:
        gr = list(range(n))
    gr = [g for g in gr if not os.path.exists(f"{OUT}/k_{g:04d}.json")]
    t0 = time.time()
    with mp.get_context("fork").Pool(PROC) as p:
        for k, rg in enumerate(p.imap_unordered(grupa, gr)):
            print(k + 1, "/", len(gr), "rg", rg, f"{time.time() - t0:.0f}s", flush=True)
    print("KONIEC", flush=True)
