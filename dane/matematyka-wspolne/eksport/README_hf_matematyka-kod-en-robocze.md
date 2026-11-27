---
license: other
language:
- en
pretty_name: Matematyka i kod (EN) dla Slayera, robocze
task_categories:
- text-generation
configs:
- config_name: default
  data_files:
  - split: train
    path: data/*/*.parquet
- config_name: finemath_4plus_en
  data_files:
  - split: train
    path: data/finemath_4plus_en_p*/*.parquet
- config_name: stack_edu_python
  data_files:
  - split: train
    path: data/stack_edu_python_p*/*.parquet
- config_name: infiwebmath_4plus_en
  data_files:
  - split: train
    path: data/infiwebmath_4plus_en_p*/*.parquet
- config_name: arxiv_math_en
  data_files:
  - split: train
    path: data/arxiv_math_en_p*/*.parquet
- config_name: stackexchange_math
  data_files:
  - split: train
    path: data/stackexchange_math_p*/*.parquet
- config_name: formal_math
  data_files:
  - split: train
    path: data/formal_math_p*/*.parquet
- config_name: oeis_en
  data_files:
  - split: train
    path: data/oeis_en_p*/*.parquet
- config_name: wikipedia_math_en
  data_files:
  - split: train
    path: data/wikipedia_math_en_p*/*.parquet
- config_name: open_textbooks_math_en
  data_files:
  - split: train
    path: data/open_textbooks_math_en_p*/*.parquet
