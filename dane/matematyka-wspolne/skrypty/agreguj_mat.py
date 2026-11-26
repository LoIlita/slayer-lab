"""Agregacja zbioru matematyki/kodu (#346): powody odrzucenia w kolejności z preregistracji, kaskada i widok niezależny, uzysk
w dokumentach i tokenach v6, wybór dokumentów do eksportu (cel eksportu) i ręczna próbka do przeglądu.
Wejście z przebieg.py DCLM-EN (u_NNNN.npz/json) i ewal_czeste.py DCLM-EN (ew13_traf.npz, ew13_ngramy.json, bez listy wykluczeń).
Reguła ewal_13gram (preregistracja.json -> ewal_13gram): dokument odpada, gdy ma trafiający 13-gram nietrywialny, który
należy do testu z listy 'testy_scisle' (niezależnie od df) albo ma df < df_min w puli.
Argumenty: zbior katalog_przebiegu katalog_ew13 preregistracja.json wyjscie.json probka_przegladu.jsonl wybor.json
           [walidacja=katalog_idx_wal] [oryg=katalog_przebiegu_oryg,katalog_ew13_oryg]"""
import collections
import json
import os
import re
import sys

import numpy as np
import pyarrow.parquet as pq

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "dclm-en", "skrypty"))
import wspolne as w  # noqa: E402
from wspolne import r, r2  # noqa: E402

ZB, D, EW13, PREREG_P, OUT, PRZEGLAD, WYBOR = sys.argv[1:8]
OPC = dict(a.split("=", 1) for a in sys.argv[8:])
P = json.load(open(PREREG_P, encoding="utf-8"))
if "aneksy_przejete" in P:  # preregistracja odsyła do aneksów InfiWebMath-4+ zamiast je kopiować (oeis, formalna)
    _baza = json.load(open(os.path.join(os.path.dirname(PREREG_P), "..", "..", "infiwebmath4", "skrypty", "preregistracja.json"), encoding="utf-8"))
    for _k in re.findall(r"aneks_\d{4}_\d{2}_\d{2}[a-z]?", json.dumps(P["aneksy_przejete"])):  # tekst albo słownik odwołań
        P.setdefault(_k, _baza[_k])
SEED = P["seed"]
jed = json.load(open(f"{D}/jednostki.json"))


def wczytaj(katalog):
    cz, meta = collections.defaultdict(list), []
    for k in range(len(jed)):
        z = np.load(f"{katalog}/u_{k:04d}.npz")
        for kk in z.files:
            cz[kk].append(z[kk])
        meta.append(json.load(open(f"{katalog}/u_{k:04d}.json", encoding="utf-8")))
    return {kk: np.concatenate(v) for kk, v in cz.items()}, meta


X, meta = wczytaj(D)
N = len(X["ntok"])
tok = X["ntok"]
pocz = np.concatenate([[0], np.cumsum([len(m["ids"]) for m in meta])])
urls = [u for m in meta for u in m["urls"]]
ids = [u for m in meta for u in m["ids"]]


def kolumna(nazwa, jednostki=None):
    """Kolumna lokalnej kopii puli w kolejności dokumentów przebiegu, strumieniowo po grupach wierszy: pełna pula części 2
    (miliony dokumentów, dziesiątki GB tekstu) nie mieści się w pamięci jako lista."""
    for sciezka, g in (jednostki or jed):
        yield from pq.ParquetFile(sciezka).read_row_group(g, columns=[nazwa]).column(0).to_pylist()


def tekst(i):
    j = int(np.searchsorted(pocz, i, "right") - 1)
    return pq.ParquetFile(jed[j][0]).read_row_group(jed[j][1], columns=["text"]).column(0)[int(i - pocz[j])].as_py()


# ---- ewal_13gram wg reguły preregistracji
R13 = P["ewal_13gram"]
SCISLE = set(R13["testy_scisle"])


