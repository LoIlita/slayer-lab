"""Indeksy porównania dla DCLM-EN w formacie RPG v2 (bazy_indeks.py): szkic 13-gramów (hash%16==0), MinHash 128, klucze LSH 32x4,
plus hasze url i znormalizowanego tekstu. Dwa zestawy:
  walidacja: walidacje i osie ewaluacji Fabryki (minimal-en-corpus-5b i 2b-v2 validation, oś FineWeb-Edu i oś DCLM/DataDecide Slayer150)
  ivme:      część DCLM miksu SlayerLab/sub150run-ivme-20b-v3 (28 batchy train-dclm, tokeny dekodowane tokenizerem zbioru)
Argumenty: walidacja|ivme katalog_pobran wyjscie procesy [minimal_5b_val.parquet minimal_2b_v2_val.parquet]"""
import hashlib
import json
import multiprocessing as mp
import os
import sys

os.environ["TOKENIZERS_PARALLELISM"] = "false"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np  # noqa: E402
import pyarrow.parquet as pq  # noqa: E402
from huggingface_hub import HfFileSystem, hf_hub_download  # noqa: E402
from tokenizers import Tokenizer  # noqa: E402

import wspolne as w  # noqa: E402
from wspolne import r, r2  # noqa: E402

TRYB, POB, OUT, PROC = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
A, B = r.perm_param(128)
IVME, IVME_REW = "SlayerLab/sub150run-ivme-20b-v3", "c9fa17d73a5134b34daa58b668ce7a400681c99d"
FWE, FWE_REW = "HuggingFaceFW/fineweb-edu", "87f09149ef4734204d70ed1d046ddc9ca3f2b8f9"
DD, DD_REW = "allenai/DataDecide-data-recipes", "3baf34ba"
DD_PLIK = "preprocessed/dclm/v0_fw_top3p/gpt-neox-olmo-dolma-v1_5/part-00-00000.npy"


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 24), b""):
            h.update(b)
    return h.hexdigest()


def licz(teksty):
    szk, sig, hx = [], [], []
    for x in teksty:
        sl = r.norm_slowa(x or "")
        hx.append(w.h64(" ".join(sl)))
        h = r.hasze_slow(sl)
        n13 = np.unique(r.ngramy(h, r.N_EVAL))
        szk.append(n13[n13 % np.uint64(r.PROBKA) == 0])
        s = r.podpis(np.unique(r.ngramy(h, 5)), A, B)
        sig.append(s if s is not None else np.zeros(128, np.uint64))
    return np.unique(np.concatenate(szk)) if szk else np.zeros(0, np.uint64), np.vstack(sig), np.array(hx, np.uint64)


def zapisz(nazwa, czesci, urls):
    szk = np.unique(np.concatenate([c[0] for c in czesci]))
    S = np.vstack([c[1] for c in czesci])
    hx = np.concatenate([c[2] for c in czesci])
    kl = r2.klucze_band(S, 32, 4).ravel()
    dk = np.repeat(np.arange(S.shape[0], dtype=np.int64), 32)
    por = np.argsort(kl, kind="stable")
    for k, v in (("szkic", szk), ("sig", S), ("kl", kl[por]), ("dok", dk[por]), ("hx", np.unique(hx)),
                 ("hu", np.unique(np.array([w.h64(w.norm_url(u)) for u in urls if u], np.uint64)))):
        np.save(f"{OUT}/idx_{nazwa}_{k}.npy", v)
    return {"dokumentow": int(S.shape[0]), "probek_szkicu": int(len(szk)), "url": len(set(u for u in urls if u))}


def paczki(teksty, n=2000):
    return [teksty[i:i + n] for i in range(0, len(teksty), n)]


