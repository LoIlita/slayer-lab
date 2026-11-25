"""Kontrola dodatnia zbiorów matematyki (#346): dokumenty wstawione przez te same skrypty (przebieg.py, ewal_czeste.py,
agreguj_mat.py) co pula; każdy musi dostać powód z preregistracji (pole 'kontrole_dodatnie').
  buduj <zbior> katalog_ewal katalog_slayer107 tokenizer.json walidacja.parquet wyjscie
      -> wyjscie/kontrola.rg5000.parquet (+ .oryg dla cranemath) i probka_kontrola.json (+ _oryg)
  sprawdz <zbior> wyjscie   -> tabela dokument -> powody (widok niezależny) i kod 1, gdy oczekiwany powód nie padł"""
import json
import os
import sys

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

TRYB, ZB = sys.argv[1], sys.argv[2]
TLO = ("To add fractions with different denominators, first find a common denominator. For example, to add one third and "
       "one quarter, rewrite both with denominator twelve: four twelfths plus three twelfths gives seven twelfths. ") * 5
KOD = ("def mean(values):\n    \"\"\"Return the arithmetic mean of a non-empty list of numbers.\"\"\"\n    total = 0\n"
       "    for v in values:\n        total += v\n    return total / len(values)\n\n\n") * 4
# para duplikatów: tekst inny niż tło, żeby dedup_wewnatrz łapał tylko drugi z pary, nie pierwszy jako kopię tła
DUP_TLO = ("The area of a triangle equals half the product of its base and height. A triangle with base ten centimetres and "
           "height six centimetres therefore has an area of thirty square centimetres. ") * 5
DUP_KOD = ("def is_prime(n):\n    if n < 2:\n        return False\n    k = 2\n    while k * k <= n:\n        if n % k == 0:\n"
           "            return False\n        k += 1\n    return True\n\n\n") * 4


def oczekiwane():
    o = {"K_dup_b": "dedup_wewnatrz", "K_kopia_107": "dedup_slayer107", "K_walidacja": "walidacja_fabryki", "K_czysty": None,
         "K_gsm8k": "ewal_13gram", "K_math": "ewal_13gram", "K_gsm_plus": "ewal_13gram", "K_gsm1k": "ewal_13gram", "K_mmlu": "ewal_13gram",
         "K_entech": "dedup_english_technical", "K_fwe109": "dedup_fineweb_edu_109", "K_pusty": "min_tresc",
         "K_en8x3b": "dedup_slayer_8x3b_en"}
    if ZB == "stackedu":
        o.update({"K_humaneval": "ewal_13gram", "K_mbpp": "ewal_13gram", "K_aws": "sekrety", "K_generated": "wygenerowany",
                  "K_licencja": "licencja", "K_int_score": "int_score", "K_email": None, "K_haslo": "haslo_w_kodzie"})
    else:
        o.update({"K_email": "pii", "K_telefon": "pii", "K_ip": "pii", "K_domena": "domena_testow", "K_at": "pii_zaciemniony"})
    if ZB == "cranemath":
        o.update({"K_think": "think", "K_gsm8k_oryg": "ewal_13gram_oryginal", "K_forum": "szablon_forum", "K_suma40": "suma40"})
    return o


