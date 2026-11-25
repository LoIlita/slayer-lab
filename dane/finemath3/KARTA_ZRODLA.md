# Karta źródła: FineMath-3+ (EN, matematyka z sieci) dla Slayera 1B

Zapisana 25.11.2026 przed pobraniem zbioru. Zbadany jeden plik (shard 0) w `/tmp`, usunięty po pomiarze. Rezerwacja:
https://github.com/slayerlabs/benchmarks-fabryka-ai/issues/346

Rola: dopełnienie zbioru matematyki ~20 mld tokenów po FineMath-4+ (pełny, `dane/finemath4`) i InfiWebMath-4+
(`dane/infiwebmath4`). Z puli odpadają strony już obecne w FineMath-4+, więc realnie bierzemy warstwę `int_score = 3`.
Oznaczenia: V = sprawdzone 2026-11-25 w podanym źródle (URL, rewizja, hash, pomiar), I = wywnioskowane.

Prawa, pochodzenie, klasyfikator, takedown i nowość wobec 1.07/1.09: **jak w `dane/finemath4/KARTA_ZRODLA.md`**
(to samo repo, ta sama rewizja, ta sama licencja i potok). Niżej tylko to, co dla 3+ inne albo zmierzone.

## 1. Identyfikacja

- V: https://huggingface.co/datasets/HuggingFaceTB/finemath, rewizja `e92b25a616738fe95dc186b64dfb19f9c8525594`,
  config `finemath-3plus`, 128 plików `finemath-3plus/train-00NNN-of-00128.parquet`.
- V (praca SmolLM2 arXiv 2502.02737 §3.3.2): FineMath-3+ = dokumenty z oceną klasyfikatora 3–5 (5-punktowa skala),
  FineMath-4+ = 4–5; 4+ jest podzbiorem 3+ (karta: „FineMath-4+ (a subset of FineMath-3+)”).

## 2. Prawa

- Jak w karcie FineMath-4+ (ODC-By 1.0 + CC ToU, tekst ludzki z Common Crawl, klauzula Llamy nie dotyczy — I).
- Bramka „można TRENOWAĆ”: **TAK** (jak 4+; takedown po `url` / `warc_filename`+`warc_record_offset`, V: kolumny są).
  Warunek: opt-out TDM, NIE SPRAWDZONY.
- Bramka „można ZGŁOSIĆ”: **NIEROZSTRZYGNIĘTY** (jak 4+). W warstwie 3 więcej domen o restrykcyjnych regulaminach
  (V: coursehero.com, teacherspayteachers.com, stackoverflow.com CC BY-SA w czołówce) — niżej.

## 3. Zawartość

- V (shard 0): kolumny identyczne z FineMath-4+: `url`, `fetch_time`, `content_mime_type`, `warc_filename`,
  `warc_record_offset`, `warc_record_length`, `text`, `token_count`, `char_count`, `metadata`, `score`, `int_score`,
  `crawl`, `snapshot_type`, `language`, `language_score`.
- V (shard 0, 167 232 wierszy): `int_score` 3: 114 997 (68,8%), 4: 47 257, 5: 4 978; min `score` 2,52 (zaokrąglenie
  do 3). `crawl` głównie CC-MAIN-2024-*; `snapshot_type` latest 133 769 / longest 33 463.
- V (shard 0, tylko `int_score = 3`): top domeny physicsforums.com 2 346, jiskha.com 2 055, coursehero.com 2 031,
  math.stackexchange.com 1 339, gmatclub.com 1 186, oeis.org 1 115, stackoverflow.com 999, mathoverflow.net 822,
  mathhelpforum.com 797, physics.stackexchange.com 737, teacherspayteachers.com 672. V: 1 619 url to gołe domeny bez
  schematu (np. `mathomat.com.au`) — strony główne.
- I (SmolLM2 §3.3.2, skala 5-punktowa): warstwa 3 to treść matematyczna z mniejszym naciskiem na rozumowanie krok po
  kroku i poziom szkolny; więcej programowania (stackoverflow), matematyki akademickiej (mathoverflow) i ciągów (OEIS).

## 4. Skala i dostęp

- V (karta/README): 21 405 610 dokumentów, 34 mld tokenów Llamy; download_size 65 039 196 945 B.
- V (API): 128 plików, łącznie 65 039 196 945 B; shard 0 = 507 607 173 B, sha256
  `a4f0e7e96b4f6af4a1b597c2fc4a42ec9a997c64ab7da96760c40582a0ac27a5` (zgodny z LFS oid).
