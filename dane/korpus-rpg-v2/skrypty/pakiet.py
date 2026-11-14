"""Generuje z PLIKÓW dokumentację korpusu: manifest.json, MANIFEST.md, ATRYBUCJA.md, sha256.txt, licenses/, README.md.
Argumenty: katalog_korpusu katalog_pracowni. Nic nie jest wpisywane ręcznie: liczby pochodzą z liczby_budowy, usuniecia, ner_decyzje, weryfikacja_koncowa, kontrola, status_indeks."""
import collections
import datetime as dt
import hashlib
import json
import os
import shutil
import sys

import pyarrow.parquet as pq

KOR, PRAC = sys.argv[1], sys.argv[2]
WN = f"{PRAC}/wyniki"
LIC_SRC = f"{PRAC}/licencje"
R_WEJ = "968a249fa69c6c5cb35b05ae6bede50c36963a80d60d5513f8a724760e018933"
J = lambda p: json.load(open(p, encoding="utf-8"))
SK = J(f"{PRAC}/skrypty/preregistracja.json")
bud = J(f"{KOR}/liczby_budowy.json" if os.path.exists(f"{KOR}/liczby_budowy.json") else f"{WN}/liczby_budowy.json")
us = J(f"{WN}/usuniecia.json")["liczby"]
ner = J(f"{WN}/ner_decyzje.json")
wer = J(f"{WN}/weryfikacja_koncowa.json")
kon = J(f"{WN}/kontrola.json")
ind = J(f"{WN}/ewal/status_indeks.json")
idx = J(f"{WN}/idx/liczby_indeks.json")
pop = J(f"{PRAC}/karty/poprzedni_manifest_skrot.json")
tok_info = J(f"{WN}/tokenizer_porownanie.json")
stan_pakiet = J(f"{WN}/paczka_slayera_stan.json")

tok_default = sum(v["tokeny"] for k, v in bud.items() if k.startswith("default/"))
wier_default = sum(v["wierszy"] for k, v in bud.items() if k.startswith("default/"))
tok_sa = sum(v["tokeny"] for k, v in bud.items() if k.startswith("cc-by-sa/"))
wier_sa = sum(v["wierszy"] for k, v in bud.items() if k.startswith("cc-by-sa/"))
kat_wiersze = us["usuniete_wg_priorytetu"].get("katalog", 0)
kat_tokeny = us["tokeny_usuniete_wg_priorytetu"].get("katalog", 0)
kat_neg = us["katalog_test_negatywny"]
jezyk_po = J(f"{WN}/jezyk_po.json")
katalog = {"przeglad_trafien_testu_negatywnego": J(f"{WN}/katalog_neg_przeglad.json"), "metoda": SK["katalog_i_listy"], "usuniete_wiersze_wg_priorytetu": kat_wiersze, "usuniete_tokeny_wg_priorytetu": kat_tokeny, "klasy": us["katalog_klasy"], "liczby_detektora": us["katalog_liczby"], "test_negatywny": kat_neg, "pozytyw_51718_cz10": us["katalog_pozytyw"]}

# źródła per config z shardów
z_stat = collections.Counter()
z_tok = collections.Counter()
atr = collections.defaultdict(dict)
for cfg in ("default", "cc-by-sa"):
    k = f"{KOR}/data/{cfg}"
    for p in sorted(os.listdir(k)):
        pf = pq.ParquetFile(f"{k}/{p}")
        for g in range(pf.num_row_groups):
            for x in pf.read_row_group(g, columns=["source_id", "n_tokens", "license", "license_url", "author", "provenance", "work_family"]).to_pylist():
                z_stat[(cfg, x["source_id"])] += 1
                z_tok[(cfg, x["source_id"])] += x["n_tokens"]
                if x["work_family"] not in atr[x["source_id"]]:
                    atr[x["source_id"]][x["work_family"]] = x

# licencje
os.makedirs(f"{KOR}/licenses", exist_ok=True)
for f in os.listdir(LIC_SRC):
    shutil.copy2(f"{LIC_SRC}/{f}", f"{KOR}/licenses/{f}")
