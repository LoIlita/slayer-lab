"""Rejestruje części <klucz>_p01.._pNN w kopii roboczej repo zgłoszeń (po nałożeniu eksport/): wpisy w src/sources.py
(kopia wpisu klucza bazowego z numerem części w pretty i provenance), configi w README.md i datasheet każdej części
w arkusze_czesci/<klucz_czesci>.md (kopia datasheetu klucza bazowego z linią o części; eksport_czesci.sh kopiuje go do data/).
Idempotentne: części już zarejestrowane są pomijane.
Użycie: python rejestr_czesci.py <katalog_repo_zgloszen> <klucz> <liczba_czesci> <datasheet_klucza.md>"""
import ast
import os
import sys

Z, KEY, N, SHEET = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
src_p, readme_p = f"{Z}/src/sources.py", f"{Z}/README.md"
src = open(src_p, encoding="utf-8").read()
mod = ast.parse(src)
reg = next(ast.literal_eval(n.value) for n in mod.body if isinstance(n, ast.AnnAssign) and n.target.id == "SOURCES")
base = reg[KEY]
nowe = [f"{KEY}_p{i:02d}" for i in range(1, N + 1) if f"{KEY}_p{i:02d}" not in reg]
wpisy = []
for k in nowe:
    i = int(k[-2:])
    e = {**base, "pretty": f"{base['pretty']}, part {i} of {N}",
         "provenance": f"{base['provenance']}; part {i} of {N} of the full filtered pool, split in pool order by v6 tokens "
                       "(slayer-lab dane/matematyka-wspolne/skrypty/czesci.py)"}
    wpisy.append(f"    {k!r}: {{\n" + "".join(f"        {f!r}: {v!r},\n" for f, v in e.items()) + "    },\n")
koniec = src.rstrip().rfind("}")
open(src_p, "w", encoding="utf-8").write(src[:koniec] + "".join(wpisy) + src[koniec:])

readme = open(readme_p, encoding="utf-8").read()
glowa_koniec = readme.index("\n---\n", 4) + 1
bloki = "".join(f"- config_name: {k}\n  data_files:\n  - split: train\n    path: data/{k}/{k}.parquet\n" for k in nowe)
open(readme_p, "w", encoding="utf-8").write(readme[:glowa_koniec] + bloki + readme[glowa_koniec:])

arkusz = open(SHEET, encoding="utf-8").read()
for k in [f"{KEY}_p{i:02d}" for i in range(1, N + 1)]:
    os.makedirs(f"{Z}/arkusze_czesci", exist_ok=True)
    linie = arkusz.split("\n", 1)
    open(f"{Z}/arkusze_czesci/{k}.md", "w", encoding="utf-8").write(
        f"{linie[0]}\n\nPart {k[-2:]} of {N} of `{KEY}`: the full filtered pool split in pool order into parts of similar v6 "
        f"token counts. Everything below describes the whole source.\n{linie[1] if len(linie) > 1 else ''}")
print(len(nowe), "nowych części", KEY)
