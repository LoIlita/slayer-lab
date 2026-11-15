"""Druga ręczna próbka (aneks preregistracji 15.11.2026, pole reczna_probka_2): 100 dokumentów na KAŻDY powód w widoku
niezależnym (wszystkie, gdy powód ma < 100) + 100 zachowanych wspólnych, rng default_rng(20261115). Dla dedupów i walidacji
para dopasowania z miarami podobieństwa:
  dedup_wewnatrz    para z agreguj.py (para_wewnatrz w powody.npz): wcześniejszy dokument próbki
  walidacja_fabryki teksty indeksu walidacji odtworzone w kolejności indeksy.py (zgodność sprawdzana podpisami MinHash)
  dedup_slayer107   skan tokenów v6 w en_mix i en_fineweb_edu (train.bin): okna 12 tokenów z dokumentu, kandydaci, najlepszy
  dedup_ivme        to samo w 28 batchach train-dclm Ivme (tokenizer zbioru)
Miary pary: jaccard_minhash (128 funkcji, 5-gramy słów), szkic13 (udział próbek szkicu 13-gramów dokumentu obecnych w parze),
identyczny_tekst (po norm_tekst). Plik wynikowy ma PII odrzuconych: zostaje w robocze/.
Argumenty: katalog_przebiegu powody.npz katalog_pobran tokenizer_v6.json wyjscie.jsonl"""
import collections
import json
import os
import sys

os.environ["TOKENIZERS_PARALLELISM"] = "false"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np  # noqa: E402
import pyarrow.parquet as pq  # noqa: E402
from tokenizers import Tokenizer  # noqa: E402

import wspolne as w  # noqa: E402
from wspolne import r  # noqa: E402

D, POW, POB, TOK, OUT = sys.argv[1:6]
SEED, NA_POWOD, MAKS_ZNAKOW = 20261115, 100, 20000
A, B = r.perm_param(128)
L_OKNA, OKIEN, P = 12, 16, np.uint64(0x100000001B3)
CHUNK = 40_000_000
EW13 = os.path.join(os.path.dirname(POW), "ew13")
LISTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ewal_13gram_wykluczone.json")

jed = json.load(open(f"{D}/jednostki.json"))
meta = [json.load(open(f"{D}/u_{k:04d}.json", encoding="utf-8")) for k in range(len(jed))]
pocz = np.concatenate([[0], np.cumsum([len(m["ids"]) for m in meta])])
urls = [u for m in meta for u in m["urls"]]
Z = np.load(POW, allow_pickle=False)
nazwy, M, zostaje, para_w, ntok = list(Z["nazwy"]), Z["m"], Z["zostaje"], Z["para_wewnatrz"], Z["ntok"]
X = {k: np.concatenate([np.load(f"{D}/u_{j:04d}.npz")[k] for j in range(len(jed))]) for k in ("pii", "moj", "dom", "sig")}
_rg = {}


def tekst(i):
    j = int(np.searchsorted(pocz, i, "right") - 1)
    if j not in _rg:
        if len(_rg) > 64:
            _rg.clear()
        _rg[j] = pq.ParquetFile(jed[j][0]).read_row_group(jed[j][1], columns=["text"]).column(0).to_pylist()
    return _rg[j][int(i - pocz[j])]


def cechy(t):
    sl = r.norm_slowa(t or "")
    h = r.hasze_slow(sl)
    n13 = np.unique(r.ngramy(h, r.N_EVAL))
    return {"hx": w.h64(" ".join(sl)), "n13": n13, "szk": n13[n13 % np.uint64(r.PROBKA) == 0], "sig": r.podpis(np.unique(r.ngramy(h, 5)), A, B)}


def miary(ta, tb):
    a, b = cechy(ta), cechy(tb)
    j = None if a["sig"] is None or b["sig"] is None else float((a["sig"] == b["sig"]).mean())
    s = None if len(a["szk"]) == 0 else float(np.isin(a["szk"], b["n13"]).mean())
    return {"jaccard_minhash": j, "szkic13": s, "identyczny_tekst": a["hx"] == b["hx"]}


def lepsza(m):
    return (m["identyczny_tekst"], max(m["szkic13"] or 0, m["jaccard_minhash"] or 0))