def ewal(katalog_ew13, n):
    tr = np.load(f"{katalog_ew13}/ew13_traf.npz")
    ng = {int(x["hasz"]): x for x in json.load(open(f"{katalog_ew13}/ew13_ngramy.json", encoding="utf-8"))["ngramy"]}

    def liczy(h):
        x = ng[h]
        if all(s.isdigit() or len(s) == 1 for s in x["tekst"].split()):
            return False
        return bool(SCISLE & set(x["testy"])) or x["df"] < R13["df_min"]

    flaga = np.zeros(n, bool)
    per_test = collections.Counter()
    for d, a, b in zip(tr["doc"], tr["poczatek"][:-1], tr["poczatek"][1:]):
        liczace = [h for h in tr["hasze"][a:b].tolist() if liczy(h)]
        if liczace:
            flaga[d] = True
            per_test.update({t for h in liczace for t in ng[h]["testy"]})
            TRAF[(katalog_ew13, int(d))] = [{"ngram": ng[h]["tekst"], "testy": ng[h]["testy"], "df": ng[h]["df"]} for h in liczace[:5]]
    return flaga, dict(per_test.most_common())


TRAF = {}  # (katalog ew13, dokument) -> do 5 liczących się 13-gramów: pokazywane w ręcznej próbce


ew, ew_per_test = ewal(EW13, N)

# ---- dedup wewnątrz puli: identyczny tekst albo MinHash LSH 32x4, J >= 0,8 do wcześniejszego dokumentu (jak DCLM-EN)
_, pierwsze, odwr = np.unique(X["hx"], return_index=True, return_inverse=True)
dup_dokl = np.ones(N, bool)
dup_dokl[pierwsze] = False
para_w = np.full(N, -1, np.int64)
para_w[dup_dokl] = pierwsze[odwr[dup_dokl]]
dup_mh = np.zeros(N, bool)
S, ms = X["sig"], X["ma_sig"]
z_sig = np.flatnonzero(ms)
kl = r2.klucze_band(S[z_sig], 32, 4)
for b in range(32):
    k = kl[:, b]
    por0 = np.argsort(k, kind="stable")
    ks, por = k[por0], z_sig[por0]
    st = np.concatenate([[0], np.flatnonzero(np.diff(ks) != 0) + 1])
    ro = np.diff(np.concatenate([st, [len(ks)]]))
    for s0, n0 in zip(st[ro > 1], ro[ro > 1]):
        g = np.sort(por[s0:s0 + n0])[:200]
        for j in range(1, len(g)):
            if dup_mh[g[j]]:
                continue
            pod = (S[g[:j]] == S[g[j]]).mean(axis=1)
            if np.max(pod) >= 0.8:
                dup_mh[g[j]] = True
                if para_w[g[j]] < 0:
                    para_w[g[j]] = g[int(np.argmax(pod))]


def baza(nz):
    a = X[f"bz_{nz}"]
    with np.errstate(invalid="ignore"):
        return (a[:, 0] >= 0.5) | (a[:, 1] >= 0.8)


powody = {"ewal_13gram": ew, "mojibake": X["moj"] >= 3, "dedup_wewnatrz": dup_dokl | dup_mh, "dedup_slayer107": baza("slayer_107_en")}
if "walidacja" in OPC:
    kat = OPC["walidacja"]
    powody["walidacja_fabryki"] = (baza("walidacja") | np.isin(X["hx"], np.load(f"{kat}/idx_walidacja_hx.npy"))
                                   | np.isin(X["hu"], np.load(f"{kat}/idx_walidacja_hu.npy")))


def baza_minhash(kat, nazwa):
    """Indeks bazy_mat.py: MinHash LSH 32x4 z J >= 0,8 do dowolnego dokumentu bazy albo identyczny znormalizowany tekst.
    Zakresy kluczy liczone wektorowo dla całej puli; pętla tylko po dokumentach z kandydatem (pełna pula: miliony dokumentów)."""
    b_sig = np.load(f"{kat}/idx_{nazwa}_sig.npy", mmap_mode="r")
    b_kl, b_dok = np.load(f"{kat}/idx_{nazwa}_kl.npy"), np.load(f"{kat}/idx_{nazwa}_dok.npy")
    traf = np.isin(X["hx"], np.load(f"{kat}/idx_{nazwa}_hx.npy"))
    kl_d = r2.klucze_band(S[z_sig], 32, 4)
    a_, e_ = np.searchsorted(b_kl, kl_d, "left"), np.searchsorted(b_kl, kl_d, "right")
    for j in np.flatnonzero((e_ > a_).any(axis=1)):
        kand = set()
        for a, e in zip(a_[j], e_[j]):
            if e > a:
                kand.update(b_dok[a:min(e, a + 500)].tolist())
        i = z_sig[j]
        if float((np.asarray(b_sig[sorted(kand)]) == S[i]).mean(axis=1).max()) >= 0.8:
            traf[i] = True
    return traf


