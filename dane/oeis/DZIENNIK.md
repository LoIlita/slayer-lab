# Dziennik zbioru: OEIS (EN) dla Slayera 1B, część 3

Przepis: [`METODOLOGIA.md` w repo zespołu](https://github.com/slayerlabs/benchmarks-fabryka-ai/blob/main/research/slayer-1b/dane/METODOLOGIA.md).
Karta źródła: [`KARTA_ZRODLA.md`](KARTA_ZRODLA.md). Reguły: [`skrypty/preregistracja.json`](skrypty/preregistracja.json).
Budowa puli: [`skrypty/buduj_pule.py`](skrypty/buduj_pule.py); detektory i agregacja: [`../matematyka-wspolne/skrypty/`](../matematyka-wspolne/skrypty/).
Logi: `robocze/logi/` (poza gitem). Dzienniki bliźniacze: [InfiWebMath-4+](../infiwebmath4/DZIENNIK.md) (reguły przejęte),
[FineMath-4+](../finemath4/DZIENNIK.md), [formalna](../formalna/DZIENNIK.md).

## Bramki praw

| bramka | wynik |
|---|---|
| Można TRENOWAĆ | TAK (CC BY-SA 4.0 per wiersz, wydana przez OEIS Foundation; takedown po A-numerze / `url`) |
| Można ZGŁOSIĆ do `dataset-team-submissions` | TAK (licencja per dokument, bez NC/ND) |
| Użycie komercyjne | dozwolone: CC BY-SA 4.0 pozwala na użycie komercyjne; copyleft (SA) dotyczy dalszego udostępniania samych danych |

## 1. Rezerwacja

| | |
|---|---|
| Co | issue [#357](https://github.com/slayerlabs/benchmarks-fabryka-ai/issues/357) (część 3 zbioru matematyki i logiki) |
| Cel | opisy ciągów całkowitych OEIS (pozycja E1 w [`../matematyka-wspolne/kandydaci_czyste.md`](../matematyka-wspolne/kandydaci_czyste.md)) |
| Wiersz w danych treningowych | nie zmierzono (krok 12) |

## 2. Karta źródła

[`KARTA_ZRODLA.md`](KARTA_ZRODLA.md), 26.11.2026, przed klonowaniem (commit `4215d12`, 14:39, razem z preregistracją i budową).
`oeis/oeisdata@976b0c73` (commit 2026-11-26T08:03:27Z), tylko `seq/*.seq`, bez LFS. Licencja `LICENSE`: CC-BY-SA-4.0.
Karta ma też przykłady przed/po budowie (A017686, A100030, A005625).

## 3. Preregistracja

[`skrypty/preregistracja.json`](skrypty/preregistracja.json), commit `4215d12`: seed 20261126, dokument = jedna sekwencja
(układ tekstu w `dokument.uklad_tekstu`), filtr budowy przed detektorami, maskowanie e-maili przy budowie, reguły i aneksy
InfiWebMath-4+ (24.11, 24.11b, 24.11c, 25.11b, 25.11c, 25.11e) przejęte bez zmian. Odstępstwa: `pii.tryb`
`maskuj_email_usun_telefon_ip`, filtr budowy, `dedup_infiwebmath4`, brak `dedup_fineweb_edu_109`.

| aneks | commit | zapisany | treść |
|---|---|---|---|
| `aneks_2026_11_26_przeglad` | `de04099` (26.11 15:14) | po przeglądzie próbki, przed eksportem | wynik przeglądu, FAIL-e `ewal_13gram` i `pii` przyjęte (podsekcja w kroku 8) |

Kolejność plików w git: preregistracja i budowa puli są w jednym commicie (`4215d12`); kolejność „preregistracja przed
klonowaniem” potwierdza tylko pole `zapisano` (czas zapisu pliku przed commitem: nie zmierzono).

## 4. Środowisko

| | |
|---|---|
| Komenda | venv `../matematyka-wspolne/robocze/venv` (jak FineMath-4+) |
| Tokenizer | v6 sha256 `0640d3bd…815dd` |
| Sprawdzenie | porównanie `pip freeze` = `requirements.txt`: nie zmierzono |

## 5. Pobranie i budowa puli

| | |
|---|---|
| Klon | `git clone --filter=blob:none --sparse`, `sparse-checkout set seq`, checkout `976b0c73`, `GIT_LFS_SKIP_SMUDGE=1` (karta §4) |
| Budowa | `buduj_pule.py buduj` kod 0, 178 s (`buduj.log`, 26.11 14:35); `buduj_pule.py sprawdz` kod 0: „OK: 311925 wierszy, 191127613 tokenów v6, 63 grup” (karta §7) |
| Liczby | 402 003 plików `.seq` (597 687 151 B, 0 błędów UTF-8); zachowane **311 925 dok., 191 127 613 tokenów v6** (mediana 533, p99 1 910, maks. 24 682); odrzucone filtrem budowy 90 078 dok. (22,4%), 28 879 398 tok. (13,1%): `bez_tresci` 84 860 / 28 010 643, `krotka` 3 130 / 599 707, `martwa` 2 088 / 269 048, `brak_n` 0 |
| E-maile | zamaskowane przy budowie: `zaciemniony` 13 744, `email` 12, `at_bez_nawiasow` 18 dopasowań; po maskowaniu 0 / 0 / 0 |
| Wynik | [`wyniki/budowa.json`](wyniki/budowa.json), [`wyniki/probka_pliki.json`](wyniki/probka_pliki.json) |

Próbka filtra budowy (40 na powód, `robocze/probka_filtra_budowy.jsonl`): recenzja nie zmierzona (karta, „Nie sprawdzone (po budowie)”).

## 6. Indeksy i kontrole

- Testy, EN 1.07, walidacja Fabryki, `entech`, `en8x3b`: te same indeksy co FineMath-4+ i InfiWebMath-4+.
- `dedup_finemath4` i `dedup_infiwebmath4`: indeksy wyboru części 2 FineMath-4+ i InfiWebMath-4+ (`bazy_mat.py wlasne:*`).
- Kontrola dodatnia: wynik dla tego źródła nie zapisany (nie zmierzono). `buduj_pule.py` sprawdza asercjami maskowanie
  e-maili na wierszach z `(AT)`, `@` i ` at ` przed budową (preregistracja → `kontrole_dodatnie`).

## 7. Przebieg

| | |
|---|---|
| Wynik | 63/63 jednostek, `KONIEC 248s` (`przebieg.log`, 26.11 14:43); kod wyjścia nie zapisany w logu |
| `ew13` | `dokumentow 311925 z_trafieniem 40705 ngramow 18835`, `KONIEC` (14:43) |

## 8. Po przebiegu

`agreguj` 26.11 14:54 (`agreguj.log`, `KONIEC`; commit `f9306d4`), wynik [`wyniki/agreguj.json`](wyniki/agreguj.json):

| powód | odrzucone dok. | odrzucone tok. v6 | zostaje dok. | zostaje tok. v6 | % tok. | niezależnie dok. / % tok. |
|---|---|---|---|---|---|---|
| `walidacja_fabryki` | 36 | 14 011 | 311 889 | 191 113 602 | 99,993 | 36 / 0,007 |
| `domena_testow` | 0 | 0 | 311 889 | 191 113 602 | 99,993 | 0 / 0,0 |
| `ewal_13gram` | 205 | 195 012 | 311 684 | 190 918 590 | 99,891 | 205 / 0,102 |
| `pii` | 136 | 148 393 | 311 548 | 190 770 197 | 99,813 | 136 / 0,078 |
| `pii_zaciemniony` | 0 | 0 | 311 548 | 190 770 197 | 99,813 | 0 / 0,0 |
| `pii_at_bez_nawiasow` | 0 | 0 | 311 548 | 190 770 197 | 99,813 | 0 / 0,0 |
| `min_tresc` | 691 | 94 809 | 310 857 | 190 675 388 | 99,763 | 691 / 0,05 |
| `mojibake` | 0 | 0 | 310 857 | 190 675 388 | 99,763 | 0 / 0,0 |
| `dedup_wewnatrz` | 843 | 698 542 | 310 014 | 189 976 846 | 99,398 | 843 / 0,365 |
| `dedup_finemath4` | 43 051 | 32 029 028 | 266 963 | 157 947 818 | 82,64 | 43 066 / 16,769 |
| `dedup_infiwebmath4` | 1 487 | 1 405 761 | 265 476 | 156 542 057 | 81,904 | 1 488 / 0,736 |
| `dedup_slayer107` | 4 009 | 2 265 803 | 261 467 | 154 276 254 | 80,719 | 4 123 / 1,218 |
| `dedup_slayer_8x3b_en` | 0 | 0 | 261 467 | 154 276 254 | 80,719 | 0 / 0,0 |
| `dedup_english_technical` | 0 | 0 | 261 467 | 154 276 254 | 80,719 | 0 / 0,0 |

- **Uzysk: 261 467 dok., 154 276 254 tokenów v6 (80,719%)**. Do eksportu: wszystkie zachowane.
- `ewal_13gram` per test: MATH 117, MBPP 70, MathQA 8, SynLogic 5, HumanEval 3, MMLU 1, SQuAD2 1.
- PII wg detektora DCLM: e-mail 0 (zamaskowane przy budowie), telefon 7, IP 129. `dedup_wewnatrz`: 0 identycznych, 843 przez MinHash.

### Przegląd próbki (26.11.2026)

Dwóch niezależnych recenzentów (A, B), pełne teksty; wycinek 03 recenzenta A powtórzony po niepełnej lekturze (aneks).
Wynik [`wyniki/przeglad_1.json`](wyniki/przeglad_1.json). Progi: fałszywe odrzucenia ≤ 10% ORAZ górna granica Wilsona ≤ 20%.

| powód | n | A: fałszywe (wątpliwe) | A: [Wilson 95%] | B: fałszywe (wątpliwe) | B: [Wilson 95%] | werdykt A/B |
|---|---|---|---|---|---|---|
| `walidacja_fabryki` | 34 | 0 (31) | [0; 10,2] | 0 (0) | [0; 10,2] | PASS/PASS |
| `ewal_13gram` | 100 | 100 (0) | [96,3; 100] | 100 (0) | [96,3; 100] | FAIL/FAIL |
| `pii` | 100 | 92 (7) | [85,0; 95,9] | 92 (7) | [85,0; 95,9] | FAIL/FAIL |
| `min_tresc` | 100 | 0 (0) | [0; 3,7] | 0 (0) | [0; 3,7] | PASS/PASS |
| `dedup_wewnatrz` | 100 | 0 (1) | [0; 3,7] | 0 (0) | [0; 3,7] | PASS/PASS |
| `dedup_finemath4` | 100 | 0 (0) | [0; 3,7] | 0 (0) | [0; 3,7] | PASS/PASS |
| `dedup_infiwebmath4` | 100 | 0 (0) | [0; 3,7] | 0 (0) | [0; 3,7] | PASS/PASS |
| `dedup_slayer107` | 100 | 0 (0) | [0; 3,7] | 0 (45) | [0; 3,7] | PASS/PASS |

| zachowane (300) | A | B | próg | werdykt |
|---|---|---|---|---|
| śmieci | 0: 0,0% [0; 1,3], wątpliwe 8 | 0: 0,0% [0; 1,3], wątpliwe 1 | ≤ 10% | PASS |
| przeoczone PII | 0/300 | 0/300 | 0/300 | PASS |
| przeoczony test | 0/300 | 0/300 | — | PASS |

**Werdykt pliku: NIE PRZESZŁO** (`ewal_13gram` i `pii` u obu). Liczba pozycji w pliku: 7 × 100 + 34 + 300 = 1034; aneks
podaje 1036 — różnica 2 pozycji niewyjaśniona w plikach.

### Aneks 26.11 przegląd (commit `de04099`)

FAIL-e przyjęte przed eksportem: `ewal_13gram` 100/100 fałszywych u obu (formułki: pętle Pythona, listy liczb pierwszych,
rekurencje), koszt 0,10% tokenów; `pii` 92/100 (symbole kafelkowań 3.4.6.4, numery sekcji Knutha jako IPv4), koszt 0,08%;
reguły usuwają dobre teksty, nie przepuszczają złych; prywatność ma pierwszeństwo (jak aneks 24.11b).

## 9. Eksport

| | |
|---|---|
| Podział | [`wyniki/czesci.json`](wyniki/czesci.json): 1 część, `oeis_en_p01`, 261 467 dok., 154 276 254 tokenów v6 |
| Key | `oeis_en`; datasheet [`eksport/oeis_en.md`](eksport/oeis_en.md); wpis w `../matematyka-wspolne/eksport/src/sources.py` (licencja `CC-BY-SA-4.0`); skrypt `../matematyka-wspolne/eksport/src/clean_oeis_en.py` (commit `18c385d`): e-maile maskowane ponownie `premask_emails` przed `shard.write`, Presidio wyłączone (`no_masking(emails=True)`) |
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

- 26.11.2026 14:35–14:39: klon `976b0c73`, budowa puli 311 925 dok., 191 127 613 tok. v6; karta, preregistracja i budowa w commicie `4215d12` (14:39).
- 26.11.2026 14:43: `przebieg` 63/63 (`KONIEC 248s`), `ew13`.
- 26.11.2026 14:54: `agreguj`: 261 467 / 154 276 254 (80,719%); commit `f9306d4`.
- 26.11.2026 15:14: przegląd próbki i `aneks_2026_11_26_przeglad` przed eksportem (`de04099`).
- 26.11.2026 15:16: nakładka eksportu `clean_oeis_en.py`, rejestr i test kontraktowy (`18c385d`).
- Eksport i `check.py`: w toku.

## Pułapki tego przebiegu

- Url `https://oeis.org/A<nr>` jest celowo zgodny z adresem strony: sekwencja, której strona jest w FineMath-4+ albo
  InfiWebMath-4+, odpada (`dedup_finemath4` zabiera 16,8% tokenów).
- Detektory telefonu i IPv4 trafiają w ciągi liczb (kafelkowania, numery sekcji): 92% fałszywych odrzuceń przy koszcie 0,08%.
- `ewal_13gram` w OEIS łapie wyłącznie formułki i programy (100/100 fałszywych), koszt 0,10%.
