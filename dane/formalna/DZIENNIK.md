# Dziennik zbioru: formalna (biblioteki matematyki formalnej i Stacks Project) dla Slayera 1B, część 3

Przepis: [`METODOLOGIA.md` w repo zespołu](https://github.com/slayerlabs/benchmarks-fabryka-ai/blob/main/research/slayer-1b/dane/METODOLOGIA.md).
Karta źródła: [`KARTA_ZRODLA.md`](KARTA_ZRODLA.md) (z sekcją „Po klonie i budowie”). Reguły: [`skrypty/preregistracja.json`](skrypty/preregistracja.json).
Budowa puli: `skrypty/buduj_pule.py`; detektory i agregacja: [`../matematyka-wspolne/skrypty/`](../matematyka-wspolne/skrypty/).
Logi: `robocze/logi/` (poza gitem). Dzienniki bliźniacze: [InfiWebMath-4+](../infiwebmath4/DZIENNIK.md) (reguły przejęte),
[OEIS](../oeis/DZIENNIK.md), [Stack-Edu Python](../stackedu/DZIENNIK.md) (maskowanie e-maili w kodzie).

## Bramki praw

| bramka | wynik |
|---|---|
| Można TRENOWAĆ | TAK: każda biblioteka ma licencję otwartą bez NC/ND; takedown po `url`/`path` wiersza |
| Można ZGŁOSIĆ do `dataset-team-submissions` | TAK dla wierszy z licencją z tabeli w kroku 5 (licencja per wiersz; AFP per wpis i nagłówek pliku) |
| Użycie komercyjne | dozwolone dla wszystkich licencji per wiersz (Apache-2.0, BSD-2/3, LGPL-2.1, CeCILL-B, MIT, CC0, GFDL-1.2, UniMath = tekst MIT); copyleft (LGPL, GFDL) dotyczy dalszego udostępniania samych danych |

## 1. Rezerwacja

| | |
|---|---|
| Co | issue [#357](https://github.com/slayerlabs/benchmarks-fabryka-ai/issues/357) (część 3 zbioru matematyki) |
| Cel | czysta matematyka formalna z bibliotek z jawną licencją (kandydaci B1–B5 w [`../matematyka-wspolne/kandydaci_czyste.md`](../matematyka-wspolne/kandydaci_czyste.md)); B6 (Proof-Pile-2 proofsteps) tylko szacunek, bez budowy |
| Wiersz w danych treningowych | nie zmierzono (krok 12) |

## 2. Karta źródła

[`KARTA_ZRODLA.md`](KARTA_ZRODLA.md), 26.11.2026 14:23 CET (mtime 14:23:56), przed klonowaniem (start 14:24:05). Dziewięć
bibliotek z rewizjami z 14:21 CET; po klonie dopisana sekcja „Po klonie i budowie” (licencje, tekst z modeli, pula końcowa).
Commit karty, preregistracji i budowy: `9cbd1b4` (26.11 14:50).

## 3. Preregistracja

[`skrypty/preregistracja.json`](skrypty/preregistracja.json), zapisana 14:23:13 CET przed klonowaniem: seed 20261126, dokument = plik
(set.mm/iset.mm w sekcjach bez dowodów), reguły i aneksy InfiWebMath-4+ przejęte (`aneksy_przejete`). Odstępstwa: `pii.tryb`
`maskuj_email_usun_telefon_ip`, brak `dedup_fineweb_edu_109`, nowy `dedup_infiwebmath4`, pula = całe źródło. Ręczna próbka:
100 odrzuconych na powód, 300 zachowanych warstwowo wg tokenów bibliotek (co najmniej 20 na bibliotekę).

| aneks | zapisany | treść |
|---|---|---|
| `aneks_2026_11_26` | 14:29 CET, po klonie, przed budową i pierwszym liczeniem | licencje per plik z plików licencji w klonach (AFP: `License: LGPL` w pliku przed toml; HOL Light: GL, Quaternions BSD-2, 2 pliki wykluczone; Stacks GFDL 1.2 or later; UniMath tekst MIT) |
| `aneks_2026_11_26b` | ok. 14:36 CET, po budowie 1 (liczby widoczne), przed przeglądem i agregacją | zasada „zero tekstu z modeli”: plik zmieniony przez commit z ujawnionym narzędziem AI (wzorzec `AI_WZORZEC`) wykluczony w całości |
| `aneks_2026_11_26c` | ok. 14:43 CET, decyzja integratora po pomiarze 26.11b | mathlib4 `9bed6a56` (2025-03-31) i HOL Light `b9a430b8` (2025-12-11): rewizje sprzed pierwszego ujawnionego commita z AI; stara pula odrzucona |
| `aneks_2026_11_26d` | po pierwszej agregacji (14:57), przed przeglądem i eksportem; commit `ceaf711` (14:58) | e-maile maskowane do `[PII]` przy eksporcie zamiast usuwania plików; `pii_zaciemniony` i `pii_at_bez_nawiasow` zdjęte z kaskady |
| `aneks_2026_11_26_przeglad` | po przeglądzie, przed eksportem; commit `de04099` (15:14) | wynik przeglądu, FAIL-e przyjęte, maskowanie uzupełnione o formy z przeglądu |

Godziny aneksów 26.11–26.11c pochodzą z pól `zapisano` i logów (karta, „Po klonie i budowie”); wszystkie trafiły do gita
dopiero w `9cbd1b4` (14:50). Aneks 26.11b ma w polu poprawkę godziny („wcześniej omyłkowo wpisane 14:45”).

## 4. Środowisko

| | |
|---|---|
| Komenda | venv `../matematyka-wspolne/robocze/venv` |
| Tokenizer | v6 sha256 `0640d3bd…815dd` |
| Sprawdzenie | porównanie `pip freeze` = `requirements.txt`: nie zmierzono |

## 5. Pobranie i budowa puli

| | |
|---|---|
| Klon | 14:24:05–14:27:32 (`klon.log`, wszystkie 9 `rev-parse HEAD` = rewizja); checkout nowych rewizji mathlib4 i HOL Light 14:43:05 |
| Budowa 1 | 14:29:03–14:30:24 (`buduj.log`, kod 0): 24 326 wierszy, 239 112 139 tok. v6 (przed regułą AI) |
| Budowa 2 | 14:37:18–14:41:10 (`buduj2.log`, kod 0): rewizje listopadowe z regułą 26.11b: 16 917 wierszy, 180 297 515 tok.; mathlib4 709 commitów AI, 6 866 plików wykluczonych; HOL Light 40 commitów, 506 plików ([`wyniki/budowa_odrzucona_rewizje_listopad.json`](wyniki/budowa_odrzucona_rewizje_listopad.json)); pula odrzucona |
| Budowa 3 (pula końcowa) | 14:43:41–14:45:30 (`buduj3.log`, kod 0): **21 385 wierszy, 213 219 274 tok. v6**; reguła AI na nowych rewizjach: mathlib4 1 plik (22 507 tok.), HOL Light 0, UniMath 49 plików (578 161 tok.), set.mm 2 fragmenty (40 573 tok.) ([`wyniki/ai_wykluczone.json`](wyniki/ai_wykluczone.json)) |
| Kontrola kontraktu | `skrypty/sprawdz_kontrakt.py` → [`wyniki/kontrakt.json`](wyniki/kontrakt.json): PASS (14:46) |
| Wynik | [`wyniki/budowa.json`](wyniki/budowa.json), [`wyniki/probka_pliki.json`](wyniki/probka_pliki.json), [`wyniki/duze_pliki.json`](wyniki/duze_pliki.json), [`wyniki/hol_light_licencje.json`](wyniki/hol_light_licencje.json) |

| biblioteka | rewizja | wiersze | tokeny v6 | licencja |
|---|---|---|---|---|
| mathlib4 | `9bed6a56` | 5 892 | 30 775 066 | Apache-2.0 |
| afp | `02fd3c6b` | 10 557 | 129 985 322 | BSD-3-Clause 10 238 / LGPL-2.1-only 319 |
| hol_light | `b9a430b8` | 541 | 12 555 462 | BSD-2-Clause |
| setmm | `ce7f29d6` | 621 | 11 155 284 | CC0-1.0 |
| rocq_stdlib | `9657c750` | 583 | 2 605 422 | LGPL-2.1-only |
| mathcomp | `656cdbcf` | 149 | 2 776 193 | CECILL-B |
| unimath | `11e01f09` | 1 659 | 10 183 276 | LicenseRef-UniMath |
| agda_stdlib | `119d1761` | 1 190 | 2 156 221 | MIT |
| stacks | `a04446e5` | 193 | 11 027 028 | GFDL-1.2-no-invariants-or-later |

## 6. Indeksy i kontrole

- Testy, EN 1.07, walidacja Fabryki, `entech`, `en8x3b`, `wlasne:finemath4`, `wlasne:infiwebmath4`: te same indeksy co w
  częściach 2 (dziennik InfiWebMath-4+, krok 6).
- Kontrola dodatnia: wynik dla tego źródła nie zapisany (nie zmierzono); planowane przypadki w preregistracji
  (`kontrole_dodatnie`: `.lean` z e-mailem w nagłówku, kopia pliku AFP, fragment set.mm po regule dowodów).

## 7. Przebieg

| | |
|---|---|
| Wynik | 12/12 jednostek, `KONIEC 174s` (`przebieg.log`, 26.11 14:53); kod wyjścia nie zapisany w logu |
| `ew13` | `dokumentow 21385 z_trafieniem 76 ngramow 244`, `KONIEC` (14:53) |

## 8. Po przebiegu

Pierwsza `agreguj` 14:57 (`agreguj.log`, z `pii_zaciemniony` 40 plików / 1 037 379 tok. i `pii_at_bez_nawiasow` 615 / 7 951 883):
zostaje 19 839 / 199 862 474 (93,736%). Po aneksie 26.11d `agreguj_26d.log` 15:02, `KONIEC` (commit `c61fe2d`), wynik
[`wyniki/agreguj.json`](wyniki/agreguj.json):

| powód | odrzucone pliki | odrzucone tok. v6 | zostaje | zostaje tok. v6 | % tok. | niezależnie pliki / % tok. |
|---|---|---|---|---|---|---|
| `walidacja_fabryki` | 0 | 0 | 21 385 | 213 219 274 | 100,0 | 0 / 0,0 |
| `domena_testow` | 0 | 0 | 21 385 | 213 219 274 | 100,0 | 0 / 0,0 |
| `ewal_13gram` | 5 | 374 277 | 21 380 | 212 844 997 | 99,824 | 5 / 0,176 |
| `pii` | 37 | 1 211 156 | 21 343 | 211 633 841 | 99,256 | 37 / 0,568 |
| `min_tresc` | 576 | 49 683 | 20 767 | 211 584 158 | 99,233 | 576 / 0,023 |
| `mojibake` | 0 | 0 | 20 767 | 211 584 158 | 99,233 | 0 / 0,0 |
| `dedup_wewnatrz` | 253 | 2 715 768 | 20 514 | 208 868 390 | 97,959 | 257 / 1,289 |
| `dedup_finemath4` | 3 | 58 434 | 20 511 | 208 809 956 | 97,932 | 3 / 0,027 |
| `dedup_infiwebmath4` | 0 | 0 | 20 511 | 208 809 956 | 97,932 | 0 / 0,0 |
| `dedup_slayer107` | 32 | 74 635 | 20 479 | 208 735 321 | 97,897 | 49 / 0,041 |
| `dedup_slayer_8x3b_en` | 0 | 0 | 20 479 | 208 735 321 | 97,897 | 0 / 0,0 |
| `dedup_english_technical` | 0 | 0 | 20 479 | 208 735 321 | 97,897 | 0 / 0,0 |

- **Uzysk: 20 479 plików, 208 735 321 tokenów v6 (97,897%)**. Do eksportu: wszystkie zachowane.
- `ewal_13gram` per test: MATH 2, SynLogic 1, MBPP 1, SQuAD2 1.
- PII wg detektora DCLM: e-mail 761 (maskowane, nie usuwają), telefon 0, IP 37. `dedup_wewnatrz`: 36 identycznych, 221 przez MinHash.

### Przegląd próbki (26.11.2026)

Dwóch niezależnych recenzentów (A, B), pełne teksty; dedupy oceniane z parą
([`../matematyka-wspolne/skrypty/probka_z_parami.py`](../matematyka-wspolne/skrypty/probka_z_parami.py), commit `1d96d53`).
Wynik [`wyniki/przeglad_1.json`](wyniki/przeglad_1.json). Progi: fałszywe odrzucenia ≤ 10% ORAZ górna granica Wilsona ≤ 20%.

| powód | n | A: fałszywe (wątpliwe) | A: [Wilson 95%] | B: fałszywe (wątpliwe) | B: [Wilson 95%] | werdykt A/B |
|---|---|---|---|---|---|---|
| `ewal_13gram` | 5 | 5 (0) | [56,6; 100] | 5 (0) | [56,6; 100] | FAIL/FAIL |
| `pii` | 36 | 16 (17) | [29,5; 60,4] | 16 (17) | [29,5; 60,4] | FAIL/FAIL |
| `min_tresc` | 100 | 0 (0) | [0; 3,7] | 0 (0) | [0; 3,7] | PASS/PASS |
| `dedup_wewnatrz` | 95 | 0 (0) | [0; 3,9] | 0 (0) | [0; 3,9] | PASS/PASS |
| `dedup_finemath4` | 3 | 0 (0) | [0; 56,2] | 0 (0) | [0; 56,2] | FAIL/FAIL |
| `dedup_slayer107` | 49 | 0 (36) | [0; 7,3] | 0 (37) | [0; 7,3] | PASS/PASS |

| zachowane (300) | A | B | próg | werdykt |
|---|---|---|---|---|
| śmieci | 11: 3,7% [2,1; 6,4], wątpliwe 9 | 9: 3,0% [1,6; 5,6], wątpliwe 11 | ≤ 10% | PASS |
| przeoczone PII (tekst przed maskowaniem) | 17/300 | 17/300 | 0/300 | FAIL |
| przeoczony test | 0/300 | 0/300 | — | PASS |

**Werdykt pliku: NIE PRZESZŁO** (u obu: `dedup_finemath4`, `ewal_13gram`, `pii`, przeoczone PII). Liczba pozycji w pliku:
5 + 36 + 100 + 95 + 3 + 49 + 300 = 588; aneks podaje 594 — różnica 6 pozycji niewyjaśniona w plikach.

### Aneks 26.11 przegląd (commit `de04099`)

- Przeoczone PII 17/300: e-maile autorów w nagłówkach AFP, oceniane na tekście PRZED maskowaniem. Maskowanie przy eksporcie
  (aneks 26.11d) uzupełnione o formy z przeglądu (`nazwa-at-domena`, `nazwa at web de`; commity `5799bec`, `b2041d2`).
  Kontrola [`../matematyka-wspolne/skrypty/resztki_email.py`](../matematyka-wspolne/skrypty/resztki_email.py) na całej puli po
  maskowaniu: **0 dokumentów z resztkami na 21 385**; 1 131 trafień wzorców `bare_at` na całej puli przejrzanych: same adresy.
- FAIL-e przyjęte: `ewal_13gram` 5/5 fałszywych (formułki, cytat Goldbacha), koszt 0,18%; `pii` 16/36 fałszywych (numery wersji,
  przykładowe adresy RFC), 3 trafne publiczne adresy instytucji, koszt 0,57% (jak aneks 24.11b); `dedup_finemath4` 0/3 — FAIL tylko
  z górnej granicy Wilsona przy n = 3.

## 9. Eksport

| | |
|---|---|
| Podział | [`wyniki/czesci.json`](wyniki/czesci.json): 1 część, `formal_math_p01`, 20 479 plików, 208 735 321 tokenów v6 |
| Key | `formal_math`; datasheet [`eksport/formal_math.md`](eksport/formal_math.md); wpis w `../matematyka-wspolne/eksport/src/sources.py` (`license_spdx` `LicenseRef-per-file`); skrypt `../matematyka-wspolne/eksport/src/clean_formal_math.py` (commit `18c385d`): `premask_emails(..., bare_at=True)` przed `shard.write`, licencja per plik, Presidio wyłączone (`no_masking(emails=True)`) |
| Kontrola po eksporcie (aneks 26.11d) | `resztki_email.py formalna/wyniki/probka_pliki.json 1` (cała pula przez `premask_emails(bare_at=True)`, ta sama funkcja co w eksporcie, 26.11): **0 dokumentów z resztkami**; na samym pliku części nie mierzone osobno |
| Eksport | `../matematyka-wspolne/skrypty/eksport_czesci.sh` (`robocze/logi/eksport.log`, `KONIEC 1`): 20 390 plików, 157 587 646 `token_count` (licznik repo zgłoszeń, nie v6); `dropped`: wrong_language 89; sha256 `06c9c5b8e09e54dee541cba189cee835bd30d7b8dab50731579b724d295431bf` |

## 10. Kontrola końcowa

| | |
|---|---|
| Test kontraktowy, `check.py` | test kontraktowy 1 passed; `check.py` 15 linii, wyłącznie oczekiwane („PII left after masking”, „no presidio record”) |
| Niezależny agent na pliku o tym samym sha256 | nie zmierzono |

## 11. Wysyłka

Repo `Lolita67/matematyka-kod-en-robocze` (gated manual), `data/formal_math_p01/`, commit HF `73eb3c08`; sha256 LFS zgodne z sha256 z logu eksportu (API HF); anonimowe pobranie: 401. Dostęp dla `Maggio33`: czeka na właścicielkę (Settings → Gated user access).

## 12. Dane treningowe

Wersja stokenizowana `tokenized/slayer-v6/formal_math_p01` (z parquetu o sha256 `06c9c5b8…`): 20 390 plików (= liczba wierszy parquetu), 208 104 938 tokenów v6; commit HF `c0ba1c48` (bin), `efbfd864` (metadane).

## Historia odtworzeń

- 26.11.2026 14:21–14:23: rewizje rozwiązane przez API GitHub; preregistracja 14:23:13, karta 14:23:56.
- 26.11.2026 14:24–14:27: klon 9 repozytoriów; 14:29 aneks 26.11 (licencje); 14:29–14:30 budowa 1 (24 326 wierszy).
- 26.11.2026 ok. 14:36: aneks 26.11b; 14:37–14:41 budowa 2 na rewizjach listopadowych (16 917 wierszy, odrzucona).
- 26.11.2026 14:43: aneks 26.11c, checkout `9bed6a56` (mathlib4) i `b9a430b8` (HOL Light); 14:43–14:45 budowa 3: 21 385 wierszy, 213 219 274 tok.; 14:46 kontrakt PASS; commit `9cbd1b4` (14:50).
- 26.11.2026 14:53: `przebieg` 12/12, `ew13`; 14:57 pierwsza `agreguj`: 19 839 / 199 862 474.
- 26.11.2026 14:58–15:02: aneks 26.11d (`ceaf711`), maskowanie `bare_at` (`b2041d2`), `agreguj_26d`: 20 479 / 208 735 321 (`c61fe2d`).
- 26.11.2026 15:05–15:14: próbka z parami (`1d96d53`), maskowanie form z przeglądu i `resztki_email.py` (`5799bec`), przegląd i aneks (`de04099`).
- 26.11.2026 15:16: nakładka eksportu `clean_formal_math.py`, rejestr, test kontraktowy (`18c385d`).
- 26.11.2026 15:25: eksport (`KONIEC 1`, sha256 `06c9c5b8…`), test kontraktowy 1 passed, `check.py` tylko oczekiwane linie; wysyłka HF `73eb3c08`, sha256 zgodne, anonimowo 401.
- 26.11.2026 18:22: tokenizacja v6 na HF (`c0ba1c48`, `efbfd864`): 20 390 plików, 208 104 938 tok. v6.

## Pułapki tego przebiegu

- Historia git bibliotek ujawnia wkład modeli zamkniętych (mathlib4 709 commitów, HOL Light 40 na rewizjach z listopada 2026):
  rewizję trzeba wybierać sprzed pierwszego ujawnionego commita z AI, a reguła per plik i tak nie łapie użycia nieujawnionego ani
  zmian nazw plików.
- Reguły PII z kontrolą „oczekiwane 0” założone dla puli maskowanej przy budowie (OEIS) nie pasują do puli bez maskowania: w formalnej
  usunęłyby 655 plików z e-mailami autorów (aneks 26.11d).
- Przegląd PII w zachowanych trzeba robić na tekście PO maskowaniu albo mierzyć resztki skryptem: ocena na tekście przed maskowaniem
  dała 17/300 „przeoczeń”, które maskowanie eksportu obejmuje.
- Reguła „> 1 MB = dane generowane” okazała się błędna dla HOL Light (ręcznie pisane teorie, I: ok. 6–7 mln tok. utracone); bez aneksu.
