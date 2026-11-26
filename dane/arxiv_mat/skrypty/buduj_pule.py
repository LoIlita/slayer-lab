"""Pula arXiv (A1 pełne teksty na licencji otwartej + A2 abstrakty prac spoza A1) wg preregistracja.json.

Użycie (venv z dane/matematyka-wspolne/robocze/venv):
  buduj_pule.py buduj    -> robocze/pula/arxiv_{papers,abstracts}.parquet, robocze/odrzucone.parquet,
                            wyniki/budowa.json, wyniki/probka_pliki.json
  buduj_pule.py probka   -> robocze/probka_filtra_budowy.jsonl (40 odrzuconych na powód filtra budowy)
  buduj_pule.py sprawdz  -> kontrola kontraktu potoku (kod 0 = OK)
Zero modeli: łączenie ze snapshotem metadanych, reguła licencji, maskowanie e-maili wyrażeniami regularnymi."""
import ast, gzip, hashlib, json, os, re, sys
from collections import Counter, defaultdict

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
from huggingface_hub import hf_hub_download, HfApi
from tokenizers import Tokenizer

KAT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # dane/arxiv_mat
ROOT = os.path.dirname(os.path.dirname(KAT))
sys.path.insert(0, os.path.join(ROOT, "dane/dclm-en/skrypty"))
import wspolne  # noqa: E402

P = json.load(open(os.path.join(KAT, "skrypty/preregistracja.json"), encoding="utf-8"))
P_INFI = json.load(open(os.path.join(ROOT, "dane/infiwebmath4/skrypty/preregistracja.json"), encoding="utf-8"))
SHA_ZR = json.load(open(os.path.join(KAT, "wyniki/przeglad_zrodla.json"), encoding="utf-8"))
ZR = P["zrodlo"]
ROB = os.path.join(KAT, "robocze")
DL = os.path.join(ROB, "pobrania")
POOL = {"A1": os.path.join(ROB, "pula/arxiv_papers.parquet"), "A2": os.path.join(ROB, "pula/arxiv_abstracts.parquet")}
ODRZ = os.path.join(ROB, "odrzucone.parquet")
META = os.path.join(ROB, "meta.parquet")
TOK = os.path.join(ROOT, "dane/dclm-en/robocze/pobrania/tokenizer_v6/tokenizer.json")
TOK_SHA = "0640d3bd3674d7a6e59c540d945a2ad275a12e1bcaeb6007c37a90751f9815dd"
TARGET = re.compile(P["wybor"]["regex"])
KOL = ("text", "url", "id", "license", "created", "author", "kategoria", "czesc")
DOZWOLONE = {"CC0-1.0", "CC-PDDC", "CC-BY-3.0", "CC-BY-4.0", "CC-BY-SA-4.0"}

# ---- e-maile (jak dane/oeis/skrypty/buduj_pule.py)
RX_EMAIL = wspolne.RX_EMAIL
RX_AT = re.compile(P_INFI["aneks_2026_11_24c"]["pii_zaciemniony"]["regex"])
RX_AB = re.compile(P_INFI["aneks_2026_11_25c"]["pii_at_bez_nawiasow"]["regex"])
WZORCE = (("email", RX_EMAIL), ("zaciemniony", RX_AT), ("at_bez_nawiasow", RX_AB))
OBLEC = [(re.compile(r"\(\s*(?:" + r.pattern + r")\s*\)"), re.compile(r"\[\s*(?:" + r.pattern + r")\s*\]"), r) for _, r in WZORCE]
RX_PUSTY_NAWIAS = re.compile(r"\(\s*\)|\[\s*\]")
RX_SPACJE = re.compile(r"(?<=\S)[ \t]{2,}")
RX_SPACJA_PRZED = re.compile(r"[ \t]+(?=[,.;:)\]])")
RX_PODWOJNY_PRZECINEK = re.compile(r",(?:[ \t]*,)+")


