"""Pula wiki_mat: reguła 1 z karty na common-pile/wikimedia (Wikipedia EN + Wikibooks), preregistracja.json.

Użycie (venv z dane/matematyka-wspolne/robocze/venv):
  buduj_pule.py pobierz K N -> strumieniowo pliki źródła (co N-ty od K), robocze/sel/<plik>.jsonl (reguła 1), surowe usuwane
  buduj_pule.py buduj       -> robocze/pula/wiki_mat.parquet, robocze/odrzucone.parquet, wyniki/budowa.json, wyniki/probka_pliki.json
  buduj_pule.py sprawdz     -> kontrola kontraktu potoku (kod 0 = OK)
Zero modeli."""
import gzip, hashlib, html, json, os, re, sys
from collections import Counter, defaultdict

import pyarrow as pa
import pyarrow.parquet as pq
from tokenizers import Tokenizer

KAT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # dane/wiki_mat
ROOT = os.path.dirname(os.path.dirname(KAT))
sys.path.insert(0, os.path.join(KAT, "skrypty"))
from wiki_rules import rule1  # noqa: E402
from wsp import math_feats  # noqa: E402

P = json.load(open(os.path.join(KAT, "skrypty/preregistracja.json"), encoding="utf-8"))
REPO = "common-pile/wikimedia"
REW = P["zrodlo"]["rewizja"]
ROB = os.path.join(KAT, "robocze")
SEL = os.path.join(ROB, "sel")
POOL = os.path.join(ROB, "pula/wiki_mat.parquet")
ODRZ = os.path.join(ROB, "odrzucone.parquet")
TOK = os.path.join(ROOT, "dane/dclm-en/robocze/pobrania/tokenizer_v6/tokenizer.json")
TOK_SHA = "0640d3bd3674d7a6e59c540d945a2ad275a12e1bcaeb6007c37a90751f9815dd"
LIC_ZRODLO = "Creative Commons - Attribution Share-Alike - https://creativecommons.org/licenses/by-sa/4.0/"
LICENSE = "CC-BY-SA-4.0"
HOST = {"wikipedia": "https://en.wikipedia.org/wiki/", "wikibooks": "https://en.wikibooks.org/wiki/"}
KOL = ("text", "url", "id", "license", "created", "author", "wiki", "title")


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


def pliki_zrodla():
    from huggingface_hub import HfApi
    fs = HfApi().list_repo_files(REPO, repo_type="dataset", revision=REW)
    return sorted(f for f in fs if f.endswith("_wikipedia.com.jsonl.gz") or f.endswith("_wikibooks.com.jsonl.gz"))


def wybrany(d):
    m = d.get("metadata", {})
    if m.get("namespace") != "0":
        return False
    s, c = math_feats(d["text"])
    return rule1({"s": s, "c": c, "text": d["text"]})


def pobierz(k, n):
    from huggingface_hub import hf_hub_download
    ref = json.load(open(os.path.join(KAT, "wyniki/przeglad_zrodla.json"), encoding="utf-8"))
    sha_ref = {f: x["sha256"] for f, x in ref["pliki"].items()}
    os.makedirs(SEL, exist_ok=True)
    pl = pliki_zrodla()
    for i, f in enumerate(pl):
        if i % n != k or os.path.exists(os.path.join(SEL, f + ".jsonl")):
            continue
        p = hf_hub_download(REPO, f, repo_type="dataset", revision=REW, local_dir=os.path.join(ROB, f"dl{k}"))
        h = sha256(p)
        assert sha_ref.get(f) == h, (f, h)
        wiki = "wikibooks" if "wikibooks" in f else "wikipedia"
        tmp = os.path.join(SEL, f + ".jsonl.tmp")
        nsel = 0
        with gzip.open(p, "rt") as fi, open(tmp, "w", encoding="utf-8") as fo:
            for nr, l in enumerate(fi):
                d = json.loads(l)
                if wybrany(d):
                    m = d["metadata"]
                    fo.write(json.dumps({"plik": f, "nr": nr, "sha256": h, "wiki": wiki, "id_zr": d["id"],
                                         "title": m.get("title"), "url_zr": m.get("url"), "license_zr": m.get("license"),
                                         "authors": m.get("authors") or [], "created": d.get("created"),
                                         "text": d["text"]}, ensure_ascii=False) + "\n")
                    nsel += 1
        os.replace(tmp, os.path.join(SEL, f + ".jsonl"))
        os.remove(p)
        print(f, h, nsel, flush=True)
    print("KONIEC", flush=True)


