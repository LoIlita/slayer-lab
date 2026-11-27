"""Porównanie tekstu przed i po nowej masce e-maili na wyeksportowanych częściach: które dokumenty się zmieniają i co
dokładnie zastępuje '[PII]' (do ręcznego przeglądu, czy to wyłącznie adresy). Tekst części jest już po dotychczasowej
masce; skrypt sprawdza, że dotychczasowa maska nic nie zmienia (idempotentna), a nowe wzorce (EMAIL_CODE_OBF dla
code_obf) zbiera dopasowanie po dopasowaniu, w kolejności stosowania — bez difflib (kwadratowy na dużych plikach).
Użycie: python porownaj_maske.py <wyjscie.json> code_obf <plik.parquet> [...]"""
import json
import os
import sys
from multiprocessing import Pool

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "eksport", "src"))
sys.modules["pii"] = type(sys)("pii")  # mat_wybor importuje pii repo zgłoszeń tylko dla no_masking
import mat_wybor as m  # noqa: E402
import pyarrow.parquet as pq  # noqa: E402

FLAGA = sys.argv[2]
assert FLAGA == "code_obf", "na razie tylko code_obf"


def job(a):
    p, g = a
    zm, nieidem = [], 0
    for r in pq.ParquetFile(p).read_row_group(g, columns=["id", "text"]).to_pylist():
        t = r["text"]
        if m._mask_emails(t)[0] != t:
            nieidem += 1
        zast = []
        for rx in m.EMAIL_CODE_OBF:
            def sub(x):
                if x.lastindex and x.group(1).lower() in m.EXAMPLE_DOMAINS:
                    return x.group(0)
                zast.append(x.group(0))
                return "[PII]"
            t = rx.sub(sub, t)
        if zast:
            zm.append({"id": r["id"], "zastapione": zast})
    return p, zm, nieidem


if __name__ == "__main__":
    OUT, pliki = sys.argv[1], sys.argv[3:]
    zad = [(p, g) for p in pliki for g in range(pq.ParquetFile(p).num_row_groups)]
    wyn, nie = {}, {}
    with Pool(4) as pool:
        for p, zm, n in pool.imap_unordered(job, zad):
            wyn.setdefault(os.path.basename(p), []).extend(zm)
            nie[os.path.basename(p)] = nie.get(os.path.basename(p), 0) + n
    json.dump({p: {"dokumenty": len(v), "stara_maska_zmienia": nie[p], "zmiany": v} for p, v in wyn.items()},
              open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for p, v in sorted(wyn.items()):
        print(p, "dokumenty", len(v), "zastąpień", sum(len(x["zastapione"]) for x in v), "stara maska zmienia", nie[p], flush=True)