def maskuj(linia, licz=None):
    zm = False
    for (ok, kw, r), (nazwa, _) in zip(OBLEC, WZORCE):
        n0 = len(r.findall(linia))
        if not n0:
            continue
        if licz is not None:
            licz[nazwa] += n0
        linia = r.sub("", kw.sub("", ok.sub("", linia)))
        zm = True
    if zm:
        linia = RX_PUSTY_NAWIAS.sub("", linia)
        linia = RX_SPACJA_PRZED.sub("", RX_SPACJE.sub(" ", linia))
        linia = RX_PODWOJNY_PRZECINEK.sub(",", linia).rstrip()
    return linia


def maskuj_tekst(t, licz):
    if not any(r.search(t) for _, r in WZORCE):
        return t
    t = "\n".join(maskuj(ln, licz) if any(r.search(ln) for _, r in WZORCE) else ln for ln in t.split("\n"))
    if any(r.search(t) for _, r in WZORCE):  # dopasowania przez złamanie wiersza (np. 'niranj\n(at) math.iitb.ac.in')
        t = maskuj(t, licz)
    return t


# ---- licencje
RANGA = {"CC0-1.0": 0, "CC-PDDC": 0, "CC-BY-3.0": 1, "CC-BY-4.0": 1, "CC-BY-SA-4.0": 2}


def spdx(s):
    """Napis licencji (Common Pile albo snapshot) -> SPDX z DOZWOLONE albo None (NC/ND/domyślna/brak/nieznany)."""
    s = (s or "").strip()
    if not s or re.search(r"nonexclusive|-nc|-nd|/nc|/nd", s, re.I):
        return None
    if re.search(r"publicdomain/zero/1\.0", s):
        return "CC0-1.0"
    if re.search(r"licenses/publicdomain|^Public Domain", s):
        return "CC-PDDC"
    for rx, k in ((r"licenses/by-sa/4\.0", "CC-BY-SA-4.0"), (r"licenses/by/4\.0", "CC-BY-4.0"), (r"licenses/by/3\.0", "CC-BY-3.0")):
        if re.search(rx, s):
            return k
    return None


def licencja_a1(cp, meta):
    a, b = spdx(cp), spdx(meta)
    if a is None or b is None:
        return None
    return a if RANGA[a] > RANGA[b] else b  # remis -> snapshot


def testy():
    przyp = {
        "Jan Kowalski (jan.kowalski@uni.pl), Uniwersytet": "Jan Kowalski, Uniwersytet",
        "Email: jk(AT)math.uni.pl": "Email:",
        "contact joe at example.edu, thanks": "contact, thanks",
        "Let $x\\in X$ be a point.": "Let $x\\in X$ be a point.",
    }
    for we, ocz in przyp.items():
        wy = maskuj(we)
        assert wy == ocz, (we, wy)
        assert not any(r.search(wy) for _, r in WZORCE), wy
    wy = maskuj_tekst("IIT Bombay. email: niranj\n(at) math.iitb.ac.in, Supported", Counter())
    assert not any(r.search(wy) for _, r in WZORCE) and wy.endswith("Supported"), wy
    by4 = "Creative Commons - Attribution - https://creativecommons.org/licenses/by/4.0/"
    assert licencja_a1(by4, "http://creativecommons.org/licenses/by/4.0/") == "CC-BY-4.0"
    assert licencja_a1(by4, "http://creativecommons.org/licenses/by-sa/4.0/") == "CC-BY-SA-4.0"
    assert licencja_a1(by4, "http://creativecommons.org/licenses/by-nc-nd/4.0/") is None
    assert licencja_a1(by4, "http://arxiv.org/licenses/nonexclusive-distrib/1.0/") is None
    assert licencja_a1(by4, None) is None
    assert licencja_a1("Public Domain", "http://creativecommons.org/publicdomain/zero/1.0/") == "CC0-1.0"
    assert licencja_a1(by4, "http://creativecommons.org/licenses/by/3.0/") == "CC-BY-3.0"


# ---- narzędzia
def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def tokeny(tk, teksty):
    out = []
    for i in range(0, len(teksty), 5000):
        out += [len(e.ids) + 1 for e in tk.encode_batch(teksty[i:i + 5000], add_special_tokens=False)]
    return out