- config_name: mikroanneal
  data_files:
  - split: train
    path: mikroanneal/*/*.parquet
---

# Matematyka i kod (EN) dla Slayera, wersja robocza

Zbiór angielskiej matematyki, logiki i kodu do (kontynuacji) pretreningu Slayera 1B i kolejnych modeli: **11 810 525
dokumentów, 17 018 612 820 tokenów v6** w dwóch postaciach — tekst (`data/`, dla dowolnego modelu i tokenizera) i ten sam
tekst stokenizowany tokenizerem Slayera v6 (`tokenized/slayer-v6/`, format trenera). Budowa: issue
[#346](https://github.com/slayerlabs/benchmarks-fabryka-ai/issues/346) (części 1–2) i
[#357](https://github.com/slayerlabs/benchmarks-fabryka-ai/issues/357) (część 3). Przepis, preregistracje, dzienniki,
datasheety i kody: [`LoIlita/slayer-lab`](https://github.com/LoIlita/slayer-lab), gałąź `dane/matematyka`, katalogi
`dane/<źródło>` (`finemath4`, `stackedu`, `infiwebmath4`, `arxiv_mat`, `stackexchange_mat`, `formalna`, `oeis`,
`wiki_mat`, `podreczniki_mat`) i `dane/matematyka-wspolne`.

Repo jest **gated** (dostęp ręczny): pobranie wymaga zalogowania i akceptacji przez właścicielkę; anonimowo HTTP 401.

## `data/`: tekst (źródło prawdy)

| źródło (klucz) | katalogi | dokumenty | tokeny v6 | licencja tekstu |
|---|---|---|---|---|
| FineMath-4+ (`finemath_4plus_en`; `HuggingFaceTB/finemath@e92b25a6`, cała pula po filtrach) | `finemath_4plus_en_p01..p07` | 4 763 307 | 6 950 748 498 | ODC-By (kompilacja); teksty stron: wyjątek TDM (art. 4 dyrektywy 2019/790) |
| Stack-Edu Python (`stack_edu_python`; `common-pile/stackv2_edu_filtered@c354dbe8`, pliki 0073–0084) | `stack_edu_python_p01..p05` | 3 516 755 | 4 815 032 734 | licencja per plik z listy Blue Oak (MIT 70%, Apache-2.0 16%, BSD 9%, …) |
| arXiv: matematyka, statystyka, logika, teoria informatyki (`arxiv_math_en`; `common-pile/arxiv_papers@963fe980`, `common-pile/arxiv_abstracts@828e35d1`) | `arxiv_math_en_p01..p08` | 599 703 | 2 425 618 929 | pełne teksty: CC BY 4.0 / 3.0, CC BY-SA 4.0, CC0, domena publiczna (per praca; domyślna licencja arXiv wykluczona); abstrakty: CC0 |
| StackExchange: math, mathoverflow, cstheory, matheducators, proofassistants, stats, cs, scicomp, or (`stackexchange_math`; `common-pile/stackexchange@5ec3aa2e`, pytania sprzed 2022-12-01) | `stackexchange_math_p01` | 1 614 905 | 1 297 166 546 | CC BY-SA (wersja per post, autorzy) |
| InfiWebMath-4+ (`infiwebmath_4plus_en`; `HuggingFaceTB/finemath@e92b25a6`, strony spoza FineMath-4+) | `infiwebmath_4plus_en_p01` | 1 025 440 | 1 138 599 522 | ODC-By (kompilacja); teksty stron: wyjątek TDM |
| Matematyka formalna: Lean mathlib4, Isabelle AFP, HOL Light, Metamath set.mm, Rocq, math-comp, UniMath, Agda, Stacks (`formal_math`; rewizje sprzed commitów z AI) | `formal_math_p01` | 20 390 | 208 104 938 | per plik: Apache-2.0, BSD, MIT, LGPL, CC0, GFDL, CeCILL-B |
| OEIS (`oeis_en`; `oeis/oeisdata@976b0c73`, wpisy jako tekst, bez e-maili) | `oeis_en_p01` | 260 277 | 153 731 738 | CC BY-SA 4.0 |
| Wikipedia EN i Wikibooks, artykuły matematyczne (`wikipedia_math_en`; `common-pile/wikimedia@781b263a`) | `wikipedia_math_en_p01` | 6 762 | 19 734 493 | CC BY-SA 4.0 |
| Otwarte podręczniki matematyki i statystyki: LibreTexts, PressBooks (`open_textbooks_math_en`; Common Pile; rozdziały z OpenStax wyłączone) | `open_textbooks_math_en_p01` | 2 986 | 9 875 422 | per wiersz: CC BY 4.0 / 3.0, CC BY-SA 4.0 / 3.0, GFDL-1.3, domena publiczna (bez NC/ND) |
| **razem** | 26 katalogów | **11 810 525** | **17 018 612 820** | |

Tokeny v6 = tokeny tekstu tokenizerem Slayera v6 + 1 token `<|endoftext|>` na dokument (dokładnie liczba tokenów
w `tokenized/slayer-v6/`). `token_count` w wierszach parquetu liczy tokenizer repo zgłoszeń (cl100k), nie v6.
Części `pNN` to rozłączne kawałki jednej puli po filtrach, w kolejności puli.

Schemat wiersza (repo zgłoszeń zespołu `SlayerLab/dataset-team-submissions`): `id`, `text`, `source`, `added`,
`created`, `token_count`, `license` (licencja TEGO wiersza), `author` (atrybucja), `language`, `text_origin`,
`generator`, `derived_from`. Każdy katalog ma datasheet `<klucz>.md` (źródło, prawa, filtry, przegląd, dane osobowe)
i `<klucz>.stats.json`.

```python
from datasets import load_dataset
ds = load_dataset("Lolita67/matematyka-kod-en-robocze", "arxiv_math_en", split="train")  # jedno źródło
ds = load_dataset("Lolita67/matematyka-kod-en-robocze", split="train")  # wszystko z data/ (config default)
```

## `tokenized/slayer-v6/`: wersja dla trenera Slayera

Dla każdego katalogu `data/<k>/` są `tokenized/slayer-v6/<k>.bin` i `<k>.json`. Format (`wygaszanie/dane.py`,
flaga `--dtype uint16`): płaski plik `uint16`, przed każdym dokumentem token 0 (`<|endoftext|>`), dokumenty
w kolejności wierszy parquetu, bez tasowania (trener losuje okna). `<k>.json`: `dokumenty` (= liczba wierszy
parquetu), `tokeny`, `bin_sha256`, `zrodlo_sha256` (sha256 parquetu z `data/`), `tokenizer_sha256`
(`0640d3bd…815dd`), `slownik`. Inny tokenizer = ponowna tokenizacja tekstu z `data/` skryptem
`dane/matematyka-wspolne/skrypty/tokenizuj_hf.py`.

```python
import numpy as np
from huggingface_hub import hf_hub_download
p = hf_hub_download("Lolita67/matematyka-kod-en-robocze", "tokenized/slayer-v6/arxiv_math_en_p01.bin", repo_type="dataset")
tokens = np.memmap(p, dtype=np.uint16, mode="r")
```

## Filtry i kontrola

Każde źródło ma kartę źródła i preregistrację reguł zapisane przed budową puli; zmiany po wynikach tylko jako datowane
aneksy przed eksportem. Filtry: 13-gramy ok. 60 testów Fabryki + GSM-Plus, GSM1k (testy matematyki i kodu ściśle),
zbiory walidacyjne Fabryki, domeny testów, PII (e-mail, telefon, IP: dokument usuwany albo e-mail maskowany `[PII]`,
wg źródła), sekrety i hasła w kodzie, mojibake, za krótkie teksty, dedup wewnątrz źródła i między źródłami
(FineMath-4+, InfiWebMath-4+, StackExchange), dedup wobec Slayera 1.07 EN, slayer-pl-8x3b EN, english-technical-1b
i url FineWeb-Edu 1.09 (źródła WWW). Kontrola: dwóch niezależnych recenzentów na próbce (100 odrzuconych na powód +
300 zachowanych, pełne teksty), progi: PII i testy 0/300 w zachowanych, śmieci ≤ 10%; `check.py` repo zgłoszeń
i test kontraktowy na każdej części; sha256 każdego parquetu zgodny z LFS.

Znane cechy: FineMath-4+ i InfiWebMath-4+ mają ok. 9–10% śmieci (spam SEO, strony bez wzorów) jako cechę źródła
(filtr jakości nie nałożony). arXiv: artefakty konwersji LaTeXML/Trafilatura (sklejone znaczniki przypisów, `~{}`,
`[?]`), wzory w `$…$`; e-maile autorów zamaskowane `[PII]`. Pozostałe źródła: 0–4% śmieci w przeglądzie.

## Kontrola jakości (27.11.2026)

Kontrola końcowa gotowych plików (skrypt + niezależne wywołania modelu; wynik w `dane/matematyka-wspolne/wyniki/kontrola_koncowa.json`):

- 26/26 części `data/` ma bliźniaka w `tokenized/slayer-v6/`: liczba dokumentów = liczba wierszy parquetu, `zrodlo_sha256` = sha256 pliku w repo.
- Kolumna `license` policzona we wszystkich wierszach: 0 wartości NC, ND albo nieznanych.
- Repo gated (ręczna akceptacja), pobranie anonimowe: 401.
- 50 losowych dokumentów z każdego źródła przeczytanych pod kątem śmieci i danych osobowych:

| źródło | śmieci | wątpliwe | dane osobowe |
|---|---|---|---|
| FineMath-4+ | 3/50 | 15 | 0/50 |
| InfiWebMath-4+ | 2/50 | 14 | 0/50 |
| Stack-Edu Python | 1/50 | 1 | 1/50 (zaciemniony e-mail w nagłówku licencji pliku) |
| arXiv | 0/50 | 1 | 0/50 |
| StackExchange | 0/50 | 1 | 0/50 |
| matematyka formalna | 0/50 | 0 | 0/50 |
| OEIS | 0/50 | 0 | 0/50 |
| Wikipedia | 0/50 | 0 | 0/50 |
| podręczniki | 1/50 | 8 | 0/50 |

## Licencje i użycie komercyjne

Wszystkie licencje dopuszczają trening modelu sprzedawanego komercyjnie; brak NC/ND. Copyleft (CC BY-SA, LGPL, GFDL)
dotyczy dalszego udostępniania samych danych (atrybucja w `author`/`id`, ta sama licencja). FineMath-4+
i InfiWebMath-4+ nie mają licencji per dokument (podstawa: wyjątek TDM, status `held_for_review`). StackExchange:
platforma od 2024 r. deklaruje `ai-train=no`, trening opiera się na licencji autorów (CC BY-SA), jak w Common Pile;
status `held_for_review`, ryzyko w datasheecie. Odrzucone: prace arXiv na licencji domyślnej (regulamin pobierania
arXiv dopuszcza tylko użytek osobisty i badawczy), FineMath-3+ (19–23% śmieci), UltraData-Math L3 (tekst z Llamy).

## `mikroanneal/`: część 1 (ramiona microannealu)

`finemath_4plus_en` (ramię B, 266 351 dok.), `cranemath_en` (ramię C, 510 129 dok., FineMath-4+ przepisany przez
Qwen3-32B), `stack_edu_python` (ramię D, 180 275 plików). **FineMath-4+ i Stack-Edu z części 1 są podzbiorami
`data/`**: do treningu bierz `data/` ALBO ramię z `mikroanneal/`, nigdy oba naraz. CraneMath nie ma wersji w `data/`
ani w `tokenized/`.

## Takedown

Po `id` (FineMath/InfiWebMath: plik WARC i offset albo WARC-Record-ID oraz url; Stack-Edu: id blobu Software Heritage
i repozytorium; arXiv: `arXiv:<id>` / `arXiv-abs:<id>`; pozostałe: id u źródła).
