"""Kontrola po maskowaniu: szerokie wyszukiwanie śladów e-maili w tekście PO mat_wybor.premask_emails (dowolne „at”, „-at-”,
„(at)”, „@”, „dot” między tokenami przypominającymi adres, z końcówką domeny). Dla źródeł z maskowaniem e-maili przy eksporcie.
Użycie: python resztki_email.py <probka_pliki.json> [bare_at=1] [maks_przykladow=60]
Wypisuje liczbę zamaskowanych, liczbę dokumentów z resztkami i przykłady resztek (do przeglądu: część to fałszywe trafienia)."""
import collections
import json
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "eksport", "src"))
sys.modules["pii"] = type(sys)("pii")  # mat_wybor importuje pii repo zgłoszeń tylko dla no_masking
import mat_wybor as m  # noqa: E402
import pyarrow.parquet as pq  # noqa: E402

PROBKA = sys.argv[1]
BARE = (sys.argv[2] if len(sys.argv) > 2 else "1") == "1"
MAKS = int(sys.argv[3]) if len(sys.argv) > 3 else 60
SEP = r"(?:@|\s?[\(\[\{<]\s?(?:at|AT)\s?[\)\]\}>]\s?|-at-|_at_|\s(?:at|AT)\s)"
DOT = r"(?:\.|\s(?:dot|DOT)\s|\s?[\(\[\{<]\s?(?:dot|DOT)\s?[\)\]\}>]\s?)"
BROAD = re.compile(r"[A-Za-z0-9._%+-]{2,}" + SEP + r"[A-Za-z0-9-]{2,}(?:" + DOT + r"[A-Za-z0-9-]+)*" + DOT
                   + r"(?:com|org|net|edu|gov|info|io|de|uk|fr|ch|it|ac|au|nz|ca|jp|nl|be|at|cz|pl|dk|se|fi|no|es|pt|us|cn|in|br|ru|il|kr|tw|sg|hk|ie)\b")
dok, ex, n = collections.Counter(), [], 0
for x in json.load(open(PROBKA))["pliki"]:
    for t in pq.read_table(x["lokalnie"], columns=["text"]).column(0).to_pylist():
        n += 1
        hits = [h.group(0) for h in BROAD.finditer(m.premask_emails(t or "", bare_at=BARE))]
        if hits:
            dok[x["plik"]] += 1
            ex.extend(hits[:2] if len(ex) < MAKS else [])
print(json.dumps({"dokumentow": n, "zamaskowano": m.MASKED["pii"], "dok_z_resztkami": sum(dok.values()), "per_plik": dok,
                  "przyklady": ex[:MAKS]}, ensure_ascii=False, indent=1))