def meta():
    if not os.path.exists(META):
        m = ZR["metadane"]
        fs = [f for f in HfApi().list_repo_files(m["repo"], repo_type="dataset", revision=m["rewizja"]) if f.endswith(".parquet")]
        tabs = []
        for f in sorted(fs):
            p = hf_hub_download(m["repo"], f, repo_type="dataset", revision=m["rewizja"], local_dir=DL)
            tabs.append(pq.read_table(p, columns=["id", "categories", "license", "title"]))
            os.remove(p)
        pq.write_table(pa.concat_tables(tabs), META)
    t = pq.read_table(META).to_pydict()
    return {i: (c, l, ti) for i, c, l, ti in zip(t["id"], t["categories"], t["license"], t["title"])}


def dokumenty(czesc):
    z = ZR[czesc]
    klucz = "arxiv-papers" if czesc == "A1" else "arxiv-abstracts"
    shas = SHA_ZR[czesc]["sha256"]
    fs = sorted(f for f in HfApi().list_repo_files(z["repo"], repo_type="dataset", revision=z["rewizja"]) if f.endswith(".jsonl.gz"))
    assert all(klucz in f for f in fs) and set(fs) == set(shas), "lista plików"
    for f in fs:
        p = hf_hub_download(z["repo"], f, repo_type="dataset", revision=z["rewizja"], local_dir=DL)
        assert sha256(p) == shas[f], f"sha256 {f}"
        with gzip.open(p, "rt", encoding="utf-8") as fh:
            for ln in fh:
                d = json.loads(ln)
                m = d.get("metadata") or {}
                if isinstance(m, str):
                    m = ast.literal_eval(m)
                d["metadata"] = m
                yield d
        os.remove(p)
        print(czesc, f, flush=True)


class Pisarz:
    def __init__(self, path, tk, extra=()):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.kol = KOL + tuple(extra)
        self.sch = pa.schema([(k, pa.string()) for k in self.kol] + [("tokeny_v6", pa.int64())] * bool(extra))
        self.w = pq.ParquetWriter(path, pa.schema([(k, pa.string()) for k in self.kol])) if not extra else pq.ParquetWriter(path, self.sch)
        self.buf, self.tk, self.extra = [], tk, bool(extra)
        self.n = self.tok = 0
        self.tok_list = []
        self.na_powod = defaultdict(lambda: {"dokumenty": 0, "tokeny_v6": 0})

    def dodaj(self, r):
        self.buf.append(r)
        if len(self.buf) == 5000:
            self.zrzut()

    def zrzut(self):
        if not self.buf:
            return
        t = tokeny(self.tk, [r["text"] for r in self.buf])
        kol = {k: [r[k] for r in self.buf] for k in self.kol}
        if self.extra:
            kol["tokeny_v6"] = t
            for r, x in zip(self.buf, t):
                self.na_powod[r["powod"]]["dokumenty"] += 1
                self.na_powod[r["powod"]]["tokeny_v6"] += x
        self.w.write_table(pa.table(kol, schema=self.w.schema), row_group_size=5000)
        self.n += len(self.buf)
        self.tok += sum(t)
        self.tok_list += t
        self.buf = []

    def zamknij(self):
        self.zrzut()
        self.w.close()


