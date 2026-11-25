# Dziennik zbioru: FineMath-4+ (EN) dla microannealu Slayera 1B

Przepis: [`METODOLOGIA.md` w repo zespołu](https://github.com/slayerlabs/benchmarks-fabryka-ai/blob/main/research/slayer-1b/dane/METODOLOGIA.md).
Karta źródła: [`KARTA_ZRODLA.md`](KARTA_ZRODLA.md). Reguły: [`skrypty/preregistracja.json`](skrypty/preregistracja.json).
Skrypty wspólne trzech zbiorów #346 (FineMath-4+, CraneMath, Stack-Edu Python): [`../matematyka-wspolne/skrypty/`](../matematyka-wspolne/skrypty/),
każdy krok to `bash dane/matematyka-wspolne/skrypty/odtworz.sh <krok> finemath4`. Logi kroków: `robocze/logi/` (poza gitem).
Dzienniki bliźniacze: [CraneMath](../cranemath/DZIENNIK.md), [Stack-Edu Python](../stackedu/DZIENNIK.md).

## Bramki praw

| bramka | wynik |
|---|---|
| Można TRENOWAĆ | TAK (wyjątek TDM art. 4 dyr. 2019/790; takedown po `url` albo rekordzie WARC); opt-out TDM NIE SPRAWDZONY |
| Można ZGŁOSIĆ do `dataset-team-submissions` | NIEROZSTRZYGNIĘTY: ODC-By dotyczy kompilacji, teksty z Common Crawl bez licencji per dokument; datasheet `held_for_review` |

## 1. Rezerwacja

| | |
|---|---|
| Co | issue [#346](https://github.com/slayerlabs/benchmarks-fabryka-ai/issues/346) na tablicy Dataset team (In progress); wiersz „w budowie” w PR [#347](https://github.com/slayerlabs/benchmarks-fabryka-ai/pull/347) |
| Poprawki | 24.11.2026 PR #347 poprawiony wg uwag Elwenor: tytuł Conventional Commits, opis z szablonu po angielsku; PR policy pass |
| Cel | ramię B microannealu (paper mat./med. 1.2): ≥ 0,4 mld tokenów v6 po filtrach (`cel_eksportu_tok_v6` 400 000 000) |

## 2. Karta źródła

[`KARTA_ZRODLA.md`](KARTA_ZRODLA.md), 24.11.2026, przed pobraniem (commit `6988094`, 19:38). `HuggingFaceTB/finemath@e92b25a6`,
podzbiór `finemath-4plus` (64 pliki). Trenować: TAK; zgłosić: NIEROZSTRZYGNIĘTY.

## 3. Preregistracja

[`skrypty/preregistracja.json`](skrypty/preregistracja.json), commit `6988094` przed pobraniem puli: seed 20261124, cel puli
600 mln tokenów v6, cel eksportu 400 mln, 12 powodów w kaskadzie (po aneksach), `ewal_13gram` ściśle dla testów matematyki i
kodu, PII usuwane, ręczna próbka 100 odrzuconych na powód + 300 zachowanych, dwóch recenzentów. Aneksy (podsekcje w kroku 8):

| aneks | commit | zapisany | treść |
|---|---|---|---|
| `aneks_2026_11_24` | `f159b6e` | przed pierwszym odczytem agregacji | `dedup_english_technical` (english-technical-1b@3b833d36, dane 1.08) i `dedup_fineweb_edu_109` (url z manifestu Slayer1B-Dataset@2d248a17); wymaganie właścicielki projektu |
| `aneks_2026_11_24b` | `8191660` | po przeglądzie odrzuconych, przed próbką zachowanych | `min_tresc` (< 50 słów); reguły z FAIL precyzji przyjęte z kosztem w tokenach |
| `aneks_2026_11_24c` | `63da6ec` | po przeglądzie zachowanych, przed eksportem | `pii_zaciemniony` (e-mail `nazwa(AT)domena`); FAIL śmieci przyjęty jako cecha ramienia porównawczego; próbka kontrolna 200 |
| `aneks_2026_11_25b` | `753d40d` (01:32) | po eksporcie roboczym, PRZED policzeniem nowego powodu na puli (`agreguj_8x3b.log` 01:37) | `dedup_slayer_8x3b_en` wobec angielskiej części Slayera 1.00-1.06: `SlayerLab/slayer-pl-8x3b@d50df04a` `shared/en.parquet` (sha256 `f3d451b7…`, 2 384 000 dok., bez url; [`../matematyka-wspolne/robocze/wyniki/bazy/en8x3b.json`](../matematyka-wspolne/robocze/wyniki/bazy/en8x3b.json)); MinHash J ≥ 0,8 albo identyczny tekst; wszystkie trzy zbiory |

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
| Komenda | `odtworz.sh pula finemath4`, 24.11.2026 (log `pula.log`, 19:46) |
| Kod wyjścia | Python: `KONIEC 418718 660554470`; bash: kod 2 PO `KONIEC` (edycja `odtworz.sh` w trakcie, pułapka niżej); dane pełne |
| Liczby | 4 pliki z 64 w kolejności `default_rng(20261124)`, rewizja `e92b25a6`; 418 718 dokumentów, 660 554 470 tokenów v6 |
| Wynik | [`wyniki/probka_pliki.json`](wyniki/probka_pliki.json) (sha256 i wiersze każdego pliku) |

## 6. Indeksy i kontrole

- Testy (wspólne): `odtworz.sh ewal_pobierz` 24.11.2026: indeks RPG v2 (60 testów, dowiązania do pobrań DCLM-EN) + T51 GSM-Plus i T52 GSM1k, oba `OK`, razem 62 pozycje statusu, `KONIEC`; `odtworz.sh ewal`: `ogolem 33302686` 13-gramów, `KONIEC` (bash kod 2 po `KONIEC`, ta sama pułapka co w `pula`).
- EN 1.07 (`idx`) i walidacja Fabryki (`idx_wal`): indeksy z katalogu roboczego DCLM-EN, bez zmian.
- Bazy z aneksu 24.11 (`bazy_mat.py`): `entech` (english-technical-1b@3b833d36) `KONIEC 209939`; `fwe109` (url FineWeb-Edu 1.09) `KONIEC 266 98512010` (266 plików, 24.11.2026 23:51; po przejściu na zakresy bajtów). Baza z aneksu 25.11b: `en8x3b` (2 384 000 dok., log `bazy_en8x3b.log` 25.11.2026 01:28).
- Kontrola dodatnia `odtworz.sh kontrola finemath4`: 14/14 przed aneksem (commit `9b7d6bd`), 18/18 po aneksach 24.11, po aneksie 25.11b
  **19/19** ([`wyniki/kontrola.json`](wyniki/kontrola.json)): K_czysty, para K_dup_a/K_dup_b, K_kopia_107, K_walidacja, K_gsm8k, K_math,
  K_gsm_plus, K_gsm1k, K_mmlu, K_email, K_telefon, K_ip, K_domena, K_entech, K_en8x3b, K_fwe109, K_pusty, K_at. Pierwsza
  wersja miała parę duplikatów na tym samym tle co dokument czysty (`K_dup_a` dostawał `dedup_wewnatrz` jako kopia tła); para
  dostała własny tekst, kontrola powtórzona.

## 7. Przebieg

| | |
|---|---|
| Komenda | `odtworz.sh przebieg finemath4` (6 procesów, `nice -n 10`), 24.11.2026 |
| Wynik | 84/84 jednostek, `KONIEC 439s` (log `przebieg.log`, 19:57); kod wyjścia nie zapisany w logu |
| `ew13` | `dokumentow 418718 z_trafieniem 13326 ngramow 70627`, `KONIEC` |

## 8. Po przebiegu

Komenda `odtworz.sh agreguj finemath4`; końcowy przebieg 25.11.2026 01:37 (`agreguj_8x3b.log`, po aneksie 25.11b), wynik
[`wyniki/agreguj.json`](wyniki/agreguj.json). Kaskada (powód = pierwszy w kolejności preregistracji):

| powód | odrzucone dok. | odrzucone tok. v6 | zostaje dok. | zostaje tok. v6 | % tok. | niezależnie dok. / % tok. |
|---|---|---|---|---|---|---|
| `walidacja_fabryki` | 231 | 207 149 | 418 487 | 660 347 321 | 99,969 | 231 / 0,031 |
| `domena_testow` | 3 011 | 7 812 679 | 415 476 | 652 534 642 | 98,786 | 3 011 / 1,183 |
| `ewal_13gram` | 5 671 | 20 942 995 | 409 805 | 631 591 647 | 95,615 | 5 741 / 3,232 |
| `pii` | 8 672 | 39 810 781 | 401 133 | 591 780 866 | 89,589 | 8 948 / 6,347 |
| `pii_zaciemniony` | 359 | 558 284 | 400 774 | 591 222 582 | 89,504 | 372 / 0,103 |
| `min_tresc` | 2 686 | 236 058 | 398 088 | 590 986 524 | 89,468 | 2 692 / 0,036 |
| `mojibake` | 3 543 | 10 121 526 | 394 545 | 580 864 998 | 87,936 | 3 741 / 1,765 |
| `dedup_wewnatrz` | 3 658 | 6 183 891 | 390 887 | 574 681 107 | 87,0 | 3 931 / 1,06 |
| `dedup_slayer107` | 35 928 | 51 579 836 | 354 959 | 523 101 271 | 79,191 | 38 514 / 8,778 |
| `dedup_slayer_8x3b_en` | 507 | 575 146 | 354 452 | 522 526 125 | 79,104 | 605 / 0,111 |
| `dedup_english_technical` | 0 | 0 | 354 452 | 522 526 125 | 79,104 | 0 / 0,0 |
| `dedup_fineweb_edu_109` | 24 740 | 30 432 805 | 329 712 | 492 093 320 | 74,497 | 31 918 / 6,449 |

- **Uzysk: 329 712 dok., 492 093 320 tokenów v6 (74,497%)**. Do eksportu wybrano 267 504 dok., 400 000 934 tokenów v6 (cel 400 mln: wystarcza).
- `ewal_13gram` per test (dokumenty): MathQA 2506, MATH 1964, BoolQ 406, MMLU 224, SciQ 217, MBPP 165, HumanEval 136, SQuAD2 54, SynLogic 36, HellaSwag 29, reszta ≤ 27.
- PII wg detektora DCLM: e-mail 7227, telefon 1250, IP 1106 (tryb `usun`). `dedup_wewnatrz`: 0 identycznych, 3931 przez MinHash.
- 2 dokumenty z `id` = 0 (`dok_z_id0`).

### Przegląd odrzuconych (24.11.2026)

Dwóch niezależnych recenzentów (A, B), po 100 dokumentów na powód, 3000 znaków; wynik
[`wyniki/przeglad_odrzuconych_1.json`](wyniki/przeglad_odrzuconych_1.json). Kolumna „koszt” = % tokenów v6 puli z powodem niezależnie. Progi z preregistracji: fałszywe odrzucenia ≤10% ORAZ górna granica Wilsona ≤20%.

| powód | n | A: fałszywe (wątpliwe) | A: stopa [Wilson 95%] | B: fałszywe (wątpliwe) | B: stopa [Wilson 95%] | werdykt A/B | koszt % tok. |
|---|---|---|---|---|---|---|---|
| `walidacja_fabryki` | 100 | 0 (13) | 0,0% [0; 3,7] | 0 (4) | 0,0% [0; 3,7] | PASS/PASS | 0,031 |
| `domena_testow` | 100 | 0 (0) | 0,0% [0; 3,7] | 0 (0) | 0,0% [0; 3,7] | PASS/PASS | 1,183 |
| `ewal_13gram` | 100 | 33 (3) | 33,0% [24,6; 42,7] | 44 (5) | 44,0% [34,7; 53,8] | FAIL/FAIL | 3,232 |
| `pii` | 100 | 9 (52) | 9,0% [4,8; 16,2] | 13 (48) | 13,0% [7,8; 21,0] | PASS/FAIL | 6,347 |
| `mojibake` | 100 | 0 (10) | 0,0% [0; 3,7] | 0 (12) | 0,0% [0; 3,7] | PASS/PASS | 1,765 |
| `dedup_wewnatrz` | 100 | 3 (1) | 3,0% [1,0; 8,5] | 1 (0) | 1,0% [0,2; 5,4] | PASS/PASS | 1,06 |
| `dedup_slayer107` | 100 | 0 (0) | 0,0% [0; 3,7] | 3 (5) | 3,0% [1,0; 8,5] | PASS/PASS | 8,778 |

Powody `pii_zaciemniony`, `min_tresc`, `dedup_english_technical`, `dedup_fineweb_edu_109` powstały lub dostały bazę po tej
próbce: fałszywe odrzucenia nie zmierzono. **Werdykt: NIE PRZESZŁO** (`ewal_13gram` u obu, `pii` u B).

### Aneks 24.11b (commit `8191660`)

`min_tresc` (< 50 słów po `rdzen.norm_slowa`) dla trzech zbiorów. Reguły z FAIL precyzji zostają, bo usuwają dobre teksty, a
nie przepuszczają złych; koszt w FineMath: `ewal_13gram` 3,2%, `pii` 6,3% tokenów (ochrona prywatności ma pierwszeństwo).
Zmiana reguł wraca jako zadanie przed częścią 2.

### Przegląd 300 zachowanych (24.11.2026)

Z agregacji wstępnej (bez `dedup_fineweb_edu_109`), dwóch recenzentów; wynik [`wyniki/przeglad_zachowanych_1.json`](wyniki/przeglad_zachowanych_1.json).

| miara | A | B | próg | werdykt |
|---|---|---|---|---|
| jakość tak / nie / wątpliwy | 198 / 39 / 63 | 194 / 39 / 67 | — | — |
| śmieci | 39: 13,0% [9,7; 17,3] | 39: 13,0% [9,7; 17,3] | ≤ 10% | FAIL |
| przeoczone PII | 1/300 | 2/300 | 0/300 | FAIL |
| przeoczony test | 1/300 | 1/300 | — | zgłoszenie MATH nie potwierdzone (grep po T34_math 24.11) |

### Aneks 24.11c (commit `63da6ec`)

- `pii_zaciemniony`: regex e-maila zapisanego jako `nazwa(AT)domena`; przed regułą [`wyniki/wzorzec_email_at.json`](wyniki/wzorzec_email_at.json):
  372 trafienia w puli, 230 z 271 467 wybranych (0,085%). Kontrola dodatnia: `K_at`.
- FAIL śmieci (13%) przyjęty z zapisem: to cecha opublikowanego FineMath-4+, który ramię B ma porównać z przepisaniem (ramię C);
  odsetek w datasheet; filtr jakości przed częścią 2, jeśli B wygra.
- Próbka kontrolna 200 zachowanych po agregacji eksportowej, `default_rng(seed+2)`, próg PII 0/200.

### Próbka kontrolna 200 (25.11.2026)

Po agregacji końcowej (z `dedup_fineweb_edu_109`), dwóch recenzentów; oceny `robocze/przeglad/oceny_{A,B}/kontr_*.json`.

| miara | A | B | próg | werdykt |
|---|---|---|---|---|
| przeoczone PII | 0/200 | 0/200 | 0/200 | PASS |
| przeoczony test | 2/200 (nr 9636, 84036, „do weryfikacji”) | 1/200 (nr 84036, „niepewne”) | — | brak odpowiedników w teście MATH (grep po T34_math, wszystkie pliki test, 25.11; sprawdzone też zgłoszenie nr 238166) |

### Aneks 25.11b (commit `753d40d`)

Nowy powód `dedup_slayer_8x3b_en` (definicja w tabeli kroku 3), zapisany przed policzeniem na puli. Efekt w końcowej agregacji:
507 dok. w kaskadzie, 605 niezależnie (0,111% tokenów). Próbka kontrolna 200 z aneksu 24.11c zostaje ważna jako podzbiór.

Przegląd 100 odrzuconych tym powodem (jeden recenzent, `robocze/przeglad/oceny_A/odrz_8x3b.json`): **99 trafnych, 0 fałszywych,
1 wątpliwy**: 0,0% fałszywych odrzuceń, PASS. Z 20 losowych pozycji (seed 20261125) sprawdzonych frazami w samej bazie: 19 z kopią,
1 prawdopodobna (różnica znaku punktora).

## 9. Eksport

| | |
|---|---|
| Komenda | `odtworz.sh eksport finemath4` (kopia robocza repo zgłoszeń w `../matematyka-wspolne/robocze/zgloszenia`, `src/clean_finemath_4plus_en.py`), końcowy log `eksport.log` 25.11.2026 02:02 |
| Key | `finemath_4plus_en`; datasheet [`eksport/finemath_4plus_en.md`](eksport/finemath_4plus_en.md) (status `held_for_review`) |
| Pierwsza próba | błąd bramki językowej krótkich wierszy (82% < 90%) → `min_chars: 200` w rejestrze dla `finemath_4plus_en` i `cranemath_en`, eksport powtórzony |
| Liczby | 266 351 dok., 1 248 763 375 znaków, 360 900 014 tokenów cl100k; `language` en, `text_origin` human; `dropped`: `min_chars` 24, `wrong_language` 1129, reszta 0 (267 504 − 1153 = 266 351) |
| PII | `pii.pass` = `none` (Presidio nie uruchomione, powód w `stats.json`); dokumenty z e-mailem, telefonem, IP, zaciemnionym e-mailem usunięte wcześniej w całości |
| Wynik | [`wyniki/eksport_stats.json`](wyniki/eksport_stats.json); sha256 parquet `c4ae6f1424dd45e482d43d7524bab5e3dbf44d44beb4acc7888ff769c0c2d4c5` ([`wyniki/eksport_sha256.txt`](wyniki/eksport_sha256.txt)); wcześniejszy eksport (00:32, przed aneksem 25.11b): `0a65c6ea…`, 266 297 dok. |

## 10. Kontrola końcowa

| | |
|---|---|
| Komenda | w `odtworz.sh eksport`: `pytest src/test_finemath_4plus_en_contract.py -q` i `python src/check.py --source finemath_4plus_en` |
| Test kontraktowy | 1 passed |
| `check.py` | kod 1 tylko z DWÓCH oczekiwanych przyczyn: (1) ponowny skan PII Presidio — 28 z 200 skanowanych dokumentów; typy trafień sprawdzone 25.11: CREDIT_CARD 3, UK_NHS 1, IP_ADDRESS 1, wszystkie to liczby i ISBN, żadne prawdziwe dane; (2) „stats.json pii has no presidio record” — Presidio wyłączone świadomie (403 trafienia PhoneRecognizer w 300 dok. FineMath) |
| Niezależny agent na pliku o tym samym sha256 | nie zmierzono |

## 11. Wysyłka (repo do wglądu Arka)

| | |
|---|---|
| Repo | `Lolita67/finemath_4plus_en-robocze`, bramka `manual`, README jednym zdaniem |
| Bramka | anonimowe pobranie dostaje 401 (sprawdzone curl) |
| Dostęp | `grant_access` dla `Maggio33` (Arek): czeka na Anię (UI); token sesji OAuth dostaje 401 na `grant_access` |
| Gotowe gdy | Arek ma link i dostęp: NIE (czeka na dostęp) |

## 12. Dane treningowe

PR [#353](https://github.com/slayerlabs/benchmarks-fabryka-ai/pull/353): status wiersza „u Arka do wglądu” z linkiem do repo. PR
rezerwacji [#347](https://github.com/slayerlabs/benchmarks-fabryka-ai/pull/347) scalony. Sprawdzenie, czy każdy link w wierszu odpowiada 200:
nie zmierzono (repo za bramką zwraca 401 anonimowo).

## Część 2 (pełna pula)

Zbiór łączny #346 (cel ok. 20 mld tokenów v6). Wyniki w [`wyniki/cz2/`](wyniki/cz2/), logi w `robocze/cz2/logi/`. **Część 1 jest
podzbiorem puli części 2** (4 pliki części 1 są w puli, `dedup_wewnatrz` obejmuje całość): w treningu NIE łączyć części 1 z częścią 2.
InfiWebMath-4+ i FineMath-3+ odcinają strony już obecne w tym eksporcie (`dedup_finemath4` po ich stronie, indeks `wlasne.log`
25.11 16:34, `KONIEC 4785130`).

| krok | wynik |
|---|---|
| Preregistracja | [`skrypty/preregistracja.json`](skrypty/preregistracja.json) → `czesc_2`, zapisane 25.11 przed pobraniem pozostałych plików (commit `380e7f0`, 07:54): wszystkie 64 pliki w tej samej permutacji, reguły części 1 (aneksy do 25.11b), eksport wszystkich zachowanych, próbka kontrolna 200 `default_rng(seed+3)`. Świadomie odroczone (decyzja właścicielki projektu): filtr jakości (aneks 24.11c) i poprawki reguł konserwatywnych (aneks 24.11b); filtry tylko usuwają, więc można je nałożyć później |
| Aneks 25.11c | `czesc_2.aneks_2026_11_25c`, commit `601e1bc` (14:30), po pierwszej próbce kontrolnej (recenzent B: 1 przeoczony e-mail osoby prywatnej `nazwa at domena.org`, FAIL 0/200; recenzenci czytali głównie początek tekstu), przed agregacją końcową i eksportem: `pii_at_bez_nawiasow`; wzorzec przed regułą: 29 350 z 4 814 480 wybranych (0,61%) ([`wyniki/cz2/wzorzec_email_at_bez_nawiasow.json`](wyniki/cz2/wzorzec_email_at_bez_nawiasow.json)) |
| Pobranie | `pula.log` 25.11 10:13: `KONIEC 6699493 10552288210`; 64 pliki, 6 699 493 dok., 10 552 288 210 tokenów v6 ([`wyniki/cz2/probka_pliki.json`](wyniki/cz2/probka_pliki.json), sha256 każdego pliku) |
| Kontrola dodatnia | na puli części 2: nie zmierzono (reguły i indeksy jak w części 1, 19/19; `pii_at_bez_nawiasow` bez przypadku kontrolnego) |
| Przebieg | trzy logi (wznawianie): `przebieg_1.log` 189/189 `KONIEC 3903s` (09:12), `przebieg_2.log` 609/609 `KONIEC 5233s` (10:40), `przebieg_3.log` 546/546 `KONIEC 4571s` (11:56), razem 1344 jednostek; `ew13`: `dokumentow 6699493 z_trafieniem 212707 ngramow 259144`, `KONIEC` (12:04) |
| Agregacja | przed aneksem `agreguj.log` 14:10: 4 814 480 / 7 127 596 409 (67,546%); po aneksie `agreguj_25c.log` 16:30, `KONIEC`: [`wyniki/cz2/agreguj.json`](wyniki/cz2/agreguj.json) |
| Podział | [`wyniki/cz2/czesci.json`](wyniki/cz2/czesci.json): 7 części po ok. 1,004 mld v6, klucze `finemath_4plus_en_p01..p07` |
| Eksport | `../matematyka-wspolne/skrypty/eksport_czesci.sh`, `eksport.log` 25.11 21:27, `KONIEC 7`; każda część: `check.py` tylko oczekiwane linie |
| Próbka kontrolna | [`wyniki/cz2/przeglad_kontrolny.json`](wyniki/cz2/przeglad_kontrolny.json) (po aneksie 25.11c, pełne teksty); wyniki niżej |
| Przegląd odrzuconych | na puli części 2: nie zmierzono (reguły jak w części 1 poza 25.11c; `pii_at_bez_nawiasow` oceniony w przeglądzie InfiWebMath-4+: [`../infiwebmath4/wyniki/przeglad_1.json`](../infiwebmath4/wyniki/przeglad_1.json), fałszywe odrzucenia 80% (A) / 34% (B), przyjęte jako reguła konserwatywna) |
| Wysyłka | repo `Lolita67/finemath_4plus_en-robocze`, katalogi `data/finemath_4plus_en_pNN/`: **w toku** |
| Dane treningowe | wiersz dla części 2: nie zmierzono (czeka na wysyłkę) |

Kaskada ([`wyniki/cz2/agreguj.json`](wyniki/cz2/agreguj.json), po aneksie 25.11c):

| powód | odrzucone dok. | odrzucone tok. v6 | zostaje dok. | zostaje tok. v6 | % tok. | niezależnie dok. / % tok. |
|---|---|---|---|---|---|---|
| `walidacja_fabryki` | 4 083 | 4 186 642 | 6 695 410 | 10 548 101 568 | 99,96 | 4 083 / 0,04 |
| `domena_testow` | 47 827 | 127 765 691 | 6 647 583 | 10 420 335 877 | 98,75 | 47 887 / 1,212 |
| `ewal_13gram` | 80 983 | 285 728 794 | 6 566 600 | 10 134 607 083 | 96,042 | 81 824 / 2,755 |
| `pii` | 140 063 | 627 830 112 | 6 426 537 | 9 506 776 971 | 90,092 | 144 082 / 6,28 |
| `pii_zaciemniony` | 5 995 | 10 103 504 | 6 420 542 | 9 496 673 467 | 89,996 | 6 289 / 0,121 |
| `pii_at_bez_nawiasow` | 41 030 | 139 638 162 | 6 379 512 | 9 357 035 305 | 88,673 | 47 693 / 1,777 |
| `min_tresc` | 42 275 | 3 709 604 | 6 337 237 | 9 353 325 701 | 88,638 | 42 350 / 0,035 |
| `mojibake` | 56 514 | 160 473 284 | 6 280 723 | 9 192 852 417 | 87,117 | 60 404 / 1,794 |
| `dedup_wewnatrz` | 640 521 | 1 017 809 945 | 5 640 202 | 8 175 042 472 | 77,472 | 691 155 / 11,211 |
| `dedup_slayer107` | 501 565 | 717 139 748 | 5 138 637 | 7 457 902 724 | 70,676 | 615 786 / 8,839 |
| `dedup_slayer_8x3b_en` | 6 560 | 7 667 216 | 5 132 077 | 7 450 235 508 | 70,603 | 9 258 / 0,107 |
| `dedup_english_technical` | 2 | 10 290 | 5 132 075 | 7 450 225 218 | 70,603 | 5 / 0,0 |
| `dedup_fineweb_edu_109` | 346 945 | 423 124 444 | 4 785 130 | 7 027 100 774 | 66,593 | 512 188 / 6,416 |

- **Uzysk: 4 785 130 dok., 7 027 100 774 tokenów v6 (66,593%)**. Do eksportu: wszystkie zachowane.
- `ewal_13gram` per test (dokumenty): MathQA 40 999, MATH 30 860, MMLU 3488, MBPP 2702, HumanEval 2008, BoolQ 949, SciQ 592,
  SQuAD2 488, GSM-Plus 440, HellaSwag 246, reszta ≤ 189.
- PII wg detektora DCLM: e-mail 116 352, telefon 20 396, IP 16 956 (tryb `usun`). `dedup_wewnatrz`: 18 identycznych, 691 137 przez
  MinHash. 2 dokumenty z `id` = 0.

Części i eksport (dok. = wiersze po `shard.write`; wybór przed `shard.write` w `czesci.json`, suma 4 785 130):

| klucz | wybór dok. | tokeny v6 | eksport dok. | linie `check.py` (oczekiwane) | sha256 parquet |
|---|---|---|---|---|---|
| `finemath_4plus_en_p01` | 679 381 | 1 003 866 835 | 676 355 | 27 | `51b6e67d1e215b99822ac7f083507da89aa5a12c43b1165581ef990d59a645e5` |
| `finemath_4plus_en_p02` | 677 662 | 1 003 851 528 | 674 766 | 26 | `3532ded4b92449de3575bd069b0900e01bca5fade78d6b486586e6d42c4e27c8` |
| `finemath_4plus_en_p03` | 683 670 | 1 003 895 722 | 680 572 | 30 | `6362c45b0c35f6821c9e9d9373341dcdee7f0b1899ea5592cf1e41ef43fd645c` |
| `finemath_4plus_en_p04` | 685 651 | 1 003 871 803 | 682 556 | 21 | `f80fab9efc1dceea7275cf9f77cfac28791ef7fe92cd6897047bdfa110131463` |
| `finemath_4plus_en_p05` | 683 293 | 1 003 869 189 | 680 148 | 21 | `017ef971d727237590ebbf1fb0bb21660b8032fc08e2f423385074c65e7e37f3` |
| `finemath_4plus_en_p06` | 688 906 | 1 003 872 498 | 685 711 | 33 | `c9a195d565165a528c66476b5b3a48a92109b6064e3e728445f0c3d82e4a19a9` |
| `finemath_4plus_en_p07` | 686 567 | 1 003 873 199 | 683 199 | 19 | `4a67a117cddda85588d96d6c12767fce6343adb6408884734eca15df896cd3af` |

- Eksport łącznie: **4 763 307 dok., 6 337 631 742 tokenów** wg licznika repo zgłoszeń (`token_count`, nie v6); `dropped`:
  `wrong_language` 21 289, `min_chars` 534 (4 785 130 − 21 823 = 4 763 307).
- Linie `check.py` to wyłącznie „PII left after masking” i „stats.json pii has no presidio record”; typy trafień Presidio dla części 2:
  nie sprawdzone.

Próbka kontrolna 200 zachowanych po aneksie 25.11c (`default_rng(seed+3)`, dwóch recenzentów, obaj zadeklarowali lekturę pełnych
3000 znaków i wyszukiwanie wzorców e-mail/telefon/IP):

| miara | A | B | próg | werdykt |
|---|---|---|---|---|
| przeoczone PII | 0/200 | 0/200 | 0/200 | PASS |
| przeoczony test | 0/200 | 0/200 | — | PASS |
| jakość tak / wątpliwy / nie | 143 / 36 / 21 | 149 / 33 / 18 | — | — |
| śmieci | 10,5% [7,0; 15,5] | 9,0% [5,8; 13,8] | raportowane (cecha źródła) | filtr jakości odroczony |

## Historia odtworzeń

- 24.11.2026 19:38: karta i preregistracja (`6988094`), `ewal_pobierz`; 19:46 `ewal` i `pula` (oba kod 2 po `KONIEC`).
- 24.11.2026 19:57–19:58: `przebieg` 84/84, `ew13`, pierwsza `agreguj` (reguły bez aneksów): zostaje 357 898 dok., 523 813 782 tokenów v6. Uwaga: `agreguj.log` ma czas modyfikacji 19:58, a commit aneksu 24.11 (deklarującego zapis „przed pierwszym odczytem agregacji”) 20:15; czas zapisu aneksu w pliku przed commitem: nie zmierzono.
- 24.11.2026 20:15: aneks 24.11 (`f159b6e`); 20:40 `agreguj_wstepne` z `entech`, `fwe109` jeszcze pusty: 357 898 / 523 813 782 (entech 0).
- 24.11.2026 20:49: `agreguj_wstepne2` z `min_tresc` (aneks 24.11b): 355 254 / 523 581 722; przegląd odrzuconych, potem zachowanych.
- 24.11.2026 23:51: indeks url FineWeb-Edu 1.09 gotowy (266 plików, 98 512 010 url).
- 25.11.2026 00:00: `agreguj_koncowe` (+ `pii_zaciemniony`, `dedup_fineweb_edu_109`): 329 994 / 492 431 609; próbka kontrolna 200.
- 25.11.2026 00:32: eksport (druga próba, `min_chars: 200`), test kontraktowy 1 passed, `check.py` kod 1 (dwa oczekiwane błędy); commit `1a28fbd`.
- 25.11.2026 01:28–01:37: aneks 25.11b (`753d40d`, 01:32), baza `en8x3b`, kontrola 19/19, `agreguj_8x3b`: 329 712 / 492 093 320; przegląd 100 odrzuconych `dedup_slayer_8x3b_en`.
- 25.11.2026 02:02: eksport końcowy: 266 351 dok., sha256 `c4ae6f14…`; `check.py` kod 1 (dwa oczekiwane błędy).
- 25.11.2026 07:54: część 2, preregistracja `czesc_2` przed pobraniem (commit `380e7f0`); 10:13 `pula`: 6 699 493 dok., 10 552 288 210 tokenów v6.
- 25.11.2026 09:12–12:04: część 2, `przebieg` w trzech podejściach (189 + 609 + 546 jednostek), `ew13`.
- 25.11.2026 14:10: część 2, `agreguj` przed aneksem: 4 814 480 / 7 127 596 409; pierwsza próbka kontrolna 200: 1 przeoczony e-mail (FAIL).
- 25.11.2026 14:30: aneks 25.11c (`601e1bc`): `pii_at_bez_nawiasow`.
- 25.11.2026 16:30–16:38: część 2, `agreguj_25c`: 4 785 130 / 7 027 100 774; indeks `wlasne` (16:34) dla `dedup_finemath4` innych źródeł; powtórna próbka kontrolna 200 pełnym tekstem: PII i testy 0/200 (commit `fdc8237`, 16:38).
- 25.11.2026 21:27: część 2, eksport 7 części (`KONIEC 7`): 4 763 307 dok., `check.py` tylko oczekiwane linie; wysyłka w toku.

## Pułapki tego przebiegu

- Nie edytuj `odtworz.sh`, gdy którykolwiek krok jest w toku: bash czyta skrypt przyrostowo; edycja w trakcie `pula` i `ewal` dała kod 2 (`syntax error near unexpected token`) PO `KONIEC`.
- macOS ma bash 3.2: pusta tablica przy `set -u` daje „unbound variable”; stąd `${ORYG[@]+"${ORYG[@]}"}`.
- Pobieranie url FineWeb-Edu przez `HfFileSystem` z `block_size` 8 MB trwało 7 min/plik; zakresy bajtów skróciły to do 31 s/plik, potem CDN zwracał 429/400: czekanie i ponowienia.
- Agenci recenzenci: 5 odmów klasyfikatora przy pierwszym uruchomieniu (ponowione raz, przeszły); część recenzentów czytała pozycje częściowo.
- Presidio w eksporcie maskuje liczby w matematyce i kodzie jako telefony (403 trafienia PhoneRecognizer w 300 dok. FineMath): wyłączone świadomie, `check.py` kończy się kodem 1 na dwóch oczekiwanych błędach (krok 10).
- Repo do wglądu zakładaj z bramką przed uploadem: 24.11 dwa repo (`cranemath_en`, `stack_edu_python`) były przez ok. 3 min bez bramki, bo skrypt zakładający repo przerwał się po pierwszym, a pozostałe założył upload; bramkę ustawiono po wykryciu.
