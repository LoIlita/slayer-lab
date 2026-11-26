"""Pula podreczniki_mat: C1 LibreTexts (math., stats.) + C2 PressBooks z Common Pile, preregistracja.json.

Użycie (venv z dane/matematyka-wspolne/robocze/venv):
  buduj_pule.py buduj    -> robocze/pula/podreczniki_mat.parquet, robocze/odrzucone.parquet, wyniki/budowa.json, wyniki/probka_pliki.json
  buduj_pule.py sprawdz  -> kontrola kontraktu potoku (kod 0 = OK)
Surowe pliki źródła pobierane do robocze/dl i usuwane po budowie. Zero modeli."""
import gzip, hashlib, json, os, re, shutil, sys
from collections import Counter, defaultdict

import pyarrow as pa
import pyarrow.parquet as pq
from tokenizers import Tokenizer

KAT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # dane/podreczniki_mat
ROOT = os.path.dirname(os.path.dirname(KAT))
P = json.load(open(os.path.join(KAT, "skrypty/preregistracja.json"), encoding="utf-8"))
ROB = os.path.join(KAT, "robocze")
DL = os.path.join(ROB, "dl")
POOL = os.path.join(ROB, "pula/podreczniki_mat.parquet")
ODRZ = os.path.join(ROB, "odrzucone.parquet")
TOK = os.path.join(ROOT, "dane/dclm-en/robocze/pobrania/tokenizer_v6/tokenizer.json")
TOK_SHA = "0640d3bd3674d7a6e59c540d945a2ad275a12e1bcaeb6007c37a90751f9815dd"
MIN_TOK = 600
KOL = ("text", "url", "id", "license", "created", "author", "czesc", "title")

# KW i LATEX dosłownie z podr_pass.py (przebieg pomiarowy karty; sam plik uruchamia pomiar przy imporcie)
_src = open(os.path.join(KAT, "skrypty/podr_pass.py"), encoding="utf-8").read()
_ns = {"re": re}
for _l in _src.splitlines():
    if _l.startswith("KW = ") or _l.startswith("LATEX = "):
        exec(_l, _ns)
KW, LATEX = _ns["KW"], _ns["LATEX"]

SPDX = {
    "Creative Commons - Attribution - https://creativecommons.org/licenses/by/4.0/": "CC-BY-4.0",
    "Creative Commons - Attribution Share-Alike - https://creativecommons.org/licenses/by-sa/4.0/": "CC-BY-SA-4.0",
    "Creative Commons - Attribution - https://creativecommons.org/licenses/by/3.0/": "CC-BY-3.0",
    "Creative Commons - Attribution Share-Alike - https://creativecommons.org/licenses/by-sa/3.0/": "CC-BY-SA-3.0",
    "Creative Commons - Attribution Share-Alike - https://creativecommons.org/licenses/by-sa/2.5/": "CC-BY-SA-2.5",
    "Creative Commons Zero - Public Domain - https://creativecommons.org/publicdomain/zero/1.0/": "CC0-1.0",
    "Public Domain": "LicenseRef-PD",
    "GNU Free Documentation License": "GFDL-1.3-or-later",
}
RX_NCND = re.compile(r"nc|noncommercial|non-commercial|nd\b|noderiv", re.I)
RX_C1 = re.compile(r"https?://(math|stats)\.libretexts\.org")
RX_NAW = re.compile(r"\s*Last updated Save as PDF Page ID \d+")
RX_LATEX_WP = re.compile(r"\[latex\](.*?)\[/latex\]", re.S)
RX_PUSTE = re.compile(r"\n{3,}")
RX_OPENSTAX = re.compile(r"openstax", re.I)


def nlatex(t, cap):
    c = 0
    for _ in LATEX.finditer(t):
        c += 1
        if c >= cap:
            break
    return c


def wybrany(czesc, d):
    m = d.get("metadata", {})
    if czesc == "C1":
        return RX_C1.match(m.get("url") or d["id"]) is not None
    return bool(KW.search((m.get("book_url") or "") + " " + (m.get("title") or ""))) and nlatex(d["text"], 3) >= 3


def normalizuj(czesc, t):
    if czesc == "C1":
        t = RX_NAW.sub("", t, count=1)
    else:
        t = RX_LATEX_WP.sub(lambda m: "\\(" + m.group(1) + "\\)", t)
    return RX_PUSTE.sub("\n\n", t).strip()


