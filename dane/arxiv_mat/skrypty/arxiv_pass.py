"""arXiv A1/A2: łączenie z metadanymi, wybór kategorii, PII, artefakty, tokeny; zapis id A1 do dedupu."""
import sys, os, re, json, random, collections
sys.path.insert(0, "/tmp/karty")
import pyarrow as pa, pyarrow.parquet as pq
from huggingface_hub import hf_hub_download, HfApi, HfFileSystem
from wsp import it, ntok_batch, sha, EMAIL, MOJI

random.seed(11)
META = "/tmp/karty/arxiv/meta.parquet"
if not os.path.exists(META):
    fs = HfFileSystem()
    base = "datasets/librarian-bots/arxiv-metadata-snapshot@c428226b689a0e17db2cd55265133b9eca15d97f/data/"
    tabs = [pq.read_table(fs.open(base + f"train-{i:05d}-of-00011.parquet", block_size=8 << 20),
                          columns=["id", "categories", "license", "title"]) for i in range(11)]
    pq.write_table(pa.concat_tables(tabs), META)
t = pq.read_table(META).to_pydict()
cat = dict(zip(t["id"], t["categories"])); lic = dict(zip(t["id"], t["license"])); title = dict(zip(t["id"], t["title"]))
print("meta", len(cat), flush=True)
TARGET = re.compile(r"^(math\.|math-ph$|stat\.|cs\.LO$|cs\.DM$|cs\.CC$|cs\.FL$|cs\.SC$|cs\.IT$|cs\.GT$|cs\.NA$)")
OPENMAP = {"by/4.0": "Creative Commons - Attribution - https://creativecommons.org/licenses/by/4.0/"}


def primary(c):
    return (c or "").split()[0] if c else ""


REV = "963fe980c55b353980653f1a27c1dc0c8a2d7058"
files = sorted(f for f in HfApi().list_repo_files("common-pile/arxiv_papers", repo_type="dataset", revision=REV) if f.endswith(".gz"))
C = collections.Counter(); B = collections.Counter(); L = collections.Counter(); idfmt = collections.Counter(); keys = collections.Counter()
licmatch = collections.Counter(); shas = {}
a1 = []; samp = []; toksamp = []
ART = {"stopka_111": re.compile(r"[a-z]1{3,}[A-Z ]"), "tylda_pusta": re.compile(r"~\{\}"), "pusty_wzor": re.compile(r"\$\s*\$"),
       "znaczniki_html": re.compile(r"</?(sup|sub|span|div)\b"), "brak_ref": re.compile(r"\[\?\]|\?\?")}
for f in files:
    p = hf_hub_download("common-pile/arxiv_papers", f, repo_type="dataset", revision=REV, local_dir="/tmp/karty/arxiv/dl")
    shas[f] = sha(p)
    for d in it(p):
        C["docs"] += 1
        i = d["id"]; m = d.get("metadata", {})
        for kk in m:
            keys[kk] += 1
        idfmt["nowy" if re.match(r"^\d{4}\.\d{4,5}$", i) else ("stary" if "/" in i else "inny")] += 1
        if m.get("url") == f"https://arxiv.org/abs/{i}":
            C["url_zgodny"] += 1
        c = cat.get(i)
        if c is None:
            C["bez_meta"] += 1
            continue
        C["polaczone"] += 1
        if not TARGET.match(primary(c)):
            continue
        t_ = d["text"]; b = len(t_.encode())
        C["a1"] += 1; B["a1"] += b
        cl = m.get("license") or ""; ml = lic.get(i) or "None"
        L[cl] += 1
        lk = re.search(r"(by-sa/4\.0|by/4\.0|by/3\.0|zero/1\.0|publicdomain)", ml)
        ck = re.search(r"(by-sa/4\.0|by/4\.0|by/3\.0|zero/1\.0|Public Domain)", cl)
        licmatch["zgodna" if lk and ck and (lk.group(1) == ck.group(1) or (lk.group(1) == "publicdomain" and ck.group(1) == "Public Domain")) else f"meta={ml[-25:]}|cp={cl[-25:]}"] += 1
        if EMAIL.search(t_):
            C["email"] += 1
        if MOJI.search(t_):
            C["mojibake"] += 1
        for k_, rx in ART.items():
            if rx.search(t_):
                C["art_" + k_] += 1
        if b < 5000:
            C["krotkie_lt5kB"] += 1
        a1.append((i, title.get(i) or "", d.get("created") or "", primary(c)))
        if random.random() < 0.02:
            toksamp.append(t_)
        if random.random() < 0.0015:
            samp.append({"id": i, "cat": c, "license": cl, "created": d.get("created"), "authors": m.get("authors"), "text": t_[:4000]})
    os.remove(p)
    print(f, dict(C), flush=True)
