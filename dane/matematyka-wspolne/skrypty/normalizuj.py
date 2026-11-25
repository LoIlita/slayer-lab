"""Pobiera pliki źródła z przypiętej rewizji w kolejności losowej (seed z preregistracji), zapisuje sha256 oryginału i lokalną
kopię parquet z grupami po 5000 wierszy (kolumny text, url, id + pola pochodzenia), aż suma tokenów v6 przekroczy cel puli.
Tekst niezmieniony. Format wyjścia jak pobierz.py DCLM-EN, więc przebieg.py DCLM-EN czyta go bez zmian.
Źródła:
  finemath4  HuggingFaceTB/finemath, finemath-4plus/*.parquet
  cranemath  allenai/dolma3_dolmino_mix-100B-1125, data/ingredient1-cranemath/*.jsonl.zst; obok kopia 'oryg' z text=original_text
             (13-gramy testów liczone też na tekście przed przepisaniem)
  stackedu   common-pile/stackv2_edu_filtered, *.json.gz; tylko metadata.language == 'Python'
  infiwebmath4  HuggingFaceTB/finemath, infiwebmath-4plus/*.parquet; id = WARC-Record-ID z metadata.WARC_HEADER
  finemath3  HuggingFaceTB/finemath, finemath-3plus/*.parquet; tylko int_score == 3
Argumenty: zrodlo katalog_pobran probka_pliki.json cel_tokenow_v6 tokenizer.json seed"""
import gzip
import hashlib
import io
import json
import os
import sys

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
import zstandard
from huggingface_hub import HfApi, hf_hub_download
from tokenizers import Tokenizer

ZRODLA = {
    "finemath4": ("HuggingFaceTB/finemath", "e92b25a616738fe95dc186b64dfb19f9c8525594", "finemath-4plus/", ".parquet"),
    "cranemath": ("allenai/dolma3_dolmino_mix-100B-1125", "f23aa129fda8335ba9760057bcc1f0c02f3d068b", "data/ingredient1-cranemath/", ".jsonl.zst"),
    "stackedu": ("common-pile/stackv2_edu_filtered", "c354dbe88469a1153e97c6a63ac50591849654de", "stack-edu-", ".json.gz"),
    "infiwebmath4": ("HuggingFaceTB/finemath", "e92b25a616738fe95dc186b64dfb19f9c8525594", "infiwebmath-4plus/", ".parquet"),
    "finemath3": ("HuggingFaceTB/finemath", "e92b25a616738fe95dc186b64dfb19f9c8525594", "finemath-3plus/", ".parquet"),
}
ZR, CEL, WYN, DOCEL, TOK, SEED = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5], int(sys.argv[6])
REPO, REW, PREF, SUF = ZRODLA[ZR]
RG = 5000
TK = Tokenizer.from_file(TOK)


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 24), b""):
            h.update(b)
    return h.hexdigest()


def tokeny(teksty):
    return sum(len(e.ids) + 1 for e in TK.encode_batch(teksty, add_special_tokens=False))


