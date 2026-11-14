"""Agregacja dnia 1: dedup wewnątrz próbki, kaskada powodów, uzysk w dokumentach i tokenach v6, nakładanie z bazami,
uzysk per plik i szacunek liczby shardów, wybór ręcznej próbki 100/100. Progi: preregistracja.json.
Argumenty: katalog_przebiegu probka_pliki.json fwe_url_h.npy edu.npz wyjscie.json probki_reczne.jsonl [walidacja=katalog ivme=katalog]
Indeksy dodatkowe z indeksy.py (te same katalogi co w przebieg.py)."""
import collections
import json
import math
import os
import sys

import numpy as np
import pyarrow.parquet as pq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wspolne as w  # noqa: E402
from wspolne import r2  # noqa: E402

D, PROBKA, FWE, EDU, OUT, RECZNE = sys.argv[1:7]
DODATKOWE = dict(a.split("=", 1) for a in sys.argv[7:])
PREREG = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "preregistracja.json"), encoding="utf-8"))
jed = json.load(open(f"{D}/jednostki.json"))
cz = collections.defaultdict(list)
meta = []
for k in range(len(jed)):
    z = np.load(f"{D}/u_{k:04d}.npz")
    for kk in z.files:
        cz[kk].append(z[kk])
    meta.append(json.load(open(f"{D}/u_{k:04d}.json", encoding="utf-8")))
X = {kk: np.concatenate(v) for kk, v in cz.items()}
N = len(X["ntok"])
plik_dok = np.concatenate([np.full(len(m["ids"]), i) for i, m in enumerate(meta)])
plik_nazwa = [m["plik"] for m in meta]
plik_dok = np.array([plik_nazwa[i] for i in plik_dok])
urls = [u for m in meta for u in m["urls"]]
ids = [u for m in meta for u in m["ids"]]
tok = X["ntok"]

# ---- dedup wewnątrz próbki: (a) identyczny tekst, (b) MinHash LSH 32x4, J >= 0,8 do wcześniejszego dokumentu
_, pierwsze = np.unique(X["hx"], return_index=True)
dup_dokl = np.ones(N, bool)
dup_dokl[pierwsze] = False
dup_mh = np.zeros(N, bool)
S, ms = X["sig"], X["ma_sig"]
z_sig = np.flatnonzero(ms)
kl = r2.klucze_band(S[z_sig], 32, 4)
for b in range(32):
    k = kl[:, b]
    por0 = np.argsort(k, kind="stable")
    ks = k[por0]
    por = z_sig[por0]
    st = np.concatenate([[0], np.flatnonzero(np.diff(ks) != 0) + 1])
    ro = np.diff(np.concatenate([st, [len(ks)]]))
    for s0, n0 in zip(st[ro > 1], ro[ro > 1]):
        g = np.sort(por[s0:s0 + n0])[:200]
        for j in range(1, len(g)):
            if dup_mh[g[j]]:
                continue
            if np.max((S[g[:j]] == S[g[j]]).mean(axis=1)) >= 0.8:
                dup_mh[g[j]] = True
dedup_w = dup_dokl | dup_mh


def baza(nz):
    a = X[f"bz_{nz}"]
    with np.errstate(invalid="ignore"):
        return (a[:, 0] >= 0.5) | (a[:, 1] >= 0.8)


def dodatkowa(nz):
    """Indeks z indeksy.py: MinHash/szkic (jak baza) albo identyczny znormalizowany tekst albo identyczny url."""
    if nz not in DODATKOWE or f"bz_{nz}" not in X:
        return None
    kat = DODATKOWE[nz]
    hx = np.isin(X["hx"], np.load(f"{kat}/idx_{nz}_hx.npy"))
    hu = np.isin(X["hu"], np.load(f"{kat}/idx_{nz}_hu.npy"))
    wyn_dod[nz] = {"minhash_lub_szkic": int(baza(nz).sum()), "identyczny_tekst": int(hx.sum()), "identyczny_url": int(hu.sum())}
    return baza(nz) | hx | hu