def walidacja(val5b, val2b):
    zr, teksty, urls = {}, [], []
    for nazwa, p in (("minimal-en-corpus-5b@bb3aec23 validation/shard-00000.parquet", val5b), ("minimal-en-corpus-2b-v2@ef0ab069 validation/shard-00000.parquet", val2b)):
        t = pq.read_table(p).to_pylist()
        for x in t:
            teksty.append(x["text"])
            u = json.loads(x["metadata_json"]).get("url") if x.get("metadata_json") else None
            urls.append(u)
        zr[nazwa] = {"dokumentow": len(t), "sha256": sha(p), "zrodla": sorted({x["source_id"] for x in t})}
    fs = HfFileSystem()
    with fs.open(f"datasets/{FWE}@{FWE_REW}/sample/100BT/000_00009.parquet", "rb") as h:
        pf = pq.ParquetFile(h)
        wz, g = [], 0
        while len(wz) < 5000:
            wz += pf.read_row_group(g, columns=["text", "url"]).to_pylist()
            g += 1
    wz = wz[:5000]
    teksty += [x["text"] for x in wz]
    urls += [x["url"] for x in wz]
    zr["os FineWeb-Edu Slayer150: fineweb-edu sample/100BT/000_00009.parquet, pierwsze 5000 wierszy (nadzbiór 3507 zachowanych)"] = {"dokumentow": 5000}
    tok = Tokenizer.from_file(hf_hub_download("EleutherAI/gpt-neox-20b", "tokenizer.json", local_dir=f"{POB}/gptneox"))
    with fs.open(f"datasets/{DD}@{DD_REW}/{DD_PLIK}", "rb") as h:
        surowe = h.read(64 << 20)
    # plik bez nagłówka npy: surowy memmap uint16 (format dolma/OLMo), dokumenty kończy EOS 50279 (sprawdzone na pierwszych 4000 B)
    opis, dt, eos = "brak nagłówka npy, surowe uint16", np.dtype("<u2"), 50279
    ids = np.frombuffer(surowe[: len(surowe) // 2 * 2], dtype=dt).astype(np.int64)
    gr = np.flatnonzero(ids == eos)
    dok = [ids[a + 1:b].tolist() for a, b in zip(np.concatenate([[-1], gr[:-1]]), gr)][:5000]
    dok = [d for d in dok if d]
    teksty += tok.decode_batch(dok, skip_special_tokens=True)
    urls += [None] * len(dok)
    zr[f"os DCLM Slayer150: {DD}@{DD_REW} {DD_PLIK}, pierwsze {len(dok)} dokumentów (nadzbiór 3457 zachowanych)"] = {
        "dokumentow": len(dok), "dtype": str(dt), "eos": int(eos), "naglowek": opis}
    with mp.get_context("fork").Pool(PROC) as p:
        cz = p.map(licz, paczki(teksty))
    wyn = {"zrodla": zr, "indeks": zapisz("walidacja", cz, urls)}
    json.dump(wyn, open(f"{OUT}/walidacja.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(json.dumps(wyn, ensure_ascii=False))


def ivme():
    lock = hf_hub_download(IVME, "metadata/sources.lock.json", repo_type="dataset", revision=IVME_REW, local_dir=f"{POB}/ivme")
    tk = hf_hub_download(IVME, "metadata/tokenizer.json", repo_type="dataset", revision=IVME_REW, local_dir=f"{POB}/ivme")
    tok = Tokenizer.from_file(tk)
    teksty, batche = [], []
    for i in range(28):
        d = f"train-batches/train-dclm-{i:06d}"
        sj = json.load(open(hf_hub_download(IVME, f"{d}/source.json", repo_type="dataset", revision=IVME_REW, local_dir=f"{POB}/ivme")))
        b = hf_hub_download(IVME, f"{d}/shard-00000.bin", repo_type="dataset", revision=IVME_REW, local_dir=f"{POB}/ivme")
        e = np.load(hf_hub_download(IVME, f"{d}/shard-00000.bin.ends.npy", repo_type="dataset", revision=IVME_REW, local_dir=f"{POB}/ivme"))
        x = np.fromfile(b, dtype=np.uint16)
        p0 = np.concatenate([[0], e[:-1]])
        dok = [x[a:c].tolist() for a, c in zip(p0, e)]
        teksty += tok.decode_batch(dok, skip_special_tokens=True)
        batche.append({"batch": d, "dokumentow": len(dok), "tokeny": int(len(x)), "sha256_bin": sha(b), "zrodlo": sj.get("provenance", sj).get("files_read", None) or sj.get("source_file") or str(sj)[:300]})
        print(d, len(dok), flush=True)
    with mp.get_context("fork").Pool(PROC) as p:
        cz = p.map(licz, paczki(teksty))
    wyn = {"repo": IVME, "rewizja": IVME_REW, "tokenizer_sha256": sha(tk), "lock_sha256": sha(lock), "batche": batche, "indeks": zapisz("ivme", cz, [])}
    json.dump(wyn, open(f"{OUT}/ivme.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(json.dumps(wyn["indeks"]), flush=True)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    if TRYB == "walidacja":
        walidacja(sys.argv[5], sys.argv[6])
    else:
        ivme()
