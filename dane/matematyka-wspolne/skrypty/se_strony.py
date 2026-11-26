"""Indeks pytań StackExchange obecnych jako strony WWW w wyeksportowanych źródłach (powód dedup_se_strony, preregistracja
dane/stackexchange_mat): url stron mają postać https://<serwis>/questions/<id>/<slug>, a dokumenty zrzutu
https://<serwis>/questions/<id>, więc identyczny url ich nie łączy. Klucz = h64(norm_url("https://<serwis>/questions/<id>")),
ten sam co X["hu"] dokumentu zrzutu w przebieg.py.
Użycie: python se_strony.py wyjscie.npy <wybor.json> <katalog_przebiegu> [<wybor.json> <katalog_przebiegu> ...]"""
import json
import os
import re
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "dclm-en", "skrypty"))
import wspolne as w  # noqa: E402

RX = re.compile(r"^(?:[a-zA-Z]+://)?(?:www\.)?([a-z0-9.-]+\.(?:stackexchange\.com|mathoverflow\.net))/(?:questions|q)/(\d+)", re.I)
OUT, pary = sys.argv[1], list(zip(sys.argv[2::2], sys.argv[3::2]))
klucze, n_stron = set(), 0
for wyb_p, prz in pary:
    wyb = set(json.load(open(wyb_p))["dokumenty_globalne"])
    jed = json.load(open(f"{prz}/jednostki.json"))
    g = 0
    for k in range(len(jed)):
        for u in json.load(open(f"{prz}/u_{k:04d}.json"))["urls"]:
            if g in wyb and (m := RX.match(u or "")):
                n_stron += 1
                klucze.add(w.h64(w.norm_url(f"https://{m.group(1).lower()}/questions/{m.group(2)}")))
            g += 1
np.save(OUT, np.array(sorted(klucze), np.uint64))
print("stron SE", n_stron, "pytań", len(klucze))