wyn_dod = {}
powody = {
    "walidacja_fabryki": dodatkowa("walidacja"),
    "domena_testow": X["dom"] > 0,
    "ewal_13gram": X["ew"],
    "pii": X["pii"] > 0,
    "mojibake": X["moj"] >= 3,
    "dedup_wewnatrz": dedup_w,
    "dedup_slayer107": baza("slayer_107_en"),
    "dedup_ivme": dodatkowa("ivme"),
}
kolej = PREREG["kolejnosc_powodow"]
T = int(tok.sum())
wyn = {"dokumenty": N, "tokeny_v6": T, "tokeny_na_dok": T / N, "dok_z_id0": int(X["id0"].sum()), "kaskada": [], "niezaleznie": {}, "niedostepne": []}
zostaje = np.ones(N, bool)
pierwszy_powod = np.array([""] * N, dtype=object)
for p in kolej:
    f = powody.get(p)
    if f is None:
        wyn["niedostepne"].append(p)
        continue
    nowe = f & zostaje
    pierwszy_powod[nowe] = p
    zostaje &= ~f
    wyn["kaskada"].append({"powod": p, "odrzucone_dok": int(nowe.sum()), "odrzucone_tok": int(tok[nowe].sum()),
                           "zostaje_dok": int(zostaje.sum()), "zostaje_tok": int(tok[zostaje].sum()),
                           "zostaje_dok_proc": round(100 * zostaje.sum() / N, 3), "zostaje_tok_proc": round(100 * tok[zostaje].sum() / T, 3)})
    wyn["niezaleznie"][p] = {"dok": int(f.sum()), "tok": int(tok[f].sum()), "dok_proc": round(100 * f.sum() / N, 3), "tok_proc": round(100 * tok[f].sum() / T, 3)}
wyn["uzysk"] = {"dok": int(zostaje.sum()), "tok": int(tok[zostaje].sum()), "dok_proc": round(100 * zostaje.sum() / N, 3), "tok_proc": round(100 * tok[zostaje].sum() / T, 3)}

# ---- szczegóły powodów
wyn["indeksy_dodatkowe"] = wyn_dod
wyn["dedup_wewnatrz_szczegoly"] ={"identyczny_tekst": int(dup_dokl.sum()), "minhash_bez_identycznych": int((dup_mh & ~dup_dokl).sum())}
wyn["domeny"] = {d: int((X["dom"] == i + 1).sum()) for i, d in enumerate(w.DOMENY_TESTOW)}
wyn["pii_klasy"] = {kk: int(((X["pii"] & v) > 0).sum()) for kk, v in (("email", 1), ("telefon", 2), ("ip", 4))}
ct = collections.Counter()
for m in meta:
    for v in m["ew_testy"].values():
        ct.update(v)
wyn["ewal_per_test"] = dict(ct.most_common())
krd = collections.Counter()
for m in meta:
    krd.update({int(a): b for a, b in m["kr_dok"].items()})
wyn["krotkie_napisy_dok_per_n"] = dict(sorted(krd.items()))
for nz in ("slayer_107_en", "ivme", "walidacja"):
    if f"bz_{nz}" in X:
        a = X[f"bz_{nz}"]
        with np.errstate(invalid="ignore"):
            wyn[f"nakladanie_{nz}"] = {"szkic13_ge_0_5": int((a[:, 0] >= 0.5).sum()), "minhash_ge_0_8": int((a[:, 1] >= 0.8).sum()),
                                       "ktorekolwiek": int(baza(nz).sum()), "ktorekolwiek_tok": int(tok[baza(nz)].sum())}

# ---- FineWeb-Edu po url (pomiar, nie filtr)
fh = np.load(FWE)
fj = json.load(open(os.path.join(os.path.dirname(FWE), "fwe_url.json")))
traf = np.isin(X["hu"], fh)
f_ = fj["udzial_probki_w_fwe"]
wyn["fineweb_edu_url"] = {"trafienia_dok": int(traf.sum()), "trafienia_proc": round(100 * traf.sum() / N, 4),
                          "trafienia_wsrod_zachowanych": int((traf & zostaje).sum()), "udzial_probki_fwe": f_,
                          "ekstrapolacja_liniowa_gorna_proc": round(min(100.0, 100 * traf.sum() / N / f_), 2),
                          "url_unikalne_w_probce_dclm": int(len(np.unique(X["hu"])))}

