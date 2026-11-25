"""Bazy porównania dodane aneksami preregistracji zbiorów #346: dane już w treningu Slayera, których nie obejmuje indeks EN 1.07.
  entech  (aneks 24.11) SlayerLab/english-technical-1b@3b833d36 (dane 1.08: kod i dokumentacja projektów open source), pliki
          data/{train,validation,test}.parquet
  en8x3b  (aneks 25.11b) SlayerLab/slayer-pl-8x3b@d50df04a, plik shared/en.parquet (angielska część 1.00-1.06: FineWeb-Edu)
          -> dla obu indeks w formacie DCLM-EN indeksy.py: MinHash 128 + klucze LSH 32x4 + hasz znormalizowanego tekstu
          (idx_<nazwa>_{sig,kl,dok,hx}.npy), plus hasz url, gdy plik ma kolumnę url (idx_<nazwa>_hu.npy)
  fwe109  kolumna url wszystkich plików FineWeb-Edu z components.csv manifestu SlayerLab/Slayer1B-Dataset@2d248a17
          (źródło fineweb-edu 1.09, c01-c17) -> idx_fwe109_hu.npy (hasz znormalizowanego url, jak przebieg.py); wznawialny,
          jeden plik .npy na plik FineWeb-Edu
Argumenty: entech|en8x3b|fwe109 katalog_pobran wyjscie procesy"""
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
BAZY_MINHASH = {
    "entech": ("SlayerLab/english-technical-1b", "3b833d36bd3ba9aeecf46f39605c9ac849bb96a3",
               ("data/train.parquet", "data/validation.parquet", "data/test.parquet")),
    "en8x3b": ("SlayerLab/slayer-pl-8x3b", "d50df04a6ad46876fa559a87cca5d3e2a96e7098", ("shared/en.parquet",)),
}
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


def indeks_minhash(nazwa):
    """Strumieniowo po grupach wierszy, więc plik 4,7 GB nie trafia w całości do pamięci."""
    repo, rew, pliki_repo = BAZY_MINHASH[nazwa]
    sigs, hxs, hus, pliki = [], [], [], []
    with mp.get_context("fork").Pool(PROC) as pool:
        for f in pliki_repo:
            p = hf_hub_download(repo, f, repo_type="dataset", revision=rew, local_dir=f"{POB}/{nazwa}")
            pf = pq.ParquetFile(p)
            kol = [c for c in ("text", "url") if c in pf.schema_arrow.names]
            n = 0
            for g in range(pf.metadata.num_row_groups):
                t = pf.read_row_group(g, columns=kol)
                teksty = t.column("text").to_pylist()
                for s_, h_ in pool.map(licz, [teksty[i:i + 2000] for i in range(0, len(teksty), 2000)]):
                    sigs.append(s_)
                    hxs.append(h_)
                if "url" in kol:
                    hus.append(np.array([w.h64(w.norm_url(u)) for u in t.column("url").to_pylist() if u], np.uint64))
                n += len(teksty)
            pliki.append({"plik": f, "sha256": sha(p), "dokumentow": n})
            print(f, n, flush=True)
    S = np.vstack(sigs)
    kl = r2.klucze_band(S, 32, 4).ravel()
    dk = np.repeat(np.arange(S.shape[0], dtype=np.int64), 32)
    por = np.argsort(kl, kind="stable")
    for k, v in (("sig", S), ("kl", kl[por]), ("dok", dk[por]), ("hx", np.unique(np.concatenate(hxs)))):
        np.save(f"{OUT}/idx_{nazwa}_{k}.npy", v)
    if hus:
        np.save(f"{OUT}/idx_{nazwa}_hu.npy", np.unique(np.concatenate(hus)))
    json.dump({"repo": repo, "rewizja": rew, "pliki": pliki, "dokumentow": int(S.shape[0]), "url": bool(hus)},
              open(f"{OUT}/{nazwa}.json", "w", encoding="utf-8"), indent=1)
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
        import time
        for proba in range(20):
            try:
                r = s.get(url, headers={"Range": f"bytes={a0}-{b0 - 1}"}, timeout=120)
                if r.status_code in (400, 403, 429, 503):  # limit Hubu i CDN (400 z xet-bridge przy przeciążeniu): czekamy
                    time.sleep(float(r.headers.get("Retry-After") or min(300, 5 * 2 ** proba)))
                    continue
                r.raise_for_status()
                assert len(r.content) == b0 - a0, (len(r.content), b0 - a0)
                return a0, r.content
            except Exception:
                if proba == 19:
                    raise
                time.sleep(min(60, 2 ** proba))
        raise RuntimeError(f"limit bez końca: {url}")

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
    with ThreadPoolExecutor(6) as ex, open(rzadki, "r+b") as f:
        for a0, dane in ex.map(lambda z: zakres(*z), zak):
            f.seek(a0)
            f.write(dane)
    u = pq.read_table(rzadki, columns=["url"]).column(0).to_pylist()
    os.remove(rzadki)
    np.save(cel + ".tmp.npy", np.unique(np.array([w.h64(w.norm_url(x)) for x in u if x], np.uint64)))
    os.replace(cel + ".tmp.npy", cel)
    return plik, len(u)

def _url_pliku_bezpiecznie(a):
    try:
        return _url_pliku(a)
    except Exception as e:  # jeden plik nie przerywa puli; brak wykrywa fwe109()
        return a[2], f"BLAD {type(e).__name__}"



def fwe109():
    m = hf_hub_download(MANIFEST, "manifest/components.csv", repo_type="dataset", revision=MANIFEST_REW, local_dir=f"{POB}/manifest")
    wiersze = [x for x in csv.DictReader(open(m, encoding="utf-8")) if x["source"] == "fineweb-edu"]
    pliki = sorted({(x["upstream_repo"], x["upstream_revision"], x["upstream_file"]) for x in wiersze})
    os.makedirs(f"{POB}/fwe109", exist_ok=True)
    zad = [(a, b, c, f"{POB}/fwe109/{c.replace('/', '__')}.npy") for a, b, c in pliki]
    with mp.get_context("spawn").Pool(PROC) as pool:
        for j, (plik, n) in enumerate(pool.imap_unordered(_url_pliku_bezpiecznie, zad), 1):
            print(j, "/", len(zad), plik, n, flush=True)
    brak = [z[2] for z in zad if not os.path.exists(z[3])]
    if brak:  # plik bez listy url: uruchom krok ponownie (gotowe pliki są pomijane)
        raise SystemExit(f"BRAK {len(brak)} plików: {brak[:5]}")
    hu = np.unique(np.concatenate([np.load(z[3]) for z in zad]))
    np.save(f"{OUT}/idx_fwe109_hu.npy", hu)
    json.dump({"manifest": MANIFEST, "rewizja": MANIFEST_REW, "components_sha256": sha(m), "plikow": len(pliki),
               "url_unikalnych": int(len(hu))}, open(f"{OUT}/fwe109.json", "w", encoding="utf-8"), indent=1)
    print("KONIEC", len(pliki), len(hu), flush=True)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    fwe109() if TRYB == "fwe109" else indeks_minhash(TRYB)
