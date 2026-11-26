"""Ile prac A1 jest w peS2o (common-pile/peS2o): dopasowanie po id arXiv z oa_url i po znormalizowanym tytule."""
import sys, re, json, collections, unicodedata
sys.path.insert(0, "/tmp/karty")
import pyarrow.parquet as pq
from huggingface_hub import hf_hub_download, HfApi
from wsp import it, sha

REV = "2caeba1585aaafa3c965410d80af85b09ed11cd9"
a1 = pq.read_table("/tmp/karty/arxiv/a1_ids.parquet").to_pydict()


def norm(s):
    s = unicodedata.normalize("NFKD", s or "").lower()
    return re.sub(r"[^a-z0-9]+", "", s)[:120]


a1_ids = set(a1["id"])
a1_tit = {norm(t): i for t, i in zip(a1["title"], a1["id"]) if len(norm(t)) >= 20}
files = sorted(f for f in HfApi().list_repo_files("common-pile/peS2o", repo_type="dataset", revision=REV) if f.endswith(".gz"))
print("pliki", len(files), flush=True)
C = collections.Counter(); shas = {}
for f in [files[1], files[len(files) // 2]]:
    p = hf_hub_download("common-pile/peS2o", f, repo_type="dataset", revision=REV, local_dir="/tmp/karty/pes2o")
    shas[f] = sha(p)
    for d in it(p):
        C["docs"] += 1
        m = d["metadata"]
        src = (m.get("pdf_src") or "")
        url = m.get("oa_url") or ""
        mm = re.search(r"arxiv\.org/(?:abs|pdf)/([0-9]{4}\.[0-9]{4,5}|[a-z\-\.]+/[0-9]{7})", url, re.I)
        aid = mm.group(1) if mm else None
        if src.lower() == "arxiv":
            C["pdf_src_arxiv"] += 1
        if aid:
            C["oa_url_arxiv"] += 1
        title = d["text"].split("\n", 1)[0]
        hit = (aid in a1_ids) if aid else False
        hit_t = norm(title) in a1_tit
        if hit:
            C["A1_po_id"] += 1
        if hit_t:
            C["A1_po_tytule"] += 1
        if hit or hit_t:
            C["A1_razem"] += 1
    import os
    os.remove(p)
    print(f, dict(C), flush=True)
print("WYNIK", json.dumps({"files_total": len(files), "sha256": shas, "C": C}))