# ---- klasyfikator FineWeb-Edu (podpróbka)
if os.path.exists(EDU):
    e = np.load(EDU)
    ix, isc = e["idx"], e["int_score"]
    rozk = {int(s): int((isc == s).sum()) for s in range(6)}
    wyn["edu"] = {"n": int(len(ix)), "rozklad_int_score": rozk, "rozklad_proc": {s: round(100 * v / len(ix), 2) for s, v in rozk.items()},
                  "srednia_score": float(e["score"].mean())}
    for prog in (2, 3):
        m = isc >= prog
        wyn["edu"][f"prog_ge_{prog}"] = {"dok_proc": round(100 * m.mean(), 2), "tok_proc": round(100 * tok[ix][m].sum() / tok[ix].sum(), 2),
                                         "tok_proc_wsrod_zachowanych": round(100 * tok[ix][m & zostaje[ix]].sum() / max(1, tok[ix][zostaje[ix]].sum()), 2)}
    wyn["edu"]["int_score_zachowane_vs_odrzucone"] = {"zachowane_srednia": float(e["score"][zostaje[ix]].mean()), "odrzucone_srednia": float(e["score"][~zostaje[ix]].mean())}

# ---- uzysk per plik i szacunek shardów do 5 mld tokenów v6
pp = []
for p in sorted(set(plik_dok)):
    m = plik_dok == p
    pp.append({"plik": os.path.basename(os.path.dirname(os.path.dirname(p))) + "/" + os.path.basename(os.path.dirname(p)) + "/" + os.path.basename(p).replace(".rg5000", ""),
               "dok": int(m.sum()), "tok": int(tok[m].sum()), "tok_zostaje": int(tok[m & zostaje].sum())})
z = np.array([x["tok_zostaje"] for x in pp], dtype=float)
sr, se = z.mean(), z.std(ddof=1) / math.sqrt(len(z))
wyn["per_plik"] = pp
wyn["szacunek_shardow_5mld"] = {"tok_zostaje_na_shard_srednia": sr, "se": se, "shardy": math.ceil(5e9 / sr),
                                "shardy_przedzial": [math.ceil(5e9 / (sr + 2 * se)), math.ceil(5e9 / (sr - 2 * se))],
                                "uwaga": "dolna granica: dedup między shardami i wobec baz rośnie z liczbą shardów"}
json.dump(wyn, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)

# ---- ręczna próbka 100 zachowanych + 100 odrzuconych (pliki tylko w pracowni: zawierają PII odrzuconych)
g = np.random.default_rng(w.SEED)
zach = np.sort(g.choice(np.flatnonzero(zostaje), 100, replace=False))
odrz = np.sort(g.choice(np.flatnonzero(~zostaje), 100, replace=False))
pocz = np.concatenate([[0], np.cumsum([len(m["ids"]) for m in meta])])
with open(RECZNE, "w", encoding="utf-8") as f:
    for grupa, idxs in (("zachowany", zach), ("odrzucony", odrz)):
        for i in idxs:
            j = int(np.searchsorted(pocz, i, "right") - 1)
            t = pq.ParquetFile(jed[j][0]).read_row_group(jed[j][1], columns=["text"]).column(0)[int(i - pocz[j])].as_py()
            f.write(json.dumps({"nr": int(i), "grupa": grupa, "powod": pierwszy_powod[i] or None, "url": urls[i], "tokeny_v6": int(tok[i]),
                                "tekst": t[:1500]}, ensure_ascii=False) + "\n")
print(json.dumps({kk: wyn[kk] for kk in ("dokumenty", "tokeny_v6", "uzysk", "niedostepne")}, ensure_ascii=False))
for x in wyn["kaskada"]:
    print(x)
print(wyn["szacunek_shardow_5mld"])