if TRYB == "buduj":
    EW, S107, TOK, WAL, OUT, ENTECH, EN8X3B, FWE_URL = sys.argv[3:11]  # aneksy 24.11 i 25.11b: teksty baz 1.08 i 1.00-1.06, url FWE 1.09
    from tokenizers import Tokenizer
    os.makedirs(OUT, exist_ok=True)

    def pierwszy(kat, f_wiersz, nr=0):
        for f in sorted(os.listdir(kat)):
            if f.endswith(".parquet") and "test" in f:
                return f_wiersz(pq.read_table(os.path.join(kat, f)).slice(nr, 1).to_pylist()[0])
        raise SystemExit("brak testu w " + kat)

    gsm = pierwszy(f"{EW}/T33_gsm8k", lambda w: w["question"] + " " + w["answer"])
    mth = pierwszy(f"{EW}/T34_math", lambda w: w["problem"] + " " + w["solution"])
    gsp = pierwszy(f"{EW}/T51_gsm_plus", lambda w: w["question"] + " " + str(w.get("solution") or ""))
    g1k = pierwszy(f"{EW}/T52_gsm1k", lambda w: w["question"] + " " + w["answer"])
    mml = pierwszy(f"{EW}/T32_mmlu", lambda w: w["question"] + " " + " ".join(w["choices"]))
    hev = pierwszy(f"{EW}/X02_humaneval", lambda w: w["prompt"] + w["canonical_solution"])
    mbp = pierwszy(f"{EW}/X03_mbpp", lambda w: w["text"] + "\n" + w["code"])
    ends = np.fromfile(f"{S107}/en_mix/docs.idx", dtype=np.uint64)
    ids = np.memmap(f"{S107}/en_mix/train.bin", dtype=np.uint16, mode="r")
    kopia107 = Tokenizer.from_file(TOK).decode(ids[int(ends[999]):int(ends[1000])].tolist(), skip_special_tokens=True)
    wal = pq.read_table(WAL).slice(100, 1).to_pylist()[0]["text"]
    baza = KOD if ZB == "stackedu" else TLO
    w = [
        ("K_czysty", "https://example.org/czysty", baza),
        ("K_dup_a", "https://example.org/dup1", DUP_KOD if ZB == "stackedu" else DUP_TLO),
        ("K_dup_b", "https://example.org/dup2", DUP_KOD if ZB == "stackedu" else DUP_TLO),
        ("K_kopia_107", "https://example.org/k107", kopia107),
        ("K_walidacja", "https://example.org/wal", wal),
        ("K_gsm8k", "https://example.org/gsm8k", baza + "\n" + gsm),
        ("K_math", "https://example.org/math", baza + "\n" + mth),
        ("K_gsm_plus", "https://example.org/gsmplus", baza + "\n" + gsp),
        ("K_gsm1k", "https://example.org/gsm1k", baza + "\n" + g1k),
        ("K_mmlu", "https://example.org/mmlu", baza + "\n" + mml),
        ("K_email", "https://example.org/email", baza + "\n# Author: John Miller <john.miller84@gmail.com>\n"),
    ]
    if ZB == "stackedu":
        w += [("K_humaneval", "https://example.org/he", baza + "\n" + hev), ("K_mbpp", "https://example.org/mbpp", baza + "\n" + mbp),
              ("K_aws", "https://example.org/aws", baza + "\nAWS_KEY = '" + "AKIA" + "Z" * 16 + "'\n"),  # sztuczny klucz pod wzorzec
              ("K_generated", "https://example.org/gen", "# Generated by Django 3.2.5 on 2021-07-01 10:00\n" + baza),
              ("K_licencja", "https://example.org/lic", baza + "\n# licencja pusta\n"),
              ("K_int_score", "https://example.org/int", baza + "\n# int_score 2\n")]
    else:
        w += [("K_telefon", "https://example.org/tel", baza + " Call the office at (415) 555-0132 after noon."),
              ("K_ip", "https://example.org/ip", baza + " The server at 84.23.117.9 went down overnight."),
              ("K_domena", "https://www.wikihow.com/Add-Fractions", baza)]
    if ZB == "cranemath":
        w += [("K_think", "https://example.org/think", "<think>\nOkay, let me rewrite this. First I need to " + baza),
              ("K_gsm8k_oryg", "https://example.org/gsm8korig", baza + " Rewritten without the test text.")]
    w += [("K_entech", "https://example.org/entech", pq.read_table(ENTECH, columns=["text"]).slice(5, 1).column(0)[0].as_py()),
          ("K_en8x3b", "https://example.org/en8x3b", pq.ParquetFile(EN8X3B).read_row_group(0, columns=["text"]).column(0)[5].as_py()),
          ("K_fwe109", FWE_URL, baza + " Page seen in FineWeb-Edu 1.09."),
          ("K_pusty", "https://example.org/pusty", "$$\n\n$$\n\n" * 200)]
    if ZB == "stackedu":
        w += [("K_haslo", "https://example.org/haslo", baza + "\nconn = connect(user='app', passwd='s3cretpw')\n")]
    else:
        w += [("K_at", "https://example.org/at", baza + " Contributed by Jan Kowalsky (jkowal(AT)example.edu), 2004.")]
    if ZB == "cranemath":
        w += [("K_forum", "https://example.org/forum", "Question: what is 7 times 8? Answer: 56. Powered by phpBB. GMAT Club Daily Prep. "
               "Thank you for using the timer. " * 2),
              ("K_suma40", "https://example.org/suma40", "To find the sum of the numbers from 1 to 40, use the formula for an arithmetic "
               "series. The sum equals n times the first plus last term divided by two, so the answer is 820. " * 3)]
    kol = {"text": [x[2] for x in w], "url": [x[1] for x in w], "id": [x[0] for x in w]}
    n = len(w)
    if ZB == "stackedu":
        kol.update({"license": ["" if x[0] == "K_licencja" else "MIT" for x in w], "license_type": ["permissive"] * n,
                    "int_score": [2 if x[0] == "K_int_score" else 4 for x in w]})
    p = f"{OUT}/kontrola.rg5000.parquet"
    pq.write_table(pa.table(kol), p, row_group_size=5000)
    wpis = {"lokalnie": p}
    if ZB == "cranemath":
        po = f"{OUT}/kontrola.oryg.rg5000.parquet"
        oryg = [(baza + "\n" + gsm) if x[0] == "K_gsm8k_oryg" else baza for x in w]
        pq.write_table(pa.table({"text": oryg, "url": kol["url"], "id": kol["id"]}), po, row_group_size=5000)
        wpis["lokalnie_oryg"] = po
        json.dump({"pliki": [{"lokalnie": po}]}, open(f"{OUT}/probka_kontrola_oryg.json", "w"))
    json.dump({"pliki": [wpis]}, open(f"{OUT}/probka_kontrola.json", "w"))
    print("wierszy", n)
else:
    OUT = sys.argv[3]
    z = np.load(f"{OUT}/powody.npz", allow_pickle=True)
    nazwy, m = [str(x) for x in z["nazwy"]], z["m"]
    ids = [i for u in sorted(os.listdir(f"{OUT}/przebieg")) if u.endswith(".json") and u.startswith("u_")
           for i in json.load(open(f"{OUT}/przebieg/{u}"))["ids"]]
    oc = oczekiwane()
    zle = 0
    wyn = {}
    for i, d in enumerate(ids):
        ma = [nazwy[j] for j in np.flatnonzero(m[i])]
        exp = oc.get(d, "?")
        ok = (not ma) if exp is None else (exp in ma) if exp != "?" else True
        if d == "K_dup_a":
            ok = "dedup_wewnatrz" not in ma
        zle += not ok
        wyn[d] = {"powody": ma, "oczekiwany": exp, "ok": ok}
        print(("OK  " if ok else "BŁĄD"), d, ma, "oczekiwany:", exp)
    json.dump({"wynik": f"{len(ids) - zle}/{len(ids)}", "przypadki": wyn}, open(f"{OUT}/kontrola_wynik.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    sys.exit(1 if zle else 0)
