"""Skan zaciemnionych e-maili w wyeksportowanych częściach (po premask_emails): formy bez '@', których wzorce eksportu
nie maskowały. Liczy pliki i trafienia per wzorzec, wypisuje przykłady z kontekstem do ręcznego przeglądu.
Wzorce wąskie: domena musi kończyć się TLD z listy (albo 'dot <tld>'), żeby nie łapać kodu typu obj_at_index.
Użycie: [PROCESY=4] python skan_zaciemnione.py <wyjscie.json> <plik.parquet> [<plik.parquet> ...]"""
import json
import os
import re
import sys
from multiprocessing import Pool

import pyarrow.parquet as pq

TLD = r"(?:com|org|net|edu|gov|mil|info|io|biz|de|uk|fr|ch|it|ac|au|nz|ca|jp|nl|be|at|cz|pl|dk|se|fi|no|es|pt|us|cn|in|br|ru|il|kr|tw|sg|hk|ie|hu|gr|ro|sk|si|lt|lv|ee|mx|ar|cl|za|tr|ir)"
SEPD = r"(?:\.|_dot_|\(dot\)|\[dot\]|\{dot\}|<dot>| dot | DOT )"
MAIL = r"(?:gmail|googlemail|yahoo|ymail|hotmail|outlook|live|msn|icloud|aol|gmx|protonmail|yandex|mail|qq|163|126|sina|web|t-online|orange|free|libero|naver|hanmail|rediffmail|zoho|comcast|verizon|att|earthlink|btinternet|cox|sbcglobal)"
WZORCE = {
    "_at_": re.compile(r"[A-Za-z0-9.+-]+_at_[A-Za-z0-9-]+(?:" + SEPD + r"[A-Za-z0-9-]+)*" + SEPD + TLD + r"\b"),
    "{at}/<at>": re.compile(r"[A-Za-z0-9._%+-]+ ?[\{<] ?(?:at|AT) ?[\}>] ?[A-Za-z0-9-]+(?:" + SEPD + r"[A-Za-z0-9-]+)*" + SEPD + TLD + r"\b"),
    "at ... dot": re.compile(r"[A-Za-z0-9._%+-]+ (?:at|AT) [A-Za-z0-9-]+(?: (?:dot|DOT) [A-Za-z0-9-]+)* (?:dot|DOT) " + TLD + r"\b"),
    "AT domena.tld": re.compile(r"[A-Za-z0-9._%+-]+ AT [A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\." + TLD + r"\b"),
    "at domena.tld (informacyjnie)": re.compile(r"[A-Za-z0-9._%+-]*[._][A-Za-z0-9._%+-]+ at [A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\." + TLD + r"\b(?![/\w.])"),
    # dodane 27.11 przy skanie tekstu stron (FineMath i pozostałe źródła): formy bez '.'/'_' w nazwie, których wzorce wyżej
    # nie widzą — tylko do pomiaru i przeglądu
    "login at poczta (informacyjnie)": re.compile(r"(?<![\w.@-])[A-Za-z0-9_%+-]+ (?:at|AT) " + MAIL + r"\.(?:com|net|org|de|fr|it|es|ru|cn|co\.uk|co\.in|ca|com\.au|nl|pl)\b(?![/\w.])"),
    "<x at y> (informacyjnie)": re.compile(r"[<(\[][A-Za-z0-9._%+-]+ (?:at|AT) [A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\." + TLD + r"[>)\]]"),
    "nagłówek archiwum listy (informacyjnie)": re.compile(r"(?m)^[^\n]{0,80}? [A-Za-z0-9_%+-]+ at [A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\." + TLD + r"\n(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun) "),
    # szeroki jak reguła pii_at_bez_nawiasow (aneks 25.11c), też z TLD wielkimi literami: głównie frazy „available at
    # Amazon.com”, „answer at math.stackexchange.com”; po masce do przeglądu próbki, czy zostały adresy osób
    "x at domena (szeroki, informacyjnie)": re.compile(r"(?<![A-Za-z0-9._%+-])[A-Za-z0-9._%+-]+ (?:at|AT) [A-Za-z0-9-]{2,}(?:\.[A-Za-z0-9-]+)*\.(?i:" + TLD[3:-1] + r")\b"),
}
# tani warunek konieczny każdego wzorca (te same trafienia, ~kilka razy szybciej na tekście stron, gdzie prawie każdy dokument
# ma " at "): pełny wzorzec liczony tylko na dokumentach, które go spełniają
WSTEPNE = {
    "_at_": re.compile(r"_at_"),
    "{at}/<at>": re.compile(r"[\{<] ?(?:at|AT) ?[\}>]"),
    "at ... dot": re.compile(r" (?:dot|DOT) "),
    "AT domena.tld": re.compile(r" AT [A-Za-z0-9-]+\."),
    "at domena.tld (informacyjnie)": re.compile(r"[._][A-Za-z0-9._%+-]* at [A-Za-z0-9-]+\."),
    "login at poczta (informacyjnie)": re.compile(r" (?:at|AT) " + MAIL + r"\."),
    "<x at y> (informacyjnie)": re.compile(r" (?:at|AT) [A-Za-z0-9.-]+[>)\]]"),
    "nagłówek archiwum listy (informacyjnie)": re.compile(r"\n(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun) "),
    "x at domena (szeroki, informacyjnie)": re.compile(r" (?:at|AT) [A-Za-z0-9-]{2,}\."),
}


def job(a):
    p, t = a
    wyn = {k: [0, 0, []] for k in WZORCE}
    for r in t:
        for k, rx in WZORCE.items():
            h = list(rx.finditer(r["text"])) if WSTEPNE[k].search(r["text"]) else []
            if h:
                wyn[k][0] += 1
                wyn[k][1] += len(h)
                if len(wyn[k][2]) < 50:
                    m = h[0]
                    wyn[k][2].append({"id": r["id"], "trafienie": m.group(0),
                                      "kontekst": r["text"][max(0, m.start() - 80):m.end() + 40]})
    return p, wyn


def paczki(p):
    """Paczki po 5 000 wierszy (eksport shard.write ma jedną grupę wierszy na plik, więc grupy nie dzielą pracy); pula
    czyta generator zachłannie, więc w pamięci jest naraz najwyżej jeden plik."""
    for b in pq.ParquetFile(p).iter_batches(batch_size=5000, columns=["id", "text"]):
        yield p, b.to_pylist()


if __name__ == "__main__":
    OUT, pliki = sys.argv[1], sys.argv[2:]
    suma = {}
    with Pool(int(os.environ.get("PROCESY", 4))) as pool:
        for plik in pliki:
            for p, w in pool.imap_unordered(job, paczki(plik), chunksize=1):
                s = suma.setdefault(p.split("/")[-1], {k: [0, 0, []] for k in WZORCE})
                for k, v in w.items():
                    s[k][0] += v[0]
                    s[k][1] += v[1]
                    s[k][2] = (s[k][2] + v[2])[:3000]  # wszystkie do ręcznego przeglądu (do 50 na paczkę)
    json.dump({p: {k: {"pliki": v[0], "trafienia": v[1], "przyklady": v[2]} for k, v in s.items()} for p, s in suma.items()},
              open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for p, s in sorted(suma.items()):
        print(p, {k: v[0] for k, v in s.items()}, flush=True)
