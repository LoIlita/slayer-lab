"""Pula OEIS: pliki seq/*.seq z oeis/oeisdata@<rewizja> -> czytelne dokumenty (preregistracja.json -> dokument, filtr_budowy).

Użycie (venv z dane/matematyka-wspolne/robocze/venv):
  buduj_pule.py buduj    -> robocze/pula/oeis_seq.parquet, robocze/odrzucone.parquet, wyniki/budowa.json, wyniki/probka_pliki.json
  buduj_pule.py probka   -> robocze/probka_filtra_budowy.jsonl (40 odrzuconych na powód filtra budowy, do recenzji)
  buduj_pule.py sprawdz  -> kontrola kontraktu potoku na probka_pliki.json i parquecie (kod 0 = OK)
Zero modeli: parser pól formatu wewnętrznego OEIS i wyrażenia regularne."""
import hashlib, json, os, re, subprocess, sys
from collections import Counter, defaultdict

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
from tokenizers import Tokenizer

KAT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # dane/oeis
ROOT = os.path.dirname(os.path.dirname(KAT))
sys.path.insert(0, os.path.join(ROOT, "dane/dclm-en/skrypty"))
import wspolne  # noqa: E402

P = json.load(open(os.path.join(KAT, "skrypty/preregistracja.json"), encoding="utf-8"))
P_INFI = json.load(open(os.path.join(ROOT, "dane/infiwebmath4/skrypty/preregistracja.json"), encoding="utf-8"))
REW = P["zrodlo"]["rewizja"]
REPO = "oeis/oeisdata@" + REW
KLON = os.path.join(KAT, "robocze/oeisdata")
POOL = os.path.join(KAT, "robocze/pula/oeis_seq.parquet")
ODRZ = os.path.join(KAT, "robocze/odrzucone.parquet")
TOK = os.path.join(ROOT, "dane/dclm-en/robocze/pobrania/tokenizer_v6/tokenizer.json")
TOK_SHA = "0640d3bd3674d7a6e59c540d945a2ad275a12e1bcaeb6007c37a90751f9815dd"
CREATED = "2026-11-26"
LICENSE = "CC-BY-SA-4.0"
MAX_WYRAZOW = 60
MIN_ZNAKOW = 200
MARTWE_K = {"dead", "dumb", "dupe"}
RX_MARTWA_N = re.compile(r"^\s*(allocated|recycled)", re.I)

# ---- e-maile (preregistracja -> dokument.maskowanie_emaili)
RX_EMAIL = wspolne.RX_EMAIL
RX_AT = re.compile(P_INFI["aneks_2026_11_24c"]["pii_zaciemniony"]["regex"])
RX_AB = re.compile(P_INFI["aneks_2026_11_25c"]["pii_at_bez_nawiasow"]["regex"])
WZORCE = (("email", RX_EMAIL), ("zaciemniony", RX_AT), ("at_bez_nawiasow", RX_AB))
OBLEC = [(re.compile(r"\(\s*(?:" + r.pattern + r")\s*\)"), re.compile(r"\[\s*(?:" + r.pattern + r")\s*\]"), r) for _, r in WZORCE]
RX_PUSTY_NAWIAS = re.compile(r"\(\s*\)|\[\s*\]")
RX_SPACJE = re.compile(r"(?<=\S)[ \t]{2,}")
RX_SPACJA_PRZED = re.compile(r"[ \t]+(?=[,.;:)\]])")
RX_PODWOJNY_PRZECINEK = re.compile(r",(?:[ \t]*,)+")
RX_PODKRESL = re.compile(r"(?<!\w)_([A-Z][^_\n]{0,80}?)_(?!\w)")