RX_PUSTE = re.compile(r"\n{3,}")


def wytnij_infobox(t):
    out, i = [], 0
    while True:
        j = t.find("{{Infobox", i)
        if j < 0:
            out.append(t[i:])
            break
        out.append(t[i:j])
        g, k = 0, j
        while k < len(t):
            if t.startswith("{{", k):
                g += 1; k += 2
            elif t.startswith("}}", k):
                g -= 1; k += 2
                if g == 0:
                    break
            else:
                k += 1
        i = k
    return "".join(out)


def normalizuj(t):
    t = html.unescape(wytnij_infobox(t))
    return RX_PUSTE.sub("\n\n", t).strip()


def url_kan(wiki, title, url_zr):
    if title:
        return HOST[wiki] + title.replace(" ", "_")
    return re.sub(r"^https?://(?:en\.)?(wikipedia|wikibooks)\.(?:com|org)/wiki/", lambda m: HOST[m.group(1)], url_zr)


def autor(authors):
    names = [a[0] if isinstance(a, (list, tuple)) else str(a) for a in authors]
    names = [x for x in names if x]
    return ", ".join(names) if names else "unknown"


def kontrole():
    t = "Group (mathematics)\n" + "In mathematics, a group is a set with an operation. " + " ".join(["$a^2 = \\frac{b}{c}$"] * 10)
    s, c = math_feats(t)
    assert rule1({"s": s, "c": c, "text": t})
    tf = "Luminosity\nIn astronomy and physics, luminosity is energy per time. " + " ".join(["$L = \\frac{E}{t}$"] * 10)
    s, c = math_feats(tf)
    assert not rule1({"s": s, "c": c, "text": tf})
    assert normalizuj("A {{Infobox graph | x = {{a}} }}B &minus;1\n\n\n\nC") == "A B \u22121\n\nC"
    assert url_kan("wikipedia", "Complete graph", None) == "https://en.wikipedia.org/wiki/Complete_graph"
    assert url_kan("wikibooks", None, "https://wikibooks.com/wiki/Algebra") == "https://en.wikibooks.org/wiki/Algebra"


