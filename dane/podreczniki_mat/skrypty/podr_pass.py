"""C1-C3: LibreTexts / PressBooks / OERCommons: wybór matematyki, licencje, tokeny, zapis wybranych."""
import sys, re, json, collections
sys.path.insert(0, "/tmp/karty")
from huggingface_hub import hf_hub_download, HfApi
from wsp import it, ntok_batch, sha, EMAIL

KW = re.compile(r"\b(math|maths|mathemat\w*|calculus|algebra\w*|geometr\w*|trigonometr\w*|precalculus|pre-calculus|statistic\w*|probabilit\w*|arithmetic|number theory|topology|combinatori\w*|differential equations?|linear algebra|discrete|logic|proofs?|real analysis|complex analysis)\b", re.I)
LATEX = re.compile(r"(\\frac|\\sum|\\int|\\mathbb|\\left|\\sqrt|\\alpha|\\beta|\\theta|\\pi\b|\\cdot|\\leq|\\geq|\\in\b|\\mathrm|\\begin\{|\$[^$\n]{1,80}\$)")
SRC = {
    "libretexts": ("common-pile/libretexts", "d4ce4b1edf95888b24992db3bbb2ae8e2bf6c22f"),
    "pressbooks": ("common-pile/pressbooks", "29fa162fc78277b160a7010f18086b5189ffb761"),
    "oercommons": ("common-pile/oercommons", "9b3305165b01bec541b6a6baaba2b5b8566dfe29"),
}


def nlatex(t, cap=1000):
    c = 0
    for _ in LATEX.finditer(t):
        c += 1
        if c >= cap:
            break
    return c


def rule(name, d):
    m = d.get("metadata", {}); t = d["text"]
    if name == "libretexts":
        return re.match(r"https?://(math|stats)\.libretexts\.org", m.get("url") or d["id"]) is not None
    head = (m.get("book_url") or "") + " " + (m.get("title") or "")
    if name == "pressbooks":
        return bool(KW.search(head)) and nlatex(t, 3) >= 3
    return bool(KW.search(m.get("title") or "")) or nlatex(t, 5) >= 5


for name, (repo, rev) in SRC.items():
    fs = sorted(f for f in HfApi().list_repo_files(repo, repo_type="dataset", revision=rev) if f.endswith(".gz"))
    C = collections.Counter(); L = collections.Counter(); LS = collections.Counter(); shas = {}; sel = []; hosts = collections.Counter()
    for f in fs:
        p = hf_hub_download(repo, f, repo_type="dataset", revision=rev, local_dir=f"/tmp/karty/podr/dl_{name}")
        shas[f] = sha(p)
        for d in it(p):
            C["docs"] += 1
            m = d.get("metadata", {})
            l = m.get("license") or "?"
            L[l] += 1
            if re.search(r"nc|noncommercial|non-commercial|nd\b|noderiv", l, re.I):
                C["nc_nd"] += 1
            if rule(name, d):
                LS[l] += 1
                u = m.get("url") or d["id"]
                hosts[re.sub(r"^https?://([^/]+).*", r"\1", u)] += 1
                t = d["text"]
                sel.append({"id": d["id"], "url": u, "title": m.get("title"), "book_url": m.get("book_url"), "license": l,
                            "author": m.get("author"), "created": d.get("created"), "latex": nlatex(t),
                            "openstax": bool(re.search(r"openstax", (u or "") + " " + t[:3000] + " " + t[-3000:], re.I)),
                            "email": bool(EMAIL.search(t)), "text": t})
    tk = ntok_batch([x["text"] for x in sel])
    for x, k in zip(sel, tk):
        x["tok"] = k
    with open(f"/tmp/karty/podr/sel_{name}.jsonl", "w") as fo:
        for x in sel:
            fo.write(json.dumps(x, ensure_ascii=False) + "\n")
    print("WYNIK", json.dumps({"name": name, "repo": repo, "rev": rev, "sha256": shas, "docs": C["docs"], "nc_nd_all": C["nc_nd"],
                               "licenses_all": L.most_common(), "sel": len(sel), "sel_tok": sum(tk), "sel_bytes": sum(len(x["text"].encode()) for x in sel),
                               "sel_licenses": LS.most_common(), "sel_openstax": sum(x["openstax"] for x in sel),
                               "sel_openstax_tok": sum(x["tok"] for x in sel if x["openstax"]), "sel_email": sum(x["email"] for x in sel),
                               "hosts": hosts.most_common(12)}, ensure_ascii=False), flush=True)
print("KONIEC")
