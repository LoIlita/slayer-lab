"""Agreguje wyniki NER: liczniki i listy kandydatów PII do ręcznego przeglądu. Argumenty: katalog_ner wyjscie_kandydaci.json wyjscie_liczby.json."""
import collections
import json
import os
import re
import sys

N, WY, LI = sys.argv[1], sys.argv[2], sys.argv[3]
kl = ["email", "telefon", "adres", "osoba_data"]
sum_ = collections.Counter()
zb = {k: [] for k in kl}
for p in sorted(os.listdir(N)):
    if p.endswith(".json"):
        d = json.load(open(f"{N}/{p}", encoding="utf-8"))
        sum_["okna"] += d["okna"]
        sum_["znaki"] += d["znaki"]
        sum_["person"] += d["person"]
        sum_["grupy"] += 1
        for k in kl:
            zb[k] += d[k]
            sum_[k] += len(d[k])


def klucz(x):
    return (x[1], x[0])


# grupowanie per wiersz i klasę, duplikaty kontekstów z tego samego wiersza zwinięte
wyj = {}
for k in kl:
    per = collections.defaultdict(list)
    for x in zb[k]:
        per[(x[0], x[1])].append({"tekst": x[2], "kontekst": x[3]})
    wyj[k] = [{"id": i, "zrodlo": z, "liczba": len(v), "przyklady": v[:3]} for (i, z), v in sorted(per.items())]
json.dump(wyj, open(WY, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
por = {k: dict(collections.Counter(x[1] for x in zb[k])) for k in kl}
wierszy = {k: len(wyj[k]) for k in kl}
wynik = {"sumy": dict(sum_), "per_zrodlo_dopasowan": por, "wierszy_z_kandydatem": wierszy, "email_domeny": collections.Counter(re.sub(r".*@", "", x[2]).lower() for x in zb["email"]).most_common(40)}
json.dump(wynik, open(LI, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(wynik, ensure_ascii=False)[:3000])
