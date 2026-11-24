# Instrukcja ręcznego przeglądu próbki (zbiory matematyki do microannealu, #346)

Oceniasz wycinek próbki jednego zbioru: plik JSONL, jedna pozycja w wierszu. Nie budowałeś zbioru i nie znasz
ocen innego recenzenta. Oceniasz każdą pozycję z wycinka, bez pomijania. Progi i reguły: `dane/<zbior>/skrypty/preregistracja.json`.

## Pola pozycji

- `grupa`: `odrzucony` albo `zachowany`.
- `powod` (odrzucony): reguła, która go odrzuciła (widok niezależny: dokument może mieć też inne powody, `pierwszy_powod` to pierwszy w kaskadzie).
- `tekst`: do 3000 pierwszych znaków; `url`; `tokeny_v6`.
- `trafienia` (ewal_13gram, ewal_13gram_oryginal): 13-gramy, które zadecydowały, z nazwą testu i df w puli.
- `para` (dedup_wewnatrz): wcześniejszy dokument, którego kopią jest ten.
- `wynik_indeksu` (dedup_slayer107, walidacja_fabryki): udział szkicu 13-gramów i szacowany Jaccard MinHash wobec indeksu.
- `tekst_oryginalny` (cranemath, zachowany): strona FineMath przed przepisaniem przez Qwen3-32B.

## Co oceniasz

**Odrzucony** — pole `trafny`:
- `tak`: dokument ma cechę opisaną przez powód. `ewal_13gram`: wspólny fragment to treść zadania lub rozwiązania testu,
  nie cytat ani formułka. `pii`: trafienie to prawdziwy e-mail, telefon albo adres IP. `domena_testow`: host pasuje do
  listy. `mojibake`: widać zepsute kodowanie. `dedup_wewnatrz`: tekst i `para` to kopia albo bliska kopia (różnica tylko
  w nazwie, liczbie albo innej wartości w tym samym szablonie to też kopia). `dedup_slayer107` / `walidacja_fabryki`:
  przy szkicu ≥ 0,5 albo MinHash ≥ 0,8 uznaj za trafny, chyba że tekst to oczywisty szablon bez treści. `think`: tekst
  zawiera znacznik `<think>`. `licencja`, `int_score`: trafny z definicji, oceń tylko, czy tekst nadawałby się do treningu.
  `sekrety`: dopasowanie to prawdziwy klucz albo token, nie przykład z dokumentacji. `wygenerowany`: plik naprawdę
  wygenerowany (migracja, stub, protobuf, plik z narzędzia), nie zwykły kod ze słowem „generated”.
- `nie`: dokument tej cechy nie ma (fałszywe odrzucenie).
- `watpliwy`: nie da się rozstrzygnąć z dostępnego tekstu; napisz dlaczego.

**Zachowany** — pola:
- `jakosc`: `tak` (nadaje się do treningu matematyki albo kodu), `nie` (śmieci: nawigacja, spam, pusty szablon,
  tekst bez treści, zła maszynowa składnia), `watpliwy`.
- `pii_przeoczone` (finemath4, cranemath): `tak`, gdy w tekście jest e-mail, telefon albo IP osoby prywatnej.
- `sekret_przeoczony` (stackedu): `tak`, gdy w kodzie jest prawdziwy klucz, hasło albo token.
- `test_przeoczony`: `tak`, gdy rozpoznajesz dosłowne zadanie z GSM8K, MATH, MMLU, HumanEval albo MBPP.
- `przepisanie` (cranemath): `poprawne`, `blad_matematyczny` (zły wynik, zły krok obliczeń), `sprzeczne` (treść
  niezgodna z `tekst_oryginalny`, zmyślone dane), `watpliwe`. Sprawdź obliczenia, nie tylko styl.

## Wynik

Plik JSON (ścieżka w zadaniu): lista obiektów `{"nr": <nr pozycji>, "grupa": ..., "powod": ..., <pola oceny>, "uwaga": "<jedno zdanie przy każdym nie/watpliwy/tak w polach przeoczeń>"}`
w kolejności pozycji z wycinka. Bez streszczeń treści. Nie kopiuj danych osobowych do uwag.