def maskuj(linia, licz=None):
    zm = False
    for (ok, kw, r), (nazwa, _) in zip(OBLEC, WZORCE):
        n0 = len(r.findall(linia))
        if not n0:
            continue
        if licz is not None:
            licz[nazwa] += n0
        linia = kw.sub("", ok.sub("", linia))
        linia = r.sub("", linia)
        zm = True
    if zm:
        linia = RX_PUSTY_NAWIAS.sub("", linia)
        linia = RX_SPACJA_PRZED.sub("", RX_SPACJE.sub(" ", linia))
        linia = RX_PODWOJNY_PRZECINEK.sub(",", linia).rstrip()
    return linia


def test_maskowania():
    przyp = {
        "F(n+1) is the number of perfect matchings. - Sharon Sela (sharonsela(AT)hotmail.com), May 19 2002":
            "F(n+1) is the number of perfect matchings. - Sharon Sela, May 19 2002",
        "_N. J. A. Sloane_ (njas@research.att.com), 1991": "_N. J. A. Sloane_, 1991",
        "Jan Kowalski [jk(AT)math.uni.pl]": "Jan Kowalski",
        "Corrected by Joe Bloggs, joe at example.edu, Jan 01 2001": "Corrected by Joe Bloggs, Jan 01 2001",
        "a(n) = 2*a(n-1) + 1.": "a(n) = 2*a(n-1) + 1.",
    }
    for we, ocz in przyp.items():
        wy = maskuj(we)
        assert wy == ocz, (we, wy)
        assert not any(r.search(wy) for _, r in WZORCE), wy


# ---- parser
POLA = ("I", "S", "T", "U", "V", "W", "X", "N", "C", "D", "H", "F", "e", "p", "t", "o", "Y", "K", "O", "A", "E")


def parsuj(surowe):
    pola = defaultdict(list)
    for ln in surowe.split("\n"):
        if len(ln) < 2 or ln[0] != "%":
            continue
        kod = ln[1]
        reszta = ln[3:]
        sp = reszta.find(" ")
        tresc = reszta[sp + 1:] if sp >= 0 else ""
        pola[kod].append(tresc.rstrip())
    return pola


def podkresl(linia):
    return RX_PODKRESL.sub(r"\1", linia)


def dokument(anr, pola, licz):
    nazwa = " ".join(pola.get("N", [])).strip()
    wyrazy = [w for w in "".join(x.strip() for k in "STU" for x in pola.get(k, [])).split(",") if w]
    sekcje = []

    def blok(tytul, linie, podk=True):
        linie = [maskuj(x, licz) for x in linie]
        if podk:
            linie = [podkresl(x) for x in linie]
        linie = [x for x in linie if x.strip()]
        if linie:
            sekcje.append(tytul + ":\n" + "\n".join(linie))

    blok("Comments", pola.get("C", []))
    blok("Formulas", pola.get("F", []))
    blok("Examples", pola.get("e", []))
    prog = []
    for kod, jezyk in (("p", "(Maple)"), ("t", "(Mathematica)")):
        if pola.get(kod):
            prog += [jezyk] + pola[kod]
    prog += pola.get("o", [])
    blok("Programs", prog, podk=False)
    blok("Cross-references", pola.get("Y", []))
    autor = " ".join(podkresl(maskuj(x, licz)) for x in pola.get("A", [])).strip()
    if autor:
        sekcje.append("Author: " + autor)
    glowa = f"{anr}: {podkresl(maskuj(nazwa, licz))}"
    terms = "Terms: " + ", ".join(wyrazy[:MAX_WYRAZOW]) + (", ..." if len(wyrazy) > MAX_WYRAZOW else "")
    tekst = "\n\n".join([glowa, terms] + sekcje)
    bez_wyrazow = "\n\n".join([glowa] + sekcje)
    return tekst, len(bez_wyrazow)