def buduj():
    kontrole()
    assert sha256(TOK) == TOK_SHA, "zły tokenizer"
    pl = pliki_zrodla()
    brak = [f for f in pl if not os.path.exists(os.path.join(SEL, f + ".jsonl"))]
    assert not brak, f"brak {len(brak)} plików w sel"
    tk = Tokenizer.from_file(TOK)
    wiersze, odrz, md5s, sha_pl = [], [], set(), {}
    for f in pl:
        for l in open(os.path.join(SEL, f + ".jsonl"), encoding="utf-8"):
            d = json.loads(l)
            sha_pl[f] = d["sha256"]
            t = normalizuj(d["text"])
            rek = {"text": t, "url": url_kan(d["wiki"], d["title"], d["url_zr"]), "id": f"{d['wiki']}:{d['id_zr']}",
                   "license": LICENSE, "created": d["created"] or "unknown", "author": autor(d["authors"]),
                   "wiki": d["wiki"], "title": d["title"] or ""}
            h = hashlib.md5(t.encode()).hexdigest()
            if d["license_zr"] != LIC_ZRODLO:
                rek["powod"] = "licencja"; rek["license"] = str(d["license_zr"]); odrz.append(rek)
            elif h in md5s:
                rek["powod"] = "dedup_dokladny"; odrz.append(rek)
            else:
                md5s.add(h); wiersze.append(rek)
    ids = [r["id"] for r in wiersze]
    assert len(set(ids)) == len(ids), "id nieunikalne"
    tok_w = tokeny(tk, [r["text"] for r in wiersze])
    tok_o = tokeny(tk, [r["text"] for r in odrz])
    os.makedirs(os.path.dirname(POOL), exist_ok=True)
    pq.write_table(pa.table({k: [r[k] for r in wiersze] for k in KOL}), POOL, row_group_size=5000)
    pq.write_table(pa.table({k: pa.array([r[k] for r in odrz], pa.string()) for k in KOL + ("powod",)}
                            | {"tokeny_v6": pa.array(tok_o, pa.int64())}), ODRZ, row_group_size=5000)
    per = defaultdict(lambda: {"dokumenty": 0, "tokeny_v6": 0})
    for r, t in zip(wiersze, tok_w):
        per[r["wiki"]]["dokumenty"] += 1; per[r["wiki"]]["tokeny_v6"] += t
    na_powod = defaultdict(lambda: {"dokumenty": 0, "tokeny_v6": 0})
    for r, t in zip(odrz, tok_o):
        na_powod[r["powod"]]["dokumenty"] += 1; na_powod[r["powod"]]["tokeny_v6"] += t
    wyn = {"repo": REPO, "rewizja": REW, "plikow_zrodla": len(pl), "sha256_plikow": sha_pl,
           "zachowane": {"dokumenty": len(wiersze), "tokeny_v6": int(sum(tok_w)), "na_wiki": dict(per)},
           "odrzucone_filtr_budowy": dict(na_powod),
           "licencje_wierszy": dict(Counter(r["license"] for r in wiersze))}
    os.makedirs(os.path.join(KAT, "wyniki"), exist_ok=True)
    json.dump(wyn, open(os.path.join(KAT, "wyniki/budowa.json"), "w"), ensure_ascii=False, indent=1)
    pp = {"repo": REPO, "rewizja": REW, "seed": P["seed"], "wiersze": len(wiersze), "tokeny_v6": int(sum(tok_w)),
          "pliki": [{"plik": "wiki_mat", "rozmiar": os.path.getsize(POOL), "sha256": sha256(POOL), "wiersze": len(wiersze),
                     "tokeny_v6": int(sum(tok_w)), "lokalnie": POOL,
                     "uwaga": f"rozmiar i sha256 lokalnego parquetu puli; źródło: {len(pl)} plików jsonl.gz (sha256 w wyniki/budowa.json)"}]}
    json.dump(pp, open(os.path.join(KAT, "wyniki/probka_pliki.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in wyn.items() if k != "sha256_plikow"}, ensure_ascii=False, indent=1))


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
        assert all(re.match(r"https://en\.wiki(pedia|books)\.org/wiki/\S+$", u) for u in t.column("url").to_pylist()), "url"
        assert set(t.column("license").to_pylist()) == {LICENSE}, "licencja"
        assert all(isinstance(a, str) and a for a in t.column("author").to_pylist()), "author"
        tok = sum(tokeny(tk, txt))
        assert tok == f["tokeny_v6"], (tok, f["tokeny_v6"])
        sw += md.num_rows; st += tok
    assert sw == pp["wiersze"] and st == pp["tokeny_v6"], "sumy"
    print(f"OK: {sw} wierszy, {st} tokenów v6, {md.num_row_groups} grup")


if __name__ == "__main__":
    a = sys.argv[1]
    if a == "pobierz":
        pobierz(int(sys.argv[2]), int(sys.argv[3]))
    else:
        {"buduj": buduj, "sprawdz": sprawdz}[a]()
