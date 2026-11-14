"""Stosuje reguły preregistracji do wyników przebiegu, NER i detektora katalogów: lista wierszy do usunięcia z powodem
(jeden powód na wiersz wg priorytetu), pełne liczniki, tokeny usunięte per powód, krótkie napisy per test, próbki kontrolne.
Tokeny v6 z EOT. Argumenty: wejscie.parquet katalog_przebieg ner_decyzje.json katalog_decyzje.json katalog_ewal wyjscie_usuniecia.json wyjscie_probki.md katalog_v6."""
import collections
import json
import os
import pickle
import random
import sys

import numpy as np
import pyarrow.parquet as pq

WE, PR, NER_D, KAT_D, EW, WY, PROB, V6 = sys.argv[1:9]
PRIORYTET = ["pg", "jezyk", "mojibake", "katalog", "pii", "ewal", "baza", "mojibake_resztki", "jezyk_resztki"]


def regula_jezyk(m):
    return (m["en"] < 0.05 and m["obcy"] >= m["en"] + 0.05) or (m["en"] < 0.03 and m["obcy"] >= m["en"]) or (m["nielat"] >= 0.30 and m["en"] < 0.05)


pf = pq.ParquetFile(WE)
pozycja, tokeny, zrodlo = {}, {}, {}
for g in range(pf.num_row_groups):
    n_v6 = np.load(f"{V6}/n_{g:04d}.npy")
    for i, x in enumerate(pf.read_row_group(g, columns=["id_zrodla", "zrodlo"]).to_pylist()):
        pozycja[x["id_zrodla"]] = (g, i)
        tokeny[(g, i)] = int(n_v6[i])
        zrodlo[(g, i)] = x["zrodlo"]
wszystkich = pf.metadata.num_rows

pii = json.load(open(NER_D, encoding="utf-8"))
kat = json.load(open(KAT_D, encoding="utf-8"))
flagi = {}
kr_dok = collections.Counter()
kr_traf = collections.defaultdict(list)
grup = 0
for p in sorted(os.listdir(PR)):
    if p.endswith(".pkl"):
        d = pickle.load(open(f"{PR}/{p}", "rb"))
        grup += 1
        for f in d["flagi"]:
            flagi[(f["rg"], f["i"])] = f
        kr_dok.update(d["kr_dok"])
        for n, v in d["kr_traf"].items():
            kr_traf[n].append(v)
if grup != pf.metadata.num_row_groups:
    raise SystemExit(f"niepełny przebieg: {grup} grup")


def wpis(k):
    return flagi.setdefault(k, {"rg": k[0], "i": k[1], "zrodlo": zrodlo[k]})


for x in pii["usun"]:
    if x["id"] not in pozycja:
        raise SystemExit("nieznany id PII: " + x["id"])
    wpis(pozycja[x["id"]])["pii"] = x["klasa"]
for x in kat["wiersze"]:
    wpis((x["rg"], x["i"]))["katalog"] = x["klasy"]

pow_w_wierszu = {}
pelne = collections.Counter()
per_zrodlo = collections.defaultdict(collections.Counter)
tok_powod = collections.Counter()
ewal_test = collections.Counter()
ewal_test_wyl = collections.Counter()
baza_cnt = collections.Counter()
baza_det = {"minhash": 0, "szkic": 0}
kat_klasy = collections.Counter()
jezyk_lista, moj_lista = [], []
moj_scisle = collections.Counter()
for k, f in flagi.items():
    prow = []
    if f.get("pg"):
        prow.append("pg")
    if "jezyk" in f:
        z = regula_jezyk(f["jezyk"])
        jezyk_lista.append((f, z))
        if z:
            prow.append("jezyk")
        elif f["jezyk"]["obcy"] > f["jezyk"]["en"]:
            prow.append("jezyk_resztki")
    if "mojibake" in f:
        z = f["mojibake"] >= 3
        moj_lista.append((f, z))
        if z:
            prow.append("mojibake")
        else:
            prow.append("mojibake_resztki")
            moj_scisle[f["mojibake"]] += 1
    if f.get("katalog"):
        prow.append("katalog")
        for c in f["katalog"]:
            kat_klasy[c] += 1
    if f.get("pii"):
        prow.append("pii")
    if f.get("ewal"):
        prow.append("ewal")
        for t in f["ewal"]:
            ewal_test[t] += 1
    if f.get("baza"):
        prow.append("baza")
        for nz, (u, est) in f["baza"].items():
            baza_cnt[nz] += 1
            if est is not None and est >= 0.8:
                baza_det["minhash"] += 1
            if u is not None and u >= 0.5:
                baza_det["szkic"] += 1
    for x in prow:
        pelne[x] += 1
    if prow:
        wyb = next(p for p in PRIORYTET if p in prow)
        pow_w_wierszu[k] = wyb
        per_zrodlo[wyb][f["zrodlo"]] += 1
        tok_powod[wyb] += tokeny[k]
        if wyb == "ewal":
            for t in f["ewal"]:
                ewal_test_wyl[t] += 1

