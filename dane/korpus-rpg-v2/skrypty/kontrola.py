"""Kontrola końcowa na gotowym korpusie (default/train): wstawione duplikaty i fragmenty ewaluacji oraz wiersze bazy.
Metody jak w poprzedniej budowie. Argumenty: katalog_wyjscia_korpusu katalog_ewal idx_baz pobrania_baz wyjscie.json."""
import hashlib
import json
import os
import random
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np  # noqa: E402
import pyarrow.parquet as pq  # noqa: E402

import rdzen as r  # noqa: E402
import rdzen2 as r2  # noqa: E402

KOR, EW, IDX, POB, WY = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
A, B = r.perm_param(128)
SEED = 20261111
rng = random.Random(SEED)
BANDY, WIERSZE = 32, 4


def sig(t):
    w = r.hasze_slow(r.norm_slowa(t))
    s = r.podpis(np.unique(r.ngramy(w, 5)), A, B)
    return s


def wykryj(n, src):
    en, es = " ".join(r.norm_slowa(n)), " ".join(r.norm_slowa(src))
    if hashlib.blake2b(en.encode(), digest_size=16).digest() == hashlib.blake2b(es.encode(), digest_size=16).digest():
        return "exact"
    sn, ss = sig(n), sig(src)
    if sn is not None and ss is not None:
        kn = r2.klucze_band(sn[None, :], BANDY, WIERSZE)
        ks = r2.klucze_band(ss[None, :], BANDY, WIERSZE)
        if (kn == ks).any() and float((sn == ss).mean()) >= 0.8:
            return "minhash"
    a, b = r.szkic(n), r.szkic(src)
    a, b = (a, b) if len(a) <= len(b) else (b, a)
    if len(a) >= r.MIN_PROBEK and len(np.intersect1d(a, b)) / len(a) >= r.PROG_ZAWIERANIA:
        return "szkic13"
    return None


pliki = sorted(f"{KOR}/data/default/{p}" for p in os.listdir(f"{KOR}/data/default") if p.startswith("train-"))
pul = []
for p in pliki[:2]:
    pf = pq.ParquetFile(p)
    for g in range(min(4, pf.num_row_groups)):
        for t in pf.read_row_group(g, columns=["text", "document_id"]).to_pylist():
            if 300 <= len(t["text"].split()) <= 8000:
                pul.append(t)
rng.shuffle(pul)
wyb, tlo = pul[:100], pul[100:3100]

# 1. duplikaty: 40 dokładnych po normalizacji, 40 bliskich (3% słów zmienione), 20 zawartych w większym tekście
typy = {"dokladny_po_normalizacji": [0, 0], "bliski_3pc_slow": [0, 0], "zawarty_w_wiekszym": [0, 0]}
det_cnt = {"exact": 0, "minhash": 0, "szkic13": 0}
sig_tlo = [sig(x["text"]) for x in tlo]
fp = 0
for j, x in enumerate(wyb):
    t = x["text"]
    if j < 40:
        typ, n = "dokladny_po_normalizacji", re.sub(r"[ ]+", "  ", t).upper()
    elif j < 80:
        sl = t.split(" ")
        for q in rng.sample(range(len(sl)), max(1, len(sl) // 33)):
            sl[q] = "qqqq" + sl[q]
        typ, n = "bliski_3pc_slow", " ".join(sl)
    else:
        ob = rng.choice(tlo)["text"]
        typ, n = "zawarty_w_wiekszym", ob[:3000] + "\n\n" + t + "\n\n" + ob[-1500:]
    typy[typ][0] += 1
    d = wykryj(n, t)
    if d:
        typy[typ][1] += 1
        det_cnt[d] += 1
    s_n = sig(n)
    if s_n is not None:
        for s_t, tl in zip(sig_tlo, tlo):
            if s_t is not None and tl["document_id"] != x["document_id"] and float((s_n == s_t).mean()) >= 0.8:
                fp += 1

wyn = {"duplikaty": {"typy_wstawione_wykryte": typy, "detektor": det_cnt, "falszywe_pary_z_tlem_jaccard_0_8": fp}}

# 2. dekontaminacja: 100 fragmentów prawdziwych tekstów ewaluacji wklejonych do dokumentów (min. 20 słów)
ind = np.load(f"{EW}/wszystkie_13.npy", mmap_mode="r")
kand = []
for tid in sorted(os.listdir(POB + "/ewal")):
    k = f"{POB}/ewal/{tid}"
    if not os.path.isdir(k):
        continue
    pl = sorted(p for p in os.listdir(k) if p.endswith(".parquet"))
    if not pl:
        continue
    try:
        pf = pq.ParquetFile(f"{k}/{pl[0]}")
        t = pf.read_row_group(0).to_pylist()
    except Exception:  # noqa: BLE001
        continue
    teksty = []
    for w in t[:500]:
        for v in w.values():
            if isinstance(v, str) and len(v.split()) >= 20:
                teksty.append(v)
                break
    if teksty:
        kand += rng.sample(teksty, min(4, len(teksty)))
rng.shuffle(kand)
kand = kand[:100]
wykr = 0
for frag, x in zip(kand, wyb):
    t = x["text"][:2000] + " " + frag + " " + x["text"][-1000:]
    n13 = np.unique(r.ngramy_tekstu(t, r.N_EVAL))
    if r.ma_trafienie(n13, ind):
        wykr += 1
wyn["ewaluacja_wstawione"] = {"wstawione": len(kand), "wykryte_13gram": wykr}

# 3. wiersze bazy: 100 wierszy technika-i-nauka (parquet) potraktowane jak dokumenty korpusu
szk = np.load(f"{IDX}/idx_technika_i_nauka_szkic.npy", mmap_mode="r")
sg = np.load(f"{IDX}/idx_technika_i_nauka_sig.npy", mmap_mode="r")
kl = np.load(f"{IDX}/idx_technika_i_nauka_kl.npy", mmap_mode="r")
dok = np.load(f"{IDX}/idx_technika_i_nauka_dok.npy", mmap_mode="r")
tx = [x for x in pq.read_table(f"{POB}/technika/validation.parquet", columns=["text"]).column(0).to_pylist() if x and len(x.split()) >= 150]
tx = rng.sample(tx, min(100, len(tx)))
wy_m, wy_s = 0, 0
for t in tx:
    w = r.hasze_slow(r.norm_slowa(t))
    x = np.unique(r.ngramy(w, r.N_EVAL))
    x = x[x % np.uint64(r.PROBKA) == 0]
    u = r.udzial(x, szk)
    if u is not None and u >= r.PROG_ZAWIERANIA:
        wy_s += 1
    s = r.podpis(np.unique(r.ngramy(w, 5)), A, B)
    klucze = r2.klucze_band(s[None, :], BANDY, WIERSZE).ravel()
    kandy = set()
    for k in klucze:
        a, e = np.searchsorted(kl, k, "left"), np.searchsorted(kl, k, "right")
        if e > a:
            kandy.update(np.asarray(dok[a:min(e, a + 500)]).tolist())
    if kandy and float((np.asarray(sg[sorted(kandy)]) == s).mean(axis=1).max()) >= 0.8:
        wy_m += 1
wyn["wiersze_bazy"] = {"baza": "technika_i_nauka", "wstawione": len(tx), "wykryte_minhash": wy_m, "wykryte_szkic13": wy_s}
wyn["seed"] = SEED
json.dump(wyn, open(WY, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(wyn, ensure_ascii=False))
