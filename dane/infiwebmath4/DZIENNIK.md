# Dziennik zbioru: InfiWebMath-4+ (EN) dla Slayera 1B, część 2

Przepis: [`METODOLOGIA.md` w repo zespołu](https://github.com/slayerlabs/benchmarks-fabryka-ai/blob/main/research/slayer-1b/dane/METODOLOGIA.md).
Karta źródła: [`KARTA_ZRODLA.md`](KARTA_ZRODLA.md). Reguły: [`skrypty/preregistracja.json`](skrypty/preregistracja.json).
Skrypty wspólne zbiorów #346: [`../matematyka-wspolne/skrypty/`](../matematyka-wspolne/skrypty/), każdy krok to
`bash dane/matematyka-wspolne/skrypty/odtworz.sh <krok> infiwebmath4`. Logi kroków: `robocze/logi/` (poza gitem).
Dzienniki bliźniacze: [FineMath-4+](../finemath4/DZIENNIK.md) (reguły i część 2, wobec której jest `dedup_finemath4`),
[CraneMath](../cranemath/DZIENNIK.md), [Stack-Edu Python](../stackedu/DZIENNIK.md).

## Bramki praw

| bramka | wynik |
|---|---|
| Można TRENOWAĆ | TAK (wyjątek TDM art. 4 dyr. 2019/790 dla tekstów, ODC-By dla kompilacji; takedown po `url` albo `WARC-Record-ID`); opt-out TDM NIE SPRAWDZONY |
| Można ZGŁOSIĆ do `dataset-team-submissions` | NIEROZSTRZYGNIĘTY: ODC-By dotyczy kompilacji, licencja per dokument nieznana, część domen z SA albo restrykcyjnym regulaminem; datasheet `held_for_review` |

## 1. Rezerwacja

| | |
|---|---|
| Co | issue [#346](https://github.com/slayerlabs/benchmarks-fabryka-ai/issues/346) (część 2) |
| Cel | część 2 zbioru matematyki i kodu ok. 20 mld tokenów v6: strony matematyczne spoza FineMath-4+ |
| Wiersz w danych treningowych | nie zmierzono (krok 12) |

## 2. Karta źródła

[`KARTA_ZRODLA.md`](KARTA_ZRODLA.md), 25.11.2026, przed pobraniem (commit `05447f8`, 08:01). `HuggingFaceTB/finemath@e92b25a6`,
config `infiwebmath-4plus` (32 pliki), z InfiMM-WebMath-40B. `id` = `WARC-Record-ID` z `metadata.WARC_HEADER`, `url` w 100% wierszy
shardu 0. Karta szacowała ok. 65-73% url wspólnych z FineMath-4+ (pomiar na 4 z 64 plików). Trenować: TAK; zgłosić: NIEROZSTRZYGNIĘTY.

## 3. Preregistracja

[`skrypty/preregistracja.json`](skrypty/preregistracja.json), commit `05447f8` (25.11 08:01) przed pobraniem puli: seed 20261125,
cała pula = eksport, reguły i aneksy (24.11, 24.11b, 24.11c, 25.11b) przejęte z FineMath-4+ bez zmian treści, nowy powód
`dedup_finemath4` (url, MinHash J ≥ 0,8 albo identyczny tekst wobec wyboru części 2 FineMath-4+), ręczna próbka 100 odrzuconych
na powód + 300 zachowanych, dwóch recenzentów.

| aneks | commit | zapisany | treść |
|---|---|---|---|
| `aneks_2026_11_25c` | `601e1bc` (14:30) | po próbce kontrolnej części 2 FineMath-4+, przed agregacją InfiWebMath-4+ (`agreguj.log` 18:29) | `pii_at_bez_nawiasow`: e-mail `nazwa at domena.tld` bez nawiasów usuwa dokument (przeoczenie w FineMath-4+ cz2, FAIL 0/200) |
| `aneks_2026_11_25e` | `3c13221` (18:49) | po przeglądzie próbki, przed eksportem | wynik przeglądu, FAIL-e reguł konserwatywnych i śmieci u B przyjęte (podsekcja w kroku 8) |

Pole `zapisano` aneksu 25.11e mówi „ok. 21:30”, a commit `3c13221` ma 18:49; godzina w polu: nie zgadza się z commitem.

## 4. Środowisko

| | |
|---|---|
| Komenda | `odtworz.sh venv` (wspólny venv `../matematyka-wspolne/robocze/venv`, jak FineMath-4+) |
| Tokenizer | v6 sha256 `0640d3bd…815dd` |
| Sprawdzenie | porównanie `pip freeze` = `requirements.txt`: nie zmierzono |

## 5. Pobranie

| | |
|---|---|
| Komenda | `odtworz.sh pula infiwebmath4`, 25.11.2026 (log `pula.log`, 10:09) |
| Kod wyjścia | `KONIEC 6296212 9310103443`; kod bash nie zapisany w logu |
| Liczby | 32 pliki z 32 w kolejności `default_rng(20261125)`, rewizja `e92b25a6`; 6 296 212 dokumentów, 9 310 103 443 tokenów v6 |
| Wynik | [`wyniki/probka_pliki.json`](wyniki/probka_pliki.json) (sha256 i wiersze każdego pliku) |

## 6. Indeksy i kontrole

- Testy, EN 1.07, walidacja Fabryki, `entech`, `fwe109`, `en8x3b`: te same indeksy co FineMath-4+ (dziennik FineMath-4+, krok 6).
- Baza `dedup_finemath4`: indeks wyboru części 2 FineMath-4+ (`bazy_mat.py wlasne:finemath4` z `dane/finemath4/robocze/cz2`); log jego
  budowy: w katalogu FineMath-4+. Log `wlasne.log` tego zbioru (25.11 18:30, `KONIEC 1027027` = uzysk InfiWebMath-4+) to [I] indeks
  własnego wyboru InfiWebMath-4+ dla kolejnych źródeł.
- Kontrola dodatnia: **nie zmierzono** na tym źródle; reguły i indeksy są te same co w FineMath-4+, gdzie kontrola przeszła 19/19
  ([`../finemath4/wyniki/kontrola.json`](../finemath4/wyniki/kontrola.json)). Nowe reguły `dedup_finemath4` i `pii_at_bez_nawiasow`
  nie mają tu przypadku kontrolnego.

## 7. Przebieg

| | |
|---|---|
| Komenda | `odtworz.sh przebieg infiwebmath4`, 25.11.2026 |
| Wynik | 1280/1280 jednostek, `KONIEC 13953s` (log `przebieg.log`, 14:01); kod wyjścia nie zapisany w logu |
| `ew13` | wynik w `robocze/wyniki/ew13`; log: nie zapisany |

## 8. Po przebiegu

Komenda `odtworz.sh agreguj infiwebmath4`; przebieg 25.11.2026 18:29 (`agreguj.log`, `KONIEC`), wynik
[`wyniki/agreguj.json`](wyniki/agreguj.json). Kaskada (powód = pierwszy w kolejności preregistracji):

| powód | odrzucone dok. | odrzucone tok. v6 | zostaje dok. | zostaje tok. v6 | % tok. | niezależnie dok. / % tok. |
|---|---|---|---|---|---|---|
| `walidacja_fabryki` | 1 968 | 2 491 853 | 6 294 244 | 9 307 611 590 | 99,973 | 1 968 / 0,027 |
| `domena_testow` | 46 217 | 108 310 030 | 6 248 027 | 9 199 301 560 | 98,81 | 46 294 / 1,165 |
| `ewal_13gram` | 74 411 | 223 125 410 | 6 173 616 | 8 976 176 150 | 96,413 | 75 211 / 2,439 |
| `pii` | 105 498 | 354 221 501 | 6 068 118 | 8 621 954 649 | 92,609 | 108 157 / 3,968 |
| `pii_zaciemniony` | 2 733 | 6 310 070 | 6 065 385 | 8 615 644 579 | 92,541 | 2 876 / 0,077 |
| `pii_at_bez_nawiasow` | 33 686 | 141 360 017 | 6 031 699 | 8 474 284 562 | 91,022 | 38 405 / 1,713 |
| `min_tresc` | 42 737 | 3 728 135 | 5 988 962 | 8 470 556 427 | 90,982 | 42 803 / 0,04 |
| `mojibake` | 20 761 | 93 153 939 | 5 968 201 | 8 377 402 488 | 89,982 | 23 557 / 1,227 |
| `dedup_wewnatrz` | 2 372 245 | 3 625 482 832 | 3 595 956 | 4 751 919 656 | 51,04 | 2 521 806 / 43,309 |
| `dedup_finemath4` | 2 156 847 | 3 112 315 778 | 1 439 109 | 1 639 603 878 | 17,611 | 3 869 230 / 63,21 |
| `dedup_slayer107` | 226 479 | 278 871 641 | 1 212 630 | 1 360 732 237 | 14,616 | 418 710 / 6,321 |
| `dedup_slayer_8x3b_en` | 3 571 | 4 173 754 | 1 209 059 | 1 356 558 483 | 14,571 | 13 932 / 0,19 |
| `dedup_english_technical` | 2 | 10 294 | 1 209 057 | 1 356 548 189 | 14,571 | 10 / 0,0 |
| `dedup_fineweb_edu_109` | 182 030 | 214 563 336 | 1 027 027 | 1 141 984 853 | 12,266 | 599 025 / 8,242 |

- **Uzysk: 1 027 027 dok., 1 141 984 853 tokenów v6 (12,266%)**. Do eksportu: wszystkie zachowane.
- `dedup_wewnatrz` zabiera w kaskadzie 38,9 pkt proc. tokenów puli (89,982% → 51,04%; niezależnie 43,3%): wiele zrzutów tej samej
  strony, 1 503 028 identycznych tekstów i 1 018 778 dopasowań MinHash. `dedup_finemath4` kolejne 33,4 pkt proc. (51,04% → 17,611%;
  niezależnie 63,2%): strona już w części 2 FineMath-4+.
- `ewal_13gram` per test (dokumenty): MathQA 31 899, MATH 31 343, HumanEval 4222, MBPP 3630, MMLU 3459, BoolQ 644, SQuAD2 580,
  GSM-Plus 365, SciQ 336, reszta ≤ 131.
- PII wg detektora DCLM: e-mail 83 361, telefon 14 053, IP 15 457 (tryb `usun`). 3 dokumenty z `id` = 0 (`dok_z_id0`).

### Przegląd próbki (25.11.2026)

Dwóch niezależnych recenzentów (A, B), 1610 pozycji: po 100 odrzuconych na powód (`dedup_english_technical`: 10, tyle było) i 300
zachowanych, pełne teksty; wynik [`wyniki/przeglad_1.json`](wyniki/przeglad_1.json). `dedup_finemath4` oceniany z parą FineMath-4+
ze skryptu [`../matematyka-wspolne/skrypty/para_wlasne.py`](../matematyka-wspolne/skrypty/para_wlasne.py); pierwsza ocena bez pary
unieważniona, bo zakładała dopasowanie po url (aneks 25.11e). Progi: fałszywe odrzucenia ≤ 10% ORAZ górna granica Wilsona ≤ 20%.

| powód | n | A: fałszywe (wątpliwe) | A: [Wilson 95%] | B: fałszywe (wątpliwe) | B: [Wilson 95%] | werdykt A/B | koszt % tok. (niezależnie) |
|---|---|---|---|---|---|---|---|
| `walidacja_fabryki` | 100 | 9 (19) | [4,8; 16,2] | 0 (1) | [0; 3,7] | PASS/PASS | 0,027 |
| `domena_testow` | 100 | 0 (0) | [0; 3,7] | 0 (0) | [0; 3,7] | PASS/PASS | 1,165 |
| `ewal_13gram` | 100 | 42 (6) | [32,8; 51,8] | 44 (8) | [34,7; 53,8] | FAIL/FAIL | 2,439 |
| `pii` | 100 | 15 (46) | [9,3; 23,3] | 4 (57) | [1,6; 9,8] | FAIL/PASS | 3,968 |
| `pii_zaciemniony` | 100 | 4 (2) | [1,6; 9,8] | 1 (42) | [0,2; 5,4] | PASS/PASS | 0,077 |
| `pii_at_bez_nawiasow` | 100 | 80 (0) | [71,1; 86,7] | 34 (46) | [25,5; 43,7] | FAIL/FAIL | 1,713 |
| `min_tresc` | 100 | 0 (0) | [0; 3,7] | 0 (0) | [0; 3,7] | PASS/PASS | 0,04 |
| `mojibake` | 100 | 0 (0) | [0; 3,7] | 0 (26) | [0; 3,7] | PASS/PASS | 1,227 |
| `dedup_wewnatrz` | 100 | 0 (0) | [0; 3,7] | 0 (0) | [0; 3,7] | PASS/PASS | 43,309 |
| `dedup_finemath4` | 100 | 0 (0) | [0; 3,7] | 0 (0) | [0; 3,7] | PASS/PASS | 63,21 |
| `dedup_slayer107` | 100 | 0 (1) | [0; 3,7] | 0 (0) | [0; 3,7] | PASS/PASS | 6,321 |
| `dedup_slayer_8x3b_en` | 100 | 0 (0) | [0; 3,7] | 0 (0) | [0; 3,7] | PASS/PASS | 0,19 |
| `dedup_english_technical` | 10 | 0 (0) | [0; 27,8] | 0 (0) | [0; 27,8] | FAIL/FAIL | 0,0 |
| `dedup_fineweb_edu_109` | 100 | 0 (0) | [0; 3,7] | 0 (0) | [0; 3,7] | PASS/PASS | 8,242 |

| zachowane (300) | A | B | próg | werdykt |
|---|---|---|---|---|
| śmieci | 26: 8,7% [6,0; 12,4], wątpliwe 46 | 31: 10,3% [7,4; 14,3], wątpliwe 58 | ≤ 10% | PASS/FAIL |
| przeoczone PII | 0/300 | 0/300 | 0/300 | PASS |
| przeoczony test | 0/300 | 0/300 | — | PASS |

**Werdykt pliku: NIE PRZESZŁO** (A: `dedup_english_technical`, `ewal_13gram`, `pii`, `pii_at_bez_nawiasow`; B:
`dedup_english_technical`, `ewal_13gram`, `pii_at_bez_nawiasow`, śmieci).

### Aneks 25.11e (commit `3c13221`)

FAIL-e przyjęte przed eksportem:
- `ewal_13gram` 42% / 44%: formułki, kod Asymptote, idiomy Pythona; koszt 2,4% tokenów puli; reguła usuwa dobre teksty, nie
  przepuszcza złych; poprawka (wykluczenie formułek) odroczona.
- `pii` A 15% (cyfry π, ISBN, numery rozdziałów jako IP), B 4%; 46-57% trafień poza widocznymi 3000 znakami (nieocenialne);
  koszt 3,7% tokenów (plik `agreguj.json`: 3,968% niezależnie); prywatność ma pierwszeństwo.
- `pii_at_bez_nawiasow` A 80%, B 34% (frazy „here at Shaalaa.com”); koszt 1,5% tokenów (plik: 1,713% niezależnie); reguła
  konserwatywna z aneksu 25.11c.
- `dedup_english_technical` 0/10 u obu: FAIL tylko z górnej granicy Wilsona przy n = 10.
- Śmieci B 10,3% (A 8,7%): cecha źródła jak FineMath-4+ (aneks 24.11c), filtr jakości odroczony, opisany w datasheet.

## 9. Eksport

| | |
|---|---|
| Podział | [`wyniki/czesci.json`](wyniki/czesci.json): 1 część, `infiwebmath_4plus_en_p01`, 1 027 027 dok., 1 141 984 853 tokenów v6 |
| Key | `infiwebmath_4plus_en`; datasheet [`eksport/infiwebmath_4plus_en.md`](eksport/infiwebmath_4plus_en.md) (status `held_for_review`); wpis w `../matematyka-wspolne/eksport/src/sources.py` |
| Eksport | `../matematyka-wspolne/skrypty/eksport_czesci.sh` (`robocze/logi/eksport.log`, `KONIEC 1`): 1 025 440 dok., 1 049 426 401 `token_count` (licznik repo zgłoszeń, nie v6); `dropped`: wrong_language 1 515, min_chars 72; sha256 `b854ae40fd66dbaf9509614f65db5c14d3d601a82587ff55b2731ddc6af5bbec` |
| PII | Presidio wyłączone jak w FineMath-4+ (`no_masking()` w `../matematyka-wspolne/eksport/src/mat_wybor.py`); dokumenty z PII usunięte wcześniej w całości |

## 10. Kontrola końcowa

| | |
|---|---|
| Test kontraktowy, `check.py` | test kontraktowy 1 passed; `check.py` 21 linii, wyłącznie oczekiwane („PII left after masking”, „no presidio record”) |
| Niezależny agent na pliku o tym samym sha256 | nie zmierzono |

## 11. Wysyłka (repo do wglądu Arka)

Repo `Lolita67/infiwebmath_4plus_en-robocze`, gated manual ustawione PRZED wysyłką (repo nigdy nie było otwarte), commit HF `3075ec3c`; sha256 LFS zgodne (API HF); anonimowe pobranie: 401. Dostęp dla `Maggio33`: czeka na właścicielkę (Settings → Gated user access).

## 12. Dane treningowe

Czeka na wysyłkę: nie zmierzono.

## Historia odtworzeń

- 25.11.2026 08:01: karta i preregistracja przed pobraniem (`05447f8`).
- 25.11.2026 10:09: `pula`: 6 296 212 dok., 9 310 103 443 tokenów v6.
- 25.11.2026 14:01: `przebieg` 1280/1280 (`KONIEC 13953s`).
- 25.11.2026 14:30: aneks 25.11c (`601e1bc`): `pii_at_bez_nawiasow`, przed agregacją.
- 25.11.2026 18:29: `agreguj`: 1 027 027 / 1 141 984 853 (12,266%); 18:30 indeks własnego wyboru (`wlasne.log`, `KONIEC 1027027`).
- 25.11.2026 18:49: przegląd 1610 pozycji i aneks 25.11e (`3c13221`), przed eksportem.
- 25.11.2026 ok. 20:00: eksport (`KONIEC 1`, sha256 `b854ae40…`), `check.py` tylko oczekiwane linie; wysyłka HF `3075ec3c`, sha256 zgodne, anonimowo 401.

## Pułapki tego przebiegu

- InfiWebMath-4+ ma wiele zrzutów tej samej strony z różnych lat: dedup wewnątrz zabiera ok. 39 pkt proc. tokenów, a dedup wobec
  FineMath-4+ kolejne 33 pkt proc.; skala źródła z karty (8,5 mld tokenów Llamy) nie mówi nic o przyroście unikalnych stron.
- Para do oceny `dedup_finemath4` musi pochodzić z indeksu (`para_wlasne.py`): pierwsza ocena bez pary zakładała dopasowanie po url i została
  unieważniona.
- Brak kolumn `warc_filename`/`offset`: takedown i `id` tylko przez `url` i `WARC-Record-ID` z `metadata.WARC_HEADER`; nagłówek
  WARC zawiera IP serwera, więc z metadanych bierzemy tylko `WARC-Record-ID` i `WARC-Date`.

## Repo po scaleniu (26.11)

`Lolita67/infiwebmath_4plus_en-robocze` usunięte 26.11. Ten sam plik parquet (sha256 LFS zgodny) leży w `Lolita67/math-code-en` (do 27.11 `Lolita67/matematyka-kod-en-robocze`), katalog `data/infiwebmath_4plus_en_p01`.
