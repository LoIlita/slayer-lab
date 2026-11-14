"""Weryfikacja gotowych shardów: schemat, zero SA w default, zero rodzin w obu splitach, reguła sha1, zero śladu znaku PG, unikalne document_id,
liczby wierszy i tokenów. Czyta grupami, kod wyjścia != 0 przy błędzie. Argumenty: katalog_korpusu preregistracja.json usuniecia.json wyjscie.json."""
import hashlib
import json
import multiprocessing as mp
import os
import re
import sys

import pyarrow.parquet as pq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rdzen import MOJIBAKE  # noqa: E402

KOR, PREREG, USUN, WY = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
OCZ = ["document_id", "source_id", "text", "register", "license", "license_url", "is_share_alike", "author", "provenance", "work_family", "first_pub_year", "content_tag", "n_tokens"]
RX_PG = re.compile(json.load(open(PREREG, encoding="utf-8"))["znak_pg"]["regex"])


def grupa(a):
    p, g, cfg, sp = a
    t = pq.ParquetFile(p).read_row_group(g).to_pylist()
    ids, rodz, zle = [], [], []
    w, tok, pg, sa, moj = 0, 0, 0, 0, 0
    for x in t:
        w += 1
        if MOJIBAKE.search(x["text"]):
            moj += 1
        tok += x["n_tokens"]
        ids.append(x["document_id"])
        rodz.append(x["work_family"])
        if x["is_share_alike"]:
            sa += 1
        if RX_PG.search(x["text"]):
            pg += 1
        if int(hashlib.sha1(x["work_family"].encode("utf-8")).hexdigest(), 16) % 200 == 0 and sp != "validation":
            zle.append(x["document_id"])
        if int(hashlib.sha1(x["work_family"].encode("utf-8")).hexdigest(), 16) % 200 != 0 and sp == "validation":
            zle.append(x["document_id"])
    return cfg, sp, w, tok, sa, pg, ids, rodz, zle, moj


def main():
    wsad, struktura = [], {}
    bl = []
    for cfg in ("default", "cc-by-sa"):
        k = f"{KOR}/data/{cfg}"
        for p in sorted(os.listdir(k)):
            if not p.endswith(".parquet"):
                bl.append("obcy plik " + p)
                continue
            pf = pq.ParquetFile(f"{k}/{p}")
            nz = pf.schema_arrow.names
            if nz != OCZ:
                bl.append("schemat " + p + str(nz))
            sp = "validation" if p.startswith("validation-") else "train"
            for g in range(pf.num_row_groups):
                wsad.append((f"{k}/{p}", g, cfg, sp))
    wyn = {}
    wszyst_id = set()
    rodz_split = {}
    powt = 0
    z = 0
    with mp.get_context("fork").Pool(6) as p:
        for cfg, sp, w, tok, sa, pg, ids, rodz, zle, moj in p.imap_unordered(grupa, wsad):
            k = f"{cfg}/{sp}"
            d = wyn.setdefault(k, {"wiersze": 0, "tokeny": 0, "sa": 0, "pg": 0, "mojibake": 0, "rodziny": set()})
            d["mojibake"] += moj
            d["wiersze"] += w
            d["tokeny"] += tok
            d["sa"] += sa
            d["pg"] += pg
            d["rodziny"].update(rodz)
            z += len(zle)
            for i in ids:
                if i in wszyst_id:
                    powt += 1
                wszyst_id.add(i)
    # rodziny w obu splitach
    for cfg in ("default", "cc-by-sa"):
        a = wyn.get(f"{cfg}/train", {"rodziny": set()})["rodziny"]
        b = wyn.get(f"{cfg}/validation", {"rodziny": set()})["rodziny"]
        wsp = a & b
        if wsp:
            bl.append(f"{cfg}: rodziny w obu splitach: {len(wsp)}")
    for k, v in wyn.items():
        if k.startswith("default") and v["sa"]:
            bl.append(f"{k}: wiersze SA {v['sa']}")
        if v["pg"]:
            bl.append(f"{k}: ślad znaku PG {v['pg']}")
        if v["mojibake"]:
            bl.append(f"{k}: wiersze z popsutymi znakami {v['mojibake']}")
        v["rodziny"] = len(v["rodziny"])
    if powt:
        bl.append(f"powtórzone document_id: {powt}")
    if z:
        bl.append(f"reguła sha1 złamana: {z}")
    us = json.load(open(USUN, encoding="utf-8"))
    razem = sum(v["wiersze"] for v in wyn.values())
    wej = us["liczby"]["wszystkich_wierszy"]
    n_us = len(us["wiersze"])
    if razem != wej - n_us:
        bl.append(f"bilans wierszy: {razem} != {wej} - {n_us}")
    out = {"splity": wyn, "razem_wierszy": razem, "razem_tokeny": sum(v["tokeny"] for v in wyn.values()), "wejscie": wej, "usuniete": n_us, "bledy": bl, "status": "PASS" if not bl else "FAIL"}
    json.dump(out, open(WY, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(out, ensure_ascii=False)[:2000])
    sys.exit(0 if not bl else 1)


if __name__ == "__main__":
    main()
