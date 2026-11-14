"""13-gramy testów, które trafiają w dokumenty próbki: które to n-gramy, w ilu dokumentach, z jakich testów.
Pomiar do aneksu preregistracji z 15.11.2026 (ewal_13gram, wykluczenie n-gramów powszechnych w sieci).
Liczy tylko dokumenty z ew=True z przebiegu: odtwarza ich 13-gramy (rdzen.norm_slowa, hasze_slow, ngramy) i bierze część
wspólną z indeksem testów (wszystkie_13.npy). Tekst dokumentu z lokalnej kopii próbki (jednostki.json przebiegu).
Wyjście:
  ew13_traf.npz   doc (globalny numer dokumentu), poczatek (offsety), hasze (trafiające 13-gramy każdego dokumentu)
  ew13_ngramy.json  per n-gram: hasz, df (dokumenty próbki), tekst (13 słów po normalizacji), same_liczby, testy
Z listą wykluczeń (opcjonalny 4. argument, plik JSON z polem 'hasze'): także ew13_po_wykl.npy, bool na każdy dokument
przebiegu: True = dokument ma co najmniej jeden trafiający 13-gram spoza listy.
Argumenty: katalog_przebiegu katalog_ewal wyjscie [lista_wykluczen.json]"""
import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np  # noqa: E402
import pyarrow.parquet as pq  # noqa: E402

from wspolne import r  # noqa: E402

D, EW, OUT = sys.argv[1:4]
LISTA = sys.argv[4] if len(sys.argv) > 4 else None
os.makedirs(OUT, exist_ok=True)
UE13 = np.load(f"{EW}/wszystkie_13.npy", mmap_mode="r")
TESTY_13 = {p[:-8]: np.load(f"{EW}/{p}", mmap_mode="r") for p in sorted(os.listdir(EW)) if p.endswith("__13.npy") and not p.startswith("wszystkie")}

jed = json.load(open(f"{D}/jednostki.json"))
docs, poczatki, hasze = [], [0], []
df = collections.Counter()
tekst = {}
pocz = 0
for k, (sciezka, g) in enumerate(jed):
    z = np.load(f"{D}/u_{k:04d}.npz")
    ew = z["ew"]
    if ew.any():
        tx = pq.ParquetFile(sciezka).read_row_group(g, columns=["text"]).column(0).to_pylist()
        for i in np.flatnonzero(ew):
            sl = r.norm_slowa(tx[i])
            h = r.hasze_slow(sl)
            g13 = r.ngramy(h, r.N_EVAL)
            u, pierwsze = np.unique(g13, return_index=True)
            j = np.minimum(np.searchsorted(UE13, u), len(UE13) - 1)
            traf = UE13[j] == u
            th = u[traf]
            for x, p in zip(th.tolist(), pierwsze[traf].tolist()):
                df[x] += 1
                if x not in tekst:
                    tekst[x] = " ".join(sl[p:p + r.N_EVAL])
            docs.append(pocz + int(i))
            hasze.append(th)
            poczatki.append(poczatki[-1] + len(th))
    pocz += len(z["ew"])
N = pocz
H = np.concatenate(hasze) if hasze else np.zeros(0, np.uint64)
np.savez(f"{OUT}/ew13_traf.npz", doc=np.array(docs, np.int64), poczatek=np.array(poczatki, np.int64), hasze=H)

ng = []
for x, c in df.most_common():
    a = np.array([x], np.uint64)
    t = tekst[x]
    ng.append({"hasz": str(x), "df": c, "tekst": t, "same_liczby": all(s.isdigit() for s in t.split()),
               "testy": [n for n, ind in TESTY_13.items() if r.ma_trafienie(a, ind)]})
json.dump({"dokumentow_przebiegu": N, "dokumentow_z_trafieniem": len(docs), "ngramow": len(ng), "ngramy": ng},
          open(f"{OUT}/ew13_ngramy.json", "w", encoding="utf-8"), indent=0, ensure_ascii=False)
print("dokumentow", N, "z_trafieniem", len(docs), "ngramow", len(ng), flush=True)

if LISTA and not os.path.exists(LISTA):
    # reguła aneksu 15.11.2026: wykluczony n-gram powszechny (df >= DF_MIN w tej próbce) albo trywialny (każde słowo to liczba
    # albo pojedynczy znak: ciągi liczb, alfabet; interpunkcję usuwa już norm_slowa). Listę budujesz RAZ z próbki głównej.
    DF_MIN = 5
    wyb = [x for x in ng if x["df"] >= DF_MIN or all(s.isdigit() or len(s) == 1 for s in x["tekst"].split())]
    json.dump({"regula": f"df >= {DF_MIN} dokumentów próbki ({N} dok.) albo każde słowo 13-gramu to liczba lub pojedynczy znak",
               "zbudowano_z": D, "ngramow": len(wyb), "hasze": [x["hasz"] for x in wyb],
               "ngramy": [{"hasz": x["hasz"], "df": x["df"], "tekst": x["tekst"], "testy": x["testy"]} for x in wyb]},
              open(LISTA, "w", encoding="utf-8"), indent=0, ensure_ascii=False)
    print("lista_wykluczen zbudowana", len(wyb), flush=True)
if LISTA:
    wykl = np.array(sorted(int(h) for h in json.load(open(LISTA, encoding="utf-8"))["hasze"]), np.uint64)
    po = np.zeros(N, bool)
    for d, a, b in zip(docs, poczatki[:-1], poczatki[1:]):
        x = H[a:b]
        po[d] = bool(len(x)) and not bool(np.isin(x, wykl).all())
    np.save(f"{OUT}/ew13_po_wykl.npy", po)
    print("po_wykluczeniu", int(po.sum()), "z", len(docs), flush=True)
print("KONIEC", flush=True)