if "entech" in OPC:  # aneks 24.11: english-technical-1b (1.08)
    powody["dedup_english_technical"] = baza_minhash(OPC["entech"], "entech")
if "en8x3b" in OPC:  # aneks 25.11b: angielska część slayer-pl-8x3b (1.00-1.06)
    powody["dedup_slayer_8x3b_en"] = baza_minhash(OPC["en8x3b"], "en8x3b")
if "fwe109" in OPC:  # aneks 24.11: identyczny znormalizowany url z plikami FineWeb-Edu 1.09
    powody["dedup_fineweb_edu_109"] = np.isin(X["hu"], np.load(f"{OPC['fwe109']}/idx_fwe109_hu.npy"))
for kat_n in filter(None, OPC.get("wlasne", "").split(",")):  # część 2: dokumenty wyeksportowane z wcześniej zbudowanego źródła
    kat, nazwa = kat_n.split(":")
    powody[f"dedup_{nazwa}"] = baza_minhash(kat, nazwa) | np.isin(X["hu"], np.load(f"{kat}/idx_{nazwa}_hu.npy"))
if "se_strony" in OPC:  # stackexchange_mat: pytanie obecne jako strona w FineMath-4+/InfiWebMath-4+ (se_strony.py)
    powody["dedup_se_strony"] = np.isin(X["hu"], np.load(f"{OPC['se_strony']}/idx_se_strony_hu.npy"))
if "min_tresc" in P["kolejnosc_powodow"]:  # aneks 24.11b: < min_slow słów po norm_slowa; cranemath także szablon_forum
    MIN = P["aneks_2026_11_24b"]["min_tresc"]["min_slow"] if isinstance(P["aneks_2026_11_24b"]["min_tresc"], dict) else 50
    slow = np.array([len(r.norm_slowa(t or "")) for t in kolumna("text")])
    powody["min_tresc"] = slow < MIN
    if "szablon_forum" in P["kolejnosc_powodow"]:
        SF = P["aneks_2026_11_24b"]["szablon_forum"]
        znak = np.array([any(z in (t or "") for z in SF["znaczniki"]) for t in kolumna("text")])
        powody["szablon_forum"] = znak & (slow < SF["max_slow"])
A3 = P.get("aneks_2026_11_24c", {})
if "pii_zaciemniony" in P["kolejnosc_powodow"]:  # aneks 24.11c: e-mail zapisany jako nazwa(AT)domena
    rx_at = re.compile(P["aneks_2026_11_24c"]["pii_zaciemniony"]["regex"] if isinstance(A3.get("pii_zaciemniony"), dict) else
                       json.load(open(os.path.join(os.path.dirname(PREREG_P), "..", "..", "finemath4", "skrypty", "preregistracja.json"),
                                      encoding="utf-8"))["aneks_2026_11_24c"]["pii_zaciemniony"]["regex"])
    powody["pii_zaciemniony"] = np.array([bool(rx_at.search(t or "")) for t in kolumna("text")])
if "pii_at_bez_nawiasow" in P["kolejnosc_powodow"]:  # aneks 25.11c: e-mail zapisany jako nazwa at domena.tld (bez nawiasów)
    rx_ab = re.compile(P["aneks_2026_11_25c"]["pii_at_bez_nawiasow"]["regex"])
    powody["pii_at_bez_nawiasow"] = np.array([bool(rx_ab.search(t or "")) for t in kolumna("text")])
if "haslo_w_kodzie" in P["kolejnosc_powodow"]:  # aneks 24.11c: literał hasła w przypisaniu
    rx_h = re.compile(A3["haslo_w_kodzie"]["regex"])
    powody["haslo_w_kodzie"] = np.array([bool(rx_h.search(t or "")) for t in kolumna("text")])
