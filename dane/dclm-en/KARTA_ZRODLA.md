# Karta źródła: DCLM-baseline 1.0 (EN) dla Slayera 1B

Zapisana 14.11.2026 przed pobraniem próbki. Progi dnia 1: `skrypty/preregistracja.json` (zapisane przed liczeniem).
Rezerwacja: https://github.com/slayerlabs/benchmarks-fabryka-ai/issues/197

Cel: dane EN pod testy, które przy 1B reagują na dane (HellaSwag, PIQA, ARC-C, WinoGrande), jako
uzupełnienie FineWeb-Edu; docelowo co najmniej 5 mld tokenów v6 po filtrach.

## 1. Identyfikacja

- URL: https://huggingface.co/datasets/mlfoundations/dclm-baseline-1.0, rewizja
  `a3b142c183aebe5af344955ae20836eb34dcf69b` (pliki `jsonl.zst`).
- Czytana kopia: https://huggingface.co/datasets/mlfoundations/dclm-baseline-1.0-parquet, rewizja
  `817d6752765f6a41261085171dd546b104f60626`; karta: „identical copy … mapped to a parquet format”,
  te same ścieżki shardów. Powód: w środowisku brak dekodera zstd. Zgodność liczby dokumentów kopii z
  `jsonl.zst` NIE sprawdzona. Kopia NIE jest identyczna co do listy plików: ma 27 938 plików, o 100
  więcej (wszystkie 27 838 nazw z `jsonl.zst` są w kopii; nadmiarowe zaczynają się od
  `global-shard_03_of_10/local-shard_1_of_10/shard_00000041`). Pełna budowa bierze tylko pliki
  obecne w repo kanonicznym; pliki próbki dnia 1 są wśród nich.
- Wydawca: zespół DataComp-LM (mlfoundations), praca Li i in. 2024, https://arxiv.org/abs/2406.11794,
  kod https://github.com/mlfoundations/dclm.

## 2. Prawa

- Licencja zbioru: CC-BY-4.0 (karta HF). To licencja wkładu twórców zbioru, nie tekstów: teksty
  pochodzą z Common Crawl i każdy ma prawa swojego wydawcy.
- Trening: podstawą jest wyjątek TDM (art. 4 dyrektywy 2019/790), jak przy FinePDFs; ścieżka
  takedown: usunięcie dokumentu po `url`/`id` w kolejnej wersji zbioru.
- Redystrybucja: osobno od treningu. CC-BY-4.0 wymaga podania autorstwa zbioru (DCLM, cytowanie z
  karty); teksty dalej podlegają prawom wydawców i warunkom Common Crawl.
- UWAGA z karty: „intended for research use only”, „not intended for training production-ready
  models”. To zastrzeżenie celu w karcie, nie warunek licencji CC-BY-4.0; wpisane jako uwaga do
  decyzji, nie weto.
- Opt-out TDM (robots.txt, TDMRep) na próbce domen: NIE SPRAWDZONE w dniu 1.

## 3. Zawartość

- Język: angielski (filtr fastText języka w DCLM).
- Dziedzina i gatunek: ogólny web z Common Crawl (DCLM-Pool, zrzuty do 2022), po heurystykach
  RefinedWeb, dedupie filtrem Bloom i klasyfikatorze fastText trenowanym na OpenHermes 2.5 i
  r/ExplainLikeImFive (preferuje tekst instruktażowy i objaśniający).
- Pliki: `global-shard_XX_of_10/local-shard_Y_of_10/shard_NNNNNNNN_processed.{jsonl.zst,parquet}`;
  pole tekstu `text`; w kopii parquet obok `url`, `id`, `language`, `language_score`,
  `fasttext_score` (bez metadanych WARC i numeru zrzutu, które ma wersja `jsonl.zst`).

## 4. Skala i dostęp

- Karta: 4T tokenów, 3 mld dokumentów (tokenizer twórców, nie v6).
- 27 838 plików danych; plik parquet ok. 140–245 MB i 84–135 tys. dokumentów (10 plików próbki).
- Dostęp: pobranie plików z HF przez `huggingface_hub`, bez bramki.

## 5. Ryzyka

- PII: karta „[More Information Needed]”; DCLM nie opisuje usuwania danych osobowych.
- Kopie: dedup DCLM tylko wewnątrz DCLM; wobec FineWeb-Edu (też Common Crawl) i EN Slayera 1.07
  oczekiwane nakładanie, do zmierzenia.
- Treści testowe: DCLM nie usuwał tekstów testów; HellaSwag (WikiHow) i PIQA (Instructables)
  pochodzą z webu, więc domeny źródłowe i 13-gramy sprawdzamy osobno.
- Dane syntetyczne: zbiór nie zawiera generowanych tekstów z zamiaru, ale klasyfikator premiuje styl
  odpowiedzi czatowych, więc web pisany przez modele może mieć wyższy udział.
- OCR: nie dotyczy (HTML).
- Użycie w zespole: DCLM jest w miksie Ivme (model 150M) i w ocenie bpb Slayer150; dokumenty
  ewaluacji wykluczamy, nakładanie z Ivme mierzymy.

## 6. Nowość

- Opisany skład Slayera 1B (DATA_CARD 1.09: c01–c06) to FineWeb-Edu, GoLLeM web i FinePDFs-Edu;
  DCLM tam nie występuje. Skład c07–c10 nieopisany (pytanie w #197).
- ALE: DCLM jest już w historii Slayera. Karta `SlayerLab/slayer-1.07-pretrain` (6a337bbf) opisuje
  `en_mix/` jako „FineWeb-Edu, FineMath, open-web-math, DCLM-baseline (subset)” z
  `SlayerLab/minimal-en-corpus-5b`; ten zbiór ma 577 998 dokumentów `dclm-baseline` w treningu.
  Dedup wobec EN 1.07 ten zakres obejmuje. Czy en_mix 1.07 jest w 1.09: pytanie do Arka.
- Przyrost pokrycia zależy od nakładania z FineWeb-Edu i EN 1.07; zakres do weryfikacji: dedup w
  zakresach z metodologii, w tym historia modeli (dostępna tylko EN 1.07), segmenty c01–c10 i gold
  (niedostępne w dniu 1).