def powod_odrzucenia(pola, dl_bez):
    if not "".join(pola.get("N", [])).strip():
        return "brak_n"
    kw = {k.strip() for x in pola.get("K", []) for k in x.split(",")}
    if kw & MARTWE_K or RX_MARTWA_N.match(" ".join(pola.get("N", []))):
        return "martwa"
    if not any(x.strip() for x in pola.get("C", [])) and not any(x.strip() for x in pola.get("F", [])):
        return "bez_tresci"
    if dl_bez < MIN_ZNAKOW:
        return "krotka"
    return None


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


def buduj():
    test_maskowania()
    assert sha256(TOK) == TOK_SHA, "zły tokenizer"
    head = subprocess.check_output(["git", "-C", KLON, "rev-parse", "HEAD"], text=True).strip()
    assert head == REW, head
    status = subprocess.check_output(["git", "-C", KLON, "status", "--porcelain"], text=True)
    assert not status.strip(), "klon zmieniony"
    pliki = sorted(subprocess.check_output(["git", "-C", KLON, "ls-files", "seq"], text=True).split())
    pliki = [p for p in pliki if p.endswith(".seq")]
    tk = Tokenizer.from_file(TOK)
    przed = Counter()  # dopasowania e-maili przy maskowaniu
    wiersze, odrz = [], []
    bajty = 0
    zle_utf8 = 0
    for p in pliki:
        anr = os.path.basename(p)[:-4]
        b = open(os.path.join(KLON, p), "rb").read()
        bajty += len(b)
        try:
            s = b.decode("utf-8")
        except UnicodeDecodeError:
            zle_utf8 += 1
            s = b.decode("utf-8", "replace")
        pola = parsuj(s)
        tekst, dl_bez = dokument(anr, pola, przed)
        pw = powod_odrzucenia(pola, dl_bez)
        rek = {"text": tekst, "url": f"https://oeis.org/{anr}", "id": anr, "license": LICENSE, "created": CREATED,
               "repo": REPO, "path": p}
        if pw:
            rek["powod"] = pw
            odrz.append(rek)
        else:
            wiersze.append(rek)
    po = Counter()
    for r in wiersze:
        for nazwa, rx in WZORCE:
            po[nazwa] += len(rx.findall(r["text"]))
    tok_w = tokeny(tk, [r["text"] for r in wiersze])
    tok_o = tokeny(tk, [r["text"] for r in odrz])
    os.makedirs(os.path.dirname(POOL), exist_ok=True)
    kol = ("text", "url", "id", "license", "created", "repo", "path")
    pq.write_table(pa.table({k: [r[k] for r in wiersze] for k in kol}), POOL, row_group_size=5000)
    pq.write_table(pa.table({k: [r[k] for r in odrz] for k in kol + ("powod",)} | {"tokeny_v6": tok_o}), ODRZ,
                   row_group_size=5000)
    # pomiar informacyjny detektora DCLM-EN na puli (bez decyzji; decyzje liczy agreguj_mat.py)
    pii_kl = Counter()
    for r in wiersze:
        for k in set(wspolne.pii(r["text"])):
            pii_kl[k] += 1
    na_powod = defaultdict(lambda: {"dokumenty": 0, "tokeny_v6": 0})
    for r, t in zip(odrz, tok_o):
        na_powod[r["powod"]]["dokumenty"] += 1
        na_powod[r["powod"]]["tokeny_v6"] += t
    n_all = len(wiersze) + len(odrz)
    t_all = sum(tok_w) + sum(tok_o)
    wyn = {
        "rewizja": REW, "plikow_seq": len(pliki), "bajty_seq": bajty, "zle_utf8": zle_utf8,
        "zachowane": {"dokumenty": len(wiersze), "tokeny_v6": int(sum(tok_w)),
                      "mediana_tok": int(np.median(tok_w)), "p99_tok": int(np.percentile(tok_w, 99)),
                      "max_tok": int(max(tok_w))},
        "odrzucone": {"dokumenty": len(odrz), "tokeny_v6": int(sum(tok_o)),
                      "odsetek_dokumentow": round(len(odrz) / n_all, 4), "odsetek_tokenow": round(sum(tok_o) / t_all, 4),
                      "na_powod": dict(sorted(na_powod.items()))},
        "emaile_maskowane_dopasowania": dict(przed),
        "emaile_po_maskowaniu_w_puli": {k: po[k] for k, _ in WZORCE},
        "pii_detektor_dclm_w_puli_dokumenty": dict(pii_kl),
        "licencje_wierszy": {LICENSE: len(wiersze)},
    }
    os.makedirs(os.path.join(KAT, "wyniki"), exist_ok=True)
    json.dump(wyn, open(os.path.join(KAT, "wyniki/budowa.json"), "w"), ensure_ascii=False, indent=1)
    pp = {"repo": "oeis/oeisdata", "rewizja": REW, "seed": P["seed"], "wiersze": len(wiersze),
          "tokeny_v6": int(sum(tok_w)),
          "pliki": [{"plik": "seq", "rozmiar": os.path.getsize(POOL), "sha256": sha256(POOL), "wiersze": len(wiersze),
                     "tokeny_v6": int(sum(tok_w)), "lokalnie": POOL,
                     "zrodlo": {"plikow_seq": len(pliki), "bajty_seq": bajty},
                     "uwaga": "rozmiar i sha256 dotyczą lokalnego parquetu puli (źródło to katalog seq/, nie jeden plik)"}]}
    json.dump(pp, open(os.path.join(KAT, "wyniki/probka_pliki.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps(wyn, ensure_ascii=False, indent=1))


def probka():
    """40 odrzuconych na powód filtra budowy, default_rng(seed) -> robocze/probka_filtra_budowy.jsonl (do recenzji)."""
    t = pq.read_table(ODRZ, columns=["id", "url", "powod", "tokeny_v6", "text"])
    pw = np.array(t.column("powod").to_pylist())
    rng = np.random.default_rng(P["seed"])
    with open(os.path.join(KAT, "robocze/probka_filtra_budowy.jsonl"), "w", encoding="utf-8") as f:
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
    for f in pp["pliki"]:
        p = f["lokalnie"]
        assert os.path.isabs(p) and os.path.exists(p), p
        assert os.path.getsize(p) == f["rozmiar"] and sha256(p) == f["sha256"], "rozmiar/sha256"
        pf = pq.ParquetFile(p)
        md = pf.metadata
        assert md.num_rows == f["wiersze"], "wiersze"
        for g in range(md.num_row_groups - 1):
            assert md.row_group(g).num_rows == 5000, f"grupa {g}"
        sch = pf.schema_arrow
        for k in ("text", "url", "id", "license", "created", "repo", "path"):
            assert pa.types.is_string(sch.field(k).type) or pa.types.is_large_string(sch.field(k).type), k
        t = pq.read_table(p)
        ids = t.column("id").to_pylist()
        assert len(set(ids)) == len(ids), "id nieunikalne"
        txt = t.column("text").to_pylist()
        assert all(isinstance(x, str) and x for x in txt), "pusty text"
        assert all(u == f"https://oeis.org/{i}" for u, i in zip(t.column("url").to_pylist(), ids)), "url"
        assert all(re.fullmatch(r"A\d{6,}", i) for i in ids), "format id"
        assert set(t.column("license").to_pylist()) == {LICENSE}, "licencja"
        assert all(not rx.search(x) for x in txt for _, rx in WZORCE), "e-mail w puli"
        tok = sum(tokeny(tk, txt))
        assert tok == f["tokeny_v6"], (tok, f["tokeny_v6"])
        sw += md.num_rows
        st += tok
    assert sw == pp["wiersze"] and st == pp["tokeny_v6"], "sumy"
    print(f"OK: {sw} wierszy, {st} tokenów v6, {md.num_row_groups} grup")


if __name__ == "__main__":
    {"buduj": buduj, "probka": probka, "sprawdz": sprawdz}[sys.argv[1]]()
