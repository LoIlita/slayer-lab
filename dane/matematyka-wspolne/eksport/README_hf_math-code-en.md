---
license: other
language:
- en
pretty_name: Math & Code (English)
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
- config_name: arxiv_math_en
  data_files:
  - split: train
    path: data/arxiv_math_en_p*/*.parquet
- config_name: stackexchange_math
  data_files:
  - split: train
    path: data/stackexchange_math_p*/*.parquet
- config_name: infiwebmath_4plus_en
  data_files:
  - split: train
    path: data/infiwebmath_4plus_en_p*/*.parquet
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

# Math & Code (English)

English mathematics, mathematical logic and Python code for (continued) pre-training of language models:
**11 810 524 documents, 17 018 594 621 tokens** (Slayer v6 tokenizer). Every document is available as text
(`data/`, for any model and tokenizer) and pre-tokenized for the Slayer trainer (`tokenized/slayer-v6/`).
Built by SlayerLab (issues [#346](https://github.com/slayerlabs/benchmarks-fabryka-ai/issues/346),
[#357](https://github.com/slayerlabs/benchmarks-fabryka-ai/issues/357)); source cards, preregistered filtering rules,
build journals and code: [`LoIlita/slayer-lab`](https://github.com/LoIlita/slayer-lab), branch `dane/matematyka`,
directories `dane/<source>` and `dane/matematyka-wspolne`.

Access is gated (manual approval).

## Contents

| source (config) | parts | documents | tokens (v6) | licence of the text |
|---|---|---|---|---|
| FineMath-4+ web pages with mathematics (`finemath_4plus_en`; `HuggingFaceTB/finemath@e92b25a6`) | 7 | 4 763 307 | 6 950 748 498 | ODC-By (compilation); page text used under the EU text-and-data-mining exception (Art. 4 DSM Directive) |
| Stack-Edu Python files (`stack_edu_python`; `common-pile/stackv2_edu_filtered@c354dbe8`, files 0073–0084) | 5 | 3 516 754 | 4 815 014 562 | per file, permissive licences only (Blue Oak list: MIT, Apache-2.0, BSD, …) |
| arXiv mathematics, statistics, logic, theoretical CS: openly licensed full texts + abstracts (`arxiv_math_en`; `common-pile/arxiv_papers@963fe980`, `common-pile/arxiv_abstracts@828e35d1`) | 8 | 599 703 | 2 425 618 929 | full texts CC BY 4.0 / 3.0, CC BY-SA 4.0, CC0, public domain (arXiv default licence excluded); abstracts CC0 |
| StackExchange math, MathOverflow, cstheory, stats, cs, scicomp, … (`stackexchange_math`; `common-pile/stackexchange@5ec3aa2e`, questions before 2022-12-01) | 1 | 1 614 905 | 1 297 166 519 | CC BY-SA (per post) |
| InfiWebMath-4+ web pages not in FineMath-4+ (`infiwebmath_4plus_en`; `HuggingFaceTB/finemath@e92b25a6`) | 1 | 1 025 440 | 1 138 599 522 | ODC-By (compilation); page text under the TDM exception |
| Formal mathematics: Lean mathlib4, Isabelle AFP, HOL Light, Metamath, Rocq, math-comp, UniMath, Agda, Stacks (`formal_math`; revisions before AI-assisted commits) | 1 | 20 390 | 208 104 938 | per file: Apache-2.0, BSD, MIT, LGPL, CC0, GFDL, CeCILL-B |
| OEIS sequences as text (`oeis_en`; `oeis/oeisdata@976b0c73`) | 1 | 260 277 | 153 731 738 | CC BY-SA 4.0 |
| Wikipedia and Wikibooks mathematics articles (`wikipedia_math_en`; `common-pile/wikimedia@781b263a`) | 1 | 6 762 | 19 734 493 | CC BY-SA 4.0 |
| Open mathematics and statistics textbooks: LibreTexts, PressBooks (`open_textbooks_math_en`; OpenStax-derived chapters excluded) | 1 | 2 986 | 9 875 422 | per row: CC BY 4.0 / 3.0, CC BY-SA 4.0 / 3.0, GFDL-1.3, public domain |
| **total** | 26 | **11 810 524** | **17 018 594 621** | |

Tokens (v6) = tokens of the text plus one `<|endoftext|>` per document, exactly as stored in `tokenized/slayer-v6/`.
Parts `pNN` are disjoint slices of one filtered pool per source, in pool order. Every part directory has a datasheet
`<part>.md` (source, rights, filters, review, personal data) and `<part>.stats.json`.

## Formats

**Text (`data/<part>/<part>.parquet`).** Row schema of the SlayerLab dataset-team submissions repo: `id`, `text`,
`source`, `added`, `created`, `token_count` (cl100k count, not v6), `license` (licence of this row), `author`
(attribution), `language`, `text_origin`, `generator`, `derived_from`.

```python
from datasets import load_dataset
ds = load_dataset("Lolita67/math-code-en", "arxiv_math_en", split="train")  # one source
ds = load_dataset("Lolita67/math-code-en", split="train")                   # everything in data/
```

**Tokenized (`tokenized/slayer-v6/<part>.bin` + `<part>.json`).** Flat `uint16` array; token 0 (`<|endoftext|>`)
before every document; documents in parquet row order, not shuffled. The `.json` holds `dokumenty` (= parquet rows),
`tokeny`, `bin_sha256`, `zrodlo_sha256` (sha256 of the source parquet), `tokenizer_sha256`. For another tokenizer,
re-tokenize the text (`dane/matematyka-wspolne/skrypty/tokenizuj_hf.py`).

```python
import numpy as np
from huggingface_hub import hf_hub_download
p = hf_hub_download("Lolita67/math-code-en", "tokenized/slayer-v6/arxiv_math_en_p01.bin", repo_type="dataset")
tokens = np.memmap(p, dtype=np.uint16, mode="r")
```

## How it was built

For every source a source card and a preregistration of the rules were written before the pool was built; rule
changes after seeing results were recorded as dated annexes before export. Filters:

- overlap with ~60 evaluation benchmarks (13-grams; strict for maths and code tests: MATH, GSM8K, GSM-Plus, GSM1k,
  MMLU, MathQA, BBH, HumanEval, MBPP) and with Fabryka validation sets, benchmark-hosting domains;
- personal data: documents with phone numbers or IP addresses dropped; e-mail addresses dropped or masked as `[PII]`
  (including obfuscated forms such as `name [at] domain dot com`); secrets and passwords in code;
- mojibake, too-short texts, licence filters (`int_score ≥ 3` for Stack-Edu);
- deduplication within each source and across sources (FineMath-4+, InfiWebMath-4+, StackExchange), and against
  Slayer 1.07 English data, slayer-pl-8x3b English, english-technical-1b and FineWeb-Edu 1.09 urls.

Each source was reviewed on a sample (100 dropped documents per reason, 300 kept documents, two independent
reviewers; thresholds: personal data and benchmark items 0/300, junk ≤ 10%), checked with the submissions repo's
`check.py` and contract tests; parquet sha256 matches the repo LFS objects.

## Quality control (2026-11-27)

Final check of the published files (`dane/matematyka-wspolne/wyniki/kontrola_koncowa.json`):

- 26/26 text parts have a tokenized twin: document count = parquet rows, `zrodlo_sha256` = sha256 of the parquet.
- The `license` column counted over all rows: no NC, ND or unknown values.
- Gated; anonymous download returns 401.
- 50 random documents per source read for junk and personal data:

| source | junk | doubtful | personal data |
|---|---|---|---|
| FineMath-4+ | 3/50 | 15 | 0/50 |
| InfiWebMath-4+ | 2/50 | 14 | 0/50 |
| Stack-Edu Python | 1/50 | 1 | 1/50 before the 2026-11-27 fix (obfuscated e-mails in code headers, now masked in all 5 parts and in `mikroanneal/stack_edu_python`) |
| arXiv | 0/50 | 1 | 0/50 |
| StackExchange | 0/50 | 1 | 0/50 |
| formal mathematics | 0/50 | 0 | 0/50 |
| OEIS | 0/50 | 0 | 0/50 |
| Wikipedia | 0/50 | 0 | 0/50 |
| textbooks | 1/50 | 8 | 0/50 |

Known properties: FineMath-4+ and InfiWebMath-4+ contain ~5–10% junk (SEO pages, pages without formulas); no extra
quality classifier was applied. arXiv texts keep LaTeXML/Trafilatura conversion artefacts (glued footnote marks,
`~{}`, `[?]`); formulas are LaTeX in `$…$`.

Obfuscated e-mails in prose (`name at domain dot com`, `name_at_domain.edu`, `name{at}domain`) are masked as `[PII]`
in arXiv, Stack-Edu, StackExchange and `mikroanneal/finemath_4plus_en` (re-export of 2026-11-27). The parts
`data/finemath_4plus_en_p01`–`p07`, `data/infiwebmath_4plus_en_p01` and `mikroanneal/cranemath_en` were published
before that mask: 205 of their 6 298 876 documents (0.003%) still contain such an address. Their ids are listed in
`dane/matematyka-wspolne/wyniki/maska27_niewyslane.json`; drop those documents if this matters for your use.

## Licences and commercial use

All licences allow training a commercially sold model; no NC/ND. Copyleft (CC BY-SA, LGPL, GFDL) applies to
redistributing the data itself (keep `author`/`id` for attribution and the same licence). FineMath-4+ and
InfiWebMath-4+ have no per-document licence (basis: TDM exception). StackExchange has declared `ai-train=no` since
2024; training relies on the authors' CC BY-SA licence, as in Common Pile (risk described in the datasheet).

## `mikroanneal/`

Arms of a micro-annealing experiment: `finemath_4plus_en` (266 351 docs), `cranemath_en` (510 129 docs, FineMath-4+
rewritten by Qwen3-32B) and `stack_edu_python` (180 275 files). **The FineMath-4+ and Stack-Edu arms are subsets of
`data/`**: train on `data/` OR an arm, never both. CraneMath has no copy in `data/` or `tokenized/`.

## Takedown

By `id` (FineMath/InfiWebMath: WARC file and offset or WARC-Record-ID, and url; Stack-Edu: Software Heritage blob id
and repository; arXiv: `arXiv:<id>` / `arXiv-abs:<id>`; other sources: the source id).