with open(f"{KOR}/licenses/PUBLIC-DOMAIN-NOTE.md", "w", encoding="utf-8") as f:
    f.write("# Public-domain rows\n\nRows with `license: public-domain` in the `default` config have no licence text to reproduce. "
            "They were selected from a public catalogue as public domain in the USA; the catalogue is the source of the US status, and the row's `provenance` keeps the catalogue statement and the author's death year.\n\n"
            "An additional filter kept only works whose author (and translator, where given) died in 1955 or earlier, which is the life + 70 years test applied by EU member states. "
            "This filter does not cover every national rule, and it is not legal advice. Verify the copyright status for your country and use.\n")

# ATRYBUCJA.md
with open(f"{KOR}/ATRYBUCJA.md", "w", encoding="utf-8") as f:
    f.write("# Attribution\n\nOne line per work family kept in the dataset. Per-row attribution and the verbatim CC BY attribution statements are in the `provenance` column.\n\n")
    for src in sorted(atr):
        f.write(f"\n## {src}\n\n")
        for fam, x in sorted(atr[src].items()):
            pr = json.loads(x["provenance"])
            tyt = pr.get("title") or pr.get("attribution_statement", "")[:160]
            url = pr.get("url") or pr.get("source_url", "")
            jeden = lambda s: " ".join(str(s).split())
            f.write(f"- {jeden(tyt)} | {jeden(x['author'])} | {url} | {x['license']}\n")

