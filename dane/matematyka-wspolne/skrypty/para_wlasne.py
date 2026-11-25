"""Para do przeglądu odrzuconych przez dedup_<baza> (indeks bazy_mat.py wlasne): dla każdej pozycji próbki z tym powodem
dokument bazy, który zadecydował — identyczny url, identyczny tekst albo najbliższy kandydat MinHash (J >= 0,8) — z jego
tekstem; agreguj_mat.py zapisuje parę tylko dla dedup_wewnatrz.
Argumenty: probka_przegladu.jsonl katalog_przebiegu_zrodla nazwa_bazy katalog_bazy wybor_bazy.json katalog_przebiegu_bazy wyjscie.jsonl
Wyjście: pozycje próbki z powodem dedup_<nazwa> z polem `para` {sposob, jaccard, url, tekst[:3000]}."""
import json
import os
import sys

import numpy as np
import pyarrow.parquet as pq

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "dclm-en", "skrypty"))
from wspolne import r2  # noqa: E402

PROBKA, PRZ, NAZWA, KAT, WYB_B, PRZ_B, OUT = sys.argv[1:8]


def wektory(prz):
    jed = json.load(open(f"{prz}/jednostki.json"))
    z = [np.load(f"{prz}/u_{k:04d}.npz") for k in range(len(jed))]
    return np.vstack([x["sig"] for x in z]), np.concatenate([x["hx"] for x in z]), np.concatenate([x["hu"] for x in z])


S, HX, HU = wektory(PRZ)
b_sig = np.load(f"{KAT}/idx_{NAZWA}_sig.npy", mmap_mode="r")
b_kl, b_dok = np.load(f"{KAT}/idx_{NAZWA}_kl.npy"), np.load(f"{KAT}/idx_{NAZWA}_dok.npy")
wb = json.load(open(WYB_B))
g_b = np.asarray(wb["dokumenty_globalne"], np.int64)
_, HX_B, HU_B = wektory(PRZ_B)
hx_b, hu_b = HX_B[g_b], HU_B[g_b]


def tekst_bazy(j):
    g = int(g_b[j])
    u = int(np.searchsorted(wb["poczatki"], g, "right") - 1)
    p, rg = wb["jednostki"][u]
    t = pq.ParquetFile(p).read_row_group(rg, columns=["text", "url"])
    i = g - wb["poczatki"][u]
    return t.column("url")[i].as_py(), (t.column("text")[i].as_py() or "")[:3000]


n = 0
with open(OUT, "w", encoding="utf-8") as f:
    for linia in open(PROBKA, encoding="utf-8"):
        o = json.loads(linia)
        if o.get("powod") != f"dedup_{NAZWA}":
            continue
        i = o["nr"]
        kand = set()
        for k in r2.klucze_band(S[i:i + 1], 32, 4)[0]:
            a, e = np.searchsorted(b_kl, k, "left"), np.searchsorted(b_kl, k, "right")
            kand.update(b_dok[a:min(e, a + 500)].tolist())
        para = None
        if kand:
            kk = np.array(sorted(kand))
            jac = (np.asarray(b_sig[kk]) == S[i]).mean(axis=1)
            if jac.max() >= 0.8:
                para = {"sposob": "minhash", "jaccard": round(float(jac.max()), 3), "j": int(kk[int(np.argmax(jac))])}
        if para is None and (m := np.flatnonzero(hx_b == HX[i])).size:
            para = {"sposob": "identyczny_tekst", "jaccard": 1.0, "j": int(m[0])}
        if para is None and (m := np.flatnonzero(hu_b == HU[i])).size:
            para = {"sposob": "identyczny_url", "jaccard": None, "j": int(m[0])}
        if para is not None:
            para["url"], para["tekst"] = tekst_bazy(para.pop("j"))
        o["para"] = para
        f.write(json.dumps(o, ensure_ascii=False) + "\n")
        n += 1
print("pozycji", n)
