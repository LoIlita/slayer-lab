"""Skan zaciemnionych e-maili w wyeksportowanych częściach (po premask_emails): formy bez '@', których wzorce eksportu
nie maskowały. Liczy pliki i trafienia per wzorzec, wypisuje przykłady z kontekstem do ręcznego przeglądu.
Wzorce wąskie: domena musi kończyć się TLD z listy (albo 'dot <tld>'), żeby nie łapać kodu typu obj_at_index.
Użycie: python skan_zaciemnione.py <wyjscie.json> <plik.parquet> [<plik.parquet> ...]"""
import json
import re
import sys
from multiprocessing import Pool

import pyarrow.parquet as pq

TLD = r"(?:com|org|net|edu|gov|mil|info|io|biz|de|uk|fr|ch|it|ac|au|nz|ca|jp|nl|be|at|cz|pl|dk|se|fi|no|es|pt|us|cn|in|br|ru|il|kr|tw|sg|hk|ie|hu|gr|ro|sk|si|lt|lv|ee|mx|ar|cl|za|tr|ir)"
SEPD = r"(?:\.|_dot_|\(dot\)|\[dot\]|\{dot\}|<dot>| dot | DOT )"
WZORCE = {
    "_at_": re.compile(r"[A-Za-z0-9.+-]+_at_[A-Za-z0-9-]+(?:" + SEPD + r"[A-Za-z0-9-]+)*" + SEPD + TLD + r"\b"),
    "{at}/<at>": re.compile(r"[A-Za-z0-9._%+-]+ ?[\{<] ?(?:at|AT) ?[\}>] ?[A-Za-z0-9-]+(?:" + SEPD + r"[A-Za-z0-9-]+)*" + SEPD + TLD + r"\b"),
    "at ... dot": re.compile(r"[A-Za-z0-9._%+-]+ (?:at|AT) [A-Za-z0-9-]+(?: (?:dot|DOT) [A-Za-z0-9-]+)* (?:dot|DOT) " + TLD + r"\b"),
    "AT domena.tld": re.compile(r"[A-Za-z0-9._%+-]+ AT [A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\." + TLD + r"\b"),
    "at domena.tld (informacyjnie)": re.compile(r"[A-Za-z0-9._%+-]*[._][A-Za-z0-9._%+-]+ at [A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\." + TLD + r"\b(?![/\w.])"),
}


def job(a):
    p, g = a
    t = pq.ParquetFile(p).read_row_group(g, columns=["id", "text"]).to_pylist()
    wyn = {k: [0, 0, []] for k in WZORCE}
    for r in t:
        for k, rx in WZORCE.items():
            h = list(rx.finditer(r["text"]))
            if h:
                wyn[k][0] += 1
                wyn[k][1] += len(h)
                if len(wyn[k][2]) < 3:
                    m = h[0]
                    wyn[k][2].append({"id": r["id"], "trafienie": m.group(0),
                                      "kontekst": r["text"][max(0, m.start() - 80):m.end() + 40]})
    return p, wyn


if __name__ == "__main__":
    OUT, pliki = sys.argv[1], sys.argv[2:]
    zad = [(p, g) for p in pliki for g in range(pq.ParquetFile(p).num_row_groups)]
    suma = {}
    with Pool(4) as pool:
        for p, w in pool.imap_unordered(job, zad):
            s = suma.setdefault(p.split("/")[-1], {k: [0, 0, []] for k in WZORCE})
            for k, v in w.items():
                s[k][0] += v[0]
                s[k][1] += v[1]
                s[k][2] = (s[k][2] + v[2])[:60]
    json.dump({p: {k: {"pliki": v[0], "trafienia": v[1], "przyklady": v[2]} for k, v in s.items()} for p, s in suma.items()},
              open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for p, s in sorted(suma.items()):
        print(p, {k: v[0] for k, v in s.items()}, flush=True)
