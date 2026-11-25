# CraneMath (FineMath-4+ rewritten by Qwen3-32B, Dolma 3 Dolmino)

Arm C of the Slayer 1B microanneal (model-rewritten mathematics), part 1. Reservation:
https://github.com/slayerlabs/benchmarks-fabryka-ai/issues/346. Status: `held_for_review`.

Marks: **V** = verified 2026-11-24 at the cited source (URL, revision, hash); **I** = inferred.

## Source

- V: https://huggingface.co/datasets/allenai/dolma3_dolmino_mix-100B-1125, revision
  `f23aa129fda8335ba9760057bcc1f0c02f3d068b`, only `data/ingredient1-cranemath` (192 `jsonl.zst` shards, no access
  gate). Publisher Ai2; paper Olmo 3, https://arxiv.org/abs/2512.13961 (§3.5, App. A.3.1); recipe
  https://github.com/allenai/dolma3/blob/1a9daced81670e0fa768e47fbed32af6694a1865/datasets/dolma3_dolmino_mix/cranemath/README.md
- V: synthetic text (100%): FineMath-4+ pages rewritten by `Qwen/Qwen3-32B` with the SwallowMath prompt (problem +
  step-by-step solution, no headers/footers). The prompt is copied verbatim to `prompts/cranemath_recipe.md`.
  Generator field: `Qwen/Qwen3-32B@unpublished prompt:cranemath_recipe.md`; Ai2 did not publish the model
  revision, sampling parameters or thinking mode.
- V: each row keeps `metadata.url` and `metadata.warc_*` of the FineMath source page; `derived_from` is that url.
  `metadata.original_text` (pre-rewrite text) is used only for filtering and is not exported.
- V: pool = shards chosen by a `numpy.default_rng(20261124)` permutation until ≥ 600M v6 tokens: 663 285 rows,
  623 303 464 v6 tokens; file list with sha256 in `wyniki/probka_pliki.json`. Export target 400M v6 tokens in
  permutation order.
- Tokens: v6 tokenizer (`tokenizer.json` sha256 `0640d3bd…815dd`), text tokens + 1 EOT.

## Rights review

- V: mix licence ODC-By 1.0 (HF card), with an "intended for research and educational use" note pointing to Ai2
  Responsible Use Guidelines (a purpose statement, not an ODC-By condition).
- V: generator Qwen3-32B is Apache-2.0 (HF `cardData.license`); no restriction on outputs or on training other models.
- V: the inputs are FineMath (ODC-By compilation) texts from Common Crawl, so each row is a derivative of a web page
  with its publisher's rights. No per-row licence.
- **Gate "may TRAIN": YES** (V/I, 2026-11-24). Basis: TDM exception, art. 4 Directive 2019/790, for the source pages;
  ODC-By and Apache-2.0 do not block. Takedown: drop by `metadata.url` / `id` in the next version (url in every row).
  Condition: TDM opt-out of source domains, not checked.
- **Gate "may SUBMIT": UNRESOLVED.** No per-document licence: the texts are rewrites of pages with unknown licences.
- **Decision: `held_for_review`.** Withheld: the whole shard until per-document rights are resolved.

Not checked:
- Qwen3-32B revision, sampling parameters and thinking mode used by Ai2.
- Whether Ai2's `decon` pass covered this directory and how much it removed.
- Exact row count of the directory (6.55M vs 7.24M in the paper vs ~6.9M estimate).
- TDM opt-out (robots.txt, TDMRep) of source domains.
- Mathematical correctness of rewrites beyond the manual sample below.
- Url overlap with FineMath in Slayer 1.07 and with arm B.

## Cleaning

Rules preregistered 2026-11-24 (`skrypty/preregistracja.json`) before any count; applied as a cascade in this order.
Counts from `wyniki/agreguj.json` (`kaskada`).