man = {
    "nazwa": "korpus-rpg-v2 (fikcja, dramat, poezja, literatura o światach, SCP, SRD RPG)",
    "status": "KANDYDAT do niezależnej kontroli; nic nie opublikowano, brak commita i PR",
    "data_generacji": dt.date.today().isoformat(),
    "wejscie": {"plik": "korpus_koncowy.parquet", "sha256": R_WEJ, "wiersze": us["wszystkich_wierszy"], "tokeny_wejscia_licznik_16384": 3694528205, "tokeny_wejscia_v6_z_eot": us["tokeny_v6_wejscia"]},
    "tokeny_uwaga": "Kolumna n_tokens i liczby tokenów w tym manifeście są liczone tokenizerem Slayer v6 (32 768, sha256 0640d3bd…, karta slayer-1.07-pretrain), z jednym EOT na dokument. Wyjątek: pole tokeny_wejscia_licznik_16384.",
    "tokenizer": {"uzyty": {"sha256": tok_info["karta_107_v6"]["sha256"], "rozmiar_slownika": tok_info["karta_107_v6"]["rozmiar_slownika"], "zrodlo": tok_info["karta_107_v6"]["zrodlo"], "plik": "paczka-slayera/tokenizer.json"}, "porownanie_z_poprzednim_licznikiem": tok_info},
    "preregistracja": SK,
    "configi": {"default": {"zrodla": ["gutenberg", "rpg_cc_by"], "wierszy": wier_default, "tokeny": tok_default, "sa_w_default": 0}, "cc-by-sa": {"zrodla": ["scp", "rpg_sa"], "wierszy": wier_sa, "tokeny": tok_sa}},
    "splity": bud,
    "usuniete": us,
    "dekontaminacja": {"metoda": SK["dekontaminacja"], "testy": ind},
    "dedup_baz": {"metoda": SK["dedup_bazy"], "indeks": idx, "trafienia": us["baza_per_baza"], "detektor": us["baza_detektor"], "nieuruchomione": ["polskie części slayer-1.07-pretrain (pl_web, pl_replay_A, pl_replay_B)"]},
    "pii": {"okna": SK["pii"]["okna"], "decyzje": ner["liczby"], "usuniete_wiersze": len(ner["usun"]), "metoda_klasy": SK["pii"]["klasy_kandydatow"], "uwaga": "NER tylko na oknach; poza oknami SCP i RPG w całości, reszta Gutenberga bez NER"},
    "katalogi_indeksy_spisy_tabele": katalog,
    "kontrola_wstawionych": kon,
    "weryfikacja_koncowa": wer,
    "znane_wady": ["Config cc-by-sa: czyszczenie SCP nie jest stabilne (poprzednia budowa: 6 z 50 stron zmienia się przy ponownym czyszczeniu). Tekst SCP wzięty bez zmian; ponowne czyszczenie niewykonane.",
                   "13-gramy nie wykrywają parafraz benchmarków.",
                   "NER nie objął środka książek Gutenberga (wzór okien ze zlecenia).",
                   "Detektor katalogów i list ocenia całą część: krótki katalog zajmujący mniej niż 20% okien części zostaje w tekście, a część mieszana znika razem ze swoją prozą.",
                   f"Język: zostało {jezyk_po['inny_zostawione'] - jezyk_po['zostawione_z_obcy_wiekszym_niz_en']} wierszy o niskim udziale angielskich słów funkcyjnych bez przewagi obcych (poezja, dialekt, listy)."],
    "paczka_slayera": stan_pakiet,
    "budowa_poprzednia_skrot": pop,
}
json.dump(man, open(f"{KOR}/manifest.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)

# MANIFEST.md
with open(f"{KOR}/MANIFEST.md", "w", encoding="utf-8") as f:
    f.write("# korpus-rpg-v2: manifest\n\nStatus: kandydat; publikacja dopiero po PASS niezależnej kontroli sha256 z sha256.txt.\n\n")
    f.write(f"Wejście: sha256 `{R_WEJ}`, {us['wszystkich_wierszy']} wierszy.\n\n## Configi\n\n| config | split | wiersze | tokeny (v6) |\n|---|---|---:|---:|\n")
    for k in sorted(k for k in bud if "/" in k and isinstance(bud[k], dict) and "wierszy" in bud[k]):
        f.write(f"| {k.split('/')[0]} | {k.split('/')[1]} | {bud[k]['wierszy']} | {bud[k]['tokeny']} |\n")
    f.write(f"\nTokeny: {man['tokeny_uwaga']}\n\n## Usunięte wiersze\n\n| powód | wierszy | tokeny (v6) |\n|---|---:|---:|\n")
    for k, v in us["usuniete_wg_priorytetu"].items():
        f.write(f"| {k} | {v} | {us['tokeny_usuniete_wg_priorytetu'].get(k, 0)} |\n")
    f.write("\nPełne liczniki (wiersz może mieć kilka powodów): `" + json.dumps(us["pelne_liczniki"], ensure_ascii=False) + "`\n")
    f.write("\nPer źródło: `" + json.dumps(us["per_zrodlo"], ensure_ascii=False) + "`\n")
    f.write("\n## Dekontaminacja (13-gramy słów)\n\n| test | status | teksty | 13-gramy | wiersze z trafieniem |\n|---|---|---:|---:|---:|\n")
    for t, v in sorted(ind.items()):
        hit = us["ewal_per_test_wszystkie"].get(t, 0)
        if v["status"] == "OK":
            f.write(f"| {t} | OK | {v['tekstow']} | {v['ngramow_13']} | {hit} |\n")
        else:
            f.write(f"| {t} | BLOCKED: {str(v.get('powod',''))[:120]} |  |  |  |\n")
    f.write("\nKrótkie napisy (<13 słów, tylko policzone): `" + json.dumps(us["krotkie_napisy"]["dokumenty_z_trafieniem_per_dlugosc"], ensure_ascii=False) + "`\n")
    f.write("\n## Dedup wobec baz\n\n" + json.dumps(man["dedup_baz"], ensure_ascii=False, indent=1) + "\n")
    f.write("\n## PII\n\n" + json.dumps(man["pii"], ensure_ascii=False, indent=1) + "\n")
    f.write("\n## Katalogi wydawców, indeksy, spisy i tabele\n\n" + json.dumps(katalog, ensure_ascii=False, indent=1) + "\n")
    f.write("\n## Kontrola wstawionych duplikatów (na końcu)\n\n" + json.dumps(kon, ensure_ascii=False, indent=1) + "\n")
    f.write("\n## Weryfikacja końcowa\n\n" + json.dumps({k: v for k, v in wer.items() if k != 'splity'}, ensure_ascii=False, indent=1) + "\n")
    f.write("\n## Znane wady\n\n" + "\n".join(f"- {x}" for x in man["znane_wady"]) + "\n")
    f.write("\n## Paczka treningowa Slayera\n\n" + json.dumps(stan_pakiet, ensure_ascii=False, indent=1) + "\n")


def fmt(n):
    return f"{n:,}"


def do_tab(rows):
    return "\n".join("| " + " | ".join(str(c) for c in r) + " |" for r in rows)


ok_testy = sum(1 for v in ind.values() if v["status"] == "OK")
bl_testy = sorted(k for k, v in ind.items() if v["status"] != "OK")
rej = do_tab([["Project Gutenberg", "default", fmt(z_stat[("default", "gutenberg")]), fmt(z_tok[("default", "gutenberg")]), "Public domain (US status from catalogue metadata; author death year in `provenance`)"],
              ["Creative Commons RPG reference documents (Blades in the Dark, D&D SRD 5.2.1, Fate Toolkits)", "default", fmt(z_stat[("default", "rpg_cc_by")]), fmt(z_tok[("default", "rpg_cc_by")]), "CC-BY-3.0, CC-BY-4.0"],
              ["SCP Foundation Wiki", "cc-by-sa", fmt(z_stat[("cc-by-sa", "scp")]), fmt(z_tok[("cc-by-sa", "scp")]), "CC-BY-SA-3.0"],
              ["Cairn SRD", "cc-by-sa", fmt(z_stat[("cc-by-sa", "rpg_sa")]), fmt(z_tok[("cc-by-sa", "rpg_sa")]), "CC-BY-SA-4.0"]])

val_d = bud.get("default/validation", {}).get("wierszy", 0)
val_sa = bud.get("cc-by-sa/validation", {}).get("wierszy", 0)
yaml_cfg = """- config_name: default
  data_files:
  - split: train
    path: data/default/train-*.parquet
  - split: validation
    path: data/default/validation-*.parquet
- config_name: cc-by-sa
  data_files:
  - split: train
    path: data/cc-by-sa/train-*.parquet
  - split: validation
    path: data/cc-by-sa/validation-*.parquet"""

readme = f"""---
license: other
license_name: per-row
license_link: ATRYBUCJA.md
language:
- en
pretty_name: Fiction and RPG Pretraining Corpus v2
task_categories:
- text-generation
size_categories:
- 100K<n<1M
tags:
- fiction
- roleplaying-games
- pretraining
configs:
{yaml_cfg}
---

# Fiction and RPG Pretraining Corpus v2

English long-form fiction, drama, poetry, world-building nonfiction, and RPG reference text prepared for pretraining a small base model. Two configs keep share-alike material apart. `default` holds {fmt(wier_default)} rows and {fmt(tok_default)} tokens; `cc-by-sa` holds {fmt(wier_sa)} rows and {fmt(tok_sa)} tokens. Token counts use the Slayer v6 tokenizer (32,768 entries, SHA-256 prefix `0640d3bd`) with one end-of-text token per row.

## Sources and licenses

| source | config | rows | tokens | license |
|---|---|---:|---:|---|
{rej}

There is no blanket license on this dataset: each row carries its own `license` and attribution. `default` contains no share-alike rows; the checks are recorded in `manifest.json`.

## Fields

`document_id` stable row id. `source_id` origin of the row. `text` the document text. `register` genre grouping (fiction, drama, poetry, history-travel-folklore, shared-world-fiction, rpg-rules). `license` SPDX id, or `public-domain`. `license_url` license URL, empty for public-domain rows. `is_share_alike` true for CC-BY-SA rows. `author` author or attribution holder. `provenance` JSON with title, URL, attribution details, revision, and the changes applied to the text. `work_family` id shared by all rows of one work. `first_pub_year` first publication year where known. `content_tag` keyword-based tags. `n_tokens` tokens per row under the v6 tokenizer, including the end-of-text token.

Held-out rows go to `validation` deterministically (`sha1(work_family) mod 200 == 0`); no family appears in both splits. `paczka-slayera/` holds the tokenized `default` train split: `train.bin` (uint16 LE), `docs.idx` (uint64 LE end offsets), token 0 as end of text after each document, and the tokenizer used.

## Processing

1. Source selection: public-domain books by catalogue status plus author death year, CC BY and CC BY-SA RPG documents, and wiki pages with a confirmed page author.
2. Cleaning: edition headers and footers, transcription notes, wiki markup and template boilerplate removed; book parts cut to about 20-50 thousand characters. Text is not otherwise edited.
3. Deduplication: exact, MinHash editions and repeated-passage removal in the source build; here, MinHash and 13-word sketch against two other corpora, removing {us['usuniete_wg_priorytetu'].get('baza', 0)} rows.
4. Evaluation hygiene: 13-word overlap against {ok_testy} evaluation sets removed {us['usuniete_wg_priorytetu'].get('ewal', 0)} rows; shorter strings were counted only. Sets that could not be fetched are listed as BLOCKED in the manifest.
5. Quality and privacy: rows with a trademark string, foreign-language text, or character corruption were removed, and the final check requires zero rows with a corrupted-character pattern. A density detector removed {fmt(kat_wiersze)} book parts ({fmt(kat_tokeny)} tokens) that were publisher catalogues, indexes, contents lists, or tables; in a final check on {kat_neg['probka'].split()[0]} random fiction rows it flagged {kat_neg['oznaczone']}. Named-entity recognition on paratext windows checked for contemporary private individuals.

## Attribution

Follow the per-row `license` and `provenance`. `ATRYBUCJA.md` lists one line per work family; verbatim CC BY statements are stored in `provenance.attribution_statement`. Public-domain sources are named only to credit their origin and do not imply endorsement.

## Limitations

Public-domain status was checked against US catalogue status and a life-plus-70-years test on author and translator death dates. Copyright differs by country and catalogue data can be wrong; this card is not legal advice. Whether CC BY-SA obligations extend to model weights is unresolved; `cc-by-sa` is separated so that it can be included or excluded by choice. The SCP cleaning step is not stable when repeated, a known flaw in that config. Word-overlap filtering does not catch paraphrases, named-entity checks did not cover the bodies of books, and a catalogue shorter than a fifth of a book part stays in the text. {len(bl_testy)} evaluation sets could not be scanned and are listed in the manifest. The corpus is English-only and historically skewed; older language and attitudes are present and tagged only by keyword search.

## Takedown

To request removal of a work or report a rights or privacy problem, open a discussion on this repository with the `document_id` and the reason.
"""
slow = len(readme.split("---", 2)[2].split())
with open(f"{KOR}/README.md", "w", encoding="utf-8") as f:
    f.write(readme)
print("README slow:", slow)

# sha256 (ostatni krok, liczy wszystkie pliki poza sha256.txt)
wyj = []
for root, _, pliki in os.walk(KOR):
    for p in sorted(pliki):
        if p == "sha256.txt" or p == "liczby_budowy.json":
            continue
        fp = os.path.join(root, p)
        h = hashlib.sha256()
        with open(fp, "rb") as x:
            for b in iter(lambda: x.read(1 << 22), b""):
                h.update(b)
        wyj.append((h.hexdigest(), os.path.relpath(fp, KOR)))
with open(f"{KOR}/sha256.txt", "w", encoding="utf-8") as f:
    for h, p in sorted(wyj, key=lambda t: t[1]):
        f.write(f"{h}  {p}\n")
if os.path.exists(f"{KOR}/liczby_budowy.json"):
    os.replace(f"{KOR}/liczby_budowy.json", f"{WN}/liczby_budowy.json")
print("OK", len(wyj))
