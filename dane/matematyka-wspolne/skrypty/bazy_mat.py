"""Bazy porównania dodane aneksem z 24.11.2026 (preregistracje zbiorów #346, pole 'aneks_2026_11_24'): dane już w treningu
Slayera, których nie obejmuje indeks EN 1.07.
  entech  SlayerLab/english-technical-1b@3b833d36 (dane 1.08: kod i dokumentacja projektów open source), pliki
          data/{train,validation,test}.parquet -> indeks w formacie DCLM-EN indeksy.py: MinHash 128 + klucze LSH 32x4 + hasz
          znormalizowanego tekstu (idx_entech_{sig,kl,dok,hx}.npy)
  fwe109  kolumna url wszystkich plików FineWeb-Edu z composants.csv manifestu SlayerLab/Slayer1B-Dataset@2d248a17
          (źródło fineweb-edu 1.09, c01-c17) -> idx_fwe109_hu.npy (hasz znormalizowanego url, jak przebieg.py); wznawialny,
          jeden plik .npy na plik FineWeb-Edu
Argumenty: entech|fwe109 katalog_pobran wyjscie procesy"""
import csv
import hashlib
import json
import multiprocessing as mp
import os
import sys

import numpy as np
import pyarrow.parquet as pq
from huggingface_hub import HfFileSystem, hf_hub_download

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "dclm-en", "skrypty"))
import wspolne as w  # noqa: E402
from wspolne import r, r2  # noqa: E402

TRYB, POB, OUT, PROC = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
ENTECH, ENTECH_REW = "SlayerLab/english-technical-1b", "3b833d36bd3ba9aeecf46f39605c9ac849bb96a3"
MANIFEST, MANIFEST_REW = "SlayerLab/Slayer1B-Dataset", "2d248a172451938fbee67477a59db12fb58c278a"
A, B = r.perm_param(128)


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 24), b""):
            h.update(b)
    return h.hexdigest()


def licz(teksty):
    sig, hx = [], []
    for x in teksty:
        sl = r.norm_slowa(x or "")
        hx.append(w.h64(" ".join(sl)))
        s = r.podpis(np.unique(r.ngramy(r.hasze_slow(sl), 5)), A, B)
        sig.append(s if s is not None else np.zeros(128, np.uint64))
    return np.vstack(sig), np.array(hx, np.uint64)


def entech():
    teksty, pliki = [], []
    for f in ("data/train.parquet", "data/validation.parquet", "data/test.parquet"):
        p = hf_hub_download(ENTECH, f, repo_type="dataset", revision=ENTECH_REW, local_dir=f"{POB}/entech")
        t = pq.read_table(p, columns=["text"]).column(0).to_pylist()
        teksty += t
        pliki.append({"plik": f, "sha256": sha(p), "dokumentow": len(t)})
        print(f, len(t), flush=True)
    with mp.get_context("fork").Pool(PROC) as pool:
        cz = pool.map(licz, [teksty[i:i + 2000] for i in range(0, len(teksty), 2000)])
    S = np.vstack([c[0] for c in cz])
    kl = r2.klucze_band(S, 32, 4).ravel()
    dk = np.repeat(np.arange(S.shape[0], dtype=np.int64), 32)
    por = np.argsort(kl, kind="stable")
    for k, v in (("sig", S), ("kl", kl[por]), ("dok", dk[por]), ("hx", np.unique(np.concatenate([c[1] for c in cz])))):
        np.save(f"{OUT}/idx_entech_{k}.npy", v)
    json.dump({"repo": ENTECH, "rewizja": ENTECH_REW, "pliki": pliki, "dokumentow": int(S.shape[0])},
              open(f"{OUT}/entech.json", "w", encoding="utf-8"), indent=1)
    print("KONIEC", S.shape[0], flush=True)