| # | Reason | Rule | dropped docs | dropped tokens (v6) |
|---|---|---|---|---|
| 1 | `walidacja_fabryki` | 13-gram sketch ≥ 0.5, MinHash ≥ 0.8, identical text or identical url vs Fabryka validation sets. | 920 | 163125 |
| 2 | `domena_testow` | Source page url from a domain that hosts benchmark sources (wikihow, instructables, Wikimedia projects). | 4800 | 4793803 |
| 3 | `ewal_13gram` | Non-trivial 13-gram in `text` from a strict math/code test (MathQA, MMLU, GSM8K, MATH, BBH, HumanEval, MBPP, GSM-Plus, GSM1k) at any df, or from another of ~60 tests at df < 5. | 7037 | 8144579 |
| 4 | `ewal_13gram_oryginal` | Same rule on `metadata.original_text`, since rewriting hides verbatim 13-grams of a test item. | 7209 | 7760745 |
| 5 | `think` | Text contains `<think>` or `</think>` (truncated Qwen3 reasoning traces). | 37231 | 147825856 |
| 6 | `min_tresc` | Fewer than 50 normalised words (annex 2026-11-24b). | 5312 | 753152 |
| 7 | `szablon_forum` | Forum footer or chatbot greeting marker (phpBB, GMAT Club, The Student Room, …) with < 200 words (annex 2026-11-24b). | 309 | 77697 |
| 8 | `suma40` | Invented "sum of 1..40 = 820" problem in `text` while the original page has no sum-to-40 problem (annexes 2026-11-24c, 2026-11-25). | 34020 | 11541195 |
| 9 | `pii` | E-mail, phone number or IPv4 address in `text` → document dropped. | 349 | 564581 |
| 10 | `pii_zaciemniony` | Obfuscated e-mail (`name(AT)domain(DOT)tld`) → document dropped (annex 2026-11-24c). | 0 | 0 |
| 11 | `mojibake` | ≥ 3 matches of a strict mojibake regex. | 9 | 7999 |
| 12 | `dedup_wewnatrz` | Identical normalised text or MinHash (5-grams, 128 perm., LSH 32×4) J ≥ 0.8 within the pool. | 516 | 817330 |
| 13 | `dedup_slayer107` | 13-gram sketch ≥ 0.5 or MinHash ≥ 0.8 of `text` vs Slayer 1.07 English data. | 322 | 425560 |
| 14 | `dedup_english_technical` | MinHash J ≥ 0.8 or identical text vs `SlayerLab/english-technical-1b@3b833d36` (1.08 data). | 0 | 0 |
| 15 | `dedup_fineweb_edu_109` | Source page url identical (normalised) to a url of FineWeb-Edu in `SlayerLab/Slayer1B-Dataset@2d248a17` (1.09). | 43270 | 32432171 |

Pool 663 285 docs / 623 303 464 v6 tokens. Kept after all reasons (`uzysk`): 521 981 docs / 407 995 671 tokens
(65.457%). Exported (`eksport`, kept documents in permutation order up to the 400M target): 511 710 docs /
400 000 473 tokens.

Positive control: 22/22 planted documents got the expected reason (`wyniki/kontrola.json`), including an unclosed
`<think>` and a GSM8K item present only in `original_text`.

Review of dropped documents (100 per reason, two reviewers A/B, false-drop thresholds ≤ 10% and Wilson 95% upper
bound ≤ 20%; `wyniki/przeglad_odrzuconych_1.json`):

| Reason | A false drops [Wilson] | B false drops [Wilson] | Verdict | Token cost |
|---|---|---|---|---|
| `walidacja_fabryki` | 95% [88.8; 97.8] | 93% [86.3; 96.6] | FAIL | 0.03% |
| `domena_testow` | 0% [0; 3.7] | 0% [0; 3.7] | PASS | 0.77% |
| `ewal_13gram` | 76% [66.8; 83.3] | 79% [70.0; 85.8] | FAIL | 1.32% |
| `ewal_13gram_oryginal` | 36% [27.3; 45.8] | 29% [21.0; 38.5] | FAIL | 1.59% |
| `think` | 0% [0; 3.7] | 0% [0; 3.7] | PASS | 24.40% |
| `pii` | 55% [45.2; 64.4] | 52% [42.3; 61.5] | FAIL | 0.11% |
| `mojibake` | 60.9% [40.8; 77.8] | 30.4% [15.6; 50.9] | FAIL | 0.01% |
| `dedup_wewnatrz` | 8% [4.1; 15.0] | 9% [4.8; 16.2] | PASS | 0.27% |
| `dedup_slayer107` | 18% [11.7; 26.7] | 61% [51.2; 70.0] | FAIL | 0.11% |
| `dedup_english_technical` | 23% [15.8; 32.2] | 77% [67.8; 84.2] | FAIL | 0.02% |