# ---------------------------------------------------------------- wybór próbki
g = np.random.default_rng(SEED)
wybor = []
for k, p in enumerate(nazwy):
    kand = np.flatnonzero(M[:, k])
    n = min(NA_POWOD, len(kand))
    for i in np.sort(g.choice(kand, n, replace=False)):
        wybor.append(("odrzucony", p, int(i), len(kand)))
kz = np.flatnonzero(zostaje)
for i in np.sort(g.choice(kz, NA_POWOD, replace=False)):
    wybor.append(("zachowany", None, int(i), len(kz)))
print("wybrano", len(wybor), collections.Counter(x[1] for x in wybor), flush=True)

# ---------------------------------------------------------------- dowody detektorów (to, co widział filtr)
ew_info = {}
if os.path.exists(f"{EW13}/ew13_traf.npz"):
    e = np.load(f"{EW13}/ew13_traf.npz")
    ng = {int(x["hasz"]): x for x in json.load(open(f"{EW13}/ew13_ngramy.json", encoding="utf-8"))["ngramy"]}
    wykl = {int(h) for h in json.load(open(LISTA, encoding="utf-8"))["hasze"]}
    for d, a, b in zip(e["doc"], e["poczatek"][:-1], e["poczatek"][1:]):
        hs = [int(h) for h in e["hasze"][a:b] if int(h) not in wykl]
        ew_info[int(d)] = [{"tekst": ng[h]["tekst"], "df": ng[h]["df"], "testy": ng[h]["testy"]} for h in hs]


def kontekst_pii(t):
    out = []
    for rx, kl in ((w.RX_EMAIL, "email"), (w.RX_TEL, "telefon"), (w.RX_IP, "ip")):
        for m in rx.finditer(t):
            if kl in w.pii(m.group(0) if kl != "email" else m.group(0)):
                a, b = m.span()
                out.append({"klasa": kl, "kontekst": t[max(0, a - 120):a] + "[" + kl.upper() + "]" + t[b:b + 120]})
                if len([o for o in out if o["klasa"] == kl]) >= 3:
                    break
    return out


