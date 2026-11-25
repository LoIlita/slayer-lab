# Karta źródła: InfiWebMath-4+ (FineMath, EN, matematyka z sieci) dla Slayera 1B

Zapisana 25.11.2026 przed pobraniem zbioru. Zbadany jeden plik (shard 0) w `/tmp`, poza repo. Rezerwacja:
https://github.com/slayerlabs/benchmarks-fabryka-ai/issues/346

Cel: kolejne źródło do zbioru matematyki ~20 mld tokenów dla Slayera 1B, obok FineMath-4+ (`dane/finemath4`).
Oznaczenia: V = sprawdzone 2026-11-25 w podanym źródle (URL, rewizja, hash, pomiar), I = wywnioskowane.

## 1. Identyfikacja

- V: URL https://huggingface.co/datasets/HuggingFaceTB/finemath, rewizja
  `e92b25a616738fe95dc186b64dfb19f9c8525594` (ta sama co FineMath-4+). Podzbiór (config) `infiwebmath-4plus`,
  32 pliki `infiwebmath-4plus/train-000NN-of-00032.parquet`.
- V (karta finemath): „filtered English text-only portion of InfiMM-WebMath-40B, classified using the same approach
  as FineMath”; InfiWebMath-4+ ⊂ InfiWebMath-3+.
- V: zbiór źródłowy https://huggingface.co/datasets/Infi-MM/InfiMM-WebMath-40B (sha `0fb36b9da0f978ddeeee2884971994d2188a1589`,
  lastModified 2025-07-26, bez bramki); praca InfiMM-WebMath, arXiv 2409.12568. Przeklasyfikowanie: praca SmolLM2,
  arXiv 2502.02737 §3.3 (I: treść §3.3 przyjęta za kartą finemath, której opis jest z nią zbieżny; sekcji nie czytano
  w tej sesji).
- V: klasyfikator https://huggingface.co/HuggingFaceTB/finemath-classifier (MIT; szczegóły w karcie FineMath-4+).

## 2. Prawa

- V: licencja podzbioru w repo finemath: ODC-By 1.0 + Common Crawl Terms of Use (README `license: odc-by`, sekcja
  „Licensing Information”, jedna dla wszystkich configów).
- V: licencja InfiMM-WebMath-40B: ODC-By 1.0 + CC ToU; karta: „We do not alter the license of any of the underlying
  data”. Obie licencje dotyczą kompilacji, nie tekstów; teksty mają prawa wydawców stron, pola licencji per wiersz
  brak (V: schemat).
- V/I: tekst ludzki z sieci: InfiMM wyciągnął tekst z HTML (Trafilatura/Resiliparse), finemath zostawił tylko część
  tekstową; nic nie generowano. Llama-3.1-70B dała tylko oceny do treningu klasyfikatora (jak w FineMath-4+) —
  klauzula Llamy nie dotyczy (I, uzasadnienie jak w karcie `finemath4`). I: web 2019–2023 może zawierać tekst
  pisany przez modele.
- Bramka „można TRENOWAĆ”: **TAK** — wyjątek TDM art. 4 dyr. 2019/790 dla tekstów, ODC-By dla kompilacji.
  Takedown: po `url` (V: obecny w 100% wierszy shardu 0) albo po `WARC-Record-ID`/`WARC-Target-URI` z
  `metadata.WARC_HEADER` (V); osobnych kolumn `warc_filename`/`offset` jak w FineMath-4+ BRAK. Warunek:
  honorowanie opt-outu TDM, NIE SPRAWDZONEGO.
- Bramka „można ZGŁOSIĆ”: **NIEROZSTRZYGNIĘTY** — licencja per dokument nieznana, część domen z SA lub
  restrykcyjnym regulaminem (V w próbce: gradesaver, byjus, geeksforgeeks, coursehero-podobne casestudyhelp),
  opt-out TDM niesprawdzony.

## 3. Zawartość

- V (shard 0, 196 757 wierszy): pola `url`, `metadata` (JSON InfiMM: `WARC_HEADER`, `snap`, `math_prob`,
  `math_prob_llama3`, `ft_lang_label`, `nsfw_num_words`, `pos_list`, `im_url_duplicate_count` itd.), `score`,
  `int_score` (4: 168 597, 5: 28 160), `token_count` (tokeny Llamy), `char_count`, `text`. Brak `id`, `crawl`,
  `snapshot_type`, `language_score` jako kolumn.
- V (shard 0): top domeny answers.everydaycalculation.com 8 060, math.stackexchange.com 7 641, socratic.org 6 799,
  metanumbers.com 4 010, physicsforums.com 3 968, gradesaver.com 3 344, geeksforgeeks.org 1 696,
  artofproblemsolving.com 1 484, physics.stackexchange.com 1 425, byjus.com 1 403, convertoctopus.com 1 392,
  jiskha.com 1 335. I: everydaycalculation/metanumbers/convertoctopus to szablonowe strony generowane programowo
  (kalkulatory) — kandydaci do wykluczenia lub mocnego dedupu.