The precision FAILs are accepted unchanged (annex 2026-11-24b): these rules drop good text rather than let bad text
through, and cost is recorded in tokens. For `walidacja_fabryki`, `dedup_slayer107`, `dedup_english_technical` and
`mojibake` the dropped texts are mostly content-free templates (forum footers, chatbot greetings), so the loss of good
data is negligible (≈ 0.2% of tokens); the same review led to `min_tresc` and `szablon_forum`. Rule changes need a new
review sample and are scheduled before part 2.

Review of 300 kept documents (`wyniki/przeglad_zachowanych_1.json`, preliminary aggregation): junk 2.0% [0.9; 4.3]
(A) and 2.7% [1.4; 5.2] (B), PASS; missed PII 0/300 for both. **Wrong rewrites** (math error or content
contradicting the original) **20.7% [16.5; 25.6]** (A) and **20.0% [15.9; 24.9]** (B), FAIL of the 10% threshold.
About a quarter of the contradicting rewrites were the same invented problem "sum of 1..40 = 820" inserted for pages
without a problem; rule `suma40` removes them. Annex 2026-11-24c dropped such a text only when the original contained
no number 40 at all; the control sample (below) still found it in kept documents whose original had a 40 somewhere
else. Annex 2026-11-25 (written before export) replaced that condition: the original must contain no sum-to-40
problem (`regex_oryginal_zadanie`: "1 to 40", "1 + 2 + … + 40", "first 40 numbers"). Measured before the change
(`wyniki/suma40_reszta.json`): 6 136 selected documents matched the rewrite pattern, 58 of them had the problem in the
original and stay, 6 078 were dropped. The remaining errors (≈ 9% arithmetic errors and
invented problems) are accepted: they are a property of CraneMath as measured by Olmo 3, and this shard is the
**comparison arm** against raw FineMath-4+ (arm B). Fixing them needs regeneration with verification, before part 2
if arm C wins. One missed-test flag (AMC 10B 2015, not in our MATH test by grep) was not confirmed.

## Personal data

- Our filters drop the whole document when `text` contains an e-mail address, phone number or IPv4 address (`pii`),
  or an obfuscated e-mail such as `name(AT)domain` (`pii_zaciemniony`). This is the only PII protection. Rewriting
  removes most headers and signatures; author names may remain. `original_text` is not exported.
- The Presidio pass of `shard.write` is **off** for this source (`no_masking()` in `src/mat_wybor.py`): measured on
  2026-11-24, Presidio's PhoneRecognizer tagged 403 spans in 300 FineMath-4+ documents (the inputs of CraneMath),
  almost all of them numbers in the mathematics itself, so masking would destroy the training signal. The `pii`
  record of `cranemath_en.stats.json` stores `"pass": "none"` and this reason.
- Consequently `src/check.py` reports a mismatch in its Presidio PII rescan of the parquet. This is expected and
  caused by the opt-out above, not by unmasked personal data missed by our rules.
- Control sample of 200 kept documents: missed PII 0/200 for both reviewers (see `## Sample`).

## Sample

- Seed `20261124` (file permutation and export order).
- Manual review: 100 dropped documents per reason and 300 kept documents, first 3000 characters each; for kept
  documents the rewrite was compared with the original text. Two independent reviewers A and B who did not build the
  set; Wilson 95% intervals as above.
- Control sample of 200 kept documents from the final selection, `default_rng(seed+2)` = `20261126`, two reviewers
  A and B: missed PII **0/200** for both; missed test items: 0 confirmed (one flag, item 187012, has no counterpart in
  the MATH test, grep 2026-11-25); `suma40` still passed in items 301032 and 359177 (their originals contain a 40
  elsewhere), which led to annex 2026-11-25. Some reviewers read items partly (beginning plus a regex over the whole
  text), as they reported.
- The inline sample generated by `src/render_sample.py` from the built shard goes in the PR description.
