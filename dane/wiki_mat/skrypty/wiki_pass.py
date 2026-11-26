"""Strumieniowy przebieg po Wikipedii EN i Wikibooks z common-pile/wikimedia.
Zapisuje tylko dokumenty z nadzbioru (ns 0, >=5 wzorów, >=3 komendy) z cechami; reguła 0 = >=10 i >=5."""
import sys, os, json
sys.path.insert(0, "/tmp/karty")
from huggingface_hub import hf_hub_download, HfApi
from wsp import it, ntok_batch, sha, math_feats

REV = "781b263a6546515543bec3968ad4743fbc152b72"
k, n = int(sys.argv[1]), int(sys.argv[2])
files = sorted(f for f in HfApi().list_repo_files("common-pile/wikimedia", repo_type="dataset", revision=REV)
               if f.endswith("_wikipedia.com.jsonl.gz") or f.endswith("_wikibooks.com.jsonl.gz"))
# najpierw co 10. shard Wikipedii (ekstrapolacja), potem reszta
files = [f for f in files if int(f[:5]) % 10 == 0] + [f for f in files if int(f[:5]) % 10 != 0]
if len(sys.argv) > 3 and sys.argv[3] == "decile":
    files = [f for f in files if int(f[:5]) % 10 == 0]
mine = [f for i, f in enumerate(files) if i % n == k]
print("pliki", len(files), "moje", len(mine), flush=True)
for f in mine:
    out_sum = f"/tmp/karty/wiki/sum/{f}.json"
    if os.path.exists(out_sum):
        continue
    p = hf_hub_download("common-pile/wikimedia", f, repo_type="dataset", revision=REV, local_dir="/tmp/karty/wiki/dl")
    h = sha(p)
    docs = ns0 = 0; byt = ns0b = 0
    sel = []
    for d in it(p):
        docs += 1
        t = d["text"]; b = len(t.encode()); byt += b
        m = d.get("metadata", {})
        if m.get("namespace") != "0":
            continue
        ns0 += 1; ns0b += b
        s, c = math_feats(t)
        if s >= 5 and c >= 3:
            sel.append({"id": d["id"], "title": m.get("title"), "url": m.get("url"), "wiki": m.get("wiki"),
                        "license": m.get("license"), "created": d.get("created"), "s": s, "c": c, "bytes": b,
                        "rule0": s >= 10 and c >= 5, "text": t})
    toks = ntok_batch([x["text"] for x in sel]) if sel else []
    for x, tk in zip(sel, toks):
        x["tok"] = tk
    with open(f"/tmp/karty/wiki/sel/{f}.jsonl", "w") as fo:
        for x in sel:
            fo.write(json.dumps(x, ensure_ascii=False) + "\n")
    summ = {"file": f, "sha256": h, "docs": docs, "bytes": byt, "ns0": ns0, "ns0_bytes": ns0b,
            "sel": len(sel), "sel_tok": sum(toks),
            "rule0": sum(1 for x in sel if x["rule0"]), "rule0_tok": sum(x["tok"] for x in sel if x["rule0"])}
    with open(out_sum, "w") as fo:
        json.dump(summ, fo)
    os.remove(p)
    print(json.dumps(summ), flush=True)
print("KONIEC", flush=True)
