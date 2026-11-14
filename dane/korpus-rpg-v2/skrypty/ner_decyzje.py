"""Decyzje PII po ręcznym przeglądzie kandydatów (reguła w preregistracja.json).
Usuwane: każdy wiersz Gutenberga z adresem e-mail (kontakt do współczesnych wolontariuszy i darczyńców), wiersze z kontaktem osoby prywatnej przy telefonie firmy,
wiersze SCP z e-mailem w realnej domenie dostawcy poczty oraz SCP-5561 (telefon istniejącej uczelni przy postaci).
Pozostają: domeny fikcyjne SCP, osoby historyczne i fikcyjne, adresy wydawców i postaci.
Argumenty: ner_kandydaci.json ner_liczby.json wyjscie.json."""
import collections
import json
import re
import sys

d = json.load(open(sys.argv[1], encoding="utf-8"))
li = json.load(open(sys.argv[2], encoding="utf-8"))
WY = sys.argv[3]
REAL = re.compile(r"(?:^|\.)(gmail|yahoo|hotmail|outlook|aol|icloud|proton(?:mail)?|gmx|comcast|verizon|att|live|msn|mail)\.(?:com|net|org|co\.uk)$")
TELEFON_OSOBA = {"1340/cz01", "448/cz01", "569/cz01", "691/cz01", "692/cz01"}
usun = {}
dom_scp = collections.Counter()
for x in d["email"]:
    if x["zrodlo"] == "gutenberg":
        usun[x["id"]] = {"id": x["id"], "zrodlo": x["zrodlo"], "klasa": "email", "powod": "adres e-mail wolontariusza lub darczyńcy w paratekście"}
    elif x["zrodlo"] == "scp":
        domeny = [p["tekst"].split("@")[-1].lower() for p in x["przyklady"]]
        dom_scp.update(domeny)
        if any(REAL.search(z) for z in domeny):
            usun[x["id"]] = {"id": x["id"], "zrodlo": "scp", "klasa": "email", "powod": "e-mail w realnej domenie poczty w treści SCP (ostrożnie, autor mógł użyć prawdziwego)"}
for x in d["telefon"]:
    if x["id"] in TELEFON_OSOBA:
        usun.setdefault(x["id"], {"id": x["id"], "zrodlo": x["zrodlo"], "klasa": "telefon", "powod": "kontakt osoby prywatnej przy telefonie firmy w paratekście"})
    if x["id"] == "SCP-5561":
        usun.setdefault(x["id"], {"id": x["id"], "zrodlo": "scp", "klasa": "telefon", "powod": "numer istniejącej uczelni przy postaci"})
wyj = {"usun": sorted(usun.values(), key=lambda z: z["id"]),
       "zostaw_klasy": {"email_scp_fikcyjne": "domeny fikcyjne SCP (m.in. scp.int, scip.net, foundation.scp) zostają", "telefon_inne": "numery firm bez osoby prywatnej, fikcyjne numery i fałszywe trafienia zostają", "osoba_data": "osoby historyczne i fikcyjne zostają", "adres": "adresy wydawców z XIX i XX w. oraz adresy z fikcji zostają; żadnego współczesnego adresu osoby prywatnej"},
       "liczby": {"kandydaci": li["sumy"], "per_zrodlo": li["per_zrodlo_dopasowan"], "wierszy_z_kandydatem": li["wierszy_z_kandydatem"], "usun": len(usun), "usun_per_klasa": dict(collections.Counter(v["klasa"] for v in usun.values())), "domeny_scp_w_przegladzie": dom_scp.most_common(60)}}
json.dump(wyj, open(WY, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(wyj["liczby"], ensure_ascii=False)[:1500])
