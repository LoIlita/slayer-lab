"""Sprawdza kontrakt potoku dla wyniki/probka_pliki.json i parquetów puli 'formalna'.

Kolumny wymagane i typy, row groups po 5000 (ostatnia <= 5000), unikalne id (w całym źródle), sha256 i rozmiar
pliku, liczby wierszy i tokenów v6 (przeliczone od nowa tokenizerem) zgodne z probka_pliki.json, licencja w
każdym wierszu, url z rewizją, brak skompresowanych dowodów w set.mm. Kod wyjścia 0 = PASS.
"""
import hashlib
import json
import os
import re
import sys

import pyarrow as pa
import pyarrow.parquet as pq
from tokenizers import Tokenizer

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOK_P = os.path.join(D, "..", "dclm-en", "robocze", "pobrania", "tokenizer_v6", "tokenizer.json")
PP = json.load(open(f"{D}/wyniki/probka_pliki.json", encoding="utf-8"))
P = json.load(open(f"{D}/skrypty/preregistracja.json", encoding="utf-8"))
tok = Tokenizer.from_file(TOK_P)
bledy = []
WYM = {"text": pa.string(), "url": pa.string(), "id": pa.string(), "license": pa.string(), "created": pa.string(),
       "repo": pa.string(), "path": pa.string()}
ids, W, T, wynik = set(), 0, 0, {}
for p in PP["pliki"]:
    f = p["lokalnie"]
    h = hashlib.sha256(open(f, "rb").read()).hexdigest()
    if h != p["sha256"] or os.path.getsize(f) != p["rozmiar"]:
        bledy.append(f"{p['plik']}: sha256/rozmiar")
    pf = pq.ParquetFile(f)
    sch = pf.schema_arrow
    for k, t in WYM.items():
        if sch.field(k).type != t if k in sch.names else True:
            bledy.append(f"{p['plik']}: kolumna {k}")
    md = pf.metadata
    rg = [md.row_group(i).num_rows for i in range(md.num_row_groups)]
    if any(n != 5000 for n in rg[:-1]) or (rg and rg[-1] > 5000):
        bledy.append(f"{p['plik']}: row groups {rg}")
    rew = P.get("aneks_2026_11_26c", {}).get("rewizje", {}).get(p["plik"]) or P["zrodlo"]["biblioteki"][p["plik"]]["rewizja"]
    if p["rewizja"] != rew:
        bledy.append(f"{p['plik']}: rewizja {p['rewizja']} != {rew}")
    n = t_sum = 0
    for i in range(md.num_row_groups):
        tb = pf.read_row_group(i, columns=["text", "url", "id", "license", "created"])
        tx = tb.column("text").to_pylist()
        enc = tok.encode_batch(tx, add_special_tokens=False)
        t_sum += sum(len(e.ids) + 1 for e in enc)
        for x, u, d, l, c in zip(tx, *(tb.column(k).to_pylist() for k in ("url", "id", "license", "created"))):
            if d in ids:
                bledy.append(f"duplikat id {d}")
            ids.add(d)
            if not x or not l or not c or f"/blob/{rew}/" not in u:
                bledy.append(f"{d}: pusty text/license/created albo url bez rewizji")
            if p["plik"] == "setmm" and re.search(r"\$=\s+(?!\?\s+\$\.)", x):
                bledy.append(f"{d}: dowód nie zastąpiony")
        n += tb.num_rows
    if n != p["wiersze"] or t_sum != p["tokeny_v6"]:
        bledy.append(f"{p['plik']}: wiersze {n} vs {p['wiersze']}, tokeny {t_sum} vs {p['tokeny_v6']}")
    wynik[p["plik"]] = {"wiersze": n, "tokeny_v6": t_sum, "row_groups": len(rg)}
    W += n
    T += t_sum
if W != PP["wiersze"] or T != PP["tokeny_v6"]:
    bledy.append(f"suma: wiersze {W} vs {PP['wiersze']}, tokeny {T} vs {PP['tokeny_v6']}")
out = {"wynik": "PASS" if not bledy else "FAIL", "wiersze": W, "tokeny_v6": T, "unikalne_id": len(ids),
       "pliki": wynik, "bledy": bledy[:50]}
json.dump(out, open(f"{D}/wyniki/kontrakt.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False))
sys.exit(0 if not bledy else 1)