- V (shard 0): suma `token_count` 262 083 102, z tego `int_score ≥ 4` 73 742 675 (28%), `= 3` 188 340 427 (72%);
  średnio 1 638 tok./dok. w warstwie 3. 167 148 unikalnych url na 167 232.
- I: warstwa 3 ≈ 188,3 mln × 128 ≈ 24,1 mld tokenów Llamy (karta: 34 − 9,6 = 24,4 mld) i ~14,7 mln dokumentów.
  To jest pula „nowa” wobec FineMath-4+; do 20 mld wystarczy część, przed dedupem wobec InfiWebMath-4+.

## 5. Ryzyka (różnice wobec FineMath-4+)

- Zawieranie 4+ (V pomiar): url shardu 0 porównane z 31 pełnymi shardami FineMath-4+ z
  `dane/finemath4/robocze/pobrania/lok/*.rg5000.parquet` (3 245 071 wierszy, 3 125 906 unikalnych url = 31/64 =
  48,4% zbioru). Trafienia: `int_score` 4 → 21 766/47 257 (46,1%), 5 → 2 256/4 978 (45,3%), 3 → 456/114 997
  (0,4%); łącznie 24 478 (14,6%). I: 46% / 48,4% ≈ 95% — wiersze 4–5 z 3+ są w FineMath-4+ (reszta to zapewne różnice
  podziału na shardy / te same url w drugim zrzucie); 4+ ⊂ 3+ potwierdzone w granicach pomiaru. Warstwa 3 prawie się
  z 4+ nie pokrywa (0,4% × 64/31 ≈ 0,8% — I: ta sama strona w innym zrzucie z inną oceną).
- Filtr dla nas: brać `int_score == 3` (prościej i pewniej niż dedup po url); dedup url+MinHash wobec InfiWebMath-4+
  i open-web-math z 1.07 nadal obowiązkowy.
- Jakość (V, SmolLM2 §3.3.2 + Rys. 1, karta finemath): 4+ lepszy od 3+ na GSM8K i MATH; 3+ i tak lepszy od OWM i
  InfiMM-WebMath; mieszanka 50% FineMath-3+ / 50% InfiWebMath-3+ dorównuje FineMath-3+. I: sama warstwa 3 (bez 4–5)
  jest słabsza niż 3+ jako całość — nieopisana w pracy, do zmierzenia w ablacji.
- Dekontaminacja: V (SmolLM2 §3.3.2) 13-gramy + LCS ≥ 0,6 wobec GSM8K, MATH, MMLU (karta dodaje ARC), każdy wariant
  osobno. Reszta testów Fabryki — nasze 13-gramy obowiązkowe (jak 4+). I: warstwa 3 ma więcej stron z zadaniami bez
  rozwiązań (coursehero, teacherspayteachers, gmatclub) — większe ryzyko przecieku testów spoza listy HF.
- Prawa domen: V coursehero 2 031 i teacherspayteachers 672 (materiały płatne, I: restrykcyjne regulaminy) oraz
  stackoverflow/mathoverflow (CC BY-SA) wyżej w czołówce niż w 4+ — kandydaci do wykluczenia domeny przed zgłoszeniem.
- PII: V e-mail (regex) w 559 z 20 000 pierwszych dokumentów (2,8%; w 4+ 1,6%) → maskowanie e-maili.
- Kopie latest/longest: V 20% wierszy `longest` (jak w 4+), dedup wewnętrzny jak w 4+.

## 6. Nowość

- Jak w karcie FineMath-4+: FineMath (podzbiór nieznany) i open-web-math są w en_mix 1.07; 1.09 bez matematyki web.
  I: jeśli en_mix 1.07 brał 3+, warstwa 3 jest już częściowo w historii Slayera — sprawdzić przed decyzją.

## Nie sprawdzone

- Opt-out TDM i regulaminy domen warstwy 3 (coursehero, teacherspayteachers, stackoverflow).
- Raport `finemath_contamination_report/finemath-3plus` (liczby usuniętych).
- Podzbiór FineMath w en_mix 1.07 (3+ czy 4+) i nakładanie z nim.
- Nakładanie warstwy 3 z InfiWebMath-4+/3+ (url i MinHash).
- Rozkład `int_score`, domen i e-maili poza shardem 0; pozostałe 33 shardy FineMath-4+ (zawieranie mierzone na 31/64).
- Współczynnik tokenów v6 / Llama.