def wiersze(p):
    """Wiersze pliku jako słowniki o polach wspólnych: text, url, id + pochodzenie; drugi element: tekst przed przepisaniem."""
    if ZR in ("finemath4", "finemath3"):
        kol = ["text", "url", "crawl", "warc_filename", "warc_record_offset", "warc_record_length", "snapshot_type"]
        t = pq.read_table(p, columns=kol + ["int_score"]) if ZR == "finemath3" else pq.read_table(p, columns=kol)
        for r in t.to_pylist():
            if ZR == "finemath3" and r.pop("int_score") != 3:  # oceny 4-5 to FineMath-4+ (karta dane/finemath3)
                continue
            r["id"] = f"{r['warc_filename']}:{r['warc_record_offset']}"
            yield r, None
    elif ZR == "infiwebmath4":
        t = pq.read_table(p, columns=["text", "url", "metadata"])
        for r in t.to_pylist():
            w = json.loads(json.loads(r.pop("metadata"))["WARC_HEADER"])
            r["id"], r["warc_record_id"], r["warc_date"] = w["WARC-Record-ID"], w["WARC-Record-ID"], w.get("WARC-Date")
            yield r, None
    elif ZR == "cranemath":
        with open(p, "rb") as f:
            for linia in io.TextIOWrapper(zstandard.ZstdDecompressor().stream_reader(f), encoding="utf-8"):
                o = json.loads(linia)
                m = o["metadata"] if isinstance(o["metadata"], dict) else _meta_python(o["metadata"])
                yield ({"text": o["text"], "url": m.get("url") or "", "id": o["id"], "crawl": m.get("crawl"),
                        "warc_filename": m.get("warc_filename"), "warc_record_offset": m.get("warc_record_offset"),
                        "warc_record_length": m.get("warc_record_length")}, m.get("original_text") or "")
    else:
        with gzip.open(p, "rt", encoding="utf-8") as f:
            for linia in f:
                o = json.loads(linia)
                m = o["metadata"]
                if m.get("language") != "Python":
                    continue
                yield ({"text": o["text"], "url": m.get("url") or "", "id": o["id"], "repo_name": m.get("repo_name"),
                        "path": m.get("path"), "revision_id": m.get("revision_id"), "license": m.get("license"),
                        "license_type": m.get("license_type"), "detected_licenses": json.dumps(m.get("detected_licenses")),
                        "gha_license_id": m.get("gha_license_id"), "int_score": o.get("int_score"), "created": o.get("created")}, None)


def _meta_python(s):
    """metadata CraneMath to repr słownika Pythona (pojedyncze cudzysłowy), nie JSON."""
    import ast
    return ast.literal_eval(s)


def zapisz(rows, lok):
    pq.write_table(pa.Table.from_pylist(rows), lok, row_group_size=RG)


api = HfApi()
wsz = sorted(f for f in api.list_repo_files(REPO, repo_type="dataset", revision=REW) if f.startswith(PREF) and f.endswith(SUF))
if ZR == "stackedu":  # Python leży w plikach 0073-0084 (karta źródła, pole 3); 0084 zaczyna się Pythonem, potem Ruby
    wsz = [f for f in wsz if 73 <= int(f[len(PREF):-len(SUF)]) <= 84]
kolej = np.random.default_rng(SEED).permutation(len(wsz)).tolist()
os.makedirs(CEL, exist_ok=True)
gotowe = {}
if os.path.exists(WYN):
    gotowe = {x["plik"]: x for x in json.load(open(WYN, encoding="utf-8"))["pliki"]}
out, suma_tok, suma_w = [], 0, 0
for i in kolej:
    f = wsz[i]
    if f in gotowe:
        x = gotowe[f]
    else:
        p = hf_hub_download(REPO, f, repo_type="dataset", revision=REW, local_dir=CEL)
        lok = os.path.join(CEL, "lok", f.replace("/", "__").replace(SUF, ".rg5000.parquet"))
        os.makedirs(os.path.dirname(lok), exist_ok=True)
        rows, oryg = [], []
        for r, o in wiersze(p):
            rows.append(r)
            oryg.append(o)
        tok = 0
        for a in range(0, len(rows), RG):
            tok += tokeny([r["text"] for r in rows[a:a + RG]])
        zapisz(rows, lok)
        x = {"plik": f, "rozmiar": os.path.getsize(p), "sha256": sha(p), "wiersze": len(rows), "tokeny_v6": tok, "lokalnie": lok}
        if ZR == "cranemath":
            lok_o = lok.replace(".rg5000.parquet", ".oryg.rg5000.parquet")
            zapisz([{"text": o, "url": r["url"], "id": r["id"]} for r, o in zip(rows, oryg)], lok_o)
            x["lokalnie_oryg"] = lok_o
        os.remove(p)  # surowy plik niepotrzebny po konwersji (sha256 zapisana); przy 20 mld tokenów dysk się nie zmieści
    out.append(x)
    suma_tok += x["tokeny_v6"]
    suma_w += x["wiersze"]
    json.dump({"repo": REPO, "rewizja": REW, "plikow_w_repo": len(wsz), "seed": SEED, "wiersze": suma_w, "tokeny_v6": suma_tok,
               "cel_tokenow_v6": DOCEL, "pliki": out}, open(WYN, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f, x["wiersze"], x["tokeny_v6"], suma_tok, flush=True)
    if suma_tok >= DOCEL:
        break
print("KONIEC", suma_w, suma_tok, flush=True)
