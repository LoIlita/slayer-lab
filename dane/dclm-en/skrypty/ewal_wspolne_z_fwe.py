"""13-gramy testów obecne w niezależnym korpusie sieciowym: próbce FineWeb-Edu z kroku fwe_url (aneks 2 preregistracji,
pole aneks_2026_11_15b.ewal_13gram). Przecięcie indeksu 13-gramów testów (wszystkie_13.npy) z 13-gramami tekstów 8 plików FWE.
Normalizacja i hasze jak w przebiegu (rdzen.norm_slowa, hasze_slow, ngramy, N_EVAL). Strumieniowo: zadanie = jedna grupa
wierszy pliku parquet, wynik zadania zapisany od razu w czesci/ (krok wznawialny, pamięć stała).
Wyjście (katalog wyjscie):
  wspolne_fwe.npz   hasze (posortowane uint64, 13-gramy testów obecne w FWE), df (w ilu dokumentach FWE)
  wspolne_fwe.json  wiersze, dokumenty z trafieniem, n-gramów, per test: 13-gramów w indeksie i ile z nich jest w FWE
  wspolne_fwe_teksty.parquet  hasz, df, tekst (13 słów po normalizacji, z pierwszego wystąpienia), plik i wiersz FWE
Argumenty: katalog_ewal fwe_url.json katalog_pobran_fwe wyjscie procesy"""
import json
import os
import sys
import time
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np  # noqa: E402
import pyarrow as pa  # noqa: E402
import pyarrow.parquet as pq  # noqa: E402

from wspolne import r  # noqa: E402

REPO, REW = "HuggingFaceFW/fineweb-edu", "87f09149ef4734204d70ed1d046ddc9ca3f2b8f9"
_UE13 = None
_PF = {}


def init(ew):
    global _UE13
    _UE13 = np.load(f"{ew}/wszystkie_13.npy", mmap_mode="r")


def zadanie(arg):
    sciezka, plik, g, cz = arg
    if os.path.exists(cz):
        return cz, 0, 0.0
    t0 = time.time()
    if sciezka not in _PF:
        _PF.clear()
        _PF[sciezka] = pq.ParquetFile(sciezka)
    tx = _PF[sciezka].read_row_group(g, columns=["text"]).column(0).to_pylist()
    wiersz0 = sum(_PF[sciezka].metadata.row_group(k).num_rows for k in range(g))
    hs, wiersze, teksty = [], [], {}
    for i, t in enumerate(tx):
        sl = r.norm_slowa(t or "")
        g13 = r.ngramy(r.hasze_slow(sl), r.N_EVAL)
        if len(g13) == 0:
            continue
        u, pierwsze = np.unique(g13, return_index=True)
        j = np.minimum(np.searchsorted(_UE13, u), len(_UE13) - 1)
        traf = _UE13[j] == u
        if not traf.any():
            continue
        th = u[traf]
        hs.append(th)
        wiersze.append(np.full(len(th), wiersz0 + i, np.int64))
        for x, p in zip(th.tolist(), pierwsze[traf].tolist()):
            if x not in teksty:
                teksty[x] = " ".join(sl[p:p + r.N_EVAL])
    H = np.concatenate(hs) if hs else np.zeros(0, np.uint64)
    W = np.concatenate(wiersze) if wiersze else np.zeros(0, np.int64)
    k = np.array(list(teksty.keys()), np.uint64)
    tmp = cz + ".tmp.npz"
    np.savez(tmp, hasze=H, wiersze=W, n_dok=np.int64(len(tx)), t_hasze=k, t_tekst=np.array(list(teksty.values()), dtype=object))
    os.replace(tmp, cz)
    return cz, len(tx), time.time() - t0