if "suma40" in P["kolejnosc_powodow"]:  # aneks 24.11c, warunek na oryginał z aneksu 25.11: brak zadania o sumie do 40
    rx_t = re.compile(A3["suma40"]["regex_tekst"])
    a4 = P.get("aneks_2026_11_25", {}).get("suma40")
    rx_o = re.compile(a4["regex_oryginal_zadanie"] if a4 else A3["suma40"]["regex_oryginal"])
    jed_s = json.load(open(f"{OPC['oryg'].split(',')[0]}/jednostki.json"))
    powody["suma40"] = np.array([bool(rx_t.search(t or "")) and not rx_o.search(o or "")
                                 for t, o in zip(kolumna("text"), kolumna("text", jed_s))])

if "domena_testow" in P["kolejnosc_powodow"]:
    _wyl = [1 + w.DOMENY_TESTOW.index(d) for d in P.get("domena_testow_wylaczone", [])]  # dom = 1 + indeks domeny
    powody["domena_testow"] = (X["dom"] > 0) & ~np.isin(X["dom"], _wyl)
if P["pii"]["tryb"] == "usun":
    powody["pii"] = X["pii"] > 0
elif P["pii"]["tryb"] == "maskuj_email_usun_telefon_ip":  # e-maile maskowane przy eksporcie (mat_wybor.premask_emails)
    powody["pii"] = (X["pii"] & 6) > 0
dodatkowe = {}
if ZB == "cranemath":
    powody["think"] = np.array(["<think>" in t or "</think>" in t for t in kolumna("text")])
    do, dk = OPC["oryg"].split(",")
    jed_o = json.load(open(f"{do}/jednostki.json"))
    assert len(jed_o) == len(jed)
    powody["ewal_13gram_oryginal"], dodatkowe["ewal_oryginal_per_test"] = ewal(dk, N)

if ZB == "stackedu":
    lic, lic_t = list(kolumna("license")), list(kolumna("license_type"))
    powody["licencja"] = np.array([not (a or "").strip() or b != "permissive" for a, b in zip(lic, lic_t)])
    powody["int_score"] = np.array([(s if s is not None else -1) < P["int_score"]["min"] for s in kolumna("int_score")])
    rx = [re.compile(x) for x in P["sekrety"]["wzorce"]]
    rx_gen = re.compile(P["wygenerowany"]["wzorzec"])
    sek = np.zeros(N, bool)
    gen = np.zeros(N, bool)
    sek_klasy = collections.Counter()
    for i, t in enumerate(kolumna("text")):
        for n, x in zip(P["sekrety"]["nazwy"], rx):
            if x.search(t):
                sek[i] = True
                sek_klasy[n] += 1
        gen[i] = bool(rx_gen.search(t[:P["wygenerowany"]["znakow"]]))
    powody["sekrety"] = sek
    powody["wygenerowany"] = gen
    dodatkowe["sekrety_klasy"] = dict(sek_klasy)
    dodatkowe["licencje_top"] = dict(collections.Counter(lic).most_common(30))

kolej = P["kolejnosc_powodow"]
brak = [p for p in kolej if p not in powody]
assert not brak, f"powody bez detektora: {brak}"
T = int(tok.sum())
wyn = {"zbior": ZB, "dokumenty": N, "tokeny_v6": T, "dok_z_id0": int(X["id0"].sum()), "kaskada": [], "niezaleznie": {}}
zostaje = np.ones(N, bool)
pierwszy = np.array([""] * N, dtype=object)
for p in kolej:
    f = powody[p]
    nowe = f & zostaje
    pierwszy[nowe] = p
    zostaje &= ~f
    wyn["kaskada"].append({"powod": p, "odrzucone_dok": int(nowe.sum()), "odrzucone_tok": int(tok[nowe].sum()),
                           "zostaje_dok": int(zostaje.sum()), "zostaje_tok": int(tok[zostaje].sum()),
                           "zostaje_tok_proc": round(100 * tok[zostaje].sum() / T, 3)})
    wyn["niezaleznie"][p] = {"dok": int(f.sum()), "tok": int(tok[f].sum()), "tok_proc": round(100 * tok[f].sum() / T, 3)}
wyn["uzysk"] = {"dok": int(zostaje.sum()), "tok": int(tok[zostaje].sum()), "tok_proc": round(100 * tok[zostaje].sum() / T, 3)}
wyn["ewal_per_test"] = ew_per_test
wyn["pii_klasy_detektor_dclm"] = {kk: int(((X["pii"] & v) > 0).sum()) for kk, v in (("email", 1), ("telefon", 2), ("ip", 4))}
wyn["pii_tryb"] = P["pii"]["tryb"]
wyn["dedup_wewnatrz_szczegoly"] = {"identyczny_tekst": int(dup_dokl.sum()), "minhash_bez_identycznych": int((dup_mh & ~dup_dokl).sum())}
wyn.update(dodatkowe)

