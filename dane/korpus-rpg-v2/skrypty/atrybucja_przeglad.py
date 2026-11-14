"""Przegląd wartości pól atrybucji: zamknięte zbiory wartości tekstowych po polsku do przetłumaczenia."""
import collections
import json
import sys

import pyarrow.parquet as pq

pf = pq.ParquetFile(sys.argv[1])
klucze = collections.defaultdict(collections.Counter)
wart = collections.defaultdict(collections.Counter)
rpg = []
reg = collections.Counter()
for g in range(pf.num_row_groups):
    t = pf.read_row_group(g, columns=["zrodlo", "id_zrodla", "atrybucja"]).to_pylist()
    for w in t:
        a = json.loads(w["atrybucja"])
        for k, v in a.items():
            klucze[w["zrodlo"]][k] += 1
            if k in ("zmiany", "uwaga", "pochodzenie_formuly", "prawa_rdf", "zakaz", "kategoria", "tagi_licencji"):
                wart[(w["zrodlo"], k)][json.dumps(v, ensure_ascii=False)] += 1
        if w["zrodlo"] != "gutenberg":
            reg[(w["zrodlo"], a.get("kategoria"))] += 1
        if w["zrodlo"].startswith("rpg"):
            rpg.append((w["id_zrodla"], a.get("autor"), a.get("formula")))
print({k: dict(v) for k, v in klucze.items()})
for k, v in wart.items():
    print(k, v.most_common(8))
print(reg)
seen = set()
for i, a, f in rpg:
    kl = i.split("/")[0]
    if kl not in seen:
        seen.add(kl)
        print(i, "|", a, "|", (f or "")[:200])
print(len(rpg))
