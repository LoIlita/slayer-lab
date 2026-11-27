"""Przebudowa ramienia mikroanneal z części data/ po aneksie maskowania (Stack-Edu, aneks 2026-11-27 zaciemnione):
wiersze ramienia brane z nowych części po tych samych id, w kolejności ramienia, zapis jak shard.write (zstd). Kolumna
`source` zostaje z ramienia (klucz ramienia, np. `stack_edu_python`; w częściach `stack_edu_python_pNN`).
Dowód: (1) ramię = podzbiór starych części (wszystkie kolumny równe poza source), (2) nowe ramię = nowe części,
(3) te same id, kolejność i liczba wierszy, tekst nowy = stary po wzorcach EMAIL_CODE_OBF (jak porownaj_eksporty.py),
pozostałe kolumny bez zmian poza token_count, który zmienia się tylko w wierszach ze zmienionym tekstem.
Użycie: python przebuduj_ramie.py <ramie.parquet> <wyjscie.parquet> <raport.json> --stare <p.parquet ...> --nowe <p.parquet ...>"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "eksport", "src"))
sys.modules["pii"] = type(sys)("pii")
import mat_wybor as m  # noqa: E402
import pyarrow as pa  # noqa: E402
import pyarrow.compute as pc  # noqa: E402
import pyarrow.parquet as pq  # noqa: E402

RAMIE, WYJ, RAPORT = sys.argv[1:4]
i_st, i_no = sys.argv.index("--stare"), sys.argv.index("--nowe")
STARE, NOWE = sys.argv[i_st + 1:i_no], sys.argv[i_no + 1:]


def maska(t):
    n = 0

    def zam(q):
        nonlocal n
        if q.lastindex and q.group(1).lower() in m.EXAMPLE_DOMAINS:
            return q.group(0)
        n += 1
        return "[PII]"
    for rx in m.EMAIL_CODE_OBF:
        t = rx.sub(zam, t)
    return t, n


ramie = pq.read_table(RAMIE)
ids = ramie.column("id")
poz = {x: i for i, x in enumerate(ids.to_pylist())}
assert len(poz) == ramie.num_rows, "powtórzone id w ramieniu"


def z_czesci(pliki):
    """Wiersze o id ramienia z części, ustawione w kolejności ramienia; liczba trafień per plik."""
    kaw, ile = [], {}
    for p in pliki:
        n = 0
        for b in pq.ParquetFile(p).iter_batches(batch_size=20000):
            t = pa.Table.from_batches([b]).filter(pc.is_in(b.column("id"), value_set=ids))
            n += t.num_rows
            if t.num_rows:
                kaw.append(t)
        ile[os.path.basename(p)] = n
    t = pa.concat_tables(kaw)
    assert t.num_rows == ramie.num_rows, f"w częściach {t.num_rows} z {ramie.num_rows} id ramienia"
    kol = pa.array([poz[x] for x in t.column("id").to_pylist()])
    t = t.take(pc.sort_indices(kol)).select(ramie.column_names)
    t = t.set_column(t.schema.get_field_index("source"), "source", ramie.column("source"))
    return t.cast(ramie.schema), ile


stare, ile_stare = z_czesci(STARE)
nowe, ile_nowe = z_czesci(NOWE)
wyn = {"ramie": os.path.basename(RAMIE), "wiersze": ramie.num_rows, "trafienia_stare": ile_stare, "trafienia_nowe": ile_nowe,
       "ramie_rowne_starym_czesciom": stare.equals(ramie),
       "te_same_id_kolejnosc": nowe.column("id").equals(ids),
       "kolumny_rowne": {c: nowe.column(c).equals(ramie.column(c)) for c in ramie.column_names}}
zm, zastapien, niezgodne, tc_poza, przyklady = 0, 0, [], 0, []
for st, no, tst, tno, i in zip(ramie.column("text").to_pylist(), nowe.column("text").to_pylist(),
                                ramie.column("token_count").to_pylist(), nowe.column("token_count").to_pylist(),
                                ids.to_pylist()):
    mk, n = maska(st)
    if mk != no:
        niezgodne.append(i)
    if st != no:
        zm += 1
        zastapien += n
        if len(przyklady) < 5:
            a = next(k for k in range(min(len(st), len(no))) if st[k] != no[k])
            przyklady.append({"id": i, "przed": st[max(0, a - 60):a + 60], "po": no[max(0, a - 60):a + 60]})
    elif tst != tno:
        tc_poza += 1
wyn.update({"tekst_zmieniony": zm, "zastapien": zastapien, "niezgodne_z_maska": len(niezgodne),
            "przyklady_niezgodne": niezgodne[:5], "token_count_zmieniony_poza_zmienionym_tekstem": tc_poza,
            "stary": {"chars": sum(pc.utf8_length(ramie.column("text")).to_pylist()),
                      "tokens": pc.sum(ramie.column("token_count")).as_py(),
                      "pii_w_tekscie": sum(t.count("[PII]") for t in ramie.column("text").to_pylist())},
            "nowy": {"chars": sum(pc.utf8_length(nowe.column("text")).to_pylist()),
                     "tokens": pc.sum(nowe.column("token_count")).as_py(),
                     "pii_w_tekscie": sum(t.count("[PII]") for t in nowe.column("text").to_pylist())},
            "przyklady": przyklady})
assert wyn["ramie_rowne_starym_czesciom"] and wyn["te_same_id_kolejnosc"] and not niezgodne and not tc_poza, wyn
assert all(v for c, v in wyn["kolumny_rowne"].items() if c not in ("text", "token_count")), wyn["kolumny_rowne"]
pq.write_table(nowe, WYJ, compression="zstd")
json.dump(wyn, open(RAPORT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in wyn.items() if k != "przyklady"}, ensure_ascii=False))
