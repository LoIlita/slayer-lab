"""A3: shard Proof-Pile-2 arxiv (RedPajama) — pola, łączenie z metadanymi, tokeny v6 na pracę w kategoriach ścisłych."""
import sys, io, json, re, collections, random
sys.path.insert(0, "/tmp/karty")
import zstandard
import pyarrow.parquet as pq
from huggingface_hub import hf_hub_download
from wsp import ntok_batch, sha

random.seed(5)
t = pq.read_table("/tmp/karty/arxiv/meta.parquet", columns=["id", "categories", "license"]).to_pydict()
cat = dict(zip(t["id"], t["categories"])); lic = dict(zip(t["id"], t["license"]))
STRICT = re.compile(r"^(math\.|math-ph$|cs\.LO$|cs\.DM$)")
TARGET = re.compile(r"^(math\.|math-ph$|stat\.|cs\.LO$|cs\.DM$|cs\.CC$|cs\.FL$|cs\.SC$|cs\.IT$|cs\.GT$|cs\.NA$)")

# 1) metadane: liczba prac A3 (licencja domyślna albo brak, bez NC/ND), id do 2304 włącznie (zakres RedPajama) i całość
C = collections.Counter()
for i, c in cat.items():
    prim = (c or "").split()[0] if c else ""
    l = lic.get(i) or "None"
    if not ("nonexclusive" in l or l == "None"):
        continue
    new = re.match(r"^(\d{2})(\d{2})\.", i)
    le2304 = (not new) or (new.group(1) + new.group(2) <= "2304")
    for name, rx in [("scisle", STRICT), ("docelowe", TARGET)]:
        if rx.match(prim):
            C[name] += 1
            if le2304:
                C[name + "_do2304"] += 1
print("META", json.dumps(C), flush=True)

# 2) shard PP2 arxiv
rev = "901a9273a770e9d4138c5ddd91802f9c5c6cdc4b"
p = hf_hub_download("EleutherAI/proof-pile-2", "arxiv/train/arXiv_000.jsonl.zst", repo_type="dataset", revision=rev, local_dir="/tmp/karty/tdm/pp2")
h = sha(p)
D = collections.Counter(); keys = None; texts = []; first = None; smp = []
with open(p, "rb") as fh:
    r = io.TextIOWrapper(zstandard.ZstdDecompressor().stream_reader(fh), encoding="utf-8")
    for l in r:
        d = json.loads(l); m = d["meta"]
        if isinstance(m, str):
            m = json.loads(m)
        keys = sorted(m.keys()); first = first or m
        D["docs"] += 1
        i = m.get("arxiv_id") or m.get("id") or ""
        i = re.sub(r"v\d+$", "", str(i))
        c = cat.get(i)
        if c is None:
            D["bez_meta"] += 1
            continue
        prim = c.split()[0]
        l_ = lic.get(i) or "None"
        D["lic_" + ("domyslna" if ("nonexclusive" in l_ or l_ == "None") else ("ncnd" if re.search(r"-nc|-nd", l_) else "otwarta"))] += 1
        if STRICT.match(prim):
            D["scisle"] += 1
            if "nonexclusive" in l_ or l_ == "None":
                D["scisle_A3"] += 1
                texts.append(d["text"])
                if len(smp) < 3 and random.random() < 0.05:
                    smp.append(d["text"][:1200])
tk = ntok_batch(texts) if texts else [0]
print("PP2", json.dumps({"file": p, "sha256": h, "meta_keys": keys, "first_meta": first, "C": D,
                         "mean_tok_scisle_A3": sum(tk) / max(1, len(tk)), "B_per_tok": sum(len(x.encode()) for x in texts) / max(1, sum(tk))}), flush=True)
for s in smp:
    print("-----\n" + s)