- V (20 tys. wierszy): zrzuty CC 2019–2023 (najczęściej 2023-40, 2021-43, 2022-40), zgodnie z kartą InfiMM.
- V: obrazki usunięte z `text` — `![` w 18, `<img` w 13 z 20 000 dokumentów; ślad pozycji obrazków zostaje w
  `metadata.pos_list`/`im_url_duplicate_count`. Notacja z obrazków ginie (karta finemath). V: CJK (≥5 znaków
  ciągiem) w 43 z 20 000 — filtr angielski skuteczny, resztki chińskiego InfiMM marginalne.

## 4. Skala i dostęp

- V (karta): 6,3 mln dokumentów, 8,5 mld tokenów Llamy; `num_examples` 6 296 212, download_size 19 234 328 998 B.
- V (API): 32 pliki po ~600 MB (598,4–603,9 MB); shard 0 = 600 695 333 B, sha256
  `8dae840ed1921e42a7e36dfa4d44db96af81f1de9bfaeddab0b1daf6c71c09a3` (zgodny z LFS oid), 196 757 wierszy,
  suma `token_count` 265 752 882 (~1 351 tok./dok.), 951 307 579 znaków. I: ×32 ≈ 8,5 mld — zgodne z kartą.
- V: duplikaty url wewnątrz shardu: 193 716 unikalnych na 196 757 (1,5% powtórzeń).
- V: dostęp bez bramki, `resolve/<rewizja>/...`.

## 5. Ryzyka

- Nakładanie z FineMath-4+ (V pomiar): 7 940 z 196 757 url shardu 0 (4,0%) występuje dokładnie w 4 pełnych shardach
  FineMath-4+ z `dane/finemath4/robocze/pobrania/lok` (416 657 url, 4/64 zbioru); po normalizacji (bez schematu,
  `www.`, końcowego `/`) 8 972 (4,6%). I: ekstrapolacja ×16 ≈ 65–73% url InfiWebMath-4+ jest też w FineMath-4+
  (zakłada losowy podział na shardy; górna wartość z normalizacji). Realny przyrost unikalnych stron ≈ 27–35%
  (~2,3–3 mld tokenów Llamy), o ile treść tych samych url jest bliska (zrzuty różnią się). Karta finemath (V): dedup
  między FineMath i InfiWebMath *obniżył* wynik — dla nas dedup i tak obowiązkowy (budżet unikalnych tokenów).
- Dekontaminacja: V (karta finemath) 13-gramy wobec GSM8K, MATH, MMLU, ARC (zakładamy, że dotyczy też configów
  infiwebmath — I); InfiMM sam nie deklaruje dekontaminacji (V karta). Nie obejmuje ~60 testów Fabryki — nasze
  13-gramy obowiązkowe.
- PII: V e-mail (regex) w 277 z 20 000 dokumentów (1,4%); InfiMM deklaruje filtr NSFW, nie PII (V karta) →
  maskowanie e-maili w naszym filtrze. `WARC_HEADER` zawiera adres IP serwera (nie osoby) — wyrzucić z metadanych.
- Opt-out TDM top domen: NIE SPRAWDZONE.
- Szablonowe strony kalkulatorów (I) zawyżają skalę bez treści matematycznej rozumowania.

## 6. Nowość

- V (karta `finemath4`): 1.07 `en_mix` zawiera FineMath i open-web-math; 1.09 = FineWeb-Edu EN + PL, bez osobnej
  matematyki web. InfiWebMath w historii Slayera nie występuje (I: brak w opisach 1.07/1.09 i w karcie finemath4;
  `REJESTR_DATASETOW.md` nie przeszukany pod tym kątem).
- I: duża część stron pokrywa się z FineMath-4+ (wyżej) i z open-web-math (te same domeny: math.stackexchange,
  physicsforums); nowe są głównie zrzuty 2019–2023 i domeny spoza potoku OpenWebMath. Przyrost oceniać po dedupie
  url + MinHash wobec FineMath-4+ i en_mix 1.07.
- V (karta finemath): InfiWebMath-4+ słabszy od FineMath-4+ na GSM8K i MATH; mieszanka 50/50 3+ dorównuje FineMath-3+.

## Nie sprawdzone

- Opt-out TDM i regulaminy top domen.
- Treść `finemath_contamination_report` dla configów infiwebmath (czy jest osobny katalog i ile usunięto).
- Treść SmolLM2 §3.3 i pracy 2409.12568 poza kartami (opis potoku przyjęty z kart).
- Nakładanie url na pełnym FineMath-4+ (zmierzone 4/64, reszta ekstrapolacja) i nakładanie treści (MinHash/13-gram)
  wobec FineMath-4+, open-web-math i en_mix 1.07.
- Rozkład domen, e-maili i zrzutów poza shardem 0.
- Współczynnik tokenów v6 / Llama na tym zbiorze.
