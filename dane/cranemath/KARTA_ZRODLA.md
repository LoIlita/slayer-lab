# Karta źródła: CraneMath (Dolma 3 Dolmino, ingredient 1) dla Slayera 1B

Zapisana 24.11.2026 przed pobraniem próbki (do sprawdzenia struktury pobrany jeden shard, do /tmp,
poza repo). Rezerwacja: https://github.com/slayerlabs/benchmarks-fabryka-ai/issues/346

Cel: ramię C microannealu (#175): matematyka przepisana przez model, co najmniej 0,4 mld tokenów v6
po filtrach i dedupie.

Oznaczenia: V = sprawdzone 24.11.2026 w podanym źródle (URL, rewizja, hash); I = wywnioskowane.

## 1. Identyfikacja

- V: URL https://huggingface.co/datasets/allenai/dolma3_dolmino_mix-100B-1125, rewizja
  `f23aa129fda8335ba9760057bcc1f0c02f3d068b`; bierzemy TYLKO katalog `data/ingredient1-cranemath`.
- V: 192 pliki `shard_NNNNNNNN-withid.jsonl.zst`, razem 15 134 942 534 B (API `tree` tej rewizji).
- V: wydawca Ai2 (allenai); praca Olmo 3, https://arxiv.org/abs/2512.13961, rozdz. 3.5 i dodatek
  A.3.1; przepis: https://github.com/allenai/dolma3/blob/1a9daced81670e0fa768e47fbed32af6694a1865/datasets/dolma3_dolmino_mix/cranemath/README.md
- V: pochodzenie: FineMath-4+ (`HuggingFaceTB/finemath`, 6 699 493 przykładów wg README dolma3)
  przepisany przez Qwen3-32B promptem SwallowMath (Fujii i in. 2025, arXiv 2505.02881).
- V: generator: model `Qwen/Qwen3-32B`; prompt opublikowany dosłownie w README dolma3 (wyżej,
  sekcja „Recipe”, system message). Rewizja modelu NIE opublikowana (ani w pracy, ani w README);
  nie podano też parametrów próbkowania ani trybu thinking.
- I: pole `generator` eksportu: `Qwen/Qwen3-32B@<rewizja nieznana> prompt:allenai/dolma3@1a9daced:datasets/dolma3_dolmino_mix/cranemath/README.md`.
  Aktualna rewizja HF modelu to `9216db5781bf21249d130ec9da846c4624c16137` (V), ale nie wiemy, czy
  tej użyto; nie wpisywać jej jako rewizji generatora bez potwierdzenia od Ai2.

## 2. Prawa

- V: licencja mieszanki ODC-By v1.0 (karta HF, YAML `license: odc-by`), z dopiskiem „intended for
  research and educational use” i odesłaniem do Responsible Use Guidelines (to zastrzeżenie celu,
  nie warunek ODC-By; uwaga do decyzji, nie weto, jak przy DCLM).
- V: licencja generatora: Qwen3-32B na Apache-2.0 (API HF `cardData.license`); Apache-2.0 nie
  nakłada ograniczeń na wyjścia (brak klauzuli nazwy ani zakazu trenowania innych modeli). To był
  powód Ai2: SwallowMath z Llamy wymagałby „Llama” w nazwie modelu (praca, A.3.1).
- V: licencja źródła: FineMath ODC-By (notatka `wplyw-0-podsumowanie`, karta FineMath); to licencja
  kompilacji, teksty z Common Crawl mają prawa wydawców. CraneMath to utwory zależne od tych tekstów
  (przepisanie, nie nowy tekst).
- V: każdy wiersz ma `metadata.url` oryginału FineMath i `metadata.warc_*` (shard 0: 36 120/36 120).

**Bramka „można TRENOWAĆ”: TAK.** Podstawa: wyjątek TDM art. 4 dyr. 2019/790 dla tekstów
źródłowych z sieci (ODC-By kompilacji + Apache-2.0 generatora nie blokują). Ścieżka takedown:
usunięcie wiersza po `metadata.url` (i `id`) w kolejnej wersji; URL jest w każdym wierszu.
Zastrzeżenie: opt-out TDM (robots.txt/TDMRep) domen źródłowych NIE sprawdzony.

**Bramka „można ZGŁOSIĆ”: NIEROZSTRZYGNIĘTY.** Brak licencji per dokument: ODC-By dotyczy
kompilacji, nie tekstów; teksty to przepisania stron o nieznanych licencjach, opt-out TDM niesprawdzony.
Zgłoszenie (redystrybucja tekstów) wymagałoby licencji per URL; tego zbiór nie daje.

## 3. Zawartość

- V: język angielski (`metadata.language` = `en`).
- V: przepisane strony matematyczne: problem + rozwiązanie w Markdown/LaTeX, bez nagłówków, stopek,
  dat (prompt SwallowMath); prompt każe też „dodać szczegóły obliczeń krok po kroku”, więc model
  dopisuje treść, nie tylko tnie.
- V: pola wiersza (shard 0): `id` (np. `shard_00000000.jsonl.gz_1`), `text` (tekst przepisany),
  `metadata` (obiekt): `url`, `original_text` (pełny tekst FineMath przed przepisaniem), `crawl`
  (np. `CC-MAIN-2021-49`), `warc_filename`, `warc_record_offset`, `warc_record_length`,
  `fetch_time`, `score`, `int_score` (klasyfikator FineMath, ≥4), `token_count`, `char_count`,
  `language`, `language_score`, `content_mime_type`, `snapshot_type`, `metadata` (pusty).
  Pól `source`, `version`, `added`, `created` z YAML karty w tym katalogu NIE ma. Licencji per wiersz
  brak.
- V: `derived_from`: `metadata.url` + `metadata.warc_filename`/`offset` identyfikują dokument FineMath
  jednoznacznie; `id` to numer linii w shardzie źródłowym Ai2, nie id FineMath.
- V (shard 0): **2 059 z 36 120 wierszy (5,7%) to surowy ślad rozumowania Qwen3**: `text` zaczyna
  się od `<think>` i nie ma `</think>` (ucięta generacja, np. „Okay, let's see… But wait, that doesn't
  seem right”). Filtr obowiązkowy: odrzucić wiersze z `<think>`.

## 4. Skala i dostęp

- V: praca (tab. rozdz. 3.5): CraneMath 5,62 mld tok., 6,55 mln dok. w puli 2T; w mieszance 100B
  5,62 mld tok. i 7,24 mln dok. README dolma3: 6 553 181 dok., 5,625 mld tok. (tokenizer Olmo 3, nie v6).
- V: shard 0: 94 334 019 B skompresowany, sha256
  `77f8fb0779d86036ae253528eead6d8e160c920acab9f259109706b0b06333d6`, 36 120 wierszy, 97 017 066 znaków
  `text` (176 734 597 znaków `original_text`); 36 107 różnych URL (13 powtórzonych), 36 083 różnych `text`.
- I: 192 shardy × ~36 tys. ≈ 6,9 mln wierszy (między 6,55 a 7,24 mln z pracy; rozbieżność
  nieustalona). ~97 mln znaków/shard ≈ 18,6 mld znaków ≈ 4–5 mld tokenów v6 przy ~4 zn./tok.;
  po odrzuceniu ~5,7% `<think>` i dedupie cel 0,4 mld osiąga ~10–15 shardów.
- V: dostęp bez bramki (pobranie `resolve/<rewizja>/…` bez tokenu). Format `jsonl.zst` wymaga
  dekodera zstd (użyto `zstandard` w venv w /tmp).

## 5. Ryzyka

- Halucynacje (I, częściowo V): prompt każe uzupełniać „niepełne” rozwiązania; Qwen3 może dopisać
  błędne kroki lub zmienić wynik. Ai2 nie opisuje weryfikacji poprawności. Ucięte ślady `<think>`
  (V, 5,7% shardu 0) zawierają wahania i błędne próby. Kontrola: losowa ocena ręczna/sędzią N
  wierszy `text` vs `metadata.original_text` (zgodność wyniku końcowego).
- Kontaminacja odziedziczona po FineMath (I): FineMath to web matematyczny, w którym krążą zadania
  GSM8K/MATH/MMLU; przepisanie może zatrzeć dosłowne 13-gramy przy zachowaniu treści zadania.
  Sprawdzamy 13-gramy na `text` I na `metadata.original_text` wobec ~60 testów + GSM-Plus, GSM1k.
- Dekontaminacja Olmo 3 (V): pakiet `allenai/decon` (n-gramy z krokiem + rozszerzanie klastra) wobec
  benchmarków OLMES, stosowany do danych midtrainingu; praca: „extent and impact … variable”, większość
  skażeń w Flan i Nemotron. Czy decon przepuszczono przed czy po zapisie tego katalogu i ile wierszy
  usunięto z CraneMath: NIE sprawdzone. Nie zastępuje naszej dekontaminacji.
- PII (I): przepisanie usuwa nagłówki/stopki, ale nazwiska autorów postów mogą zostać; `original_text`
  ma pełny surowy tekst (nie trafia do treningu).
- Dane syntetyczne: 100% (V); styl Qwen3 „gadatliwy” (praca: 5,6 mld vs 2,3 mld SwallowMath).

## 6. Nowość

- V (fakty historii): Slayer 1.07 miał w `en_mix` FineMath i open-web-math
  (`SlayerLab/slayer-1.07-pretrain@6a337bbf`, z `SlayerLab/minimal-en-corpus-5b`). CraneMath to
  przepisania FineMath-4+, więc część dokumentów źródłowych Slayer już widział w surowej postaci.
  Dedup: po `metadata.url` i po `original_text` wobec EN 1.07 (nie tylko po `text`, bo przepisanie
  zmienia n-gramy).
- V: skład 1.09 (FineWeb-Edu EN, GoLLeM web, FinePDFs-Edu PL, FineWeb-2 PL) nie ma matematyki
  przepisanej; 1.08b (niewydany) miał OpenR1-Math i OpenThoughts (ślady rozumowania, inny format).
  Forma „oczyszczone zadanie + rozwiązanie krok po kroku” jest dla Slayera nowa (I).
- V (dowód efektu, notatka `wplyw-2`): microanneal Olmo 3 4,34 mld tok. (50/50 z miksem pretreningu,
  baza po 6T tok.): MATH +18,5, GSM8K +27,4, MMLU ≈ 0 (praca A.3.1). Ramię C mierzy to samo przy 1B
  wobec ramienia B (surowy FineMath-4+), więc nakładanie URL B/C trzeba raportować.
- Dedup planowany: wobec EN 1.07, walidacji Fabryki, wewnątrz zbioru (V: 13 powtórzonych URL w
  shardzie 0), 13-gramy wobec ~60 testów (GSM8K, MATH, MMLU, MathQA, HumanEval, MBPP…) + GSM-Plus, GSM1k.

## Nie sprawdzone

- Rewizja Qwen3-32B użyta do generacji, parametry próbkowania, tryb thinking.
- Czy decon Ai2 objął ten katalog i ile usunął.
- Udział `<think>` i duplikatów w pozostałych 191 shardach (sprawdzony tylko shard 0).
- Dokładna liczba wierszy katalogu (6,55 vs 7,24 mln vs ~6,9 mln szacunku) i tokeny v6.
- Opt-out TDM (robots.txt, TDMRep) domen źródłowych.
- Poprawność matematyczna przepisanych rozwiązań (brak pomiaru).
- Nakładanie URL z FineMath w EN 1.07 i z ramieniem B.
