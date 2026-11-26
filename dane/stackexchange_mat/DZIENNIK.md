# Dziennik zbioru: Stack Exchange — matematyka i logika (EN) dla Slayera 1B, część 3

Przepis: [`METODOLOGIA.md` w repo zespołu](https://github.com/slayerlabs/benchmarks-fabryka-ai/blob/main/research/slayer-1b/dane/METODOLOGIA.md).
Karta źródła: [`KARTA_ZRODLA.md`](KARTA_ZRODLA.md). Reguły: [`skrypty/preregistracja.json`](skrypty/preregistracja.json).
Detektory i agregacja: [`../matematyka-wspolne/skrypty/`](../matematyka-wspolne/skrypty/). Logi: `robocze/logi/` (poza gitem).
Dzienniki bliźniacze: [InfiWebMath-4+](../infiwebmath4/DZIENNIK.md) (reguły przejęte), [FineMath-4+](../finemath4/DZIENNIK.md),
[OEIS](../oeis/DZIENNIK.md), [formalna](../formalna/DZIENNIK.md).

## Bramki praw

| bramka | wynik |
|---|---|
| Można TRENOWAĆ (także komercyjnie) | TAK na licencji autorów: CC BY-SA 2.5/3.0/4.0 per dokument (wszystkie posty z licencją); zapasowo wyjątek TDM; takedown po serwisie i id pytania |
| Można ZGŁOSIĆ do `dataset-team-submissions` | NIEROZSTRZYGNIĘTY: do przeglądu praw zespołu (opt-out platformy `ai-train=no` wobec licencji autorów); decyzja `held_for_review` |
| Użycie komercyjne | dozwolone: CC BY-SA pozwala na użycie komercyjne; SA dotyczy dalszego udostępniania samych danych |
| Opt-out platformy | V (karta §2): od 2024 r. `Content-signal: search=no, ai-train=no` w robots.txt math.SE i mathoverflow oraz formularz zrzutów („projects that do not include training a large language model”). I: platforma nie jest właścicielem praw do postów i nie może odwołać CC BY-SA. Kopia Common Pile pochodzi ze zrzutów wrzuconych przez społeczność w 12.2024 i z oficjalnych zrzutów z 07.2024; czy pierwotny pobierający zaakceptował nowe warunki: NIE SPRAWDZONE (ryzyko) |

## 1. Rezerwacja

| | |
|---|---|
| Co | issue [#357](https://github.com/slayerlabs/benchmarks-fabryka-ai/issues/357) (część 3; karta wskazuje #346) |
| Cel | pytania i odpowiedzi z serwisów SE o matematyce i logice |
| Wiersz w danych treningowych | nie zmierzono (krok 12) |

## 2. Karta źródła

[`KARTA_ZRODLA.md`](KARTA_ZRODLA.md), commit `1d3e564` (26.11 14:03), przed preregistracją. `common-pile/stackexchange@5ec3aa2e` w wersji
„raw” (wersja „filtered” maskuje liczby jako PII). Wybór 9 serwisów z 14 zmierzonych; luka licencyjna `'None'` w `all_licenses`;
nakładanie z FineMath-4+/InfiWebMath-4+ zmierzone po id pytania. Trenować: TAK; zgłosić: NIEROZSTRZYGNIĘTY.

## 3. Preregistracja

[`skrypty/preregistracja.json`](skrypty/preregistracja.json), commit `805bf5b` (26.11 14:21) przed pobraniem puli: seed 20261127,
9 serwisów, wybór wierszy przed pulą (`wybor_wierszy`: pytanie z `created` < 2022-12-01, bo odpowiedzi od grudnia 2022 mogą zawierać
tekst z ChatGPT; `all_licenses` bez `'None'`), reguły i aneksy InfiWebMath-4+ (24.11, 24.11b, 24.11c, 25.11b, 25.11c), nowy powód
`dedup_se_strony`, bez `dedup_fineweb_edu_109`, PII w trybie `usun`.

| aneks | commit | zapisany | treść |
|---|---|---|---|
| `aneks_2026_11_26_przeglad` | `3865ee2` (26.11 15:20) | po przeglądzie próbki, przed eksportem | wynik przeglądu, FAIL-e `ewal_13gram`, `pii`, `pii_at_bez_nawiasow`, `mojibake` przyjęte (podsekcja w kroku 8) |

## 4. Środowisko

| | |
|---|---|
| Komenda | venv `../matematyka-wspolne/robocze/venv` |
| Tokenizer | v6 sha256 `0640d3bd…815dd` |
| Sprawdzenie | porównanie `pip freeze` = `requirements.txt`: nie zmierzono |

## 5. Pobranie

| | |
|---|---|
| Komenda | `odtworz.sh pula stackexchange_mat` (commit `78a54d8`: serwisy i wybór wierszy z preregistracji), log `pula.log` 26.11 14:37 |
| Kod wyjścia | `KONIEC 1938345 1667484804`; kod bash nie zapisany w logu |
| Liczby | 23 pliki, **1 938 345 dok., 1 667 484 804 tokenów v6**; plik `math.stackexchange.com/documents/00005_se.jsonl.gz` (sha256 `59d1100b…`) bez wierszy po wyborze (pole `puste`) |
| Wynik | [`wyniki/probka_pliki.json`](wyniki/probka_pliki.json) (sha256 i wiersze każdego pliku) |

| serwis | pliki | dok. | tokeny v6 |
|---|---|---|---|
| math.stackexchange.com | 6 (+1 pusty) | 1 528 962 | 1 264 279 214 |
| stats.stackexchange.com | 2 | 194 855 | 172 863 100 |
| mathoverflow.net | 2 | 139 833 | 158 746 924 |
| cs.stackexchange.com | 2 | 45 097 | 36 789 139 |
| cstheory.stackexchange.com | 2 | 12 068 | 12 327 267 |
| scicomp.stackexchange.com | 2 | 10 500 | 11 552 078 |
| matheducators.stackexchange.com | 2 | 3 423 | 6 935 484 |
| or.stackexchange.com | 2 | 3 085 | 3 288 406 |
| proofassistants.stackexchange.com | 2 | 522 | 703 192 |

## 6. Indeksy i kontrole

- Testy, EN 1.07, walidacja Fabryki, `entech`, `en8x3b`, `wlasne:finemath4`, `wlasne:infiwebmath4`: te same indeksy co
  w częściach 2.
- `dedup_se_strony`: indeks [`../matematyka-wspolne/skrypty/se_strony.py`](../matematyka-wspolne/skrypty/se_strony.py) pytań SE obecnych
  jako strony w wybranych do eksportu FineMath-4+ części 2 i InfiWebMath-4+: **386 409 pytań**
  (`../matematyka-wspolne/robocze/wyniki/bazy/idx_se_strony_hu.npy`; commity `f2a18ec`, `3a9e1bb`).
- Kontrola dodatnia: wynik dla tego źródła nie zapisany (nie zmierzono).

## 7. Przebieg

| | |
|---|---|
| Wynik | 402/402 jednostek, `KONIEC 1040s` (`przebieg.log`, 26.11 15:02); kod wyjścia nie zapisany w logu |
| `ew13` | `dokumentow 1938345 z_trafieniem 17285 ngramow 25840`, `KONIEC` (15:03) |

## 8. Po przebiegu

`agreguj` 26.11 15:14 (`agreguj.log`; commit `7151944`), wynik [`wyniki/agreguj.json`](wyniki/agreguj.json):

| powód | odrzucone dok. | odrzucone tok. v6 | zostaje dok. | zostaje tok. v6 | % tok. | niezależnie dok. / % tok. |
|---|---|---|---|---|---|---|
| `walidacja_fabryki` | 72 | 69 725 | 1 938 273 | 1 667 415 079 | 99,996 | 72 / 0,004 |
| `domena_testow` | 0 | 0 | 1 938 273 | 1 667 415 079 | 99,996 | 0 / 0,0 |
| `ewal_13gram` | 5 783 | 7 783 924 | 1 932 490 | 1 659 631 155 | 99,529 | 5 783 / 0,467 |
| `pii` | 2 729 | 4 777 218 | 1 929 761 | 1 654 853 937 | 99,243 | 2 735 / 0,287 |
| `pii_zaciemniony` | 79 | 178 577 | 1 929 682 | 1 654 675 360 | 99,232 | 82 / 0,012 |
| `pii_at_bez_nawiasow` | 1 607 | 2 798 551 | 1 928 075 | 1 651 876 809 | 99,064 | 1 634 / 0,172 |
| `min_tresc` | 4 525 | 311 696 | 1 923 550 | 1 651 565 113 | 99,045 | 4 527 / 0,019 |
| `mojibake` | 6 | 8 842 | 1 923 544 | 1 651 556 271 | 99,045 | 6 / 0,001 |
| `dedup_wewnatrz` | 531 | 456 247 | 1 923 013 | 1 651 100 024 | 99,017 | 535 / 0,028 |
| `dedup_finemath4` | 170 589 | 197 320 547 | 1 752 424 | 1 453 779 477 | 87,184 | 170 755 / 11,857 |
| `dedup_infiwebmath4` | 13 966 | 14 500 140 | 1 738 458 | 1 439 279 337 | 86,314 | 14 106 / 0,879 |
| `dedup_se_strony` | 108 541 | 125 253 635 | 1 629 917 | 1 314 025 702 | 78,803 | 284 638 / 19,494 |
| `dedup_slayer107` | 14 947 | 16 731 779 | 1 614 970 | 1 297 293 923 | 77,799 | 15 090 / 1,017 |
| `dedup_slayer_8x3b_en` | 13 | 8 033 | 1 614 957 | 1 297 285 890 | 77,799 | 17 / 0,001 |
| `dedup_english_technical` | 0 | 0 | 1 614 957 | 1 297 285 890 | 77,799 | 0 / 0,0 |

- **Uzysk: 1 614 957 dok., 1 297 285 890 tokenów v6 (77,799%)**. Do eksportu: wszystkie zachowane. Dedup wobec FineMath-4+,
  InfiWebMath-4+ i stron SE zabiera w kaskadzie 20,9 pkt proc. tokenów (99,017% → 78,803%).
- `ewal_13gram` per test: MATH 4768, MMLU 710, MathQA 164, BoolQ 82, SQuAD2 32, HumanEval 31, MBPP 22, reszta ≤ 16.
- PII wg detektora DCLM: e-mail 1269, telefon 34, IP 1448 (tryb `usun`). `dedup_wewnatrz`: 93 identyczne, 442 przez MinHash.

### Przegląd próbki (26.11.2026)

Dwóch niezależnych recenzentów (A, B), pełne teksty; 5 wycinków powtórzonych po odmowie dostawcy modelu (aneks). Wynik
[`wyniki/przeglad_1.json`](wyniki/przeglad_1.json). Progi: fałszywe odrzucenia ≤ 10% ORAZ górna granica Wilsona ≤ 20%.

| powód | n | A: fałszywe (wątpliwe) | A: [Wilson 95%] | B: fałszywe (wątpliwe) | B: [Wilson 95%] | werdykt A/B |
|---|---|---|---|---|---|---|
| `walidacja_fabryki` | 72 | 0 (1) | [0; 5,1] | 0 (1) | [0; 5,1] | PASS/PASS |
| `ewal_13gram` | 100 | 95 (0) | [88,8; 97,8] | 85 (9) | [76,7; 90,7] | FAIL/FAIL |
| `pii` | 100 | 45 (30) | [35,6; 54,8] | 44 (32) | [34,7; 53,8] | FAIL/FAIL |
| `pii_zaciemniony` | 82 | 2 (43) | [0,7; 8,5] | 2 (43) | [0,7; 8,5] | PASS/PASS |
| `pii_at_bez_nawiasow` | 100 | 66 (31) | [56,3; 74,5] | 67 (31) | [57,3; 75,4] | FAIL/FAIL |
| `min_tresc` | 100 | 0 (0) | [0; 3,7] | 0 (0) | [0; 3,7] | PASS/PASS |
| `mojibake` | 6 | 0 (3) | [0; 39,0] | 0 (3) | [0; 39,0] | FAIL/FAIL |
| `dedup_wewnatrz` | 100 | 0 (1) | [0; 3,7] | 0 (1) | [0; 3,7] | PASS/PASS |
| `dedup_finemath4` | 99 | 0 (0) | [0; 3,7] | 0 (0) | [0; 3,7] | PASS/PASS |
| `dedup_infiwebmath4` | 100 | 0 (0) | [0; 3,7] | 0 (0) | [0; 3,7] | PASS/PASS |
| `dedup_se_strony` | 100 | 0 (0) | [0; 3,7] | 0 (0) | [0; 3,7] | PASS/PASS |
| `dedup_slayer107` | 100 | 0 (0) | [0; 3,7] | 0 (0) | [0; 3,7] | PASS/PASS |
| `dedup_slayer_8x3b_en` | 17 | 0 (0) | [0; 18,4] | 0 (0) | [0; 18,4] | PASS/PASS |

| zachowane (300) | A | B | próg | werdykt |
|---|---|---|---|---|
| śmieci | 0: 0,0% [0; 1,3], wątpliwe 1 | 0: 0,0% [0; 1,3], wątpliwe 2 | ≤ 10% | PASS |
| przeoczone PII | 0/300 | 0/300 | 0/300 | PASS |
| przeoczony test | 0/300 | 0/300 | — | PASS |

**Werdykt pliku: NIE PRZESZŁO** (u obu: `ewal_13gram`, `mojibake`, `pii`, `pii_at_bez_nawiasow`). Liczba pozycji w pliku: 1076
odrzuconych + 300 zachowanych = 1376; aneks podaje 1377 — różnica 1 pozycji niewyjaśniona w plikach.

### Aneks 26.11 przegląd (commit `3865ee2`)

FAIL-e przyjęte przed eksportem (reguły usuwają dobre teksty, nie przepuszczają złych; jak aneks 24.11b):
- `ewal_13gram` 95% / 85% fałszywych (macierz jednostkowa, tan(a+b), Fibonacci); 5–6 dosłownych zadań MATH/MathQA trafionych;
  koszt 0,47% tokenów.
- `pii` 45% / 44% fałszywych (numery sekcji twierdzeń jako IPv4); koszt 0,29%; prywatność ma pierwszeństwo.
- `pii_at_bez_nawiasow` 66% / 67% fałszywych („at stats.stackexchange.com”); koszt 0,17%; aneks 25.11c.
- `mojibake` 0/6 fałszywych, 3 wątpliwe poza widocznym tekstem; FAIL tylko z górnej granicy Wilsona przy n = 6.

## 9. Eksport

| | |
|---|---|
| Podział | [`wyniki/czesci.json`](wyniki/czesci.json): 1 część, `stackexchange_math_p01`, 1 614 957 dok., 1 297 285 890 tokenów v6 |
| Key | `stackexchange_math`; datasheet [`eksport/stackexchange_math.md`](eksport/stackexchange_math.md) (status `held_for_review`); wpis w `../matematyka-wspolne/eksport/src/sources.py`; skrypt `../matematyka-wspolne/eksport/src/clean_stackexchange_math.py` (commit `18c385d`): `id` = `<serwis>/<id pytania>`, `license` = wersja CC BY-SA pytania (SPDX), `author` = nazwy wyświetlane autorów postów (bez linków profili), Presidio wyłączone (`no_masking()`) |
| Eksport, liczby, `dropped`, sha256 | **w toku** |

## 10. Kontrola końcowa

| | |
|---|---|
| Test kontraktowy, `check.py` | **w toku** |
| Niezależny agent na pliku o tym samym sha256 | nie zmierzono |

## 11. Wysyłka

**W toku.** Przed zgłoszeniem do repo zespołu: przegląd praw (opt-out platformy).

## 12. Dane treningowe

Czeka na wysyłkę: nie zmierzono.

## Historia odtworzeń

- 26.11.2026 14:03: karta (`1d3e564`); 14:21 preregistracja przed pobraniem (`805bf5b`).
- 26.11.2026 14:21–14:37: źródło w `normalizuj`/`odtworz` (`78a54d8`), powód `dedup_se_strony` (`f2a18ec`, `3a9e1bb`); `pula`: 1 938 345 dok., 1 667 484 804 tok. v6.
- 26.11.2026 15:02–15:03: `przebieg` 402/402 (`KONIEC 1040s`), `ew13`.
- 26.11.2026 15:14: `agreguj`: 1 614 957 / 1 297 285 890 (77,799%); commit `7151944` (15:15).
- 26.11.2026 15:16: nakładka eksportu `clean_stackexchange_math.py`, rejestr, test kontraktowy (`18c385d`).
- 26.11.2026 15:20: przegląd próbki i `aneks_2026_11_26_przeglad` przed eksportem (`3865ee2`).
- Eksport i `check.py`: w toku.

## Pułapki tego przebiegu

- Url stron SE w FineMath-4+/InfiWebMath-4+ ma slug tytułu (`/questions/<id>/<slug>`), a dokument zrzutu nie: dedup po
  identycznym url ich nie łączy, potrzebny osobny indeks po (serwis, id pytania) — `dedup_se_strony` niezależnie dotyka 19,5% tokenów.
- Wersja „filtered” Common Pile maskuje PII placeholderami, które trafiają w liczby w matematyce: bierzemy „raw” i własne reguły.
- Data dokumentu to data pytania: odcięcie przed 2022-12-01 nie wyklucza nowszych odpowiedzi z tekstem z modeli (ryzyko zapisane).
- Wybór wierszy po dacie i licencji może opróżnić cały plik: math.SE `00005` nie ma wierszy po wyborze (pole `puste`). Przyczyna
  (data pytania czy brak licencji) nie zmierzona; [I] karta wiąże pliki 00001–00005 z kolejnymi latami do 2024.
