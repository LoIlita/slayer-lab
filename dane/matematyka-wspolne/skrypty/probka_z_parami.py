"""Próbka przeglądu z parami dla powodów dedup_<źródło> (para_wlasne.py) podmienionymi w probka_przegladu.jsonl.
Użycie: python probka_z_parami.py <probka_przegladu.jsonl> <wyjscie.jsonl> <pary.jsonl> [<pary.jsonl> ...]"""
import json
import sys

pary = {}
for p in sys.argv[3:]:
    for linia in open(p, encoding="utf-8"):
        o = json.loads(linia)
        pary[(o["nr"], o["powod"])] = o
with open(sys.argv[2], "w", encoding="utf-8") as f:
    for linia in open(sys.argv[1], encoding="utf-8"):
        o = json.loads(linia)
        f.write(json.dumps(pary.get((o["nr"], o["powod"]), o), ensure_ascii=False) + "\n")
print("par", len(pary))
