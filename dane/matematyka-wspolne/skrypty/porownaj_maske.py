"""Porównanie tekstu przed i po nowej masce e-maili na wyeksportowanych częściach: które dokumenty się zmieniają i co
dokładnie zastępuje '[PII]' (do ręcznego przeglądu, czy to wyłącznie adresy). Tekst części jest już po dotychczasowej
masce źródła (albo bez maski: FineMath, InfiWebMath, StackExchange, CraneMath); skrypt liczy, co zmieniają wzorce
zawsze włączone w premask_emails (EMAIL, EMAIL_AT: 'stara_maska_zmienia' i ich zastąpienia — w źródłach z maską ma być 0),
a nowe wzorce (EMAIL_CODE_OBF dla code_obf, EMAIL_PROSE_OBF dla prose_obf) zbiera dopasowanie po dopasowaniu, w kolejności
stosowania jak w mat_wybor._mask_emails — bez difflib (kwadratowy na dużych plikach). Na koniec sprawdza, że zebrane
zastąpienia dają ten sam tekst co _mask_emails (te same flagi).
Użycie: [PROCESY=4] python porownaj_maske.py <wyjscie.json> code_obf|prose_obf <plik.parquet> [...]"""
import json
import os
import sys
from multiprocessing import Pool

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "eksport", "src"))
sys.modules["pii"] = type(sys)("pii")  # mat_wybor importuje pii repo zgłoszeń tylko dla no_masking
import mat_wybor as m  # noqa: E402
import pyarrow.parquet as pq  # noqa: E402

FLAGA = sys.argv[2]
assert FLAGA in ("code_obf", "prose_obf"), FLAGA
NOWE = ([(None, rx) for rx in m.EMAIL_CODE_OBF] if FLAGA == "code_obf"
        else list(zip(m._PROSE_GUARDS, m.EMAIL_PROSE_OBF)))


def job(a):
    p, wiersze = a
    zm, stara = [], []
    for r in wiersze:
        t = r["text"]
        zast, zast_st = [], []

        def sub_do(lista):
            def sub(x):
                if x.lastindex and x.group(1).lower() in m.EXAMPLE_DOMAINS:
                    return x.group(0)
                lista.append(x.group(0))
                return "[PII]"
            return sub
        if m._EMAIL_FIND.search(t):
            t = m.EMAIL.sub(sub_do(zast_st), t)
        if m._EMAIL_AT_FIND.search(t):
            t = m.EMAIL_AT.sub(sub_do(zast_st), t)
        for i, (g, rx) in enumerate(NOWE):
            if g is None or g.search(t):
                przed = len(zast)
                t = rx.sub(sub_do(zast), t)
                zast[przed:] = [f"{i}:{s}" for s in zast[przed:]]
        assert t == m._mask_emails(r["text"], **{FLAGA: True})[0], r["id"]
        if zast_st:
            stara.append({"id": r["id"], "zastapione": zast_st})
        if zast:
            zm.append({"id": r["id"], "zastapione": zast})
    return p, zm, stara


def paczki(p):
    for b in pq.ParquetFile(p).iter_batches(batch_size=5000, columns=["id", "text"]):
        yield p, b.to_pylist()


if __name__ == "__main__":
    OUT, pliki = sys.argv[1], sys.argv[3:]
    wyn, nie = {}, {}
    with Pool(int(os.environ.get("PROCESY", 4))) as pool:
        for plik in pliki:  # pula czyta generator zachłannie: w pamięci najwyżej jeden plik
            for p, zm, st in pool.imap_unordered(job, paczki(plik), chunksize=1):
                wyn.setdefault(os.path.basename(p), []).extend(zm)
                nie.setdefault(os.path.basename(p), []).extend(st)
    json.dump({p: {"dokumenty": len(v), "stara_maska_zmienia": len(nie[p]), "stara_maska_zmiany": nie[p], "zmiany": v}
               for p, v in wyn.items()}, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for p, v in sorted(wyn.items()):
        print(p, "dokumenty", len(v), "zastąpień", sum(len(x["zastapione"]) for x in v), "stara maska zmienia",
              len(nie[p]), flush=True)
