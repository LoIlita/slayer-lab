"""Czytelny wydruk kandydatów PII do przeglądu. Argumenty: ner_kandydaci.json klasa [filtr_zrodla]."""
import json
import re
import sys

d = json.load(open(sys.argv[1], encoding="utf-8"))
k = sys.argv[2]
fz = sys.argv[3] if len(sys.argv) > 3 else None
SCP_FIK = re.compile(r"scp|scip|foundation|torchmail|prometheus|raisa|dadolaundry|dadomail|\.int$|\.drk$|\.internal$|\.iu$|\.wls$|\.mu\d")
for x in d[k]:
    if fz and x["zrodlo"] != fz:
        continue
    pr = x["przyklady"][0]
    if k == "email" and SCP_FIK.search(pr["tekst"].split("@")[-1].lower()) and x["zrodlo"] == "scp":
        continue
    print(x["zrodlo"][:3], x["id"], x["liczba"], "|", pr["tekst"], "|", pr["kontekst"][:170])
