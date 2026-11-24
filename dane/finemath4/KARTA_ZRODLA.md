# Karta źródła: FineMath-4+ (EN, matematyka z sieci) dla Slayera 1B

Zapisana 24.11.2026 przed pobraniem próbki. Rezerwacja: https://github.com/slayerlabs/benchmarks-fabryka-ai/issues/346

Cel: ramię B microannealu („+15% matematyki z sieci” w ramieniu 2 mld), docelowo co najmniej 0,4 mld tokenów v6
po filtrach. Oznaczenia: V = sprawdzone 2026-11-24 w podanym źródle (URL, rewizja, hash), I = wywnioskowane.

## 1. Identyfikacja

- V: URL https://huggingface.co/datasets/HuggingFaceTB/finemath, rewizja
  `e92b25a616738fe95dc186b64dfb19f9c8525594` (API `/api/datasets/HuggingFaceTB/finemath/revision/<rewizja>`:
  lastModified 2025-02-06, bez bramki dostępu). Podzbiór `finemath-4plus`, 64 pliki
  `finemath-4plus/train-000NN-of-00064.parquet`.
- V: wydawca Hugging Face (HuggingFaceTB); praca SmolLM2, Ben Allal i in. 2025, https://arxiv.org/abs/2502.02737.
- V: klasyfikator https://huggingface.co/HuggingFaceTB/finemath-classifier (rewizja
  `bd0b0e330750ccaafb16c47066f875b3fcb707c3`, licencja MIT, baza `intfloat/multilingual-e5-small`).
- V: raport dekontaminacji https://huggingface.co/datasets/HuggingFaceTB/finemath_contamination_report, rewizja
  `3dc3725bac1125fb17a12b742102b91a45198f0e` (katalogi per podzbiór, w tym `finemath-4plus/`; karta bez pola licencji).

## 2. Prawa

