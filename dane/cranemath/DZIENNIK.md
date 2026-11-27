# Dziennik zbioru: CraneMath (EN, przepisana matematyka) dla microannealu Slayera 1B

Przepis: [`METODOLOGIA.md` w repo zespołu](https://github.com/slayerlabs/benchmarks-fabryka-ai/blob/main/research/slayer-1b/dane/METODOLOGIA.md).
Karta źródła: [`KARTA_ZRODLA.md`](KARTA_ZRODLA.md). Reguły: [`skrypty/preregistracja.json`](skrypty/preregistracja.json).
Skrypty wspólne trzech zbiorów #346 (FineMath-4+, CraneMath, Stack-Edu Python): [`../matematyka-wspolne/skrypty/`](../matematyka-wspolne/skrypty/),
każdy krok to `bash dane/matematyka-wspolne/skrypty/odtworz.sh <krok> cranemath`. Logi kroków: `robocze/logi/` (poza gitem).
Dzienniki bliźniacze: [FineMath-4+](../finemath4/DZIENNIK.md), [Stack-Edu Python](../stackedu/DZIENNIK.md).

## Bramki praw

| bramka | wynik |
|---|---|
| Można TRENOWAĆ | TAK (wyjątek TDM art. 4 dyr. 2019/790 dla stron źródłowych; ODC-By kompilacji i Apache-2.0 generatora nie blokują; takedown po `metadata.url` i `id`); opt-out TDM NIE SPRAWDZONY |
| Można ZGŁOSIĆ do `dataset-team-submissions` | NIEROZSTRZYGNIĘTY: brak licencji per dokument, teksty to przepisania stron o nieznanych licencjach |

## 1. Rezerwacja

| | |
|---|---|
| Co | issue [#346](https://github.com/slayerlabs/benchmarks-fabryka-ai/issues/346) na tablicy Dataset team (In progress); wiersz „w budowie” w PR [#347](https://github.com/slayerlabs/benchmarks-fabryka-ai/pull/347) |
| Poprawki | 24.11.2026 PR #347 poprawiony wg uwag Elwenor: tytuł Conventional Commits, opis z szablonu po angielsku; PR policy pass |
| Cel | ramię C microannealu (paper mat./med. 1.2): +15% matematyki przepisanej otwartym modelem, cel eksportu 400 mln tokenów v6 |

## 2. Karta źródła

[`KARTA_ZRODLA.md`](KARTA_ZRODLA.md), 24.11.2026, przed pobraniem (commit `6988094`). `allenai/dolma3_dolmino_mix-100B-1125@f23aa129`,
`data/ingredient1-cranemath/*.jsonl.zst` (192 pliki); generator Qwen/Qwen3-32B (rewizja nieopublikowana), tekst przed
przepisaniem w `metadata.original_text`. Trenować: TAK; zgłosić: NIEROZSTRZYGNIĘTY.

## 3. Preregistracja

[`skrypty/preregistracja.json`](skrypty/preregistracja.json), commit `6988094`: reguły jak FineMath-4+, seed 20261124, cel puli 600 mln,
eksportu 400 mln tokenów v6. Odstępstwa: dwa powody 13-gramowe (`ewal_13gram` na tekście i `ewal_13gram_oryginal` na tekście
przed przepisaniem), powód `think` (znaczniki think), dedup wobec 1.07 tylko po tekście przepisanym; w ręcznej próbce
dodatkowo przepisanie z błędem matematycznym albo sprzeczne z oryginałem ≤ 10% i górna granica Wilsona ≤ 20%.

| aneks | commit | zapisany | treść |
|---|---|---|---|
| `aneks_2026_11_24` | `f159b6e` | przed odczytem agregacji | `dedup_english_technical`, `dedup_fineweb_edu_109` po url strony źródłowej przepisania |
| `aneks_2026_11_24b` | `8191660` | po przeglądzie odrzuconych | `min_tresc`, `szablon_forum` (stopki phpBB/GMAT Club/The Student Room, powitania czatbota, < 200 słów) |
| `aneks_2026_11_24c` | `63da6ec` | po przeglądzie zachowanych, przed eksportem | `suma40` (zmyślone zadanie „suma 1..40 = 820”), `pii_zaciemniony`; FAIL przepisań przyjęty jako cecha ramienia |
| `aneks_2026_11_25` | `1a28fbd` | po próbce kontrolnej 200, przed eksportem | `suma40`: warunek na oryginał zmieniony z „brak liczby 40” na „brak zadania o sumie do 40” |
| `aneks_2026_11_25b` | `753d40d` (01:32) | przed policzeniem nowego powodu na puli (`agreguj_8x3b.log` 01:50) | `dedup_slayer_8x3b_en` jak [FineMath-4+](../finemath4/DZIENNIK.md) → `aneks_2026_11_25b` (angielska część Slayera 1.00-1.06, `slayer-pl-8x3b@d50df04a` `shared/en.parquet`, 2 384 000 dok.) |

## 4. Środowisko

| | |
|---|---|
| Komenda | `odtworz.sh venv` (wspólny venv `../matematyka-wspolne/robocze/venv`) |
| Wersje | Python 3.12, [`../matematyka-wspolne/requirements.txt`](../matematyka-wspolne/requirements.txt) (numpy 2.5.4, pyarrow 26.0.1, tokenizers 0.23.3, huggingface_hub 2.4.0, zstandard, ftfy 6.3.1) |
| Tokenizer | v6 sha256 `0640d3bd…815dd` z katalogu roboczego DCLM-EN, sprawdzany w `ewal_pobierz` |
| Sprawdzenie | porównanie `pip freeze` = `requirements.txt`: nie zmierzono |
| Eksport | osobny venv repo zgłoszeń (`dane/pr-zgloszenia/venv`, Presidio, spaCy `en_core_web_lg`); wersje nie zapisane w tym katalogu |

## 5. Pobranie

| | |
|---|---|
| Komenda | `odtworz.sh pula cranemath`, 24.11.2026 (log `pula.log`, 19:49) |
| Kod wyjścia | Python: `KONIEC 663285 623303464`; bash: kod 2 PO `KONIEC` (edycja `odtworz.sh` w trakcie); dane pełne |
| Liczby | 23 pliki z 192 w kolejności `default_rng(20261124)`, rewizja `f23aa129`; 663 285 dokumentów, 623 303 464 tokenów v6; każdy plik w dwóch wersjach (tekst i oryginał) |
| Wynik | [`wyniki/probka_pliki.json`](wyniki/probka_pliki.json) (sha256 i wiersze każdego pliku) |

## 6. Indeksy i kontrole

- Testy (wspólne): `odtworz.sh ewal_pobierz` 24.11.2026: indeks RPG v2 (60 testów, dowiązania do pobrań DCLM-EN) + T51 GSM-Plus i T52 GSM1k, oba `OK`, razem 62 pozycje statusu, `KONIEC`; `odtworz.sh ewal`: `ogolem 33302686` 13-gramów, `KONIEC` (bash kod 2 po `KONIEC`, ta sama pułapka co w `pula`).
- EN 1.07 (`idx`) i walidacja Fabryki (`idx_wal`): indeksy z katalogu roboczego DCLM-EN, bez zmian.
- Bazy z aneksu 24.11 (`bazy_mat.py`): `entech` (english-technical-1b@3b833d36) `KONIEC 209939`; `fwe109` (url FineWeb-Edu 1.09) `KONIEC 266 98512010` (266 plików, 24.11.2026 23:51; po przejściu na zakresy bajtów). Baza z aneksu 25.11b: `en8x3b` (2 384 000 dok., 25.11.2026 01:28).
- Kontrola dodatnia `odtworz.sh kontrola cranemath`: 16/16 przed aneksem (commit `9b7d6bd`), 22/22 po aneksach 24.11-25.11, po aneksie
  25.11b **23/23** ([`wyniki/kontrola.json`](wyniki/kontrola.json)): przypadki FineMath (w tym K_en8x3b) plus K_think, K_gsm8k_oryg
  (treść GSM8K tylko w oryginale), K_forum, K_suma40.

## 7. Przebieg

| | |
|---|---|
| Komenda | `odtworz.sh przebieg cranemath` (6 procesów), 24.11.2026; drugi przebieg 13-gramów na oryginale |
| Wynik | 147/147 jednostek, `KONIEC 888s` (log `przebieg.log`, 20:30); kod wyjścia nie zapisany w logu |
| `ew13` | tekst: `dokumentow 663285 z_trafieniem 11113 ngramow 15053`; oryginał: `z_trafieniem 20957 ngramow 90132`; oba `KONIEC` |

## 8. Po przebiegu

Komenda `odtworz.sh agreguj cranemath`; końcowy przebieg 25.11.2026 01:50 (`agreguj_8x3b.log`, po aneksie 25.11b),
wynik [`wyniki/agreguj.json`](wyniki/agreguj.json):

| powód | odrzucone dok. | odrzucone tok. v6 | zostaje dok. | zostaje tok. v6 | % tok. | niezależnie dok. / % tok. |
|---|---|---|---|---|---|---|
| `walidacja_fabryki` | 920 | 163 125 | 662 365 | 623 140 339 | 99,974 | 920 / 0,026 |
| `domena_testow` | 4 800 | 4 793 803 | 657 565 | 618 346 536 | 99,205 | 4 800 / 0,769 |
| `ewal_13gram` | 7 037 | 8 144 579 | 650 528 | 610 201 957 | 97,898 | 7 084 / 1,318 |
| `ewal_13gram_oryginal` | 7 209 | 7 760 745 | 643 319 | 602 441 212 | 96,653 | 8 891 / 1,587 |
| `think` | 37 231 | 147 825 856 | 606 088 | 454 615 356 | 72,936 | 38 660 / 24,403 |
| `min_tresc` | 5 312 | 753 152 | 600 776 | 453 862 204 | 72,816 | 5 943 / 0,132 |
| `szablon_forum` | 309 | 77 697 | 600 467 | 453 784 507 | 72,803 | 1 641 / 0,039 |
| `suma40` | 34 020 | 11 541 195 | 566 447 | 442 243 312 | 70,952 | 36 725 / 2,643 |
| `pii` | 349 | 564 581 | 566 098 | 441 678 731 | 70,861 | 392 / 0,111 |
| `pii_zaciemniony` | 0 | 0 | 566 098 | 441 678 731 | 70,861 | 1 / 0,001 |
| `mojibake` | 9 | 7 999 | 566 089 | 441 670 732 | 70,86 | 23 / 0,011 |
| `dedup_wewnatrz` | 516 | 817 330 | 565 573 | 440 853 402 | 70,729 | 4 351 / 0,268 |
| `dedup_slayer107` | 322 | 425 560 | 565 251 | 440 427 842 | 70,66 | 1 360 / 0,113 |
| `dedup_slayer_8x3b_en` | 0 | 0 | 565 251 | 440 427 842 | 70,66 | 1 / 0,0 |
| `dedup_english_technical` | 0 | 0 | 565 251 | 440 427 842 | 70,66 | 115 / 0,021 |
| `dedup_fineweb_edu_109` | 43 270 | 32 432 171 | 521 981 | 407 995 671 | 65,457 | 50 628 / 7,129 |

- **Uzysk: 521 981 dok., 407 995 671 tokenów v6 (65,457%)**. Do eksportu wybrano 511 710 dok., 400 000 473 tokenów v6 (wystarcza).
- `ewal_13gram` per test (tekst): MATH 5458, MathQA 879, MMLU 461, MBPP 212, HumanEval 82, reszta ≤ 35; na oryginale: MathQA 4081, MATH 3030, BoolQ 524, MMLU 334, SciQ 286, MBPP 264, HumanEval 181.
- PII wg detektora DCLM: e-mail 178, telefon 50, IP 178 (tryb `usun`). `dedup_wewnatrz`: 2218 identycznych, 2133 przez MinHash.
- Ograniczenie: wiersze z url bez schematu (ok. 1,3%) nie mogły być porównane po url z FineWeb-Edu 1.09 (`dedup_fineweb_edu_109`).
- `dedup_slayer_8x3b_en` (aneks 25.11b): 0 dok. w kaskadzie, 1 niezależnie; uzysk i wybór do eksportu bez zmian. Przeglądu odrzuconych tego powodu nie było (brak odrzuconych w kaskadzie).

### Przegląd odrzuconych (24.11.2026)

Dwóch recenzentów, 100 na powód (`mojibake`: 23, tyle było); [`wyniki/przeglad_odrzuconych_1.json`](wyniki/przeglad_odrzuconych_1.json). Kolumna „koszt” = % tokenów v6 puli z powodem niezależnie. Progi z preregistracji: fałszywe odrzucenia ≤10% ORAZ górna granica Wilsona ≤20%.

| powód | n | A: fałszywe (wątpliwe) | A: stopa [Wilson 95%] | B: fałszywe (wątpliwe) | B: stopa [Wilson 95%] | werdykt A/B | koszt % tok. |
|---|---|---|---|---|---|---|---|
| `walidacja_fabryki` | 100 | 95 (0) | 95,0% [88,8; 97,8] | 93 (7) | 93,0% [86,3; 96,6] | FAIL/FAIL | 0,026 |
| `domena_testow` | 100 | 0 (0) | 0,0% [0; 3,7] | 0 (0) | 0,0% [0; 3,7] | PASS/PASS | 0,769 |
| `ewal_13gram` | 100 | 76 (8) | 76,0% [66,8; 83,3] | 79 (3) | 79,0% [70,0; 85,8] | FAIL/FAIL | 1,318 |
| `ewal_13gram_oryginal` | 100 | 36 (9) | 36,0% [27,3; 45,8] | 29 (14) | 29,0% [21,0; 38,5] | FAIL/FAIL | 1,587 |
| `think` | 100 | 0 (4) | 0,0% [0; 3,7] | 0 (4) | 0,0% [0; 3,7] | PASS/PASS | 24,403 |
| `pii` | 100 | 55 (16) | 55,0% [45,2; 64,4] | 52 (19) | 52,0% [42,3; 61,5] | FAIL/FAIL | 0,111 |
| `mojibake` | 23 | 14 (0) | 60,9% [40,8; 77,8] | 7 (7) | 30,4% [15,6; 50,9] | FAIL/FAIL | 0,011 |
| `dedup_wewnatrz` | 100 | 8 (1) | 8,0% [4,1; 15,0] | 9 (0) | 9,0% [4,8; 16,2] | PASS/PASS | 0,268 |
| `dedup_slayer107` | 100 | 18 (57) | 18,0% [11,7; 26,7] | 61 (5) | 61,0% [51,2; 70,0] | FAIL/FAIL | 0,113 |
| `dedup_english_technical` | 100 | 23 (77) | 23,0% [15,8; 32,2] | 77 (23) | 77,0% [67,8; 84,2] | FAIL/FAIL | 0,021 |

`min_tresc`, `szablon_forum`, `suma40`, `pii_zaciemniony`, `dedup_fineweb_edu_109` powstały lub dostały bazę po tej próbce: nie
zmierzono. **Werdykt: NIE PRZESZŁO** (8 z 10 powodów FAIL). Odrzucone `walidacja_fabryki` (93-95/100) i `dedup_slayer107` (57-61/100)
to głównie stopki forów i powitania czatbota zamiast treści (aneks 24.11b).

### Aneks 24.11b (commit `8191660`)

`min_tresc` i `szablon_forum`. FAIL `walidacja_fabryki`, `dedup_slayer107`, `dedup_english_technical`, `mojibake` przyjęty: odrzucone
teksty to głównie szablony bez treści, koszt łącznie ok. 0,2% tokenów. `ewal_13gram` kosztuje 1,3% + 1,6% tokenów.

### Przegląd 300 zachowanych (24.11.2026)

Z agregacji wstępnej (bez `dedup_fineweb_edu_109`); [`wyniki/przeglad_zachowanych_1.json`](wyniki/przeglad_zachowanych_1.json).

| miara | A | B | próg | werdykt |
|---|---|---|---|---|
| jakość tak / wątpliwy / nie | 269 / 25 / 6 | 258 / 34 / 8 | — | — |
| śmieci | 6: 2,0% [0,9; 4,3] | 8: 2,7% [1,4; 5,2] | ≤ 10% | PASS |
| przeoczone PII | 0/300 | 0/300 | 0/300 | PASS |
| przeoczony test | 0/300 | 1/300 | — | zgłoszenie nie potwierdzone w teście MATH (grep 24.11) |
| przepisanie: poprawne / błąd mat. / wątpliwe / sprzeczne | 200 / 28 / 38 / 34 | 214 / 23 / 26 / 37 | — | — |
| przepisania błędne (błąd + sprzeczne) | 62: 20,7% [16,5; 25,6] | 60: 20,0% [15,9; 24,9] | ≤ 10% | FAIL |

### Aneks 24.11c (commit `63da6ec`)

- `suma40`: generator wstawiał to samo zmyślone zadanie „suma 1..40 = 820” w miejsce stron bez zadania (19-20 z 71 przepisań
  sprzecznych). Przed regułą [`wyniki/wzorzec_suma40.json`](wyniki/wzorzec_suma40.json): 36 801 trafień w puli, 28 618 z 529 328 wybranych (5,406%).
  Warunek: tekst pasuje ORAZ oryginał nie zawiera liczby 40.
- `pii_zaciemniony` jak FineMath.
- FAIL przepisań przyjęty z zapisem: cecha CraneMath, na którym Olmo 3 zmierzyło efekt microannealu; naprawa wymaga ponownej
  generacji z weryfikacją; odsetek w datasheet; zadanie przed częścią 2, jeśli C wygra.
- Próbka kontrolna 200 z polem `suma40` na 100 pierwszych.

### Próbka kontrolna 200 (25.11.2026)

Po agregacji końcowej (`agreguj_koncowe.log`, 00:09: 528 214 dok., 410 273 160 tokenów v6); oceny `robocze/przeglad/oceny_A|B/kontr_*.json`.

| miara | A | B | próg | werdykt |
|---|---|---|---|---|
| przeoczone PII | 0/200 | 0/200 | 0/200 | PASS |
| przeoczony test | 0/200 | 0/200 | — | aneks 25.11: zgłoszenie nr 187012 bez odpowiednika w teście MATH (grep 25.11) |
| `suma40` w zachowanych | 1/100 (nr 301032) | 1/100 (nr 301032) | — | aneks 25.11 wymienia też nr 359177: oryginał zawiera gdzieś liczbę 40 |

### Aneks 25.11 (commit `1a28fbd`)

Warunek `suma40` na oryginał zastąpiony wzorcem zadania o sumie do 40. Pomiar przed zmianą
([`wyniki/suma40_reszta.json`](wyniki/suma40_reszta.json)): 6136 wybranych pasuje do wzorca tekstu, 58 ma zadanie w oryginale, 6078 do
usunięcia. Ponowna `agreguj` (00:17): `suma40` w kaskadzie 34 020 dok., zostaje 521 981 / 407 995 671. Nowej próbki po tej zmianie: nie zmierzono.

## 9. Eksport

| | |
|---|---|
| Komenda | `odtworz.sh eksport cranemath`, końcowy log `eksport.log` 25.11.2026 02:19 |
| Key | `cranemath_en`; datasheet [`eksport/cranemath_en.md`](eksport/cranemath_en.md) |
| Bramka językowa | `min_chars: 200` w rejestrze (po błędzie krótkich wierszy w pierwszej próbie FineMath) |
| Liczby | 510 129 dok., 1 120 137 336 znaków, 363 789 411 tokenów cl100k; `language` en, `text_origin` synthetic; `dropped`: `wrong_language` 1574, `placeholder_only` 7, reszta 0 (511 710 − 1581 = 510 129) |
| PII | `pii.pass` = `none` (Presidio nie uruchomione); usuwanie wcześniej w kaskadzie |
| Wynik | [`wyniki/eksport_stats.json`](wyniki/eksport_stats.json); sha256 parquet `1aecacfa36842b3be24a06f5a08430a342d45d08d252df3a8d10aac745767e8f` ([`wyniki/eksport_sha256.txt`](wyniki/eksport_sha256.txt)); wcześniejszy eksport (00:48): `2f42e38f…` |
| `derived_from` | dla wierszy z url bez schematu (ok. 1,3%) to rekord WARC `https://data.commoncrawl.org/<warc_filename>#offset=<offset>` ([`../matematyka-wspolne/eksport/src/clean_cranemath_en.py`](../matematyka-wspolne/eksport/src/clean_cranemath_en.py)); błąd `malformed derived_from` (6801 w eksporcie z 00:48) zniknął |

## 10. Kontrola końcowa

| | |
|---|---|
| Komenda | w `odtworz.sh eksport`: `pytest src/test_cranemath_en_contract.py -q` i `python src/check.py --source cranemath_en` |
| Test kontraktowy | 1 passed |
| `check.py` | kod 1 tylko z DWÓCH oczekiwanych przyczyn: (1) ponowny skan PII Presidio — 8 z 200 skanowanych dokumentów, same telefony (liczby), brak trafień kategorii pii (sprawdzone 25.11); (2) „stats.json pii has no presidio record” — Presidio wyłączone świadomie (403 trafienia PhoneRecognizer w 300 dok. FineMath) |
| Niezależny agent na pliku o tym samym sha256 | nie zmierzono |

## 11. Wysyłka (repo do wglądu Arka)

| | |
|---|---|
| Repo | `Lolita67/cranemath_en-robocze`, bramka `manual`, README jednym zdaniem |
| Bramka | anonimowe pobranie dostaje 401 (sprawdzone curl); 24.11 repo było przez ok. 3 min bez bramki (założył je upload, bo skrypt zakładający repo przerwał się po pierwszym), bramka ustawiona po wykryciu |
| Dostęp | `grant_access` dla `Maggio33` (Arek): czeka na Anię (UI); token sesji OAuth dostaje 401 na `grant_access` |
| Gotowe gdy | Arek ma link i dostęp: NIE (czeka na dostęp) |

## 12. Dane treningowe

PR [#353](https://github.com/slayerlabs/benchmarks-fabryka-ai/pull/353): status wiersza „u Arka do wglądu” z linkiem do repo. PR
rezerwacji [#347](https://github.com/slayerlabs/benchmarks-fabryka-ai/pull/347) scalony. Sprawdzenie, czy każdy link w wierszu odpowiada 200:
nie zmierzono (repo za bramką zwraca 401 anonimowo).

## Historia odtworzeń

- 24.11.2026 19:38: karta i preregistracja (`6988094`); 19:49 `pula` (kod 2 po `KONIEC`).
- 24.11.2026 20:30–20:31: `przebieg` 147/147 i przebieg oryginału, `ew13`; pierwsza `agreguj` przerwana: `AssertionError: powody bez detektora: dedup_english_technical, dedup_fineweb_edu_109` (powody z aneksu 24.11 przed zbudowaniem baz).
- 24.11.2026 20:42: `agreguj_wstepne` (`entech`, `fwe109` pusty): 601 511 dok., 452 063 451 tokenów v6.
- 24.11.2026 20:55: `agreguj_wstepne2` (aneks 24.11b): 597 543 / 451 586 981; przegląd odrzuconych i zachowanych.
- 25.11.2026 00:09: `agreguj_koncowe` (aneks 24.11c, url FineWeb-Edu 1.09): 528 214 / 410 273 160; próbka kontrolna 200.
- 25.11.2026 00:17: `agreguj_koncowe2` (aneks 25.11): 521 981 / 407 995 671.
- 25.11.2026 00:48: eksport, test kontraktowy 1 passed, `check.py` kod 1 (dwa oczekiwane błędy, 6801 `malformed derived_from`); commit `1a28fbd`.
- 25.11.2026 01:28–01:50: aneks 25.11b (`753d40d`), baza `en8x3b`, kontrola 23/23, `agreguj_8x3b`: 521 981 / 407 995 671 (bez zmian).
- 25.11.2026 02:19: eksport końcowy z `derived_from` z rekordu WARC: 510 129 dok., sha256 `1aecacfa…`; test kontraktowy 1 passed; `check.py` kod 1 (dwa oczekiwane błędy).

## Pułapki tego przebiegu

- Nie edytuj `odtworz.sh`, gdy którykolwiek krok jest w toku: bash czyta skrypt przyrostowo; edycja w trakcie `pula` i `ewal` dała kod 2 (`syntax error near unexpected token`) PO `KONIEC`.
- macOS ma bash 3.2: pusta tablica przy `set -u` daje „unbound variable”; stąd `${ORYG[@]+"${ORYG[@]}"}`.
- Pobieranie url FineWeb-Edu przez `HfFileSystem` z `block_size` 8 MB trwało 7 min/plik; zakresy bajtów skróciły to do 31 s/plik, potem CDN zwracał 429/400: czekanie i ponowienia.
- Agenci recenzenci: 5 odmów klasyfikatora przy pierwszym uruchomieniu (ponowione raz, przeszły); część recenzentów czytała pozycje częściowo.
- Presidio w eksporcie maskuje liczby w matematyce i kodzie jako telefony (403 trafienia PhoneRecognizer w 300 dok. FineMath): wyłączone świadomie, `check.py` kończy się kodem 1 na dwóch oczekiwanych błędach (krok 10).
- Repo do wglądu zakładaj z bramką przed uploadem: 24.11 dwa repo (`cranemath_en`, `stack_edu_python`) były przez ok. 3 min bez bramki, bo skrypt zakładający repo przerwał się po pierwszym, a pozostałe założył upload.
- Url w CraneMath bywa bez schematu (sama domena): `derived_from` trzeba brać z rekordu WARC, a porównanie po url z FineWeb-Edu takich wierszy nie obejmuje.

## Repo po scaleniu (26.11)

`Lolita67/cranemath_en-robocze` usunięte 26.11. Ten sam plik parquet (sha256 LFS zgodny) leży w `Lolita67/math-code-en` (do 27.11 `Lolita67/matematyka-kod-en-robocze`), katalog `mikroanneal/cranemath_en`.
