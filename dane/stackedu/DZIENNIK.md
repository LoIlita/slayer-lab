# Dziennik zbioru: Stack-Edu Python dla microannealu Slayera 1B

Przepis: [`METODOLOGIA.md` w repo zespołu](https://github.com/slayerlabs/benchmarks-fabryka-ai/blob/main/research/slayer-1b/dane/METODOLOGIA.md).
Karta źródła: [`KARTA_ZRODLA.md`](KARTA_ZRODLA.md). Reguły: [`skrypty/preregistracja.json`](skrypty/preregistracja.json).
Skrypty wspólne trzech zbiorów #346 (FineMath-4+, CraneMath, Stack-Edu Python): [`../matematyka-wspolne/skrypty/`](../matematyka-wspolne/skrypty/),
każdy krok to `bash dane/matematyka-wspolne/skrypty/odtworz.sh <krok> stackedu`. Logi kroków: `robocze/logi/` (poza gitem).
Dzienniki bliźniacze: [FineMath-4+](../finemath4/DZIENNIK.md), [CraneMath](../cranemath/DZIENNIK.md).

## Bramki praw

| bramka | wynik |
|---|---|
| Można TRENOWAĆ | TAK (licencja per plik z listy Blue Oak; zapasowo wyjątek TDM; takedown po `id` = `blob_id` albo `repo_name`) |
| Można ZGŁOSIĆ do `dataset-team-submissions` | TAK, warunkowo: wiersze z niepustą licencją per plik z listy Blue Oak (bez NC/ND); puste licencje odrzucone powodem `licencja`; opt-out TDM per repo NIE SPRAWDZONY |

## 1. Rezerwacja

| | |
|---|---|
| Co | issue [#346](https://github.com/slayerlabs/benchmarks-fabryka-ai/issues/346) na tablicy Dataset team (In progress); wiersz „w budowie” w PR [#347](https://github.com/slayerlabs/benchmarks-fabryka-ai/pull/347) |
| Poprawki | 24.11.2026 PR #347 poprawiony wg uwag Elwenor: tytuł Conventional Commits, opis z szablonu po angielsku; PR policy pass |
| Cel | ramię D microannealu (paper mat./med. 1.2, decyzja M3): +10% kodu Python z licencją per plik, cel eksportu 250 mln tokenów v6 |

## 2. Karta źródła

[`KARTA_ZRODLA.md`](KARTA_ZRODLA.md), 24.11.2026, przed pobraniem (commit `6988094`). `common-pile/stackv2_edu_filtered@c354dbe8`,
pliki Pythona `stack-edu-0073..0084.json.gz` (12). Trenować: TAK; zgłosić: TAK warunkowo.

## 3. Preregistracja

[`skrypty/preregistracja.json`](skrypty/preregistracja.json), commit `6988094`: seed 20261124, cel puli 600 mln, eksportu 250 mln
tokenów v6. Odstępstwa od FineMath: PII maskowane zamiast usuwania, powody `licencja`, `sekrety`, `wygenerowany`, `int_score` (< 3),
brak `domena_testow`; w zachowanych liczone przeoczone sekrety (cel 0/300) zamiast PII.

| aneks | commit | zapisany | treść |
|---|---|---|---|
| `aneks_2026_11_24` | `f159b6e` | przed odczytem agregacji | `dedup_english_technical` (główna baza dla Pythona), `dedup_fineweb_edu_109` dla jednolitości |
| `aneks_2026_11_24b` | `8191660` | po przeglądzie odrzuconych | `min_tresc` (puste `__init__.py`, pliki z samą licencją); reguły z FAIL precyzji przyjęte, koszt ok. 1,7% tokenów |
| `aneks_2026_11_24c` | `63da6ec` | po przeglądzie zachowanych, przed eksportem | `haslo_w_kodzie`; próbka kontrolna 200 |
| `aneks_2026_11_25b` | `753d40d` (01:32) | przed policzeniem nowego powodu na puli (`agreguj_8x3b.log` 01:42) | `dedup_slayer_8x3b_en` jak [FineMath-4+](../finemath4/DZIENNIK.md) → `aneks_2026_11_25b` (angielska część Slayera 1.00-1.06, `slayer-pl-8x3b@d50df04a` `shared/en.parquet`, 2 384 000 dok.) |

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
| Komenda | `odtworz.sh pula stackedu`, 24.11.2026 (log `pula.log`, 19:47) |
| Kod wyjścia | Python: `KONIEC 639779 988588081`; bash: kod 2 PO `KONIEC` (edycja `odtworz.sh` w trakcie); dane pełne |
| Liczby | 1 plik z 12 w kolejności `default_rng(20261124)`: `stack-edu-0080.json.gz` (971 712 713 B), rewizja `c354dbe8`; 639 779 plików Pythona, 988 588 081 tokenów v6 |
| Wynik | [`wyniki/probka_pliki.json`](wyniki/probka_pliki.json) (sha256) |

## 6. Indeksy i kontrole

- Testy (wspólne): `odtworz.sh ewal_pobierz` 24.11.2026: indeks RPG v2 (60 testów, dowiązania do pobrań DCLM-EN) + T51 GSM-Plus i T52 GSM1k, oba `OK`, razem 62 pozycje statusu, `KONIEC`; `odtworz.sh ewal`: `ogolem 33302686` 13-gramów, `KONIEC` (bash kod 2 po `KONIEC`, ta sama pułapka co w `pula`).
- EN 1.07 (`idx`) i walidacja Fabryki (`idx_wal`): indeksy z katalogu roboczego DCLM-EN, bez zmian.
- Bazy z aneksu 24.11 (`bazy_mat.py`): `entech` (english-technical-1b@3b833d36) `KONIEC 209939`; `fwe109` (url FineWeb-Edu 1.09) `KONIEC 266 98512010` (266 plików, 24.11.2026 23:51; po przejściu na zakresy bajtów). Baza z aneksu 25.11b: `en8x3b` (2 384 000 dok., 25.11.2026 01:28).
- Kontrola dodatnia `odtworz.sh kontrola stackedu`: 17/17 przed aneksem (commit `9b7d6bd`), 21/21 po aneksach 24.11, po aneksie 25.11b
  **22/22** ([`wyniki/kontrola.json`](wyniki/kontrola.json)): K_czysty, para K_dup_a/K_dup_b, K_kopia_107, K_walidacja, K_gsm8k, K_math,
  K_gsm_plus, K_gsm1k, K_mmlu, K_email (zostaje, liczony), K_humaneval, K_mbpp, K_aws, K_generated, K_licencja, K_int_score, K_entech,
  K_en8x3b, K_fwe109, K_pusty, K_haslo.

## 7. Przebieg

| | |
|---|---|
| Komenda | `odtworz.sh przebieg stackedu` (6 procesów), 24.11.2026 |
| Wynik | 128/128 jednostek, `KONIEC 593s` (log `przebieg.log`, 20:07); kod wyjścia nie zapisany w logu |
| `ew13` | `dokumentow 639779 z_trafieniem 4392 ngramow 9858`, `KONIEC` |

## 8. Po przebiegu

Komenda `odtworz.sh agreguj stackedu`; końcowy przebieg 25.11.2026 01:42 (`agreguj_8x3b.log`, po aneksie 25.11b), wynik
[`wyniki/agreguj.json`](wyniki/agreguj.json):

| powód | odrzucone dok. | odrzucone tok. v6 | zostaje dok. | zostaje tok. v6 | % tok. | niezależnie dok. / % tok. |
|---|---|---|---|---|---|---|
| `licencja` | 3 278 | 5 306 732 | 636 501 | 983 281 349 | 99,463 | 3 278 / 0,537 |
| `walidacja_fabryki` | 1 725 | 902 542 | 634 776 | 982 378 807 | 99,372 | 1 730 / 0,091 |
| `ewal_13gram` | 524 | 1 426 367 | 634 252 | 980 952 440 | 99,228 | 527 / 0,145 |
| `sekrety` | 300 | 1 009 334 | 633 952 | 979 943 106 | 99,126 | 305 / 0,103 |
| `haslo_w_kodzie` | 3 667 | 8 129 734 | 630 285 | 971 813 372 | 98,303 | 3 707 / 0,832 |
| `wygenerowany` | 4 089 | 13 286 581 | 626 196 | 958 526 791 | 96,959 | 4 123 / 1,376 |
| `min_tresc` | 40 051 | 3 681 755 | 586 145 | 954 845 036 | 96,587 | 40 339 / 0,375 |
| `int_score` | 263 980 | 515 436 817 | 322 165 | 439 408 219 | 44,448 | 291 333 / 54,483 |
| `mojibake` | 38 | 97 081 | 322 127 | 439 311 138 | 44,438 | 58 / 0,095 |
| `dedup_wewnatrz` | 27 | 20 472 | 322 100 | 439 290 666 | 44,436 | 77 / 0,007 |
| `dedup_slayer107` | 399 | 170 737 | 321 701 | 439 119 929 | 44,419 | 2 265 / 0,117 |
| `dedup_slayer_8x3b_en` | 2 | 1 208 | 321 699 | 439 118 721 | 44,419 | 2 / 0,0 |
| `dedup_english_technical` | 11 | 7 180 | 321 688 | 439 111 541 | 44,418 | 21 / 0,003 |
| `dedup_fineweb_edu_109` | 0 | 0 | 321 688 | 439 111 541 | 44,418 | 0 / 0,0 |

- **Uzysk: 321 688 plików, 439 111 541 tokenów v6 (44,418%)**; największy koszt `int_score` < 3. Do eksportu wybrano 186 072 pliki, 250 000 074 tokenów v6 (cel 250 mln: wystarcza).
- `dedup_slayer_8x3b_en` (aneks 25.11b): 2 pliki w kaskadzie i niezależnie; przegląd tych 2 odrzuconych: nie zmierzono.
- `ewal_13gram` per test: MBPP 289, HumanEval 136, SynLogic 37, MATH 21, MMLU 10, reszta ≤ 9.
- `sekrety` wg klas: google_api_key 188, aws_access_key 44, klucz_prywatny 51, slack_token 22.
- PII wg detektora DCLM (tylko liczone, tryb `maskuj`): e-mail 27 636, telefon 262, IP 3743. `dedup_wewnatrz`: 16 identycznych, 61 przez MinHash.
- Licencje w puli (top): MIT 414 354, Apache-2.0 127 377, BSD-3-Clause 44 403, BSD-2-Clause 15 614, Unlicense 7241, CC0-1.0 3973, pusta 3278.
- 44 pliki z `id` = 0 (`dok_z_id0`).

### Przegląd odrzuconych (24.11.2026)

Dwóch recenzentów, 100 na powód (mniej, gdy tyle było); [`wyniki/przeglad_odrzuconych_1.json`](wyniki/przeglad_odrzuconych_1.json). Kolumna „koszt” = % tokenów v6 puli z powodem niezależnie. Progi z preregistracji: fałszywe odrzucenia ≤10% ORAZ górna granica Wilsona ≤20%.

| powód | n | A: fałszywe (wątpliwe) | A: stopa [Wilson 95%] | B: fałszywe (wątpliwe) | B: stopa [Wilson 95%] | werdykt A/B | koszt % tok. |
|---|---|---|---|---|---|---|---|
| `licencja` | 100 | 0 (0) | 0,0% [0; 3,7] | 0 (0) | 0,0% [0; 3,7] | PASS/PASS | 0,537 |
| `walidacja_fabryki` | 100 | 49 (0) | 49,0% [39,4; 58,7] | 0 (98) | 0,0% [0; 3,7] | FAIL/PASS | 0,091 |
| `ewal_13gram` | 100 | 88 (2) | 88,0% [80,2; 93,0] | 85 (6) | 85,0% [76,7; 90,7] | FAIL/FAIL | 0,145 |
| `sekrety` | 100 | 16 (24) | 16,0% [10,1; 24,4] | 13 (28) | 13,0% [7,8; 21,0] | FAIL/FAIL | 0,103 |
| `wygenerowany` | 100 | 34 (1) | 34,0% [25,5; 43,7] | 34 (1) | 34,0% [25,5; 43,7] | FAIL/FAIL | 1,376 |
| `int_score` | 100 | 0 (0) | 0,0% [0; 3,7] | 0 (0) | 0,0% [0; 3,7] | PASS/PASS | 54,483 |
| `mojibake` | 58 | 1 (19) | 1,7% [0,3; 9,1] | 0 (19) | 0,0% [0; 6,2] | PASS/PASS | 0,095 |
| `dedup_wewnatrz` | 77 | 0 (0) | 0,0% [0,0; 4,8] | 0 (4) | 0,0% [0,0; 4,8] | PASS/PASS | 0,007 |
| `dedup_slayer107` | 100 | 0 (13) | 0,0% [0; 3,7] | 0 (0) | 0,0% [0; 3,7] | PASS/PASS | 0,117 |
| `dedup_english_technical` | 21 | 0 (0) | 0,0% [0; 15,5] | 0 (1) | 0,0% [0; 15,5] | PASS/PASS | 0,003 |

`haslo_w_kodzie`, `min_tresc` i `dedup_fineweb_edu_109` powstały lub dostały bazę po tej próbce: nie zmierzono. **Werdykt: NIE
PRZESZŁO** (`ewal_13gram`, `sekrety`, `wygenerowany` u obu; `walidacja_fabryki` u A, u B 98 wątpliwych).

### Aneks 24.11b (commit `8191660`)

`min_tresc`. Reguły z FAIL przyjęte: `walidacja_fabryki` i `dedup_slayer107` łapią wspólny nagłówek licencji (szkic 13-gramów),
`ewal_13gram` idiomy kodu (pętle, klasa Node, sortowanie bąbelkowe), `wygenerowany` frazę w komentarzach, `sekrety` przykładowe klucze
z dokumentacji; łączny koszt ok. 1,7% tokenów. Zmiana reguł (szkic bez nagłówków licencji) przed częścią 2.

### Przegląd 300 zachowanych (24.11.2026)

Z agregacji wstępnej (bez `dedup_fineweb_edu_109`); [`wyniki/przeglad_zachowanych_1.json`](wyniki/przeglad_zachowanych_1.json).

| miara | A | B | próg | werdykt |
|---|---|---|---|---|
| jakość tak / wątpliwy / nie | 295 / 4 / 1 | 295 / 3 / 2 | — | — |
| śmieci | 1: 0,3% [0,1; 1,9] | 2: 0,7% [0,2; 2,4] | ≤ 10% | PASS |
| przeoczony sekret | 1/300 | 1/300 (ten sam plik nr 468782: hasło do lokalnej bazy MySQL) | 0/300 | FAIL |
| przeoczony test | 0/300 | 0/300 | — | PASS |

### Aneks 24.11c (commit `63da6ec`)

`haslo_w_kodzie`: przypisanie hasła literałem (`password|passwd|pwd` = napis ≥ 4 znaki) → plik usuwany. Przed regułą
[`wyniki/wzorzec_haslo.json`](wyniki/wzorzec_haslo.json): 3707 trafień w puli, 784 z 184 198 wybranych (0,426%); łapie też hasła
przykładowe, koszt przyjęty. Kontrola dodatnia: `K_haslo`.

### Próbka kontrolna 200 (25.11.2026)

Po agregacji końcowej, `default_rng(seed+2)`, dwóch recenzentów; oceny `robocze/przeglad/oceny_A|B/kontr_*.json`.

| miara | A | B | próg | werdykt |
|---|---|---|---|---|
| przeoczony sekret | 0/200 | 0/200 | 0/200 | PASS |
| przeoczony test | 0/200 | 0/200 | 0/200 | PASS |

## 9. Eksport

| | |
|---|---|
| Komenda | `odtworz.sh eksport stackedu`, końcowy log `eksport.log` 25.11.2026 02:53 |
| Key | `stack_edu_python`; datasheet [`eksport/stack_edu_python.md`](eksport/stack_edu_python.md) |
| Liczby | 180 275 plików, 763 432 617 znaków, 188 819 386 tokenów cl100k; `language` en, `text_origin` human; `dropped`: `wrong_language` 5797, `min_chars` 0, reszta 0 (186 072 − 5797 = 180 275); licencja per plik (MIT 126 028, Apache-2.0 29 389, BSD-3-Clause 11 508, BSD-2-Clause 3916, Unlicense 2513, CC0-1.0 1303, …) |
| PII | `pii.pass` = `regex e-mail only, before the language gate`, `counts.pii` 9484: 9 484 e-maili zamaskowanych do `[PII]` PRZED `shard.write` (`mat_wybor.premask_emails`, wołane z `eksport/src/clean_stack_edu_python.py`); Presidio nie uruchomione |
| Wynik | [`wyniki/eksport_stats.json`](wyniki/eksport_stats.json); sha256 parquet `4ccfbb8c3e483192545a2264cb813c88d21bfd5e4f9abd5b525884fdeadd2d83` ([`wyniki/eksport_sha256.txt`](wyniki/eksport_sha256.txt)); wcześniejsze eksporty: 00:39 `58a52663…` (180 098 plików), 02:10 `87b00034…` (180 282 pliki, maskowanie po bramce językowej) |

## 10. Kontrola końcowa

| | |
|---|---|
| Komenda | w `odtworz.sh eksport`: `pytest src/test_stack_edu_python_contract.py -q` i `python src/check.py --source stack_edu_python` |
| Test kontraktowy | 1 passed |
| `check.py` | kod 1 tylko z DWÓCH oczekiwanych przyczyn: (1) ponowny skan PII Presidio — 11 wierszy „PII left after masking”; typy trafień sprawdzone 25.11 na eksporcie `87b00034…` (19 z 200 skanowanych plików): IP_ADDRESS 73 (adresy lokalne i przykładowe w kodzie), EMAIL_ADDRESS 1 (szablon `{LOGIN_INFO}@github.com`), CREDIT_CARD, MEDICAL_LICENSE, US_BANK_NUMBER po 1 (stałe, hashe), żadne prawdziwe dane; dla eksportu `4ccfbb8c…` typy trafień nie sprawdzone; (2) „stats.json pii has no presidio record” — Presidio wyłączone świadomie (403 trafienia PhoneRecognizer w 300 dok. FineMath); 0 wierszy bramki językowej |
| Niezależny agent na pliku o tym samym sha256 | na `87b00034…` (plik z HF): wykrył 8 wierszy „fails the en language gate” w `check.py`, pominiętych przy filtrze logu po prefiksie `stack_edu_python:` (te wiersze mają `stack_edu_python/<id>:`); przyczyna: maskowanie e-maili do `[PII]` szło po bramce językowej `shard.write`, a `check.py` bada tekst zamaskowany; poprawka `premask_emails`, eksport powtórzony. Na `4ccfbb8c…` (pobrany z HF, sha zgodny): pytest PASS, `check.py` kod 1 wyłącznie z 11 „PII left after masking” i 1 „no presidio record”, wszystkie linie policzone bez filtra, innych błędów brak |

## 11. Wysyłka (repo do wglądu Arka)

| | |
|---|---|
| Repo | `Lolita67/stack_edu_python-robocze`, bramka `manual`, README jednym zdaniem; upload eksportu `4ccfbb8c…`: commit HF `a345d3e5` |
| Bramka | anonimowe pobranie dostaje 401 (sprawdzone curl, także po commicie `a345d3e5`); 24.11 repo było przez ok. 3 min bez bramki (założył je upload, bo skrypt zakładający repo przerwał się po pierwszym), bramka ustawiona po wykryciu |
| Dostęp | `grant_access` dla `Maggio33` (Arek): czeka na Anię (UI); token sesji OAuth dostaje 401 na `grant_access` |
| Gotowe gdy | Arek ma link i dostęp: NIE (czeka na dostęp) |

## 12. Dane treningowe

PR [#353](https://github.com/slayerlabs/benchmarks-fabryka-ai/pull/353): status wiersza „u Arka do wglądu” z linkiem do repo. PR
rezerwacji [#347](https://github.com/slayerlabs/benchmarks-fabryka-ai/pull/347) scalony. Sprawdzenie, czy każdy link w wierszu odpowiada 200:
nie zmierzono (repo za bramką zwraca 401 anonimowo).

## Część 2 (pełna pula)

Zbiór łączny #346 (cel ok. 20 mld tokenów v6). Wyniki w [`wyniki/cz2/`](wyniki/cz2/), logi w `robocze/cz2/logi/`. **Część 1 jest
podzbiorem puli części 2** (plik 0080 jest w puli, `dedup_wewnatrz` obejmuje całość): w treningu NIE dodawać części 1 do części 2.

| krok | wynik |
|---|---|
| Preregistracja | [`skrypty/preregistracja.json`](skrypty/preregistracja.json) → `czesc_2`, zapisane 25.11.2026 przed pobraniem pozostałych plików (commit `380e7f0`, 07:54): wszystkie 12 plików Pythona w tej samej permutacji, reguły bez zmian względem części 1 (z aneksami do 25.11b), eksport wszystkich zachowanych, próbka kontrolna 200 `default_rng(seed+3)` |
| Pobranie | `pula.log` 25.11 09:54: `KONIEC 7218355 11140913173`; 12 plików 0073–0084, 7 218 355 plików Pythona, 11 140 913 173 tokenów v6 ([`wyniki/cz2/probka_pliki.json`](wyniki/cz2/probka_pliki.json), sha256 każdego pliku) |
| Kontrola dodatnia | osobny wynik dla puli części 2: nie zmierzono (reguły i indeksy jak w części 1, 22/22) |
| Przebieg | 1452/1452 jednostek, `KONIEC 11818s` (`przebieg.log` 13:11); `ew13`: `dokumentow 7218355 z_trafieniem 50423 ngramow 43239`, `KONIEC` |
| Agregacja | `agreguj.log` 14:40, `KONIEC`; [`wyniki/cz2/agreguj.json`](wyniki/cz2/agreguj.json); kaskada niżej |
| Podział | [`wyniki/cz2/czesci.json`](wyniki/cz2/czesci.json) (`../matematyka-wspolne/skrypty/czesci.py`): 5 części po ok. 0,99 mld v6, klucze `stack_edu_python_p01..p05` |
| Eksport | `../matematyka-wspolne/skrypty/eksport_czesci.sh`, `eksport.log` 25.11 17:20, `KONIEC 5`; każda część: `shard.write`, test kontraktowy 1 passed, `check.py` tylko oczekiwane linie |
| Próbka kontrolna | [`wyniki/cz2/przeglad_kontrolny.json`](wyniki/cz2/przeglad_kontrolny.json); wyniki niżej |
| Wysyłka | repo `Lolita67/stack_edu_python-robocze`, katalogi `data/stack_edu_python_pNN/`: **w toku** |
| Dane treningowe | wiersz dla części 2: nie zmierzono (czeka na wysyłkę) |

Kaskada ([`wyniki/cz2/agreguj.json`](wyniki/cz2/agreguj.json)):

| powód | odrzucone dok. | odrzucone tok. v6 | zostaje dok. | zostaje tok. v6 | % tok. | niezależnie dok. / % tok. |
|---|---|---|---|---|---|---|
| `licencja` | 37 976 | 59 580 580 | 7 180 379 | 11 081 332 593 | 99,465 | 37 976 / 0,535 |
| `walidacja_fabryki` | 19 198 | 9 983 175 | 7 161 181 | 11 071 349 418 | 99,376 | 19 211 / 0,09 |
| `ewal_13gram` | 5 930 | 14 665 069 | 7 155 251 | 11 056 684 349 | 99,244 | 5 961 / 0,132 |
| `sekrety` | 3 254 | 15 450 727 | 7 151 997 | 11 041 233 622 | 99,105 | 3 278 / 0,14 |
| `haslo_w_kodzie` | 43 141 | 85 495 814 | 7 108 856 | 10 955 737 808 | 98,338 | 43 564 / 0,778 |
| `wygenerowany` | 44 529 | 150 438 674 | 7 064 327 | 10 805 299 134 | 96,988 | 44 995 / 1,367 |
| `min_tresc` | 450 825 | 41 463 792 | 6 613 502 | 10 763 835 342 | 96,615 | 454 286 / 0,375 |
| `int_score` | 2 974 444 | 5 796 572 174 | 3 639 058 | 4 967 263 168 | 44,586 | 3 282 607 / 54,299 |
| `mojibake` | 404 | 1 855 568 | 3 638 654 | 4 965 407 600 | 44,569 | 710 / 0,066 |
| `dedup_wewnatrz` | 4 204 | 6 515 276 | 3 634 450 | 4 958 892 324 | 44,511 | 9 121 / 0,131 |
| `dedup_slayer107` | 4 502 | 2 070 622 | 3 629 948 | 4 956 821 702 | 44,492 | 25 079 / 0,116 |
| `dedup_slayer_8x3b_en` | 12 | 10 560 | 3 629 936 | 4 956 811 142 | 44,492 | 12 / 0,0 |
| `dedup_english_technical` | 140 | 249 311 | 3 629 796 | 4 956 561 831 | 44,49 | 289 / 0,006 |
| `dedup_fineweb_edu_109` | 0 | 0 | 3 629 796 | 4 956 561 831 | 44,49 | 0 / 0,0 |

- **Uzysk: 3 629 796 plików, 4 956 561 831 tokenów v6 (44,49%)**; `int_score` < 3 zabiera 54,3% tokenów puli niezależnie.
- `ewal_13gram` per test: MBPP 3305, HumanEval 1832, MATH 258, SynLogic 151, MMLU 118, MathQA 85, reszta ≤ 74.
- `sekrety` wg klas: google_api_key 2013, klucz_prywatny 566, aws_access_key 443, slack_token 225, github_token 39.
- PII wg detektora DCLM (tylko liczone, tryb `maskuj`): e-mail 313 414, telefon 3211, IP 43 034. `dedup_wewnatrz`: 2009 identycznych, 7112 przez MinHash. 581 plików z `id` = 0.
- Przegląd odrzuconych na puli części 2: nie zmierzono (reguły bez zmian, obowiązuje przegląd części 1).

Części i eksport:

| klucz | dok. (wybór) | tokeny v6 | linie `check.py` (oczekiwane) | sha256 parquet |
|---|---|---|---|---|
| `stack_edu_python_p01` | 722 555 | 991 310 853 | 15 | `8e0a40ab3d829ab526ac4b499cad4a13cd101af02ef3fd4e249cf9c8e46c7c9d` |
| `stack_edu_python_p02` | 729 634 | 991 312 955 | 13 | `0a2a596e3e30c0bf69ab4d85fae665194c912dd7e375c9733b14c98ee4bfa66c` |
| `stack_edu_python_p03` | 728 181 | 991 312 869 | 16 | `582896c2bb8ff00c5e288fd96163e2e65b7ccee9fae47a661396437ce4705c09` |
| `stack_edu_python_p04` | 726 339 | 991 308 269 | 9 | `2455ab6a61c849f41d42c09a300b285409b47610eda611c8ac58c1614ec5afca` |
| `stack_edu_python_p05` | 723 087 | 991 316 885 | 17 | `ccfb85dbd6dd2d13e7e133f6b193229f43932c722a32cf36766be5f108d8cf8f` |

- Linie `check.py` to wyłącznie „PII left after masking” i „stats.json pii has no presidio record”; typy trafień Presidio dla części 2: nie sprawdzone.
- Eksport łącznie: **3 516 755 plików, 3 744 422 806 tokenów** wg licznika repo zgłoszeń (`token_count`, inny tokenizer niż v6); bramka językowa `shard.write` odrzuciła 113 041 (3 629 796 − 113 041 = 3 516 755); e-maile zamaskowane przed bramką: 185 412. Liczby eksportu per część: nie zapisane w tym katalogu.
- Licencje top: MIT 2 460 101, Apache-2.0 573 192, BSD-3-Clause 224 976, BSD-2-Clause 75 616, Unlicense 48 516, CC0-1.0 24 234, ISC 10 175.

Próbka kontrolna 200 zachowanych (`default_rng(seed+3)`, dwóch recenzentów, obaj zadeklarowali lekturę pełnych 3000 znaków):

| miara | A | B | próg | werdykt |
|---|---|---|---|---|
| przeoczony sekret | 0/200 | 0/200 | 0/200 | PASS |
| przeoczone PII | 0/200 | 0/200 | — | PASS |
| przeoczony test | 0/200 | 0/200 | 0/200 | PASS |
| jakość tak / wątpliwy | 196 / 4 | 195 / 5 | — | — |

Uwaga z pliku: w pozycji 6015718 numery kart to publiczne numery testowe bramek płatniczych (komentarz „test card numbers”), sprawdzone 25.11.

## Historia odtworzeń

- 24.11.2026 19:38: karta i preregistracja (`6988094`); 19:47 `pula` (kod 2 po `KONIEC`).
- 24.11.2026 20:07–20:08: `przebieg` 128/128, `ew13`, pierwsza `agreguj` (bez aneksów): 344 216 plików, 443 158 514 tokenów v6.
- 24.11.2026 20:41: `agreguj_wstepne` (`entech`, `fwe109` pusty): 344 205 / 443 151 334 (entech 11).
- 24.11.2026 20:52: `agreguj_wstepne2` (aneks 24.11b): 323 048 / 441 205 383; przegląd odrzuconych i zachowanych.
- 25.11.2026 00:04: `agreguj_koncowe` (aneks 24.11c): 321 690 / 439 112 749; próbka kontrolna 200.
- 25.11.2026 00:39: eksport, test kontraktowy 1 passed, `check.py` kod 1 (dwa oczekiwane błędy); commit `1a28fbd`.
- 25.11.2026 01:28–01:42: aneks 25.11b (`753d40d`), baza `en8x3b`, kontrola 22/22, `agreguj_8x3b`: 321 688 / 439 111 541.
- 25.11.2026 02:10: eksport: 180 282 pliki, sha256 `87b00034…`; test kontraktowy 1 passed; niezależna kontrola: 8 wierszy bramki językowej w `check.py`.
- 25.11.2026 02:53: eksport końcowy z maskowaniem e-maili przed bramką językową: 180 275 plików, sha256 `4ccfbb8c…`; `check.py`: 11 „PII left after masking”, 1 „no presidio record”, 0 bramki językowej; upload HF `a345d3e5`; powtórna niezależna kontrola na pliku z HF: PASS (tylko oczekiwane linie).
- 25.11.2026 07:54: część 2, preregistracja `czesc_2` przed pobraniem (commit `380e7f0`); 09:54 `pula`: 7 218 355 plików, 11 140 913 173 tokenów v6.
- 25.11.2026 13:11–14:40: część 2, `przebieg` 1452/1452 (`KONIEC 11818s`), `ew13`, `agreguj`: 3 629 796 / 4 956 561 831; podział na 5 części i próbka kontrolna 200 (commit `b54d108`, 14:43).
- 25.11.2026 17:20: część 2, eksport 5 części (`KONIEC 5`): 3 516 755 plików, test kontraktowy 1 passed w każdej, `check.py` tylko oczekiwane linie (15/13/16/9/17); wysyłka w toku.

## Pułapki tego przebiegu

- Nie edytuj `odtworz.sh`, gdy którykolwiek krok jest w toku: bash czyta skrypt przyrostowo; edycja w trakcie `pula` i `ewal` dała kod 2 (`syntax error near unexpected token`) PO `KONIEC`.
- macOS ma bash 3.2: pusta tablica przy `set -u` daje „unbound variable”; stąd `${ORYG[@]+"${ORYG[@]}"}`.
- Pobieranie url FineWeb-Edu przez `HfFileSystem` z `block_size` 8 MB trwało 7 min/plik; zakresy bajtów skróciły to do 31 s/plik, potem CDN zwracał 429/400: czekanie i ponowienia.
- Agenci recenzenci: 5 odmów klasyfikatora przy pierwszym uruchomieniu (ponowione raz, przeszły); część recenzentów czytała pozycje częściowo.
- Presidio w eksporcie maskuje liczby w matematyce i kodzie jako telefony (403 trafienia PhoneRecognizer w 300 dok. FineMath): wyłączone świadomie, `check.py` kończy się kodem 1 na dwóch oczekiwanych błędach (krok 10).
- Repo do wglądu zakładaj z bramką przed uploadem: 24.11 dwa repo (`cranemath_en`, `stack_edu_python`) były przez ok. 3 min bez bramki, bo skrypt zakładający repo przerwał się po pierwszym, a pozostałe założył upload.
- Przeglądaj całe wyjście `check.py`, nie tylko linie z prefiksem `<key>:`: błędy per wiersz mają postać `<key>/<id>:` (tak przeoczono 8 wierszy bramki językowej).
- Maskowanie zmieniające tekst (tu e-maile do `[PII]`) musi iść PRZED bramką językową `shard.write`, bo `check.py` bada tekst po maskowaniu.