tk = ntok_batch(toksamp)
bpt = sum(len(x.encode()) for x in toksamp) / sum(tk)
pq.write_table(pa.table({"id": [x[0] for x in a1], "title": [x[1] for x in a1], "created": [x[2] for x in a1], "cat": [x[3] for x in a1]}), "/tmp/karty/arxiv/a1_ids.parquet")
with open("/tmp/karty/arxiv/sample_a1.jsonl", "w") as fo:
    for x in samp:
        fo.write(json.dumps(x, ensure_ascii=False) + "\n")
res = {"rev": REV, "files": len(files), "sha256": shas, "C": C, "bytes_a1": B["a1"], "B_per_tok": bpt, "tok_sample_docs": len(toksamp),
       "tok_a1_est": B["a1"] / bpt, "id_format": idfmt, "meta_keys": keys, "cp_license": L.most_common(), "lic_vs_meta": licmatch.most_common(10)}
print("WYNIK_A1", json.dumps(res), flush=True)

# A2: abstrakty prac docelowych spoza A1
a1set = set(x[0] for x in a1)
REV2 = "828e35d1000f94579da8850f5f640c138279bdb5"
f2 = sorted(f for f in HfApi().list_repo_files("common-pile/arxiv_abstracts", repo_type="dataset", revision=REV2) if f.endswith(".gz"))
C2 = collections.Counter(); B2 = 0; ts2 = []; shas2 = {}; L2 = collections.Counter(); smp2 = []
for f in f2:
    p = hf_hub_download("common-pile/arxiv_abstracts", f, repo_type="dataset", revision=REV2, local_dir="/tmp/karty/arxiv/dl")
    shas2[f] = sha(p)
    for d in it(p):
        C2["docs"] += 1
        i = d["id"]; c = cat.get(i)
        if c is None:
            C2["bez_meta"] += 1
            continue
        if not TARGET.match(primary(c)):
            continue
        C2["docelowe"] += 1
        if i in a1set:
            C2["w_A1"] += 1
            continue
        C2["a2"] += 1; B2 += len(d["text"].encode()); L2[d["metadata"].get("license", "")[:40]] += 1
        if EMAIL.search(d["text"]):
            C2["email"] += 1
        if random.random() < 0.05:
            ts2.append(d["text"])
        if random.random() < 0.00005:
            smp2.append({"id": i, "cat": c, "meta": d["metadata"], "text": d["text"]})
    os.remove(p)
    print(f, dict(C2), flush=True)
tk2 = ntok_batch(ts2)
with open("/tmp/karty/arxiv/sample_a2.jsonl", "w") as fo:
    for x in smp2:
        fo.write(json.dumps(x, ensure_ascii=False) + "\n")
print("WYNIK_A2", json.dumps({"rev": REV2, "sha256": shas2, "C": C2, "bytes": B2, "B_per_tok": B2 and sum(len(x.encode()) for x in ts2) / sum(tk2),
                              "tok_est": B2 / (sum(len(x.encode()) for x in ts2) / sum(tk2)), "mean_tok": sum(tk2) / len(tk2), "lic": L2.most_common()}), flush=True)
print("KONIEC")
