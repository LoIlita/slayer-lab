# Dziennik zbioru: Wikipedia EN i Wikibooks — artykuły matematyczne dla Slayera 1B, część 3

Przepis: [`METODOLOGIA.md` w repo zespołu](https://github.com/slayerlabs/benchmarks-fabryka-ai/blob/main/research/slayer-1b/dane/METODOLOGIA.md).
Karta źródła: [`KARTA_ZRODLA.md`](KARTA_ZRODLA.md). Reguły: [`skrypty/preregistracja.json`](skrypty/preregistracja.json).
Budowa puli: [`skrypty/buduj_pule.py`](skrypty/buduj_pule.py) (reguły wyboru: `wiki_rules.py`, `wsp.py`); detektory i agregacja:
[`../matematyka-wspolne/skrypty/`](../matematyka-wspolne/skrypty/). Logi: `robocze/logi/` (poza gitem). Dzienniki bliźniacze:
[InfiWebMath-4+](../infiwebmath4/DZIENNIK.md) (reguły przejęte), [podręczniki](../podreczniki_mat/DZIENNIK.md), [OEIS](../oeis/DZIENNIK.md).

## Bramki praw

| bramka | wynik |
|---|---|
| Można TRENOWAĆ (także komercyjnie) | TAK: CC BY-SA 4.0 per dokument; takedown po `id`/tytule |
| Można ZGŁOSIĆ do `dataset-team-submissions` | TAK (licencja per dokument, bez NC/ND; SA i atrybucja w eksporcie) → `admitted` |
| Użycie komercyjne | dozwolone: CC BY-SA 4.0 pozwala na użycie komercyjne; SA dotyczy dalszego udostępniania samych danych |

## 1. Rezerwacja

| | |
|---|---|
| Co | issue [#357](https://github.com/slayerlabs/benchmarks-fabryka-ai/issues/357) (część 3); karta pod #346 |
| Cel | encyklopedyczne definicje, twierdzenia i dowody z matematyki i logiki (D1, D2 w [`../matematyka-wspolne/kandydaci_czyste.md`](../matematyka-wspolne/kandydaci_czyste.md)) |
| Wiersz w danych treningowych | nie zmierzono (krok 12) |

## 2. Karta źródła

[`KARTA_ZRODLA.md`](KARTA_ZRODLA.md), commit `8dad0b6` (26.11 15:25), przed pobraniem do budowy. `common-pile/wikimedia@781b263a`,
189 plików (sha256 w [`wyniki/przeglad_zrodla.json`](wyniki/przeglad_zrodla.json)). Reguła 1 wyboru (gęstość wzorów + słownik
dziedziny w leadzie): precyzja 52/60 = 86,7% (Wilson 95% 76–93%, [`wyniki/ocena_precyzji.json`](wyniki/ocena_precyzji.json)), recall 16/20 haseł
kontrolnych; szacunek 8 521 + 1 469 dok., ~30,9 mln tok. v6. Trenować: TAK; zgłosić: TAK.

## 3. Preregistracja

[`skrypty/preregistracja.json`](skrypty/preregistracja.json): seed 20261126, reguła 1 z karty, normalizacja (`html.unescape`, wycięcie
`{{Infobox …}}`), filtr budowy (licencja, dedup dokładny md5), reguły i aneksy InfiWebMath-4+ (24.11, 24.11b, 24.11c, 25.11b, 25.11c,
25.11e). Odstępstwa: `domena_testow` bez reguły „projekty Wikimedia” (usunęłaby 100%), dodane `dedup_infiwebmath4` i
`dedup_fineweb_edu_109`, filtr budowy przed detektorami. Preregistracja jest w gicie dopiero w commicie budowy `8e954ff`
(26.11 16:21); kolejność „przed budową” potwierdza tylko pole `zapisano`.

| aneks / zapis | zapisany | treść |
|---|---|---|
| `domena_testow_wylaczone` | 26.11, przez integratora przed przebiegiem (commit `8e954ff`) | zapis maszynowy reguły z pola `domena_testow`: wikipedia.org, wikinews.org, wikivoyage.org, wikibooks.org wyłączone; treść reguły bez zmian; przeciek testów z Wikipedii (WikiText-2, BoolQ) łapie `ewal_13gram` |
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
| Liczby | **9 990 dok., 30 824 027 tokenów v6**: Wikipedia 8 521 / 26 769 474, Wikibooks 1 469 / 4 054 553 (zgodne z kartą: 8 521 i 1 469); filtr budowy odrzucił 0; licencja CC-BY-SA-4.0 w 9 990 / 9 990 |
| Wynik | [`wyniki/budowa.json`](wyniki/budowa.json) (sha256 189 plików), [`wyniki/probka_pliki.json`](wyniki/probka_pliki.json) |

## 6. Indeksy i kontrole

- Testy, EN 1.07, walidacja Fabryki, `entech`, `en8x3b`, `fwe109`, `wlasne:finemath4`, `wlasne:infiwebmath4`: te same indeksy co
  w częściach 2.
- Kontrola dodatnia: wynik dla tego źródła nie zapisany (nie zmierzono).

## 7. Przebieg

| | |
|---|---|
| Wynik | 2/2 jednostek, `KONIEC 88s` (`przebieg.log`, 26.11 16:22); kod wyjścia nie zapisany w logu |
| `ew13` | `dokumentow 9990 z_trafieniem 369 ngramow 4401`, `KONIEC` (16:22) |

## 8. Po przebiegu

`agreguj` 26.11 16:26 (`agreguj.log`; commit `1caa30c`, 16:31), wynik [`wyniki/agreguj.json`](wyniki/agreguj.json):

| powód | odrzucone dok. | odrzucone tok. v6 | zostaje dok. | zostaje tok. v6 | % tok. | niezależnie dok. / % tok. |
|---|---|---|---|---|---|---|
| `walidacja_fabryki` | 1 | 536 | 9 989 | 30 823 491 | 99,998 | 1 / 0,002 |
| `domena_testow` | 0 | 0 | 9 989 | 30 823 491 | 99,998 | 0 / 0,0 |
| `ewal_13gram` | 200 | 999 883 | 9 789 | 29 823 608 | 96,754 | 200 / 3,244 |
| `pii` | 8 | 59 837 | 9 781 | 29 763 771 | 96,56 | 9 / 0,207 |
| `pii_zaciemniony` | 0 | 0 | 9 781 | 29 763 771 | 96,56 | 0 / 0,0 |
| `pii_at_bez_nawiasow` | 3 | 6 305 | 9 778 | 29 757 466 | 96,54 | 3 / 0,02 |
| `min_tresc` | 0 | 0 | 9 778 | 29 757 466 | 96,54 | 0 / 0,0 |
| `mojibake` | 0 | 0 | 9 778 | 29 757 466 | 96,54 | 0 / 0,0 |
| `dedup_wewnatrz` | 86 | 100 815 | 9 692 | 29 656 651 | 96,213 | 87 / 0,332 |
| `dedup_finemath4` | 72 | 218 577 | 9 620 | 29 438 074 | 95,504 | 76 / 0,746 |
| `dedup_infiwebmath4` | 230 | 628 899 | 9 390 | 28 809 175 | 93,463 | 237 / 2,112 |
| `dedup_slayer107` | 361 | 1 385 742 | 9 029 | 27 423 433 | 88,968 | 368 / 4,569 |
| `dedup_slayer_8x3b_en` | 1 | 2 615 | 9 028 | 27 420 818 | 88,959 | 1 / 0,008 |
| `dedup_english_technical` | 0 | 0 | 9 028 | 27 420 818 | 88,959 | 0 / 0,0 |
| `dedup_fineweb_edu_109` | 2 266 | 7 686 325 | 6 762 | 19 734 493 | 64,023 | 2 622 / 29,296 |

- **Uzysk: 6 762 dok., 19 734 493 tokenów v6 (64,023%)**. Do eksportu: wszystkie zachowane. `dedup_fineweb_edu_109` zabiera
  w kaskadzie 24,9 pkt proc. (strona artykułu już w FineWeb-Edu 1.09).
- `ewal_13gram` per test: MATH 114, BoolQ 46, MMLU 24, PAWS 8, SQuAD2 7, HumanEval 4, MedMCQA 3, Belebele 1, ANLI 1.
- PII wg detektora DCLM: e-mail 0, telefon 0, IP 9 (tryb `usun`). `dedup_wewnatrz`: 1 identyczny, 86 przez MinHash.

### Przegląd próbki (26.11.2026)

Dwóch niezależnych recenzentów (A, B), pełne teksty zachowanych; wycinki z niepełną lekturą doczytane (aneks). Wynik
[`wyniki/przeglad_1.json`](wyniki/przeglad_1.json). Progi: fałszywe odrzucenia ≤ 10% ORAZ górna granica Wilsona ≤ 20%.

| powód | n | A: fałszywe (wątpliwe) | A: [Wilson 95%] | B: fałszywe (wątpliwe) | B: [Wilson 95%] | werdykt A/B |
|---|---|---|---|---|---|---|
| `walidacja_fabryki` | 1 | 0 (0) | [0; 79,3] | 0 (0) | [0; 79,3] | FAIL/FAIL |
| `ewal_13gram` | 93 | 66 (2) | [61,1; 79,2] | 63 (2) | [57,7; 76,4] | FAIL/FAIL |
| `pii` | 9 | 0 (9) | [0; 29,9] | 0 (9) | [0; 29,9] | FAIL/FAIL |
| `pii_at_bez_nawiasow` | 3 | 0 (3) | [0; 56,2] | 0 (3) | [0; 56,2] | FAIL/FAIL |
| `dedup_wewnatrz` | 87 | 0 (0) | [0; 4,2] | 0 (0) | [0; 4,2] | PASS/PASS |
| `dedup_finemath4` | 75 | 0 (0) | [0; 4,9] | 0 (0) | [0; 4,9] | PASS/PASS |
| `dedup_infiwebmath4` | 98 | 0 (0) | [0; 3,8] | 0 (0) | [0; 3,8] | PASS/PASS |
| `dedup_slayer107` | 97 | 0 (0) | [0; 3,8] | 0 (0) | [0; 3,8] | PASS/PASS |
| `dedup_slayer_8x3b_en` | 1 | 0 (0) | [0; 79,3] | 0 (0) | [0; 79,3] | FAIL/FAIL |
| `dedup_fineweb_edu_109` | 100 | 0 (0) | [0; 3,7] | 0 (0) | [0; 3,7] | PASS/PASS |

| zachowane (300) | A | B | próg | werdykt |
|---|---|---|---|---|
| śmieci | 1: 0,3% [0,1; 1,9], wątpliwe 13 | 1: 0,3% [0,1; 1,9], wątpliwe 13 | ≤ 10% | PASS |
| przeoczone PII | 0/300 | 0/300 | 0/300 | PASS |
| przeoczony test | 0/300 | 0/300 | — | PASS |

**Werdykt pliku: NIE PRZESZŁO** (u obu: `dedup_slayer_8x3b_en`, `ewal_13gram`, `pii`, `pii_at_bez_nawiasow`, `walidacja_fabryki`).

### Aneks 26.11 przegląd (commit `df8f74a`)

FAIL-e przyjęte przed eksportem:
- `ewal_13gram`: fałszywe 66–68% (macierze, wzory); trafne 28–31% to pasaże testów czytania z Wikipedii (BoolQ, PAWS, ANLI, SQuAD2,
  Belebele) — reguła działa tu zgodnie z celem; koszt 3,24% tokenów.
- `pii`: 0/9 fałszywych w ocenie (9 poza widocznym tekstem; pełny tekst: 2 prawdziwe, reszta numery); FAIL tylko z małej próby;
  koszt 0,19%.
- `pii_at_bez_nawiasow`: 0/3, wszystkie poza widocznym tekstem; koszt 0,02%.
- `walidacja_fabryki`, `dedup_slayer_8x3b_en`: 0/1 — FAIL tylko z górnej granicy Wilsona przy n = 1.

## 9. Eksport

| | |
|---|---|
| Podział | [`wyniki/czesci.json`](wyniki/czesci.json): 1 część, `wikipedia_math_en_p01`, 6 762 dok., 19 734 493 tokenów v6 |
| Key | `wikipedia_math_en`; datasheet [`eksport/wikipedia_math_en.md`](eksport/wikipedia_math_en.md); wpis w `../matematyka-wspolne/eksport/src/sources.py` (licencja `CC-BY-SA-4.0`); skrypt `../matematyka-wspolne/eksport/src/clean_wikipedia_math_en.py` (commit `47e715e`): `author` = loginy edytorów, Presidio wyłączone (`no_masking()`) |
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
- 26.11.2026 16:21: preregistracja z `domena_testow_wylaczone` i pula 9 990 dok., 30 824 027 tok. v6 (`8e954ff`).
- 26.11.2026 16:22: `przebieg` 2/2 (`KONIEC 88s`), `ew13`; 16:26 `agreguj`: 6 762 / 19 734 493 (64,023%); commit `1caa30c` (16:31).
- 26.11.2026 16:38: przegląd próbki i `aneks_2026_11_26_przeglad` przed eksportem (`df8f74a`).
- 26.11.2026 19:50: nakładka eksportu `clean_wikipedia_math_en.py`, rejestr, test kontraktowy (`47e715e`).
- Eksport i `check.py`: w toku.

## Pułapki tego przebiegu

- Reguła `domena_testow` z DCLM-EN („projekty Wikimedia”) usunęłaby całe źródło: wyłączenie zapisane maszynowo przed przebiegiem.
- Url źródła (`wikipedia.com`) trzeba zamienić na kanoniczny `en.wikipedia.org`, inaczej dedup po url wobec FineMath-4+,
  InfiWebMath-4+ i FineWeb-Edu nie łączy tych samych stron; po zamianie `dedup_fineweb_edu_109` zabiera 24,9 pkt proc.
- Wybór po gęstości wzorów gubi artykuły z logiki i geometrii syntetycznej (mało LaTeX-a): recall 16/20 na hasłach kontrolnych.
