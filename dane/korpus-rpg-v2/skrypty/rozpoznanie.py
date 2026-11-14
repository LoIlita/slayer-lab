"""Rozpoznanie wejścia: rozkłady metadanych bez wczytywania tekstu."""
import collections
import json
import sys

import pyarrow.parquet as pq

P = sys.argv[1]
pf = pq.ParquetFile(P)
print("wiersze", pf.metadata.num_rows, "grupy", pf.metadata.num_row_groups)
print(pf.schema_arrow)
c = collections.Counter()
lic = collections.Counter()
rok = collections.Counter()
tag = collections.Counter()
rodz = collections.Counter()
przyklady = {}
kol = ["zrodlo", "id_zrodla", "rewizja_zrodla", "licencja", "atrybucja", "tokeny", "rodzina_dziela", "rok_wydania", "tag_tresci"]
for rg in range(pf.num_row_groups):
    t = pf.read_row_group(rg, columns=kol).to_pylist()
    for w in t:
        c[w["zrodlo"]] += 1
        lic[(w["zrodlo"], w["licencja"])] += 1
        rok[(w["zrodlo"], type(w["rok_wydania"]).__name__, w["rok_wydania"] is None)] += 1
        tag[str(w["tag_tresci"])[:40]] += 1
        rodz[(w["zrodlo"], w["rodzina_dziela"] is None)] += 1
        przyklady.setdefault(w["zrodlo"], [])
        if len(przyklady[w["zrodlo"]]) < 2:
            przyklady[w["zrodlo"]].append({k: (v[:900] if isinstance(v, str) else v) for k, v in w.items()})
print(dict(c))
print(lic.most_common(30))
print(rok.most_common(10))
print(tag.most_common(12))
print(rodz.most_common(10))
print(json.dumps(przyklady, ensure_ascii=False, indent=0, default=str)[:7000])
t = pf.read_row_group(0, columns=["text"]).column(0).to_pylist()
print("grupa0", len(t), sum(len(x) for x in t))
print("bajty_grupa_dane", pf.metadata.row_group(0).total_byte_size)