def openstax(url, t):
    return bool(RX_OPENSTAX.search((url or "") + " " + t[:3000] + " " + t[-3000:]))


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 24), b""):
            h.update(b)
    return h.hexdigest()


def tokeny(tk, teksty):
    out = []
    for i in range(0, len(teksty), 5000):
        out += [len(e.ids) + 1 for e in tk.encode_batch(teksty[i:i + 5000], add_special_tokens=False)]
    return out


def kontrole():
    assert normalizuj("C1", "1.1: Scale Last updated Save as PDF Page ID 34976 Body\n\n\n\nx") == "1.1: Scale Body\n\nx"
    assert normalizuj("C2", "a [latex]\\frac{1}{2}[/latex] b") == "a \\(\\frac{1}{2}\\) b"
    assert openstax("https://x.pressbooks.pub/a", "Access for free at OpenStax") and not openstax("https://math.libretexts.org/a", "Algebra")
    assert all(not RX_NCND.search(k) for k in SPDX)
    assert wybrany("C1", {"id": "https://stats.libretexts.org/x", "text": "", "metadata": {}})
    assert not wybrany("C1", {"id": "https://chem.libretexts.org/x", "text": "", "metadata": {}})
    assert wybrany("C2", {"id": "a", "text": "$x=1$ $y=2$ \\frac{1}{2}", "metadata": {"title": "College Algebra"}})


def buduj():
    from huggingface_hub import hf_hub_download
    kontrole()
    assert sha256(TOK) == TOK_SHA, "zły tokenizer"
    tk = Tokenizer.from_file(TOK)
    wsz = []
    for czesc in ("C1", "C2"):
        z = P["zrodlo"][czesc]
        repo = z["repo"].split("datasets/")[1]
        sel = []
        for f, sh in z["pliki"].items():
            p = hf_hub_download(repo, f, repo_type="dataset", revision=z["rewizja"], local_dir=DL)
            assert sha256(p) == sh, (f, "sha256")
            with gzip.open(p, "rt") as fi:
                for l in fi:
                    d = json.loads(l)
                    if not wybrany(czesc, d):
                        continue
                    m = d.get("metadata", {})
                    lz = m.get("license") or ""
                    t = normalizuj(czesc, d["text"])
                    sel.append({"text": t, "url": d["id"].split("#")[0], "id": d["id"],
                                "license": SPDX.get(lz) if not RX_NCND.search(lz) else None, "license_zr": lz,
                                "created": str(d.get("created") or "unknown"), "author": (m.get("author") or "").strip() or "unknown",
                                "czesc": czesc, "title": m.get("title") or "",
                                "openstax": openstax(m.get("url") or d["id"], d["text"]) or openstax(d["id"], t)})
        sel.sort(key=lambda r: r["id"])
        wsz += sel
    tok = tokeny(tk, [r["text"] for r in wsz])
    wiersze, odrz, md5s = [], [], set()
    for r, t in zip(wsz, tok):
        r["tok"] = t
        h = hashlib.md5(r["text"].encode()).hexdigest()
        if r["license"] is None:
            r["powod"] = "licencja"; r["license"] = r["license_zr"]
        elif h in md5s:
            r["powod"] = "dedup_dokladny"
        elif t < MIN_TOK:
            r["powod"] = "krotki"
        elif r["openstax"]:
            r["powod"] = "openstax"
        md5s.add(h)
        (odrz if "powod" in r else wiersze).append(r)
    ids = [r["id"] for r in wiersze]
    assert len(set(ids)) == len(ids), "id nieunikalne"
    os.makedirs(os.path.dirname(POOL), exist_ok=True)
    pq.write_table(pa.table({k: [r[k] for r in wiersze] for k in KOL}), POOL, row_group_size=5000)
    pq.write_table(pa.table({k: pa.array([r[k] for r in odrz], pa.string()) for k in KOL + ("powod",)}
                            | {"tokeny_v6": pa.array([r["tok"] for r in odrz], pa.int64())}), ODRZ, row_group_size=5000)

    def zlicz(rs, klucz):
        o = defaultdict(lambda: {"dokumenty": 0, "tokeny_v6": 0})
        for r in rs:
            o[klucz(r)]["dokumenty"] += 1; o[klucz(r)]["tokeny_v6"] += r["tok"]
        return dict(sorted(o.items()))
    tw = sum(r["tok"] for r in wiersze)
    wyn = {"zrodla": {c: P["zrodlo"][c] for c in ("C1", "C2")},
           "wybrane_przed_filtrem": zlicz(wsz, lambda r: r["czesc"]),
           "zachowane": {"dokumenty": len(wiersze), "tokeny_v6": tw, "na_czesc": zlicz(wiersze, lambda r: r["czesc"])},
           "odrzucone_filtr_budowy": zlicz(odrz, lambda r: f"{r['powod']}/{r['czesc']}"),
           "openstax_wsrod_wybranych_przed_filtrem": zlicz([r for r in wsz if r["openstax"]], lambda r: r["czesc"]),
           "licencje_wierszy": dict(Counter(r["license"] for r in wiersze).most_common()),
           "licencje_wierszy_tokeny_v6": dict(Counter({l: sum(r["tok"] for r in wiersze if r["license"] == l)
                                                       for l in set(r["license"] for r in wiersze)}).most_common())}
    os.makedirs(os.path.join(KAT, "wyniki"), exist_ok=True)
    json.dump(wyn, open(os.path.join(KAT, "wyniki/budowa.json"), "w"), ensure_ascii=False, indent=1)
    pp = {"repo": "common-pile/libretexts + common-pile/pressbooks",
          "rewizja": ", ".join(f"{c}@{P['zrodlo'][c]['rewizja']}" for c in ("C1", "C2")), "seed": P["seed"],
          "wiersze": len(wiersze), "tokeny_v6": tw,
          "pliki": [{"plik": "podreczniki_mat", "rozmiar": os.path.getsize(POOL), "sha256": sha256(POOL),
                     "wiersze": len(wiersze), "tokeny_v6": tw, "lokalnie": POOL,
                     "uwaga": "rozmiar i sha256 lokalnego parquetu puli; sha256 plików źródła w preregistracja.json (sprawdzane)"}]}
    json.dump(pp, open(os.path.join(KAT, "wyniki/probka_pliki.json"), "w"), ensure_ascii=False, indent=1)
    shutil.rmtree(DL)
    print(json.dumps(wyn, ensure_ascii=False, indent=1))


