"""Trzecia ręczna próbka (aneks 2 preregistracji 15.11.2026, pole aneks_2026_11_15b.reczna_probka_3), rng default_rng(2026111502):
  100 dokumentów z ewal_13gram PO zmianie (widok niezależny; wszystkie, gdy < 100) z trafiającymi 13-gramami spoza sumy list,
  200 nowych zachowanych do kontroli PII, z wyłączeniem 100 zachowanych ocenionych w drugim przeglądzie.
Wejście: powody.npz z agreguj.py liczonego z ew13b. Plik wynikowy ma PII: zostaje w robocze/.
Argumenty: katalog_przebiegu powody.npz katalog_ew13b probka_przegladu_2.jsonl listy_wykluczen(po przecinku) wyjscie.jsonl"""
import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np  # noqa: E402
import pyarrow.parquet as pq  # noqa: E402

import wspolne as w  # noqa: E402

D, POW, EW13, P2, LISTY, OUT = sys.argv[1:7]
SEED, N_EWAL, N_ZACH, MAKS_EWAL, MAKS_ZACH = 2026111502, 100, 200, 20000, 400000

jed = json.load(open(f"{D}/jednostki.json"))
meta = [json.load(open(f"{D}/u_{k:04d}.json", encoding="utf-8")) for k in range(len(jed))]
pocz = np.concatenate([[0], np.cumsum([len(m["ids"]) for m in meta])])
urls = [u for m in meta for u in m["urls"]]
Z = np.load(POW, allow_pickle=False)
nazwy, M, zostaje, ntok = list(Z["nazwy"]), Z["m"], Z["zostaje"], Z["ntok"]
assert int(M[:, nazwy.index("ewal_13gram")].sum()) == int(np.load(f"{EW13}/ew13_po_wykl.npy").sum())


def tekst(i):
    j = int(np.searchsorted(pocz, i, "right") - 1)
    return pq.ParquetFile(jed[j][0]).read_row_group(jed[j][1], columns=["text"]).column(0).to_pylist()[int(i - pocz[j])]


g = np.random.default_rng(SEED)
kand = np.flatnonzero(M[:, nazwy.index("ewal_13gram")])
wybor = [("odrzucony", "ewal_13gram", int(i), len(kand)) for i in np.sort(g.choice(kand, min(N_EWAL, len(kand)), replace=False))]
stare = {json.loads(x)["nr"] for x in open(P2, encoding="utf-8") if json.loads(x)["grupa"] == "zachowany"}
assert len(stare) == 100 and all(zostaje[i] for i in stare)
kz = np.array([i for i in np.flatnonzero(zostaje) if int(i) not in stare])
wybor += [("zachowany", None, int(i), len(kz)) for i in np.sort(g.choice(kz, N_ZACH, replace=False))]
print("wybrano", collections.Counter(x[0] for x in wybor), "populacja ewal", len(kand), "zachowanych bez starych", len(kz), flush=True)

czesci = []
for sc in LISTY.split(","):
    czesci.append(np.load(sc)["hasze"] if sc.endswith(".npz") else np.array([int(h) for h in json.load(open(sc, encoding="utf-8"))["hasze"]], np.uint64))
wykl = set(np.unique(np.concatenate(czesci)).tolist())
e = np.load(f"{EW13}/ew13_traf.npz")
ng = {int(x["hasz"]): x for x in json.load(open(f"{EW13}/ew13_ngramy.json", encoding="utf-8"))["ngramy"]}
ew_info = {}
for d, a, b in zip(e["doc"], e["poczatek"][:-1], e["poczatek"][1:]):
    hs = [int(h) for h in e["hasze"][a:b] if int(h) not in wykl]
    ew_info[int(d)] = [{"tekst": ng[h]["tekst"], "df_w_probce": ng[h]["df"], "testy": ng[h]["testy"]} for h in hs]

with open(OUT, "w", encoding="utf-8") as f:
    for gr, p, i, n_pop in wybor:
        t = tekst(i) or ""
        rec = {"nr": i, "grupa": gr, "powod_probki": p, "populacja": n_pop, "wszystkie_powody": [nazwy[k] for k in np.flatnonzero(M[i])],
               "url": urls[i], "host": w.host(urls[i]), "tokeny_v6": int(ntok[i]), "znakow": len(t)}
        if p == "ewal_13gram":
            assert ew_info.get(i), i
            rec["tekst"] = t[:MAKS_EWAL]
            rec["dowod_filtra"] = {"trafiajace_13gramy_poza_listami": ew_info[i][:20], "trafien_poza_listami": len(ew_info[i])}
        else:
            rec["tekst"] = t[:MAKS_ZACH]
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
print("KONIEC", flush=True)