kr_final = {n: np.unique(np.concatenate(v)) for n, v in kr_traf.items() if v}
kr_wyn = {"dokumenty_z_trafieniem_per_dlugosc": {str(k): v for k, v in kr_dok.items()}, "testy": {}}
for p in sorted(os.listdir(EW)):
    if p.endswith("__krotkie.npz") and not p.startswith("wszystkie"):
        t = p[:-len("__krotkie.npz")]
        d = np.load(f"{EW}/{p}")
        ogol, traf = 0, 0
        for n in range(1, 13):
            a = d[f"n{n}"]
            ogol += len(a)
            if n in kr_final and len(a):
                traf += int(np.isin(a, kr_final[n]).sum())
        kr_wyn["testy"][t] = {"krotkich_napisow": ogol, "trafionych_w_korpusie": traf}

kat_tok = collections.Counter()
for x in kat["wiersze"]:
    kat_tok[x["klasy"][0]] += tokeny[(x["rg"], x["i"])]
kat["liczby"]["tokeny_wg_pierwszej_klasy"] = dict(kat_tok)
liczby = {"tokeny_v6_wejscia": sum(tokeny.values()), "mojibake_resztki_wg_liczby_scislej": {str(a): b for a, b in sorted(moj_scisle.items())}, "wszystkich_wierszy": wszystkich, "usuniete_wg_priorytetu": dict(collections.Counter(pow_w_wierszu.values())), "tokeny_usuniete_wg_priorytetu": dict(tok_powod),
          "pelne_liczniki": dict(pelne), "per_zrodlo": {k: dict(v) for k, v in per_zrodlo.items()}, "ewal_per_test_wszystkie": dict(ewal_test),
          "ewal_per_test_przy_powodzie_ewal": dict(ewal_test_wyl), "baza_per_baza": dict(baza_cnt), "baza_detektor": baza_det, "katalog_klasy": dict(kat_klasy),
          "katalog_liczby": kat["liczby"], "katalog_test_negatywny": kat["test_negatywny_pelny_przebieg"], "katalog_pozytyw": kat["pozytyw_51718_cz10"],
          "jezyk": {"oznaczone_inny": len(jezyk_lista), "usuniete": sum(1 for _, z in jezyk_lista if z)},
          "mojibake": {"oznaczone_regexem": len(moj_lista), "usuniete": sum(1 for _, z in moj_lista if z), "z_trafieniem_ponizej_progu": sum(1 for _, z in moj_lista if not z)}, "krotkie_napisy": kr_wyn,
          "pii_decyzje": {"usun": len(pii["usun"]), "zostaw_klasy": pii.get("zostaw_klasy")}}
json.dump({"wiersze": sorted([list(k) + [v] for k, v in pow_w_wierszu.items()]), "liczby": liczby}, open(WY, "w", encoding="utf-8"), ensure_ascii=False)

rng = random.Random(20261110)
with open(PROB, "w", encoding="utf-8") as f:
    for nazwa, lista, klucz in (("JEZYK usunięte", [x for x in jezyk_lista if x[1]], "jezyk"), ("JEZYK zostają", [x for x in jezyk_lista if not x[1]], "jezyk"),
                                ("MOJIBAKE usunięte", [x for x in moj_lista if x[1]], "mojibake"), ("MOJIBAKE zostają", [x for x in moj_lista if not x[1]], "mojibake")):
        f.write(f"\n## {nazwa}: {len(lista)}\n")
        for fl, _ in rng.sample(lista, min(30, len(lista))):
            f.write(f"- {fl['zrodlo']} {fl.get('id')} {fl.get(klucz)}\n")
print(json.dumps({k: v for k, v in liczby.items() if k != "krotkie_napisy"}, ensure_ascii=False)[:3500])