# ---- wybór do eksportu: zachowane w kolejności losowej aż suma tokenów v6 >= cel eksportu
g = np.random.default_rng(SEED)
zach = np.flatnonzero(zostaje)
kol = g.permutation(zach)
cum = np.cumsum(tok[kol])
CEL_EKSP = P["pula"].get("cel_eksportu_tok_v6") or 10**15  # brak celu = „wszystkie zachowane” (oeis, formalna)
ile = int(np.searchsorted(cum, CEL_EKSP) + 1)
wybrane = np.sort(kol[:ile])
wyn["eksport"] = {"cel_tok_v6": CEL_EKSP, "dok": int(len(wybrane)), "tok_v6": int(tok[wybrane].sum()),
                  "wystarcza": bool(cum[-1] >= CEL_EKSP) if len(cum) else False}
json.dump({"zbior": ZB, "dokumenty_globalne": wybrane.tolist(), "jednostki": jed, "poczatki": pocz.tolist()},
          open(WYBOR, "w", encoding="utf-8"))
np.savez(os.path.join(os.path.dirname(OUT), "powody.npz"), nazwy=np.array(kolej),
         m=np.stack([powody[p] for p in kolej], axis=1), zostaje=zostaje, para_wewnatrz=para_w, ntok=tok)
json.dump(wyn, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)

# ---- ręczna próbka: do 100 odrzuconych na powód (widok niezależny) + n zachowanych spośród wybranych do eksportu
RP = P["reczna_probka"]
g = np.random.default_rng(SEED + 1)
with open(PRZEGLAD, "w", encoding="utf-8") as f:
    for p in kolej:
        kand = np.flatnonzero(powody[p])
        for i in np.sort(g.choice(kand, min(RP["odrzucone_na_powod"], len(kand)), replace=False)):
            o = {"nr": int(i), "grupa": "odrzucony", "powod": p, "pierwszy_powod": pierwszy[i], "url": urls[i], "tokeny_v6": int(tok[i]),
                 "tekst": tekst(i)[:RP["znakow"]]}
            if p == "dedup_wewnatrz" and para_w[i] >= 0:
                o["para"] = {"nr": int(para_w[i]), "url": urls[para_w[i]], "tekst": tekst(int(para_w[i]))[:RP["znakow"]]}
            if p == "ewal_13gram":
                o["trafienia"] = TRAF.get((EW13, int(i)))
            if p == "ewal_13gram_oryginal":
                o["trafienia"] = TRAF.get((OPC["oryg"].split(",")[1], int(i)))
            if p in ("dedup_slayer107", "walidacja_fabryki"):
                nz = "slayer_107_en" if p == "dedup_slayer107" else "walidacja"
                o["wynik_indeksu"] = {"szkic13": float(X[f"bz_{nz}"][i, 0]), "minhash": float(X[f"bz_{nz}"][i, 1])}
            f.write(json.dumps(o, ensure_ascii=False) + "\n")
    for i in np.sort(g.choice(wybrane, min(RP["zachowane"], len(wybrane)), replace=False)):
        o = {"nr": int(i), "grupa": "zachowany", "powod": None, "url": urls[i], "tokeny_v6": int(tok[i]), "tekst": tekst(i)[:RP["znakow"]]}
        if ZB == "cranemath":  # przegląd poprawności przepisania: tekst przed przepisaniem z kopii 'oryg'
            j = int(np.searchsorted(pocz, i, "right") - 1)
            o["tekst_oryginalny"] = pq.ParquetFile(jed_o[j][0]).read_row_group(jed_o[j][1], columns=["text"]).column(0)[
                int(i - pocz[j])].as_py()[:RP["znakow"]]
        f.write(json.dumps(o, ensure_ascii=False) + "\n")
print(json.dumps({kk: wyn[kk] for kk in ("dokumenty", "tokeny_v6", "uzysk", "eksport")}, ensure_ascii=False))
for x in wyn["kaskada"]:
    print(x)
print("KONIEC", flush=True)