def _url_pliku(a):
    """Kolumna url jednego pliku parquet bez pobierania całego pliku: stopka, potem dokładne zakresy bajtów kawałków kolumny url
    (Range, wątki) zapisane pod tymi samymi offsetami w pliku rzadkim; pyarrow czyta z niego tylko te zakresy.
    Poprzednia wersja (HfFileSystem, block_size 8 MB) czytała 8 MB na każdą grupę wierszy: ok. 7 min na plik."""
    import requests
    from concurrent.futures import ThreadPoolExecutor
    from huggingface_hub.utils import build_hf_headers
    repo, rew, plik, cel = a
    if os.path.exists(cel):
        return plik, int(len(np.load(cel)))
    url = f"https://huggingface.co/datasets/{repo}/resolve/{rew}/{plik}"
    s = requests.Session()
    s.headers.update(build_hf_headers())

    def zakres(a0, b0):
        for proba in range(5):
            try:
                r = s.get(url, headers={"Range": f"bytes={a0}-{b0 - 1}"}, timeout=120)
                r.raise_for_status()
                assert len(r.content) == b0 - a0, (len(r.content), b0 - a0)
                return a0, r.content
            except Exception:
                if proba == 4:
                    raise

    rozm = int(s.head(url, allow_redirects=True, timeout=60).headers["Content-Length"])
    _, ogon = zakres(rozm - 8, rozm)
    dl = int.from_bytes(ogon[:4], "little")
    rzadki = cel + ".parquet.tmp"
    with open(rzadki, "wb") as f:
        f.truncate(rozm)
        a0, stopka = zakres(rozm - 8 - dl, rozm)
        f.seek(a0)
        f.write(stopka)
    md = pq.ParquetFile(rzadki).metadata
    ci = md.schema.to_arrow_schema().get_field_index("url")
    zak = []
    for g in range(md.num_row_groups):
        c = md.row_group(g).column(ci)
        p0 = c.dictionary_page_offset if c.has_dictionary_page and c.dictionary_page_offset else c.data_page_offset
        zak.append((p0, p0 + c.total_compressed_size))
    with ThreadPoolExecutor(16) as ex, open(rzadki, "r+b") as f:
        for a0, dane in ex.map(lambda z: zakres(*z), zak):
            f.seek(a0)
            f.write(dane)
    u = pq.read_table(rzadki, columns=["url"]).column(0).to_pylist()
    os.remove(rzadki)
    np.save(cel + ".tmp.npy", np.unique(np.array([w.h64(w.norm_url(x)) for x in u if x], np.uint64)))
    os.replace(cel + ".tmp.npy", cel)
    return plik, len(u)


def fwe109():
    m = hf_hub_download(MANIFEST, "manifest/components.csv", repo_type="dataset", revision=MANIFEST_REW, local_dir=f"{POB}/manifest")
    wiersze = [x for x in csv.DictReader(open(m, encoding="utf-8")) if x["source"] == "fineweb-edu"]
    pliki = sorted({(x["upstream_repo"], x["upstream_revision"], x["upstream_file"]) for x in wiersze})
    os.makedirs(f"{POB}/fwe109", exist_ok=True)
    zad = [(a, b, c, f"{POB}/fwe109/{c.replace('/', '__')}.npy") for a, b, c in pliki]
    with mp.get_context("spawn").Pool(PROC) as pool:
        for j, (plik, n) in enumerate(pool.imap_unordered(_url_pliku, zad), 1):
            print(j, "/", len(zad), plik, n, flush=True)
    hu = np.unique(np.concatenate([np.load(z[3]) for z in zad]))
    np.save(f"{OUT}/idx_fwe109_hu.npy", hu)
    json.dump({"manifest": MANIFEST, "rewizja": MANIFEST_REW, "components_sha256": sha(m), "plikow": len(pliki),
               "url_unikalnych": int(len(hu))}, open(f"{OUT}/fwe109.json", "w", encoding="utf-8"), indent=1)
    print("KONIEC", len(pliki), len(hu), flush=True)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    entech() if TRYB == "entech" else fwe109()
