# Dziennik zbioru: arXiv — matematyka, statystyka, logika (pełne teksty CC i abstrakty CC0) dla Slayera 1B, część 3

Przepis: [`METODOLOGIA.md` w repo zespołu](https://github.com/slayerlabs/benchmarks-fabryka-ai/blob/main/research/slayer-1b/dane/METODOLOGIA.md).
Karta źródła: [`KARTA_ZRODLA.md`](KARTA_ZRODLA.md). Reguły: [`skrypty/preregistracja.json`](skrypty/preregistracja.json).
Budowa puli: [`skrypty/buduj_pule.py`](skrypty/buduj_pule.py) (`wsp.py`, `arxiv_pass.py`); detektory i agregacja:
[`../matematyka-wspolne/skrypty/`](../matematyka-wspolne/skrypty/) (`potok_zrodla.sh`). Logi: `robocze/logi/` (poza gitem).
Dzienniki bliźniacze: [InfiWebMath-4+](../infiwebmath4/DZIENNIK.md) (reguły przejęte), [OEIS](../oeis/DZIENNIK.md) (ten sam tryb PII).

## Bramki praw

| bramka | wynik |
|---|---|
| Można TRENOWAĆ (także komercyjnie) | TAK: licencja per wiersz — pełne teksty CC BY 4.0 / 3.0, CC BY-SA 4.0, CC0, domena publiczna (bardziej restrykcyjna z Common Pile i snapshotu arXiv), abstrakty CC0 (Terms of Use for arXiv APIs); takedown po `id` |
| Można ZGŁOSIĆ do `dataset-team-submissions` | TAK (bez NC/ND, bez licencji domyślnej arXiv; atrybucja `author`, `url`) → `admitted` |
| Użycie komercyjne | dozwolone; prace na domyślnej licencji arXiv (A3) wykluczone: regulamin pobierania arXiv dopuszcza tylko użytek osobisty i badawczy (karta §2.3) |

## 1. Rezerwacja

| | |
|---|---|
| Co | issue [#357](https://github.com/slayerlabs/benchmarks-fabryka-ai/issues/357) (część 3); karta pod #346 |
| Cel | matematyka „wyższa” (prace badawcze w LaTeX) na licencjach pozwalających sprzedawać model; A1 + A2 z [`../matematyka-wspolne/kandydaci_czyste.md`](../matematyka-wspolne/kandydaci_czyste.md) |
| Wiersz w danych treningowych | nie zmierzono (krok 12) |

## 2. Karta źródła

[`KARTA_ZRODLA.md`](KARTA_ZRODLA.md), commit `8dad0b6` (26.11 15:25), przed pobraniem do budowy. A1 `common-pile/arxiv_papers@963fe980`
(22 pliki), A2 `common-pile/arxiv_abstracts@828e35d1` (4 pliki), kategorie i licencje z `librarian-bots/arxiv-metadata-snapshot@c428226b`
(CC0); sha256 w [`wyniki/przeglad_zrodla.json`](wyniki/przeglad_zrodla.json). Szacunek: A1 ~2,40 mld, A2 ~0,11 mld tok. v6; A3
(licencja domyślna, ~8 mld w Proof-Pile-2) odrzucone. Trenować: TAK (A1, A2); zgłosić: TAK.

## 3. Preregistracja

[`skrypty/preregistracja.json`](skrypty/preregistracja.json): seed 20261126, jedno źródło z dwoma plikami puli (A1, A2), wybór po
kategorii głównej (pełna lista docelowa), reguła licencji (bardziej restrykcyjna z dwóch zapisów), maskowanie e-maili przy budowie
(trzy wzorce), filtr budowy (licencja, pusty), reguły i aneksy InfiWebMath-4+ (24.11, 24.11b, 24.11c, 25.11b, 25.11c, 25.11e).
Odstępstwa: tryb PII `maskuj_email_usun_telefon_ip`, dodany `dedup_infiwebmath4`, bez `dedup_fineweb_edu_109` (źródło nie jest
stroną WWW; url `arxiv.org/abs/<id>` sprawdzany wobec FineMath-4+ i InfiWebMath-4+), filtr budowy przed detektorami. Preregistracja
jest w gicie dopiero w commicie puli `cf4dba5` (26.11 20:34); kolejność „przed budową” potwierdzają pole `zapisano` i dopiski
`poprawka_2026_11_26` (łamane e-maile) i `poprawka_2026_11_26_a2_id` (powtórzone id), oba przed eksportem i przeglądem.

| aneks / zapis | zapisany | treść |
|---|---|---|
| `dokument.maskowanie_emaili.poprawka_2026_11_26` | po 1. przebiegu budowy, przed przeglądem (commit `cf4dba5`) | e-mail złamany wierszem: maska na całym tekście, gdy maska wierszowa zostawia dopasowanie |
| `dokument.maskowanie_emaili.poprawka_2026_11_26_a2_id` | po 2. przebiegu budowy (commit `cf4dba5`) | 3 powtórzone id w abstraktach (8 wierszy): zostaje pierwsze |
| `aneks_2026_11_26_przeglad` | po przeglądzie, przed eksportem; commit `5b2d407` (22:36) | wynik przeglądu, FAIL-e przyjęte, szersze maskowanie e-maili przy eksporcie (krok 8) |

## 4. Środowisko

| | |
|---|---|
| Komenda | venv `../matematyka-wspolne/robocze/venv`; eksport: venv `../pr-zgloszenia/venv` |
| Tokenizer | v6 sha256 `0640d3bd…815dd` |
| Sprawdzenie | porównanie `pip freeze` = `requirements.txt`: nie zmierzono |

## 5. Pobranie i budowa puli

| | |
|---|---|
| Budowa | `buduj_pule.py` (commit `cf4dba5`); log `robocze/build.log` (pliki A1 00000–00021, A2 00000–00003, snapshot 3 224 542 prac) |
| Wybór | A1 docelowe 73 320 z 304 048; A2 docelowe 652 417 z 2 538 935 (8 powtórzonych id pominiętych) |
| Filtr budowy | 1 059 dok. / 22 759 056 tok. v6: `A1_licencja` 563 / 22 758 064 (abstrakty tych prac są w A2), `A1_pusty` 496 / 992 |
| Liczby | **652 409 dok., 2 532 068 972 tokenów v6**: A1 72 261 / 2 410 548 069 (mediana 24 998 tok., p99 155 383, max 9 942 746), A2 580 148 / 121 520 903 (mediana 191) |
| Licencje wierszy | A1: CC-BY-4.0 62 163, CC0-1.0 4 074, CC-BY-SA-4.0 3 807, CC-BY-3.0 1 747, CC-PDDC 470; A2: CC0-1.0 580 148 |
| E-maile przy budowie | zamaskowane dopasowania: `nazwa@domena` 117 796, `(AT)` 114, `at` bez nawiasów 714; po masce 0 / 0 / 0 tych trzech wzorców |
| Wynik | [`wyniki/budowa.json`](wyniki/budowa.json), [`wyniki/probka_pliki.json`](wyniki/probka_pliki.json) (sha256 plików puli) |

## 6. Indeksy i kontrole

- Testy, EN 1.07, walidacja Fabryki, `entech`, `en8x3b`, `wlasne:finemath4`, `wlasne:infiwebmath4`: te same indeksy co w częściach 2.
- Kontrola dodatnia: w `buduj_pule.py` asercje maskowania (`@`, `(AT)`, ` at `) i reguły licencji przed budową; wynik dla detektorów
  potoku nie zapisany (nie zmierzono).
- Próbka filtra budowy (40 na powód, `robocze/probka_filtra_budowy.jsonl`, jeden recenzent, `robocze/przeglad/oceny_filtra_budowy.json`):
  `A1_licencja` 40/40 trafne (licencja pusta = domyślna arXiv albo brak), `A1_pusty` 40/40.

## 7. Przebieg

| | |
|---|---|
| Komenda | `bash ../matematyka-wspolne/skrypty/potok_zrodla.sh arxiv_mat 4` (4 procesy) |
| Wynik | 132/132 jednostek, `KONIEC 2061s` (`przebieg.log`, 26.11 21:29); tokenizacja po 256 dok. (commit `e18ee48`: pełne prace dawały ~13 GB na proces, OOM i kernel panic przy pierwszej próbie) |
| `ew13` | `dokumentow 652409 z_trafieniem 4092 ngramow 9949`, `KONIEC` (21:29) |

## 8. Po przebiegu

`agreguj` 26.11 21:36 (`agreguj.log`), wynik [`wyniki/agreguj.json`](wyniki/agreguj.json):

| powód | odrzucone dok. | odrzucone tok. v6 | zostaje dok. | zostaje tok. v6 | % tok. | niezależnie dok. / % tok. |
|---|---|---|---|---|---|---|
| `walidacja_fabryki` | 2 | 328 | 652 407 | 2 532 068 644 | 100,0 | 2 / 0,0 |
| `domena_testow` | 0 | 0 | 652 407 | 2 532 068 644 | 100,0 | 0 / 0,0 |
| `ewal_13gram` | 624 | 28 909 335 | 651 783 | 2 503 159 309 | 98,858 | 624 / 1,142 |
| `pii` | 1 277 | 69 711 230 | 650 506 | 2 433 448 079 | 96,105 | 1 291 / 2,838 |
| `min_tresc` | 47 065 | 3 003 353 | 603 441 | 2 430 444 726 | 95,987 | 47 065 / 0,119 |
| `mojibake` | 30 | 1 263 777 | 603 411 | 2 429 180 949 | 95,937 | 33 / 0,062 |
| `dedup_wewnatrz` | 378 | 409 951 | 603 033 | 2 428 770 998 | 95,92 | 493 / 0,016 |
| `dedup_finemath4` | 2 | 1 195 | 603 031 | 2 428 769 803 | 95,92 | 2 / 0,0 |
| `dedup_infiwebmath4` | 2 | 905 | 603 029 | 2 428 768 898 | 95,92 | 2 / 0,0 |
| `dedup_slayer107` | 3 236 | 787 338 | 599 793 | 2 427 981 560 | 95,889 | 3 260 / 0,031 |
| `dedup_slayer_8x3b_en` | 2 | 578 | 599 791 | 2 427 980 982 | 95,889 | 2 / 0,0 |
| `dedup_english_technical` | 0 | 0 | 599 791 | 2 427 980 982 | 95,889 | 0 / 0,0 |

- **Uzysk: 599 791 dok., 2 427 980 982 tokenów v6 (95,889%)**: pełne teksty 70 226 / 2 310 331 144, abstrakty 529 565 / 117 649 838.
  Do eksportu: wszystkie zachowane.
- `min_tresc` to prawie wyłącznie krótkie abstrakty (< 50 słów); koszt 0,12% tokenów.
- `ewal_13gram` per test: MATH 523, MMLU 87, SQuAD2 7, HumanEval 5, TriviaQA 3, SynLogic 2, IFEval 2, MedMCQA 1, PolQA 1, BoolQ 1, MathQA 1.
- PII wg detektora DCLM (tryb `maskuj_email_usun_telefon_ip`): e-mail 0 (zamaskowane przy budowie), telefon 184, IP 1 112.
  `dedup_wewnatrz`: 210 identycznych, 283 przez MinHash.
- `dedup_fineweb_edu_109` nie ma w kaskadzie (odstępstwo z preregistracji: źródło nie jest stroną WWW). Pary dla `dedup_finemath4`
  i `dedup_infiwebmath4`: `para_wlasne.py`, w próbce 2 + 2 (strony abstraktów arXiv w FineMath-4+ i InfiWebMath-4+).

### Przegląd próbki (26.11.2026)

Próbka 841 pozycji (`robocze/probka_przegladu.jsonl`; 100 odrzuconych na powód, wszystkie przy mniejszych powodach, i 300 zachowanych,
tekst do 3000 znaków), pary z `para_wlasne.py` / `probka_z_parami.py`, dla `pii` i `mojibake` dopisane dopasowania detektora z pełnego
tekstu ±300 znaków ([`../matematyka-wspolne/skrypty/trafienia_probki.py`](../matematyka-wspolne/skrypty/trafienia_probki.py)), bo trafienie
leżało zwykle poza 3000 znakami. Recenzenci A i B: osobne, bezstanowe wywołania modelu na każdą pozycję (A: model domyślny, B: model
„slow”), pełny tekst pozycji, para i dopasowania w poleceniu z [`instrukcja_przegladu.md`](../matematyka-wspolne/instrukcja_przegladu.md).
**Odstępstwo od „dwóch agentów”**: z 32 uruchomień agentów recenzujących (16 wycinków × 2 próby) 25 zablokował dostawca
(„Refusal (reasoning_extraction)”), 7 ukończyło (w tym 1 z przyznaną niepełną lekturą par); ich oceny (`robocze/przeglad/oceny_agenci_A|B`,
841 ocen z 1 682 potrzebnych) nie są liczone. Porównanie z ocenami końcowymi na tych samych pozycjach: 0 sprzeczności tak/nie; różnice to
„wątpliwy” agentów bez dopasowań z pełnego tekstu (`pii` 79, `mojibake` 16 + 16 + 16) i 2 abstrakty „wątpliwe” u A końcowego. Wynik
[`wyniki/przeglad_1.json`](wyniki/przeglad_1.json). Progi: fałszywe odrzucenia ≤ 10% ORAZ górna granica Wilsona ≤ 20%.

| powód | n | A: fałszywe (wątpliwe) | A: [Wilson 95%] | B: fałszywe (wątpliwe) | B: [Wilson 95%] | werdykt A/B |
|---|---|---|---|---|---|---|
| `walidacja_fabryki` | 2 | 0 (0) | [0; 65,8] | 0 (0) | [0; 65,8] | FAIL/FAIL |
| `ewal_13gram` | 100 | 100 (0) | [96,3; 100] | 100 (0) | [96,3; 100] | FAIL/FAIL |
| `pii` | 100 | 89 (0) | [81,4; 93,7] | 89 (0) | [81,4; 93,7] | FAIL/FAIL |
| `min_tresc` | 100 | 0 (0) | [0; 3,7] | 0 (0) | [0; 3,7] | PASS/PASS |
| `mojibake` | 33 | 0 (0) | [0; 10,4] | 0 (0) | [0; 10,4] | PASS/PASS |
| `dedup_wewnatrz` | 100 | 0 (0) | [0; 3,7] | 0 (0) | [0; 3,7] | PASS/PASS |
| `dedup_finemath4` | 2 | 0 (0) | [0; 65,8] | 0 (0) | [0; 65,8] | FAIL/FAIL |
| `dedup_infiwebmath4` | 2 | 0 (0) | [0; 65,8] | 0 (0) | [0; 65,8] | FAIL/FAIL |
| `dedup_slayer107` | 100 | 0 (0) | [0; 3,7] | 0 (0) | [0; 3,7] | PASS/PASS |
| `dedup_slayer_8x3b_en` | 2 | 0 (2) | [0; 65,8] | 0 (2) | [0; 65,8] | FAIL/FAIL |

| zachowane (300) | A | B | próg | werdykt |
|---|---|---|---|---|
| śmieci | 0: 0% [0; 1,3], wątpliwe 5 | 0: 0% [0; 1,3], wątpliwe 2 | ≤ 10% | PASS |
| przeoczone PII | 2/300 | 2/300 | 0/300 | FAIL → aneks (maskowanie) |
| przeoczony test | 0/300 | 0/300 | 0/300 | PASS |

**Werdykt pliku: NIE PRZESZŁO** (u obu: `ewal_13gram`, `pii`, `pii_przeoczone`, `walidacja_fabryki`, `dedup_finemath4`,
`dedup_infiwebmath4`, `dedup_slayer_8x3b_en`).

### Aneks 26.11 przegląd (commit `5b2d407`)

FAIL-e przyjęte przed eksportem (reguły zachowawcze, koszt < 5%):
- `ewal_13gram`: 100/100 fałszywych u obu (wspólne formułki LaTeX: macierze, definicje); koszt 1,14% tokenów.
- `pii`: 89/100 fałszywych u obu (numery podrozdziałów `8.2.3.1` i wersji jako IPv4); 11 prawdziwych telefonów/faksów w nagłówkach;
  koszt 2,84%; prywatność ma pierwszeństwo.
- `walidacja_fabryki`, `dedup_finemath4`, `dedup_infiwebmath4`, `dedup_slayer_8x3b_en`: 0/2 — FAIL tylko z górnej granicy Wilsona
  przy n = 2 (`dedup_slayer_8x3b_en`: 2 wątpliwe, bo w próbce brak `wynik_indeksu`).

Przeoczone PII 2/300 (próg 0/300 nie dopuszcza przyjęcia): e-mail w klamrach `{a, b}@domena` i adres z domeną złamaną wierszem po
łączniku. Zmiana przed eksportem: `premask_emails(text, wrapped=True)` w
[`../matematyka-wspolne/eksport/src/mat_wybor.py`](../matematyka-wspolne/eksport/src/mat_wybor.py) (`EMAIL_LATEX`, `EMAIL_BRACED`,
`EMAIL_WRAPPED`): nazwy w składni `$…$@domena`, listy w klamrach/nawiasach/`<>` lub zniekształconych `–…˝` do 3 wierszy, łamanie
wiersza przed, po i w domenie, spacje wokół `@`, `@@`. Kontrole:
- 300 zachowanych po zmianie: 0 adresów (przed: 2).
- Cała pula po pierwszej wersji poprawki (klamry w jednym wierszu, łącznik): `resztki_email.py wyniki/probka_pliki.json 0 300 1` —
  880 dokumentów z `@domena` (`robocze/przeglad/resztki_email_pula.json`, 23 min); formy z 829 trafień weszły do wzorców.
- Cała pula po wersji końcowej (652 409 dok., 4 procesy, 3,5 min): **0 dokumentów z nazwą lokalną przed `@domena.tld`**; zostają
  same domeny bez nazwy (`mailto:@uni.edu`, „Corresponding author: @uni.edu” — nazwę usunęło już źródło), to nie są dane osobowe.
- Nadmiarowe maskowanie: do jednego słowa przed `\n@domena` i fragment do 200 znaków grupy `$…$` tuż przed `@domena` (nagłówki autorów).

## 9. Eksport

| | |
|---|---|
| Podział | [`wyniki/czesci.json`](wyniki/czesci.json) (`czesci.py`, cel 300 mln tok. v6): 8 części po ~303 mln tok. v6; p01–p07 pełne teksty (9 034–10 104 dok.), p08 reszta prac i wszystkie abstrakty (535 098 dok.). Mniejsze niż ~1 mld w innych źródłach: `shard.write` i `check.py` liczą tokeny całej części w pamięci (proces eksportu p08: ~12 GB RSS) |
| Key | `arxiv_math_en`; datasheet [`eksport/arxiv_math_en.md`](eksport/arxiv_math_en.md); wpis w `../matematyka-wspolne/eksport/src/sources.py` (licencja per wiersz); skrypt `../matematyka-wspolne/eksport/src/clean_arxiv_math_en.py` (commity `14f44f4`, `5b2d407`): `premask_emails(..., wrapped=True)` przed `shard.write`, Presidio wyłączone (`no_masking(emails=True)`) |
| Eksport | `../matematyka-wspolne/skrypty/eksport_czesci.sh arxiv_mat robocze/czesci robocze/eksport` (`robocze/logi/eksport.log`, `KONIEC 8`, 26.11 22:36–23:55; p03, p06, p07, p08 ponownie po aneksie 27.11, `eksport2.log`, 00:30–01:20; p02, p03, p04, p06, p08 ponownie po aneksie 27.11 nr 2, `eksport3.log`): **599 703 dok.**, 2 231 710 716 `token_count` (licznik repo zgłoszeń, nie v6); `dropped`: wrong_language 88 (z 599 791); zamaskowane przy eksporcie: 3 724 adresy (`stats.json` `pii.counts.pii`) |

| część | dok. | `token_count` | wrong_language | sha256 | linie `check.py` |
|---|---|---|---|---|---|
| `arxiv_math_en_p01` | 10 094 | 278 854 233 | 10 | `6b274a3e0c8be034e97fad7d200178c65841dfda924816044ad9fd85a6752adb` | 115 |
| `arxiv_math_en_p02` | 9 063 | 279 289 772 | 7 | `24cb9b143c32e3108a863cd9f1d42491e8c08de880fe845894c9d7ed9332f655` | 116 |
| `arxiv_math_en_p03` | 9 257 | 279 490 716 | 9 | `81640d0ad5fcd752559e5d4096586c43d4474401335abbf92f080d9cb8be29da` | 137 |
| `arxiv_math_en_p04` | 9 068 | 279 496 121 | 7 | `84d47945618db4753dd6f6c8338ceec1d2eeede9e84c5c115bedfedb9d008073` | 127 |
| `arxiv_math_en_p05` | 9 100 | 279 251 299 | 9 | `930c71a692699f0356c03c69e1fa4a4db0c2b3e369bbe9b7783065d9aebd70a3` | 135 |
| `arxiv_math_en_p06` | 9 028 | 279 871 473 | 6 | `e9addecb892ffc7b3fc3ae1babdbac9929bd74d8a2981381d47afe5ddca67ab9` | 139 |
| `arxiv_math_en_p07` | 9 025 | 279 489 431 | 10 | `1db60e067882e5fc1870a6eaa1e56459cf07d5abce041caf398164bf9c77d8d4` | 140 |
| `arxiv_math_en_p08` | 535 068 | 275 967 671 | 30 | `6246ac2a8212cfea30cbbf5d57690765e3ad7f349d9b11280f018777ccbb1f3a` | 5 |

## 10. Kontrola końcowa

| | |
|---|---|
| Test kontraktowy, `check.py` | test kontraktowy 1 passed w każdej z 8 części; `check.py` 5–140 linii na część, wyłącznie oczekiwane („PII left after masking: second pass adds ['[PHONE]']” — numery w matematyce, Presidio wyłączone; „stats.json pii has no presidio record”); `eksport_czesci.sh` przerywa przy każdej innej linii |
| Resztki e-maili po eksporcie (pierwszy eksport) | `resztki_email.py robocze/eksport/pliki_eksportu.json 0 300 1` na 8 plikach parquet: 232 dok. z trafieniem szerokiego wzorca (`robocze/logi/resztki_email_eksport.json`), w tym 7 adresów osób w formach bez `@` (`[at] … dot com`, `{at}`, `AT\n`) → aneks 27.11, ponowny eksport p03, p06, p07, p08 (zmiana tylko tych 7 adresów, porównanie tekstu przed i po masce); reszta: „available at\ngithub.com”, same domeny `@uni.edu` bez nazwy, `@numba.jit`. Pełny `resztki_email.py` po ponownym eksporcie: nie uruchomiony (sprawdzone tylko 7 znanych adresów i brak innych zmian) |
| Resztki e-maili po aneksach 27.11 (pełny `resztki_email.py` na 8 częściach) | po aneksie nr 1: 225 dok. z trafieniem (`robocze/logi/resztki_email_eksport_po_aneksie.log`), w tym 5 adresów `login at\ngmail dot com` → aneks nr 2; po aneksie nr 2: **220 dok.** (`robocze/logi/resztki_email_eksport_po_aneksie2.json`; p01 26, p02 25, p03 32, p04 30, p05 29, p06 21, p07 19, p08 38), wszystkie przejrzane przykłady bez nazwy osoby: proza „available at\ngithub.com”, „tz at\nwww.uhasselt.be” (adres strony), same domeny `@uni.edu`, `@numba.jit`; skan puli: 0 dok. z nazwą lokalną przed `@domena` |
| Niezależny agent na pliku o tym samym sha256 | nie zmierzono (kontrola skryptem: 26 części `data/` = 26 bliźniaków `tokenized/slayer-v6/`, `dokumenty` = wiersze parquetu, `zrodlo_sha256` = sha256 LFS, 27.11) |

## 11. Wysyłka

Repo `Lolita67/matematyka-kod-en-robocze` (gated manual), `data/arxiv_math_en_p01..p08/` (parquet, datasheet części, `stats.json`),
commity HF `712be5ab` (p01–p04), `7eed66e6` (p05–p07), `8a16f958` (p08), po aneksie 27.11 `1fecb954` (p03, p06, p07, p08 zastąpione), po aneksie 27.11 nr 2 `cd727d60` (p02, p03, p04, p06, p08 zastąpione, stare `tokenized` usunięte w tym samym commicie; sha256 w tabeli §9); sha256 LFS zgodne z `robocze/eksport/<k>/<k>.sha256` w 8/8
(API HF); anonimowe pobranie: 401. Dostęp dla `Maggio33`: czeka na właścicielkę (Settings → Gated user access).

## 12. Dane treningowe

Wersja stokenizowana `tokenized/slayer-v6/arxiv_math_en_p01..p08` (`tokenizuj_hf.py`, po 256 dok.): **599 703 dok. (= wiersze parquetów), 2 425 618 929 tokenów v6** (z EOT; o 2,36 mln mniej niż `uzysk` 2 427 980 982 przez 88 dok. odrzuconych bramką języka i maskowanie e-maili). p01, p02, p04, p05 z 27.11 ~00:00 (`robocze/logi/tokenizacja.log`); p03, p06, p07, p08 usunięte (`8763e5d7`) i stokenizowane ponownie z nowych parquetów (`tokenizacja2.log`). `zrodlo_sha256` w każdym `.json` = sha256 LFS parquetu.

## Historia odtworzeń

- 26.11.2026 15:25: karta (`8dad0b6`).
- 26.11.2026 przed 20:34: budowa puli (dwa przebiegi z poprawkami maskowania i id), preregistracja i pula w gicie (`cf4dba5`); nakładka
  eksportu (`14f44f4`, 20:35).
- 26.11.2026 przed 20:54: pierwsza próba przebiegu: OOM i kernel panic (tokenizacja całych grup wierszy pełnych prac); poprawka `e18ee48`.
- 26.11.2026 21:29: `przebieg` 132/132 (`KONIEC 2061s`), `ew13`; 21:36 `agreguj`: 599 791 / 2 427 980 982 (95,889%).
- 26.11.2026 21:40–22:30: przegląd próbki (wywołania modelu A/B po próbach z agentami), skan e-maili w puli, aneks
  `aneks_2026_11_26_przeglad` przed eksportem (`5b2d407`, 22:36).
- 26.11.2026 22:36–23:55: eksport 8 części (`KONIEC 8`), testy kontraktowe, `check.py` tylko oczekiwane linie; wysyłka HF `712be5ab`,
  `7eed66e6`, `8a16f958`, sha256 zgodne, anonimowo 401.
- 27.11.2026 00:00–00:30: tokenizacja v6 8 części; `resztki_email.py` na eksporcie: 7 adresów bez `@` → `aneks_2026_11_27_resztki`.
- 27.11.2026 00:30–01:50: ponowny eksport p03, p06, p07, p08, wysyłka `1fecb954`, ponowna tokenizacja; kontrola 26/26 części z bliźniakiem, README HF.
- 27.11.2026 rano: pełny `resztki_email.py` (225 dok.), `aneks_2026_11_27_resztki_2`, ponowny eksport p02, p03, p04, p06, p08 (`eksport3.log`), wysyłka `cd727d60`, tokenizacja (`tokenizacja3.log`), pełny `resztki_email.py` (220 dok., 0 adresów osób), kontrola końcowa (`../matematyka-wspolne/DZIENNIK.md`).

## Pułapki tego przebiegu

- Pełne prace arXiv są długie (mediana 25 tys., max 9,9 mln tokenów v6): tokenizacja całych grup wierszy (do 5 000 prac) dawała ~13 GB
  na proces i kernel panic; teraz po 256 dok. (`przebieg.py`, `tokenizuj_hf.py`), części eksportu po ~300 mln tok.
- Detektor PII DCLM bierze numery podrozdziałów (`8.2.3.1`) za IPv4: 89% fałszywych odrzuceń `pii` (koszt 2,84%, przyjęty).
- E-maile autorów mają w arXiv wiele form (listy w klamrach przez kilka wierszy, `$nazwa$@`, łamanie po łączniku, `@@`): trzy wzorce
  z budowy zostawiły 2/300 w próbce i ~880 dokumentów w puli; wzorce dopisane aneksem przed eksportem.
- Próbka pokazuje 3000 znaków, a trafienia `pii`/`mojibake` leżą zwykle dalej: bez `trafienia_probki.py` recenzent nie rozstrzyga.
- Agenci recenzujący byli masowo blokowani przez dostawcę („Refusal (reasoning_extraction)”) już na etapie lektury; recenzja
  wywołaniami modelu na pozycję omija problem i gwarantuje lekturę pełnego tekstu pozycji.
