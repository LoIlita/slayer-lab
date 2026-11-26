# Dziennik zbioru: otwarte podręczniki matematyki i statystyki (LibreTexts, PressBooks) dla Slayera 1B, część 3

Przepis: [`METODOLOGIA.md` w repo zespołu](https://github.com/slayerlabs/benchmarks-fabryka-ai/blob/main/research/slayer-1b/dane/METODOLOGIA.md).
Karta źródła: [`KARTA_ZRODLA.md`](KARTA_ZRODLA.md). Reguły: [`skrypty/preregistracja.json`](skrypty/preregistracja.json).
Budowa puli: [`skrypty/buduj_pule.py`](skrypty/buduj_pule.py) (reguły wyboru: `podr_pass.py`, `podr_rules.py`); detektory i agregacja:
[`../matematyka-wspolne/skrypty/`](../matematyka-wspolne/skrypty/). Logi: `robocze/logi/` (poza gitem). Dzienniki bliźniacze:
[InfiWebMath-4+](../infiwebmath4/DZIENNIK.md) (reguły przejęte), [Wikipedia](../wiki_mat/DZIENNIK.md), [OEIS](../oeis/DZIENNIK.md).

## Bramki praw

| bramka | wynik |
|---|---|
| Można TRENOWAĆ (także komercyjnie) | TAK: licencja per wiersz (CC BY 3.0/4.0, CC BY-SA 3.0/4.0, GFDL 1.3, domena publiczna); takedown po `id`/url |
| Można ZGŁOSIĆ do `dataset-team-submissions` | TAK (licencja per dokument, bez NC/ND; atrybucja, SA i GFDL w eksporcie) → `admitted` |
| Użycie komercyjne | dozwolone dla wszystkich licencji per wiersz; SA i GFDL dotyczą dalszego udostępniania samych danych |
| OpenStax | wykluczone decyzją konserwatywną (preregistracja): wydawca zmienił licencję nowych wersji na CC BY-NC-SA (22.04.2026), wskazując AI jako powód; kopie z 03.2025 są na CC BY 4.0 (I: prawnie dozwolone, ryzyko reputacyjne) |

## 1. Rezerwacja

| | |
|---|---|
| Co | issue [#357](https://github.com/slayerlabs/benchmarks-fabryka-ai/issues/357) (część 3); karta pod #346 |
| Cel | podręcznikowa matematyka szkolna i akademicka (C1 LibreTexts, C2 PressBooks w [`../matematyka-wspolne/kandydaci_czyste.md`](../matematyka-wspolne/kandydaci_czyste.md)) |
| Wiersz w danych treningowych | nie zmierzono (krok 12) |

## 2. Karta źródła

[`KARTA_ZRODLA.md`](KARTA_ZRODLA.md), commit `8dad0b6` (26.11 15:25), przed pobraniem do budowy. `common-pile/libretexts@d4ce4b1e`,
`common-pile/pressbooks@29fa162f` (sha256 plików w karcie §1); OERCommons (C3) odrzucone (precyzja 11/20 i 8/20). Precyzja wyboru: C1
20/20, C2 20/20. Analiza OpenStax (regulamin bez zapisu o AI; zmiana licencji 22.04.2026). Trenować: TAK; zgłosić: TAK.

## 3. Preregistracja

[`skrypty/preregistracja.json`](skrypty/preregistracja.json): seed 20261126, wybór C1/C2 z karty, normalizacja, filtr budowy (licencja,
dedup dokładny, próg 600 tok. v6, `openstax` z `decyzja_openstax`), reguły i aneksy InfiWebMath-4+ (24.11, 24.11b, 24.11c, 25.11b,
25.11c, 25.11e). Odstępstwa: filtr budowy przed detektorami, dodane `dedup_infiwebmath4` i `dedup_fineweb_edu_109`. Preregistracja
jest w gicie dopiero w commicie budowy `8e954ff` (26.11 16:21); kolejność „przed budową” potwierdza tylko pole `zapisano`.

| aneks | zapisany | treść |
|---|---|---|
| `aneks_2026_11_26_openstax_okno` | po pierwszym przebiegu budowy (liczby filtra widziane, treści puli nie oglądane), przed eksportem; commit `8e954ff` | reguła `openstax` sprawdzana też na id i oknach 3000 znaków tekstu PO normalizacji (normalizacja przesuwa granicę okna); tylko zaostrza wykluczenie |
| `aneks_2026_11_26_przeglad` | po przeglądzie, przed eksportem; commit `df8f74a` (16:38) | wynik przeglądu, FAIL-e przyjęte (podsekcja w kroku 8) |

## 4. Środowisko

| | |
|---|---|
| Komenda | venv `../matematyka-wspolne/robocze/venv` |
| Tokenizer | v6 sha256 `0640d3bd…815dd` |
| Sprawdzenie | porównanie `pip freeze` = `requirements.txt`: nie zmierzono |

## 5. Pobranie i budowa puli

| | |
|---|---|
| Budowa | `buduj_pule.py` (commit `8e954ff`, 26.11 16:21); log budowy: nie zapisany w `robocze/logi/` |
| Wybrane przed filtrem | C1 9 733 dok. / 31 638 141 tok. v6; C2 2 415 / 14 373 361 (zgodne z kartą §4 dla dokumentów; tokeny C2 inne niż w karcie: 16,06 mln, przyczyna nie zmierzona) |
| Filtr budowy | dedup dokładny C1 515 / 1 654 348, C2 1 293 / 8 937 721; krótkie (< 600 tok.) C1 2 053 / 552 348, C2 34 / 14 703; OpenStax C1 1 228 / 6 571 450, C2 206 / 1 858 392 (wśród wybranych przed filtrem OpenStax: C1 1 640 / 6 759 374, C2 559 / 5 482 649) |
| Pula | **6 819 dok., 26 422 540 tokenów v6**: C1 5 937 / 22 859 995, C2 882 / 3 562 545 |
| Licencje (wiersze / tokeny) | CC-BY-4.0 4 240 / 17 950 232; CC-BY-SA-4.0 1 611 / 5 496 494; GFDL-1.3-or-later 384 / 1 003 229; CC-BY-3.0 288 / 1 185 921; CC-BY-SA-3.0 152 / 321 838; LicenseRef-PD 144 / 464 826 |
| Wynik | [`wyniki/budowa.json`](wyniki/budowa.json), [`wyniki/probka_pliki.json`](wyniki/probka_pliki.json) |

## 6. Indeksy i kontrole

- Testy, EN 1.07, walidacja Fabryki, `entech`, `en8x3b`, `fwe109`, `wlasne:finemath4`, `wlasne:infiwebmath4`: te same indeksy co
  w częściach 2.
- Kontrola dodatnia: wynik dla tego źródła nie zapisany (nie zmierzono).

## 7. Przebieg

| | |
|---|---|
| Wynik | 2/2 jednostek, `KONIEC 154s` (`przebieg.log`, 26.11 16:28); kod wyjścia nie zapisany w logu |
| `ew13` | `dokumentow 6819 z_trafieniem 304 ngramow 752`, `KONIEC` (16:28) |

## 8. Po przebiegu

`agreguj` 26.11 16:31 (`agreguj.log`; commit `1caa30c`), wynik [`wyniki/agreguj.json`](wyniki/agreguj.json):

| powód | odrzucone dok. | odrzucone tok. v6 | zostaje dok. | zostaje tok. v6 | % tok. | niezależnie dok. / % tok. |
|---|---|---|---|---|---|---|
| `walidacja_fabryki` | 0 | 0 | 6 819 | 26 422 540 | 100,0 | 0 / 0,0 |
| `domena_testow` | 0 | 0 | 6 819 | 26 422 540 | 100,0 | 0 / 0,0 |
| `ewal_13gram` | 140 | 842 158 | 6 679 | 25 580 382 | 96,813 | 140 / 3,187 |
| `pii` | 33 | 211 628 | 6 646 | 25 368 754 | 96,012 | 35 / 0,864 |
| `pii_zaciemniony` | 0 | 0 | 6 646 | 25 368 754 | 96,012 | 0 / 0,0 |
| `pii_at_bez_nawiasow` | 119 | 701 044 | 6 527 | 24 667 710 | 93,359 | 126 / 2,879 |
| `min_tresc` | 0 | 0 | 6 527 | 24 667 710 | 93,359 | 0 / 0,0 |
| `mojibake` | 2 | 6 220 | 6 525 | 24 661 490 | 93,335 | 2 / 0,024 |
| `dedup_wewnatrz` | 1 597 | 6 742 284 | 4 928 | 17 919 206 | 67,818 | 1 728 / 28,527 |
| `dedup_finemath4` | 1 544 | 6 875 442 | 3 384 | 11 043 764 | 41,797 | 2 103 / 37,119 |
| `dedup_infiwebmath4` | 100 | 313 897 | 3 284 | 10 729 867 | 40,609 | 181 / 2,191 |
| `dedup_slayer107` | 240 | 773 959 | 3 044 | 9 955 908 | 37,68 | 387 / 5,083 |
| `dedup_slayer_8x3b_en` | 4 | 5 882 | 3 040 | 9 950 026 | 37,657 | 7 / 0,034 |
| `dedup_english_technical` | 0 | 0 | 3 040 | 9 950 026 | 37,657 | 0 / 0,0 |
| `dedup_fineweb_edu_109` | 51 | 70 776 | 2 989 | 9 879 250 | 37,389 | 124 / 0,794 |

- **Uzysk: 2 989 dok., 9 879 250 tokenów v6 (37,389%)**. Do eksportu: wszystkie zachowane. Największe ubytki w kaskadzie:
  `dedup_wewnatrz` 25,5 pkt proc. (bliskie kopie C1↔C2 i wersji książek; 3 identyczne, 1 725 przez MinHash) i `dedup_finemath4`
  26,0 pkt proc.
- `ewal_13gram` per test: MATH 120, MMLU 11, MedMCQA 2, MathQA 2, HumanEval 2, MBPP 1, TriviaQA 1, GSM-Plus 1.
- PII wg detektora DCLM: e-mail 5, telefon 3, IP 27 (tryb `usun`).

### Przegląd próbki (26.11.2026)

Dwóch niezależnych recenzentów (A, B), pełne teksty zachowanych; wycinki z niepełną lekturą doczytane (aneks). Wynik
[`wyniki/przeglad_1.json`](wyniki/przeglad_1.json). Progi: fałszywe odrzucenia ≤ 10% ORAZ górna granica Wilsona ≤ 20%.

| powód | n | A: fałszywe (wątpliwe) | A: [Wilson 95%] | B: fałszywe (wątpliwe) | B: [Wilson 95%] | werdykt A/B |
|---|---|---|---|---|---|---|
| `ewal_13gram` | 91 | 80 (11) | [79,6; 93,1] | 84 (7) | [85,0; 96,2] | FAIL/FAIL |
| `pii` | 32 | 7 (25) | [11,0; 38,8] | 7 (25) | [11,0; 38,8] | FAIL/FAIL |
| `pii_at_bez_nawiasow` | 88 | 6 (82) | [3,2; 14,1] | 11 (77) | [7,1; 21,0] | PASS/FAIL |
| `mojibake` | 2 | 0 (2) | [0; 65,8] | 0 (2) | [0; 65,8] | FAIL/FAIL |
| `dedup_wewnatrz` | 94 | 0 (0) | [0; 3,9] | 0 (0) | [0; 3,9] | PASS/PASS |
| `dedup_finemath4` | 100 | 0 (0) | [0; 3,7] | 0 (0) | [0; 3,7] | PASS/PASS |
| `dedup_infiwebmath4` | 98 | 0 (0) | [0; 3,8] | 0 (0) | [0; 3,8] | PASS/PASS |
| `dedup_slayer107` | 96 | 0 (0) | [0; 3,8] | 0 (0) | [0; 3,8] | PASS/PASS |
| `dedup_slayer_8x3b_en` | 6 | 0 (0) | [0; 39,0] | 0 (0) | [0; 39,0] | FAIL/FAIL |
| `dedup_fineweb_edu_109` | 100 | 0 (0) | [0; 3,7] | 0 (0) | [0; 3,7] | PASS/PASS |

| zachowane (300) | A | B | próg | werdykt |
|---|---|---|---|---|
| śmieci | 7: 2,3% [1,1; 4,7], wątpliwe 17 | 6: 2,0% [0,9; 4,3], wątpliwe 19 | ≤ 10% | PASS |
| przeoczone PII | 0/300 | 0/300 | 0/300 | PASS |
| przeoczony test | 0/300 | 0/300 | — | PASS |

**Werdykt pliku: NIE PRZESZŁO** (u obu: `dedup_slayer_8x3b_en`, `ewal_13gram`, `mojibake`, `pii`; u B także `pii_at_bez_nawiasow`).

### Aneks 26.11 przegląd (commit `df8f74a`)

FAIL-e przyjęte przed eksportem (reguły usuwają dobre teksty, nie przepuszczają złych):
- `ewal_13gram` 88–92% fałszywych (wzory, definicje); koszt 3,19%.
- `pii` 7/32 fałszywych (numery ćwiczeń jako IP), reszta poza widocznym tekstem; koszt 0,80%.
- `pii_at_bez_nawiasow` (B) 11/88 fałszywych w widocznym tekście, reszta poza nim (pełny tekst: frazy „available at …”); koszt 2,65%;
  jak aneks 25.11c.
- `mojibake` 0/2, `dedup_slayer_8x3b_en` 0/6 — FAIL tylko z małej próby.
- Śmieci w zachowanych 7/300 i 6/300: sama nawigacja LibreTexts, rozdziały bez matematyki.

## 9. Eksport

| | |
|---|---|
| Podział | [`wyniki/czesci.json`](wyniki/czesci.json): 1 część, `open_textbooks_math_en_p01`, 2 989 dok., 9 879 250 tokenów v6 |
| Key | `open_textbooks_math_en`; datasheet [`eksport/open_textbooks_math_en.md`](eksport/open_textbooks_math_en.md); wpis w `../matematyka-wspolne/eksport/src/sources.py` (`license_spdx` `LicenseRef-per-row`); skrypt `../matematyka-wspolne/eksport/src/clean_open_textbooks_math_en.py` (commit `47e715e`): licencja per wiersz, Presidio wyłączone (`no_masking()`) |
| Eksport, liczby, `dropped`, sha256 | **w toku** |

## 10. Kontrola końcowa

| | |
|---|---|
| Test kontraktowy, `check.py` | **w toku** |
| Niezależny agent na pliku o tym samym sha256 | nie zmierzono |

## 11. Wysyłka

**W toku.**

## 12. Dane treningowe

Czeka na wysyłkę: nie zmierzono.

## Historia odtworzeń

- 26.11.2026 15:25: karta (`8dad0b6`).
- 26.11.2026 16:21: preregistracja z aneksem `openstax_okno` i pula 6 819 dok., 26 422 540 tok. v6 (`8e954ff`).
- 26.11.2026 16:28: `przebieg` 2/2 (`KONIEC 154s`), `ew13`; 16:31 `agreguj`: 2 989 / 9 879 250 (37,389%), commit `1caa30c`.
- 26.11.2026 16:38: przegląd próbki i `aneks_2026_11_26_przeglad` przed eksportem (`df8f74a`).
- 26.11.2026 19:50: nakładka eksportu `clean_open_textbooks_math_en.py`, rejestr, test kontraktowy (`47e715e`).
- Eksport i `check.py`: w toku.

## Pułapki tego przebiegu

- PressBooks ma ten sam rozdział pod kilkoma `id` z różnym `#chapter-…-section-N`: dedup dokładny usunął 1 293 kopie C2 (62% tokenów C2).
- Normalizacja tekstu przesuwa granicę okna 3000 znaków: wykrywanie OpenStax trzeba robić na tekście surowym i po normalizacji (aneks).
- Podręczniki te same w LibreTexts, PressBooks i na stronach w FineMath-4+: po dedupach zostaje 37% puli.