def main():
    EW, FWE_JSON, POB, OUT, PROC = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5])
    os.makedirs(f"{OUT}/czesci", exist_ok=True)
    info = json.load(open(FWE_JSON, encoding="utf-8"))
    assert info["rewizja"] == REW, info["rewizja"]
    pliki = [x["plik"] for x in info["probka"]]
    from huggingface_hub import hf_hub_download
    lok = {}
    for p in pliki:  # pobranie wznawialne; liczba wierszy musi się zgadzać z fwe_url.json
        lok[p] = hf_hub_download(REPO, p, repo_type="dataset", revision=REW, local_dir=POB)
        n = pq.ParquetFile(lok[p]).metadata.num_rows
        assert n == next(x["wiersze"] for x in info["probka"] if x["plik"] == p), (p, n)
        print("plik", p, n, flush=True)
    zad = []
    for p in pliki:
        md = pq.ParquetFile(lok[p]).metadata
        for g in range(md.num_row_groups):
            zad.append((lok[p], p, g, f"{OUT}/czesci/{p.replace('/', '__')}__rg{g:05d}.npz"))
    print("zadan", len(zad), "procesy", PROC, flush=True)
    t0, wier = time.time(), 0
    with Pool(PROC, initializer=init, initargs=(EW,), maxtasksperchild=200) as pool:
        for k, (cz, n, dt) in enumerate(pool.imap_unordered(zadanie, zad, chunksize=1)):
            wier += n
            if k % 100 == 0:
                print(f"{k + 1}/{len(zad)} wierszy_w_tym_przebiegu {wier} {time.time() - t0:.0f}s", flush=True)

    # scalanie
    hs, docs, n_dok = [], 0, 0
    tekst, gdzie = {}, {}
    for (_, p, g, cz) in zad:
        z = np.load(cz, allow_pickle=True)
        n_dok += int(z["n_dok"])
        H, W = z["hasze"], z["wiersze"]
        hs.append(H)
        docs += len(np.unique(W))
        uh, pierwszy = np.unique(H, return_index=True)
        wiersz_pierwszy = dict(zip(uh.tolist(), W[pierwszy].tolist()))
        for x, t in zip(z["t_hasze"].tolist(), z["t_tekst"].tolist()):
            if x not in tekst:
                tekst[x] = t
                gdzie[x] = (p, int(wiersz_pierwszy[x]))
    H = np.concatenate(hs) if hs else np.zeros(0, np.uint64)
    u, df = np.unique(H, return_counts=True)  # w części hasz występuje raz na dokument, więc liczność = df dokumentów
    np.savez(f"{OUT}/wspolne_fwe.npz", hasze=u, df=df.astype(np.int64))
    pq.write_table(pa.table({"hasz": [str(x) for x in u.tolist()], "df": df.tolist(),
                             "tekst": [tekst[x] for x in u.tolist()],
                             "plik": [gdzie[x][0] for x in u.tolist()], "wiersz": [gdzie[x][1] for x in u.tolist()]}),
                   f"{OUT}/wspolne_fwe_teksty.parquet")
    testy = {}
    for nz in sorted(os.listdir(EW)):
        if nz.endswith("__13.npy") and not nz.startswith("wszystkie"):
            ind = np.load(f"{EW}/{nz}", mmap_mode="r")
            testy[nz[:-8]] = {"ngramow_testu": int(len(ind)), "w_fwe": int(np.isin(u, ind).sum())}
    wyn = {"repo": REPO, "rewizja": REW, "pliki": pliki, "wiersze_fwe": n_dok, "wiersze_fwe_oczekiwane": info["wiersze_probki"],
           "dokumenty_fwe_z_trafieniem": docs, "ngramow_indeksu_testow": int(len(np.load(f"{EW}/wszystkie_13.npy", mmap_mode="r"))),
           "ngramow_testow_w_fwe": int(len(u)), "testy": testy, "czas_s": round(time.time() - t0)}
    assert n_dok == info["wiersze_probki"], (n_dok, info["wiersze_probki"])
    json.dump(wyn, open(f"{OUT}/wspolne_fwe.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(json.dumps({k: v for k, v in wyn.items() if k != "testy"}), flush=True)
    print("KONIEC", flush=True)


if __name__ == "__main__":
    main()