- V: licencja zbioru ODC-By 1.0 (karta: „Open Data Commons Attribution License (ODC-By) v1.0 … also subject to
  CommonCrawl's Terms of Use”). To licencja kompilacji (bazy), nie tekstów: każdy tekst ma prawa wydawcy strony
  (math.stackexchange CC BY-SA, fora, coursehero, jiskha itd.); w danych brak pola licencji per wiersz (V: schemat).
- I: klauzula Llamy NIE dotyczy. Llama-3.1-70B-Instruct wygenerowała tylko oceny (skala 3 i 5 pkt), na których
  wytrenowano klasyfikator (MIT); teksty w zbiorze są oryginalnymi stronami z Common Crawl, nie wyjściem Llamy.
  Licencja Llama 3.1 wiąże „Llama Materials” i wyniki (outputs) użyte do trenowania/ulepszania modelu; ocen nie
  trenujemy ani nie dystrybuujemy, a wybór dokumentów przez filtr nie czyni z tekstu „outputu”. Ryzyko szczątkowe:
  obowiązek „Built with Llama” przy redystrybucji zbioru pochodnego — dotyczy co najwyżej klasyfikatora, nie nas.
- Bramka „można TRENOWAĆ”: **TAK** — podstawą wyjątek TDM art. 4 dyr. 2019/790 (dla tekstów), ODC-By dla kompilacji;
  ścieżka takedown: usunięcie dokumentu po `url` / `warc_filename`+`warc_record_offset` w kolejnej wersji zbioru.
  Warunek: honorowanie opt-outu TDM, NIE SPRAWDZONEGO (niżej).
- Bramka „można ZGŁOSIĆ”: **NIEROZSTRZYGNIĘTY** — licencja per dokument nieznana (brak pola; ODC-By kompilacji ≠
  licencja tekstów), część domen ma licencje z SA lub regulaminy zakazujące kopiowania (I: coursehero, gradesaver),
  opt-out TDM niesprawdzony.

## 3. Zawartość

- V (karta): angielski (langid FineWeb); matematyka edukacyjna: zadania krok po kroku, fora QA, Markdown + LaTeX;
  ekstrakcja potokiem OpenWebMath (Resiliparse), MinHash-LSH, wynik klasyfikatora ≥ 4 (FineMath-4+ ⊂ FineMath-3+).
- V (shard 0, 20 000 pierwszych wierszy): top domeny math.stackexchange.com 853, physicsforums.com 835,
  mathhelpforum.com 826, jiskha.com 554, coursehero.com 414, socratic.org 403, gmatclub.com 379, gradesaver.com 297,
  nrich.maths.org 283, oeis.org 216; `snapshot_type` latest 15 733 / longest 4 267; zrzuty CC-MAIN 2013–2024
  (najczęściej 2024, 2018, 2017).
- V: pola: tekst `text`; `url`, `fetch_time`, `content_mime_type`, `warc_filename`, `warc_record_offset`,
  `warc_record_length`, `token_count` (tokeny Llamy), `char_count`, `metadata` (JSON OpenWebMath: liczniki
  znaczników matematyki), `score`, `int_score`, `crawl`, `snapshot_type`, `language`, `language_score`. Licencji
  per wiersz brak.

## 4. Skala i dostęp

- V (karta): 6 699 493 dokumentów, 9,6 mld tokenów (tokenizer Llama); download_size 18 365 184 633 B.
- V (API): 64 pliki, łącznie 18 365 184 633 B; shard 0 = 286 267 316 B, sha256
  `5d0b26114b4cf309c82a4ba8f6f45857480b27812e23a46b61b45e8bbed61fe5`, 104 680 wierszy, suma `token_count`
  149 262 381, średnio ~1 434 tok./dok. (próbka 20 tys.).
- I: 0,4 mld tokenów v6 po filtrach ≈ 3–5 shardów (BPE 32 768 daje zwykle więcej tokenów niż Llama na tekst
  angielski z LaTeX; współczynnik do zmierzenia w dniu 1). Zbiór ma ~25× zapasu.
- V: dostęp bez bramki, pobranie przez `huggingface_hub` / `resolve/<rewizja>/...`.

## 5. Ryzyka

- Dekontaminacja: V (karta) 13-gramy wobec GSM8K, MATH, MMLU, ARC; praca SmolLM2 wymienia tylko GSM8K/MATH/MMLU
  (z notatek `wplyw-1`). Nie obejmuje: MathQA, HumanEval, MBPP, GSM-Plus, GSM1k i reszty ~60 testów Fabryki — nasze
  13-gramy obowiązkowe. Zawartość raportu (liczby usuniętych) NIE przeczytana. I: GSM-Plus to perturbacje GSM8K,
  więc mogą przetrwać filtr GSM8K.
- PII: V w 324 z 20 000 dokumentów (1,6%) jest wzorzec adresu e-mail (regex, shard 0); fora (mathhelpforum,
  physicsforums, jiskha) mają nicki i podpisy. Karta nie opisuje usuwania PII → maskowanie e-maili w naszym filtrze.
- Opt-out TDM (robots.txt, TDMRep, ai.txt) dla top domen: NIE SPRAWDZONE. I: coursehero i gradesaver mają
  restrykcyjne regulaminy; kandydaci do wykluczenia domeny.
- Kopie: `snapshot_type` latest/longest — ta sama strona może wystąpić w dwóch wersjach (I, do zmierzenia
  dedupem wewnątrz zbioru); MinHash twórców jednopasmowy.
- Syntetyczne: I — web do 2024 może zawierać tekst pisany przez modele (socratic, strony z rozwiązaniami).
- OCR: nie dotyczy (HTML); V (karta) notacja z obrazków ginie.

## 6. Nowość

- V: FineMath jest już w historii Slayera: karta `SlayerLab/slayer-1.07-pretrain@6a337bbf` opisuje `en_mix` jako
  m.in. FineMath i open-web-math z `SlayerLab/minimal-en-corpus-5b`. Który podzbiór (3+/4+) i ile dokumentów —
  NIE SPRAWDZONE. REJESTR_DATASETOW.md wymienia też finemath w `SlayerLab/slayer-pl-8x3b` → `en` (wg `dataset.json`).
- I: OpenWebMath (też w 1.07) dał URL-e do FineMath, więc nakładanie z en_mix 1.07 może być znaczne (math.stackexchange,
  physicsforums są czołowymi domenami obu). Dedup wobec EN 1.07 obowiązkowy, a przyrost oceniamy dopiero po nim.
- V (opis 1.09): skład FineWeb-Edu EN, GoLLeM web, FinePDFs-Edu PL, FineWeb-2 PL — bez osobnej matematyki web.
  1.08b (niewydany) miał OpenR1-Math (syntetyczne), nie web. I: w 1.09 matematyka web jest śladowa.
- Efekt (notatki `wplyw-1`): TinyLlama 1,1B CPT 55 mld: GSM8K 3,0 → 21,1, MATH 3,1 → 11,4 (arXiv 2504.02807 Tab. 21);
  słabszy od MegaMath-Web-Pro (Core 39,0 vs 43,3), ale tekst oryginalny, nie przepisany przez Llamę.

## Nie sprawdzone

- Opt-out TDM top domen; licencje/regulaminy per domena.
- Treść raportu `finemath_contamination_report` (liczby trafień, które testy dokładnie).
- Liczba dokumentów FineMath w en_mix 1.07 i podzbiór (3+/4+); nakładanie URL/13-gram z próbką.
- Współczynnik tokenów v6 / Llama na tym zbiorze.
- Rozkład domen, e-maili i `snapshot_type` poza shardem 0 (pierwsze 20 tys. wierszy).
- Pełny tekst licencji Llama 3.1 w kontekście ocen (wniosek „nie dotyczy” = I).
