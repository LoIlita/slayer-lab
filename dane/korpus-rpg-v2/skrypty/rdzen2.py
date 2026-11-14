"""Dodatki rdzenia: klucze LSH, winnowing dla podciągów, detektory znaków i mojibake, tagi treści, heurystyka osób i adresów."""
import collections
import re
import unicodedata

import ftfy.badness
import numpy as np

import rdzen as r

C_BAND = np.uint64(0x9E3779B97F4A7C15)


def klucze_band(sig, bands, rows):
    """sig: (n, perms) uint64 -> (n, bands) klucze pasm; stabilne między przebiegami."""
    n = sig.shape[0]
    wyj = np.zeros((n, bands), dtype=np.uint64)
    for b in range(bands):
        h = np.zeros(n, dtype=np.uint64)
        for j in range(rows):
            h = h * C_BAND + sig[:, b * rows + j]
        h ^= np.uint64(b) * np.uint64(0xC2B2AE3D27D4EB4F)
        wyj[:, b] = h
    return wyj


def winnowing(w, k=41, okno=10):
    """Odcisk: (pozycje, hasze) k-gramów słów wybranych minimum okna. Wspólny ciąg >= k+okno-1 słów (tu 50) ma wspólny odcisk."""
    sh = r.ngramy(w, k)
    if len(sh) < okno:
        if len(sh) == 0:
            return np.zeros(0, dtype=np.int64), np.zeros(0, dtype=np.uint64)
        return np.array([int(np.argmin(sh))], dtype=np.int64), sh[[int(np.argmin(sh))]]
    widok = np.lib.stride_tricks.sliding_window_view(sh, okno)
    poz = np.unique(np.arange(len(widok)) + widok.argmin(axis=1))
    return poz.astype(np.int64), sh[poz]


# ---- znaki: detektor przekodowań ze słownikiem i obce glify

SLOWO_L = re.compile(r"[^\W\d_]+(?:['’][^\W\d_]+)*")
NIEASCII = re.compile(r"\S*[^\x00-\x7f]\S*")
OK_TYPO = set("’‘“”—–…«»£§°¼½¾×·ß")
ALFABET = "abcdefghijklmnopqrstuvwxyz'"


def licz_slowa(tekst):
    return collections.Counter(w.lower() for w in SLOWO_L.findall(tekst))


def _obetnij(w):
    while w and unicodedata.category(w[0])[0] in "PS" and w[0] not in OK_TYPO:
        w = w[1:]
    while w and unicodedata.category(w[-1])[0] in "PS" and w[-1] not in OK_TYPO:
        w = w[:-1]
    return w


def _cp1252(c):
    """Tylko znak możliwy w źle zdekodowanym cp1252 jest kandydatem; bloki redakcji SCP (█) i inne symbole nie są."""
    try:
        c.encode("cp1252")
        return True
    except UnicodeEncodeError:
        return False


def slowo_przekodowane(w, slownik):
    """True, gdy słowo wygląda na przekodowanie: odwrócenie cp1252->utf8 daje inne słowo, albo podmiana 1-2 znaków spoza
    liter daje słowo znacznie częstsze w słowniku korpusu."""
    try:
        odw = w.encode("cp1252").decode("utf-8")
        if odw != w:
            return True
    except (UnicodeEncodeError, UnicodeDecodeError):
        pass
    poz = [i for i, c in enumerate(w) if ord(c) > 127 and unicodedata.category(c)[0] != "L" and c not in OK_TYPO and _cp1252(c)]
    if not 1 <= len(poz) <= 2 or not any(unicodedata.category(c)[0] == "L" for c in w):
        return False
    orig = max(1, slownik.get(w.lower(), 0))
    baza = list(w.lower())
    for a in ALFABET:
        for b in (ALFABET if len(poz) == 2 else [""]):
            baza[poz[0]] = a
            if len(poz) == 2:
                baza[poz[1]] = b
            c = "".join(baza)
            f = slownik.get(c, 0)
            if f >= 20 and f >= 20 * orig:
                return True
    return False


def wada_znakow(t, slownik):
    """Zwraca licznik przyczyn dla tekstu końcowego."""
    w = collections.Counter()
    lit = obce = 0
    for s in NIEASCII.findall(t):
        s2 = _obetnij(s)
        if s2 and slowo_przekodowane(s2, slownik):
            w["przekodowane_slowa"] += 1
        skr = {unicodedata.name(c, "").split(" ")[0] for c in s2 if unicodedata.category(c)[0] == "L"}
        if "LATIN" in skr and (skr & {"CYRILLIC", "GREEK"}):
            w["mieszane_pismo_w_slowie"] += 1
    for c in re.findall(r"[^\x00-\x7f]", t):
        kat = unicodedata.category(c)
        if kat[0] == "L":
            lit += 1
            if not unicodedata.name(c, "LATIN").startswith("LATIN"):
                obce += 1
        if kat in ("Co", "Cn") or c == "�":
            w["prywatne_lub_fffd"] += 1
    lit += len(re.findall(r"[A-Za-z]", t))
    w["obce_litery_udzial_x1e6"] = int(1e6 * obce / max(1, lit))
    return w


def moj_metryki(t):
    """Liczniki per dokument (do raportu na 1 mln znaków)."""
    return {"badness": int(ftfy.badness.badness(t)), "fffd": t.count("�"),
            "c0c1": len(re.findall(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]", t)), "shy": t.count("­"),
            "zero_szer": len(re.findall(r"[​-‍﻿]", t)), "znaki": len(t)}


def moj_wynik(m):
    """Wskaźnik dokumentu: wszystkie dopasowania na 1 mln znaków."""
    return 1e6 * (m["badness"] + m["fffd"] + m["c0c1"] + m["shy"] + m["zero_szer"]) / max(1, m["znaki"])


# ---- tagi treści (słownikowe, nie klasyfikator; tylko tag, bez wycinania)

TOKS = {
    "rasistowski_jezyk": r"\b(nigger|niggers|nigga|coon|coons|darkey|darkie|darky|chink|chinks|kike|kikes|wop|wops|gook|gooks|injun|injuns|pickaninny|pickaninnies|mulatto|mulattoes|sambo)\b",
    "przemoc_drastyczna": r"\b(disembowel\w*|dismember\w*|mutilat\w*|eviscerat\w*|decapitat\w*|flay(ed|ing)?|torture[ds]?)\b",
    "seksualne": r"\b(rape[ds]?|raping|fornicat\w*|lewd\w*)\b",
    "samobojstwo": r"\bsuicid\w*\b",
}
TOKS = {k: re.compile(v, re.I) for k, v in TOKS.items()}


def tagi_tresci(t):
    return sorted(k for k, rx in TOKS.items() if rx.search(t))


# ---- heurystyka osób z datami i adresów (NIE NER: model spaCy zablokowany przez hook pip-zrodlo)

OSOBA_DATA = re.compile(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})\b[^.\n]{0,40}?\b((?:1[5-9]|20)\d\d)\b")
ADRES = re.compile(r"\b\d{1,4}\s+[A-Z][a-z]+\s+(Street|St\.|Road|Rd\.|Avenue|Ave\.|Lane|Square|Terrace|Place)\b|\bP\.?\s?O\.?\s+Box\b")


def osoby_i_adresy(t):
    return len(OSOBA_DATA.findall(t)), len(ADRES.findall(t))
