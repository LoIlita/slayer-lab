"""NER spaCy en_core_web_sm na oknach korpusu: pierwsze 2000 i ostatnie 1000 znaków wierszy Gutenberga; cały tekst SCP i RPG.
Argumenty: wejscie.parquet katalog_wyjscia liczba_procesow. Wyjście: ner_NNNN.json dla każdej grupy wierszy."""
import json
import os
import re
import sys
import warnings
from multiprocessing import Pool

import pyarrow.parquet as pq
import spacy

PLIK, OUT, PROC = sys.argv[1], sys.argv[2], int(sys.argv[3])
MODEL = "/private/tmp/claude-501/-Users-lolita-Documents-GitHub-labaj-agency/427bd419-cf49-48c0-9472-968edec57894/scratchpad/kontrola-110/model_spacy"
RX_BIRTH = re.compile(r"\bborn\b|\bb\.\s*\d|\bbirth\b|\bn[ée]e\b|\bdate of birth\b|\bDOB\b|\(\s*\d{4}\s*[-–—]\s*(?:\d{4})?\s*\)", re.I)
RX_ROK = re.compile(r"\b(1[5-9]\d\d|20[0-2]\d)\b")
RX_HOUSE = re.compile(r"\b\d{1,5}[A-Za-z]?,?\s+(?:[A-Z][\w'.]*\s){0,3}(?:Street|St\.?|Avenue|Ave\.?|Road|Rd\.?|Lane|Square|Place|Boulevard|Blvd\.?|Terrace|Drive|Dr\.?|Court|Ct\.?|Way|Row|Gardens|Crescent)\b")
RX_ZIP = re.compile(r"\b[A-Z]{2}\s\d{5}(?:-\d{4})?\b|\b[A-Z]{1,2}\d[A-Z\d]?\s\d[A-Z]{2}\b")
RX_MAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
RX_TEL = re.compile(r"\+\d{1,3}[\s.-]?\(?\d{1,4}\)?[\s.-]?\d{2,4}[\s.-]?\d{2,4}[\s.-]?\d{0,4}|\(\d{3}\)\s?\d{3}[-.\s]\d{4}|\b\d{3}[-.]\d{3}[-.]\d{4}\b")
NLP = None


def okna(zrodlo, text):
    if zrodlo == "gutenberg":
        if len(text) <= 3000:
            return [(0, text)]
        return [(0, text[:2000]), (len(text) - 1000, text[-1000:])]
    return [(i, text[i:i + 100000]) for i in range(0, len(text), 100000)]


def init():
    global NLP
    warnings.filterwarnings("ignore")
    NLP = spacy.load(MODEL, exclude=["parser", "lemmatizer", "tagger", "attribute_ruler", "senter"])


def przetworz(rg):
    pf = pq.ParquetFile(PLIK)
    t = pf.read_row_group(rg, columns=["text", "zrodlo", "id_zrodla"])
    texts = t.column("text").to_pylist()
    zr = t.column("zrodlo").to_pylist()
    ids = t.column("id_zrodla").to_pylist()
    jobs = [(i, off, w) for i in range(len(texts)) for off, w in okna(zr[i], texts[i])]
    w = {"rg": rg, "email": [], "telefon": [], "osoba_data": [], "adres": [], "person": 0, "okna": len(jobs), "znaki": 0}
    for (i, off, x), doc in zip(jobs, NLP.pipe((j[2] for j in jobs), batch_size=64)):
        w["znaki"] += len(x)
        for m in RX_MAIL.finditer(x):
            w["email"].append([ids[i], zr[i], m.group(0), x[max(0, m.start() - 80):m.end() + 80].replace("\n", " ")])
        for m in RX_TEL.finditer(x):
            w["telefon"].append([ids[i], zr[i], m.group(0), x[max(0, m.start() - 80):m.end() + 80].replace("\n", " ")])
        for e in doc.ents:
            if e.label_ == "PERSON":
                w["person"] += 1
                c = x[max(0, e.start_char - 120):e.end_char + 120]
                roki = [int(y) for y in RX_ROK.findall(c)]
                if RX_BIRTH.search(c) and roki and max(roki) >= 1920:
                    w["osoba_data"].append([ids[i], zr[i], e.text, c.replace("\n", " ")])
            elif e.label_ == "FAC":
                c = x[max(0, e.start_char - 60):e.end_char + 60]
                if RX_HOUSE.search(c) or RX_ZIP.search(c):
                    w["adres"].append([ids[i], zr[i], e.text, c.replace("\n", " ")])
    with open(f"{OUT}/ner_{rg:04d}.json", "w", encoding="utf-8") as f:
        json.dump(w, f, ensure_ascii=False)
    return rg, len(jobs)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    pf = pq.ParquetFile(PLIK)
    rgs = [rg for rg in range(pf.metadata.num_row_groups) if not os.path.exists(f"{OUT}/ner_{rg:04d}.json")]
    with Pool(PROC, initializer=init) as p:
        for rg, n in p.imap_unordered(przetworz, rgs):
            print(rg, n, flush=True)
    print("KONIEC", flush=True)