def buduj():
    testy()
    assert sha256(TOK) == TOK_SHA, "zły tokenizer"
    tk = Tokenizer.from_file(TOK)
    M = meta()
    print("meta", len(M), flush=True)
    pis = {c: Pisarz(POOL[c], tk) for c in ("A1", "A2")}
    odrz = Pisarz(ODRZ, tk, extra=("powod",))
    przed = Counter()
    lic_par = Counter()
    lic_w = {"A1": Counter(), "A2": Counter()}
    art = Counter()
    RX_ART = {"stopka_111": re.compile(r"[a-z]1{3,}[A-Z ]"), "tylda_pusta": re.compile(r"~\{\}"),
              "brak_ref": re.compile(r"\[\?\]|\?\?")}
    licz = Counter()
    a1_ids, a2_ids = set(), set()
    for czesc in ("A1", "A2"):
        for d in dokumenty(czesc):
            i = d["id"]
            mm = M.get(i)
            licz[czesc + "_wszystkie"] += 1
            if mm is None:
                licz[czesc + "_bez_meta"] += 1
                continue
            kat = (mm[0] or "").split()[0] if mm[0] else ""
            if not TARGET.match(kat):
                continue
            licz[czesc + "_docelowe"] += 1
            m = d["metadata"]
            if czesc == "A1":
                lic = licencja_a1(m.get("license"), mm[1])
                lic_par[f"{spdx(m.get('license'))} | {mm[1]}"] += 1
                tekst = d["text"] or ""
                pref = "arXiv:"
            else:
                if i in a1_ids:
                    continue
                if i in a2_ids:  # źródło A2 ma powtórzone id (3 id, 8 wierszy) -> pierwsze wystąpienie
                    licz["A2_duplikat_id"] += 1
                    continue
                a2_ids.add(i)
                lic = "CC0-1.0" if "publicdomain/zero" in (m.get("license") or "") else None
                tytul = " ".join((mm[2] or "").split())
                abs_ = (d["text"] or "").strip()
                tekst = (tytul + "\n\n" + abs_) if abs_ else ""
                pref = "arXiv-abs:"
            powod = "licencja" if lic is None else ("pusty" if not tekst.strip() else None)
            tekst = maskuj_tekst(tekst, przed)
            if czesc == "A1" and not powod:
                for k, rx in RX_ART.items():
                    if rx.search(tekst):
                        art[k] += 1
            r = {"text": tekst, "url": f"https://arxiv.org/abs/{i}", "id": pref + i, "license": lic or "",
                 "created": str(d.get("created") or ""), "author": (m.get("authors") or "").strip() or "unknown",
                 "kategoria": kat, "czesc": czesc}
            if powod:
                r["powod"] = f"{czesc}_{powod}"
                odrz.dodaj(r)
            else:
                lic_w[czesc][lic] += 1
                if czesc == "A1":
                    a1_ids.add(i)
                pis[czesc].dodaj(r)
    for p in (*pis.values(), odrz):
        p.zamknij()
    # kontrola po maskowaniu i pomiar informacyjny PII DCLM-EN
    po = Counter()
    pii_kl = Counter()
    for c in ("A1", "A2"):
        for b in pq.ParquetFile(POOL[c]).iter_batches(columns=["text"], batch_size=5000):
            for x in b.column(0).to_pylist():
                for nazwa, rx in WZORCE:
                    po[nazwa] += len(rx.findall(x))
                for k in set(wspolne.pii(x)):
                    pii_kl[k] += 1
    tw = {c: pis[c].tok_list for c in pis}
    wyn = {
        "rewizje": {c: ZR[c]["rewizja"] for c in ("A1", "A2", "metadane")},
        "liczniki": dict(licz),
        "zachowane": {c: {"dokumenty": pis[c].n, "tokeny_v6": int(pis[c].tok), "mediana_tok": int(np.median(tw[c])),
                          "p99_tok": int(np.percentile(tw[c], 99)), "max_tok": int(max(tw[c]))} for c in pis},
        "odrzucone_filtr_budowy": {"dokumenty": odrz.n, "tokeny_v6": int(odrz.tok), "na_powod": dict(sorted(odrz.na_powod.items()))},
        "licencje_wierszy": {c: dict(lic_w[c]) for c in lic_w},
        "licencje_A1_pary_cp_spdx_snapshot": dict(lic_par.most_common()),
        "artefakty_trafilatury_A1_dokumenty": dict(art),
        "emaile_maskowane_dopasowania": dict(przed),
        "emaile_po_maskowaniu_w_puli": {k: po[k] for k, _ in WZORCE},
        "pii_detektor_dclm_w_puli_dokumenty": dict(pii_kl),
    }
    os.makedirs(os.path.join(KAT, "wyniki"), exist_ok=True)
    json.dump(wyn, open(os.path.join(KAT, "wyniki/budowa.json"), "w"), ensure_ascii=False, indent=1)
    pliki = []
    for c, plik in (("A1", "arxiv_papers"), ("A2", "arxiv_abstracts")):
        p = POOL[c]
        if pis[c].n == 0:
            continue
        pliki.append({"plik": plik, "rozmiar": os.path.getsize(p), "sha256": sha256(p), "wiersze": pis[c].n,
                      "tokeny_v6": int(pis[c].tok), "lokalnie": p,
                      "zrodlo": f"{ZR[c]['repo']}@{ZR[c]['rewizja']}", "licencje": dict(lic_w[c]),
                      "uwaga": "rozmiar i sha256 dotyczą lokalnego parquetu puli (źródło to wiele plików jsonl.gz)"})
    pp = {"repo": f"{ZR['A1']['repo']} + {ZR['A2']['repo']}",
          "rewizja": f"{ZR['A1']['rewizja']} + {ZR['A2']['rewizja']} (metadane {ZR['metadane']['repo']}@{ZR['metadane']['rewizja']})",
          "seed": P["seed"], "wiersze": sum(f["wiersze"] for f in pliki), "tokeny_v6": sum(f["tokeny_v6"] for f in pliki),
          "pliki": pliki}
    json.dump(pp, open(os.path.join(KAT, "wyniki/probka_pliki.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps(wyn, ensure_ascii=False, indent=1)[:6000])


def probka():
    t = pq.read_table(ODRZ, columns=["id", "url", "license", "powod", "tokeny_v6", "text"])
    pw = np.array(t.column("powod").to_pylist())
    rng = np.random.default_rng(P["seed"])
    with open(os.path.join(ROB, "probka_filtra_budowy.jsonl"), "w", encoding="utf-8") as f:
        for p in sorted(set(pw)):
            idx = np.flatnonzero(pw == p)
            for i in sorted(rng.choice(idx, min(40, len(idx)), replace=False)):
                r = {k: t.column(k)[int(i)].as_py() for k in t.column_names}
                r["text"] = r["text"][:3000]
                f.write(json.dumps(r, ensure_ascii=False) + "\n")


def sprawdz():
    pp = json.load(open(os.path.join(KAT, "wyniki/probka_pliki.json"), encoding="utf-8"))
    tk = Tokenizer.from_file(TOK)
    for k in ("repo", "rewizja", "seed", "wiersze", "tokeny_v6", "pliki"):
        assert k in pp, k
    sw = st = 0
    wszystkie_id = set()
    lic = Counter()
    for f in pp["pliki"]:
        p = f["lokalnie"]
        assert os.path.isabs(p) and os.path.exists(p), p
        assert os.path.getsize(p) == f["rozmiar"] and sha256(p) == f["sha256"], "rozmiar/sha256"
        pf = pq.ParquetFile(p)
        md = pf.metadata
        assert md.num_rows == f["wiersze"] > 0, "wiersze"
        for g in range(md.num_row_groups - 1):
            assert md.row_group(g).num_rows == 5000, f"grupa {g}"
        sch = pf.schema_arrow
        for k in KOL:
            assert pa.types.is_string(sch.field(k).type), k
        tok = 0
        for b in pf.iter_batches(batch_size=5000):
            d = b.to_pydict()
            for x, u, i, l, a in zip(d["text"], d["url"], d["id"], d["license"], d["author"]):
                assert isinstance(x, str) and x.strip(), "pusty text"
                m = re.fullmatch(r"arXiv(-abs)?:(.+)", i)
                assert m and u == f"https://arxiv.org/abs/{m.group(2)}", (i, u)
                assert l in DOZWOLONE, l
                assert a, "author"
                assert not any(rx.search(x) for _, rx in WZORCE), ("e-mail w puli", i)
                assert i not in wszystkie_id, ("id nieunikalne", i)
                wszystkie_id.add(i)
                lic[l] += 1
            tok += sum(tokeny(tk, d["text"]))
        assert tok == f["tokeny_v6"], (tok, f["tokeny_v6"])
        sw += md.num_rows
        st += tok
    assert sw == pp["wiersze"] and st == pp["tokeny_v6"], "sumy"
    print(f"OK: {len(pp['pliki'])} pliki, {sw} wierszy, {st} tokenów v6, licencje {dict(lic)}")


if __name__ == "__main__":
    {"buduj": buduj, "probka": probka, "sprawdz": sprawdz}[sys.argv[1]]()