def sprawdz():
    pp = json.load(open(os.path.join(KAT, "wyniki/probka_pliki.json"), encoding="utf-8"))
    tk = Tokenizer.from_file(TOK)
    for k in ("repo", "rewizja", "seed", "wiersze", "tokeny_v6", "pliki"):
        assert k in pp, k
    sw = st = 0
    for f in pp["pliki"]:
        p = f["lokalnie"]
        assert os.path.isabs(p) and os.path.exists(p), p
        assert os.path.getsize(p) == f["rozmiar"] and sha256(p) == f["sha256"], "rozmiar/sha256"
        pf = pq.ParquetFile(p)
        md = pf.metadata
        assert md.num_rows == f["wiersze"] > 0, "wiersze"
        for g in range(md.num_row_groups - 1):
            assert md.row_group(g).num_rows == 5000, f"grupa {g}"
        for k in ("text", "url", "id", "license", "created", "author"):
            assert pa.types.is_string(pf.schema_arrow.field(k).type), k
        t = pq.read_table(p)
        ids = t.column("id").to_pylist()
        assert len(set(ids)) == len(ids), "id nieunikalne"
        txt = t.column("text").to_pylist()
        assert all(isinstance(x, str) and x for x in txt), "pusty text"
        assert all(u.startswith("https://") and "#" not in u for u in t.column("url").to_pylist()), "url"
        assert set(t.column("license").to_pylist()) <= set(SPDX.values()), "licencja"
        assert all(isinstance(a, str) and a for a in t.column("author").to_pylist()), "author"
        assert not any(openstax(u, x) for u, x in zip(t.column("url").to_pylist(), txt)), "openstax w puli"
        tok = tokeny(tk, txt)
        assert min(tok) >= MIN_TOK, "krótki"
        assert sum(tok) == f["tokeny_v6"], (sum(tok), f["tokeny_v6"])
        sw += md.num_rows; st += sum(tok)
    assert sw == pp["wiersze"] and st == pp["tokeny_v6"], "sumy"
    print(f"OK: {sw} wierszy, {st} tokenów v6, {md.num_row_groups} grup")


if __name__ == "__main__":
    {"buduj": buduj, "sprawdz": sprawdz}[sys.argv[1]]()