# ---------------------------------------------------------------- pary: walidacja
def teksty_walidacji():
    cache = f"{POB}/idx_wal_teksty.parquet"
    if not os.path.exists(cache):
        import pyarrow as pa
        from huggingface_hub import HfFileSystem
        teksty, zr = [], []
        for nz, p in (("minimal-en-corpus-5b validation", f"{POB}/mincorp/minimal-en-corpus-5b/validation/shard-00000.parquet"),
                      ("minimal-en-corpus-2b-v2 validation", f"{POB}/mincorp/minimal-en-corpus-2b-v2/validation/shard-00000.parquet")):
            for x in pq.read_table(p, columns=["text"]).column(0).to_pylist():
                teksty.append(x)
                zr.append(nz)
        fs = HfFileSystem()
        with fs.open("datasets/HuggingFaceFW/fineweb-edu@87f09149ef4734204d70ed1d046ddc9ca3f2b8f9/sample/100BT/000_00009.parquet", "rb") as h:
            pf = pq.ParquetFile(h)
            wz, gg = [], 0
            while len(wz) < 5000:
                wz += pf.read_row_group(gg, columns=["text"]).column(0).to_pylist()
                gg += 1
        teksty += wz[:5000]
        zr += ["os FineWeb-Edu Slayer150"] * 5000
        tok = Tokenizer.from_file(f"{POB}/idx/gptneox/tokenizer.json")
        with fs.open("datasets/allenai/DataDecide-data-recipes@3baf34ba/preprocessed/dclm/v0_fw_top3p/gpt-neox-olmo-dolma-v1_5/part-00-00000.npy", "rb") as h:
            s = h.read(64 << 20)
        ids = np.frombuffer(s[: len(s) // 2 * 2], dtype="<u2").astype(np.int64)
        gr = np.flatnonzero(ids == 50279)
        dok = [ids[a + 1:b].tolist() for a, b in zip(np.concatenate([[-1], gr[:-1]]), gr)][:5000]
        dok = [d for d in dok if d]
        teksty += tok.decode_batch(dok, skip_special_tokens=True)
        zr += ["os DCLM Slayer150 (DataDecide)"] * len(dok)
        pq.write_table(pa.table({"text": teksty, "zrodlo": zr}), cache)
    t = pq.read_table(cache)
    return t.column("text").to_pylist(), t.column("zrodlo").to_pylist()


def pary_walidacji(cele):
    tw, zw = teksty_walidacji()
    S = np.load(f"{D}/../idx_wal/idx_walidacja_sig.npy")
    assert len(tw) == S.shape[0], (len(tw), S.shape)
    for i in (0, 5000, len(tw) - 1):  # kolejność = kolejność indeksu: podpis MinHash odtworzony z tekstu
        c = cechy(tw[i])
        assert c["sig"] is None or (c["sig"] == S[i]).all(), i
    hx = np.array([w.h64(r.norm_tekst(x or "")) for x in tw], np.uint64)
    cc = {i: cechy(tekst(i)) for i in cele}
    wsz = np.unique(np.concatenate([c["szk"] for c in cc.values()] + [np.zeros(0, np.uint64)]))
    traf_szk = {}  # wiersz indeksu -> próbki szkicu celów obecne w jego 13-gramach
    for j, x in enumerate(tw):
        n13 = np.unique(r.ngramy(r.hasze_slow(r.norm_slowa(x or "")), r.N_EVAL))
        q = wsz[np.isin(wsz, n13)]
        if len(q):
            traf_szk[j] = q
    wyn = {}
    for i in cele:
        t = tekst(i)
        c = cc[i]
        kand = set(np.flatnonzero(hx == c["hx"]).tolist())
        if c["sig"] is not None:
            kand.update(np.argsort(-(S == c["sig"]).mean(axis=1))[:5].tolist())
        if len(c["szk"]):
            sc = sorted(((int(np.isin(c["szk"], q).sum()), j) for j, q in traf_szk.items()), reverse=True)[:3]
            kand.update(j for s, j in sc if s > 0)
        best = max(((lepsza(miary(t, tw[j])), j) for j in kand), default=None)
        if best:
            j = best[1]
            wyn[i] = {"zrodlo_pary": zw[j] + f" (wiersz indeksu {j})", "tekst_pary": tw[j][:MAKS_ZNAKOW], **miary(t, tw[j])}
    return wyn


# ---------------------------------------------------------------- pary: skan tokenów (1.07, Ivme)
def okna(ids):
    if len(ids) < L_OKNA:
        return []
    poz = np.unique(np.linspace(0, len(ids) - L_OKNA, OKIEN).astype(int))
    pw = P ** np.arange(L_OKNA, dtype=np.uint64)
    a = np.asarray(ids, np.uint64)
    return [int((a[p:p + L_OKNA] * pw).sum()) for p in poz]


def skan(bin_sciezki, cel_hasze):
    """bin_sciezki: lista (nazwa, train.bin, ends) -> {hasz: [(nazwa, nr_dok)]}"""
    tg = np.array(sorted(cel_hasze), np.uint64)
    pw = P ** np.arange(L_OKNA, dtype=np.uint64)
    traf = collections.defaultdict(list)
    for nz, b, ends in bin_sciezki:
        x = np.memmap(b, dtype=np.uint16, mode="r")
        for s0 in range(0, len(x), CHUNK):
            c = np.asarray(x[s0:s0 + CHUNK + L_OKNA - 1], np.uint64)
            m = len(c) - L_OKNA + 1
            if m <= 0:
                continue
            h = np.zeros(m, np.uint64)
            for j in range(L_OKNA):
                h += c[j:j + m] * pw[j]
            for p in np.flatnonzero(tg[np.minimum(np.searchsorted(tg, h), len(tg) - 1)] == h):
                if len(traf[int(h[p])]) < 1000:  # okno szablonowe z tysiącami trafień nie wskazuje pary
                    traf[int(h[p])].append((nz, int(np.searchsorted(ends, s0 + p, "right"))))
        print("skan", nz, b, flush=True)
    return traf


def pary_skan(cele, bazy, tok_bazy):
    tk = Tokenizer.from_file(tok_bazy)
    cel_okna = {i: okna(tk.encode(tekst(i), add_special_tokens=False).ids) for i in cele}
    traf = skan([(nz, b, e) for nz, (b, e) in bazy.items()], {h for v in cel_okna.values() for h in v})
    wyn = {}
    for i, ok in cel_okna.items():
        licz = collections.Counter(d for h in ok for d in traf.get(h, []))
        t = tekst(i)
        naj = None
        for (nz, d), _ in licz.most_common(20):
            b, e = bazy[nz]
            a0 = 0 if d == 0 else int(e[d - 1])
            tb = tk.decode(np.asarray(np.memmap(b, dtype=np.uint16, mode="r")[a0:int(e[d])]).tolist(), skip_special_tokens=True)
            m = miary(t, tb)
            if naj is None or lepsza(m) > lepsza(naj[0]):
                naj = (m, nz, d, tb)
        if naj:
            wyn[i] = {"zrodlo_pary": f"{naj[1]} dokument {naj[2]}", "tekst_pary": naj[3][:MAKS_ZNAKOW], **naj[0],
                      "okien_trafionych": sum(1 for h in ok if h in traf), "okien": len(ok)}
        else:
            wyn[i] = {"zrodlo_pary": None, "okien_trafionych": 0, "okien": len(ok)}
    return wyn


cele = collections.defaultdict(list)
for gr, p, i, _ in wybor:
    cele[p].append(i)
pary = {}
for i in cele.get("dedup_wewnatrz", []):
    j = int(para_w[i])
    pary[("dedup_wewnatrz", i)] = {"zrodlo_pary": f"próbka DCLM dokument {j} ({urls[j]})" if j >= 0 else None,
                                    **({"tekst_pary": tekst(j)[:MAKS_ZNAKOW], **miary(tekst(i), tekst(j))} if j >= 0 else {})}
for i, v in pary_walidacji(cele.get("walidacja_fabryki", [])).items():
    pary[("walidacja_fabryki", i)] = v
print("pary walidacji", sum(1 for k in pary if k[0] == "walidacja_fabryki"), flush=True)
b107 = {nz: (f"{POB}/slayer107/{nz}/train.bin", np.fromfile(f"{POB}/slayer107/{nz}/docs.idx", dtype=np.uint64)) for nz in ("en_mix", "en_fineweb_edu")}
for i, v in pary_skan(cele.get("dedup_slayer107", []), b107, TOK).items():
    pary[("dedup_slayer107", i)] = v
IV = f"{POB}/idx/ivme"
biv = {f"train-dclm-{k:06d}": (f"{IV}/train-batches/train-dclm-{k:06d}/shard-00000.bin",
                               np.load(f"{IV}/train-batches/train-dclm-{k:06d}/shard-00000.bin.ends.npy").astype(np.uint64)) for k in range(28)}
for i, v in pary_skan(cele.get("dedup_ivme", []), biv, f"{IV}/metadata/tokenizer.json").items():
    pary[("dedup_ivme", i)] = v

# ---------------------------------------------------------------- zapis
with open(OUT, "w", encoding="utf-8") as f:
    for gr, p, i, n_pop in wybor:
        t = tekst(i)
        rec = {"nr": i, "grupa": gr, "powod_probki": p, "populacja_powodu": n_pop,
               "wszystkie_powody": [nazwy[k] for k in np.flatnonzero(M[i])], "url": urls[i], "host": w.host(urls[i]),
               "tokeny_v6": int(ntok[i]), "znakow": len(t), "tekst": t[:MAKS_ZNAKOW]}
        if p == "pii":
            rec["dowod_filtra"] = {"klasy_bitmaska": int(X["pii"][i]), "trafienia": kontekst_pii(t)}
        elif p == "ewal_13gram":
            rec["dowod_filtra"] = {"trafiajace_13gramy_poza_lista": ew_info.get(i, [])[:20]}
        elif p == "mojibake":
            rec["dowod_filtra"] = {"dopasowan_regexu": int(X["moj"][i])}
        elif p == "domena_testow":
            rec["dowod_filtra"] = {"domena_reguly": w.domena_testu(urls[i])}
        elif p in ("dedup_wewnatrz", "walidacja_fabryki", "dedup_slayer107", "dedup_ivme"):
            rec["para"] = pary.get((p, i), {"zrodlo_pary": None})
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
st = collections.Counter((p, (pary.get((p, i)) or {}).get("zrodlo_pary") is not None) for gr, p, i, _ in wybor if (p, i) in pary)
print("pary znalezione", dict(st), flush=True)
print("KONIEC", flush=True)
