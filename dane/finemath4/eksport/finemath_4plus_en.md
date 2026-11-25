# FineMath-4+ (English mathematical web text)

Arm B of the Slayer 1B microanneal (raw mathematical web text), part 1. Reservation:
https://github.com/slayerlabs/benchmarks-fabryka-ai/issues/346. Status: `held_for_review`.

Marks: **V** = verified 2026-11-24 at the cited source (URL, revision, hash); **I** = inferred.

## Source

- V: https://huggingface.co/datasets/HuggingFaceTB/finemath, revision
  `e92b25a616738fe95dc186b64dfb19f9c8525594`, subset `finemath-4plus` (64 parquet files, no access gate).
  Publisher Hugging Face (HuggingFaceTB); paper SmolLM2, Ben Allal et al. 2025, https://arxiv.org/abs/2502.02737.
- V: texts are pages from Common Crawl (CC-MAIN 2013–2024) extracted with the OpenWebMath pipeline, kept when the
  FineMath classifier (https://huggingface.co/HuggingFaceTB/finemath-classifier @ `bd0b0e33`, MIT) scores ≥ 4.
  English, Markdown + LaTeX: step-by-step solutions, Q&A forums (math.stackexchange, physicsforums, mathhelpforum,
  jiskha, socratic, …).
- V: pool = 4 files chosen by a `numpy.default_rng(20261124)` permutation until ≥ 600M v6 tokens:
  `train-00063` (sha256 `ca21ff1b…dfee`), `train-00013` (`2188e377…6ff2`), `train-00018` (`6234f2ef…40e2ff`),
  `train-00042` (`209b4839…afe`); 418 718 documents, 660 554 470 v6 tokens. Full hashes in
  `wyniki/probka_pliki.json`. Export target 400M v6 tokens, taken from kept documents in permutation order.
- Tokens: v6 tokenizer (`tokenizer.json` sha256 `0640d3bd…815dd`), text tokens + 1 EOT.
- Per-row ids: `warc_filename:warc_record_offset`; `url` kept for takedown.

## Rights review

- V: compilation licence ODC-By 1.0 (dataset card, also "subject to CommonCrawl's Terms of Use"). It licenses the
  compilation, not the texts: each page keeps its publisher's rights (CC BY-SA on math.stackexchange, forum terms,
  restrictive terms on e.g. coursehero/gradesaver (I)). No per-row licence field (V: schema).
- I: the Llama 3.1 licence does not attach: Llama-3.1-70B-Instruct only produced the scores used to train the
  classifier; the texts are original pages, not model output.
- **Gate "may TRAIN": YES** (V/I, 2026-11-24). Basis: TDM exception, art. 4 Directive 2019/790, for the texts;
  ODC-By for the compilation. Takedown: drop by `url` / WARC id in the next version. Condition: TDM opt-out honoured,
  not checked.
- **Gate "may SUBMIT": UNRESOLVED.** No per-document licence (ODC-By of the compilation ≠ licence of the texts),
  some domains carry SA or no-copy terms, TDM opt-out not checked.
- **Decision: `held_for_review`.** Withheld: the whole shard until per-document rights are resolved.

Not checked:
- TDM opt-out (robots.txt, TDMRep, ai.txt) and terms of use of the top domains.
- Content of `HuggingFaceTB/finemath_contamination_report` @ `3dc3725b` (counts, exact tests).
- Number of FineMath documents and subset (3+/4+) in Slayer 1.07 `en_mix`; overlap is handled by `dedup_slayer107`.
- Full Llama 3.1 licence text against classifier-only use (conclusion above is I).
- Domain, e-mail and `snapshot_type` distribution beyond the first 20 000 rows of shard 0.

## Cleaning

Rules preregistered 2026-11-24 (`skrypty/preregistracja.json`) before any count; applied as a cascade in this order.
Counts from the final `wyniki/agreguj.json` (`kaskada`; "independent" = documents with the reason regardless of order).

| # | Reason | Rule | dropped docs | dropped tokens (v6) |
|---|---|---|---|---|
| 1 | `walidacja_fabryki` | 13-gram sketch ≥ 0.5, MinHash ≥ 0.8, identical text or identical url vs Fabryka validation sets. | 231 | 207149 |
| 2 | `domena_testow` | Page from a domain that hosts benchmark sources (wikihow, instructables, Wikimedia projects). | 3011 | 7812679 |
| 3 | `ewal_13gram` | Non-trivial 13-gram from a strict math/code test (MathQA, MMLU, GSM8K, MATH, BBH, HumanEval, MBPP, GSM-Plus, GSM1k) at any df, or from another of ~60 tests at df < 5. | 5671 | 20942995 |
| 4 | `pii` | E-mail, phone number or IPv4 address found → document dropped. | 8672 | 39810781 |
| 5 | `pii_zaciemniony` | Obfuscated e-mail (`name(AT)domain(DOT)tld`) → document dropped (annex 2026-11-24c). | 359 | 558284 |
| 6 | `min_tresc` | Fewer than 50 normalised words → document dropped (annex 2026-11-24b). | 2686 | 236058 |
| 7 | `mojibake` | ≥ 3 matches of a strict mojibake regex. | 3543 | 10121526 |
| 8 | `dedup_wewnatrz` | Identical normalised text or MinHash (5-grams, 128 perm., LSH 32×4) J ≥ 0.8 within the pool. | 3658 | 6183891 |
| 9 | `dedup_slayer107` | 13-gram sketch ≥ 0.5 or MinHash ≥ 0.8 vs Slayer 1.07 English data (FineMath, open-web-math, FineWeb-Edu). | 35928 | 51579836 |
| 10 | `dedup_slayer_8x3b_en` | MinHash J ≥ 0.8 or identical text vs the English part of Slayer 1.00–1.06, `SlayerLab/slayer-pl-8x3b@d50df04a` `shared/en.parquet` (sha256 `f3d451b7…`, 2 384 000 docs; annex 2026-11-25b). Independent: 605 docs, 0.11% tokens. | 507 | 575146 |
| 11 | `dedup_english_technical` | MinHash J ≥ 0.8 or identical text vs `SlayerLab/english-technical-1b@3b833d36` (1.08 data). | 0 | 0 |
| 12 | `dedup_fineweb_edu_109` | Identical normalised url vs FineWeb-Edu files in `SlayerLab/Slayer1B-Dataset@2d248a17` (1.09). | 24740 | 30432805 |

Pool 418 718 docs / 660 554 470 v6 tokens. Kept after all reasons (`uzysk`): 329 712 docs / 492 093 320 tokens
(74.497%). Selected for export (`eksport`, kept documents in permutation order up to the 400M target): 267 504 docs /
400 000 934 v6 tokens.

Export (`wyniki/eksport_stats.json`): **266 351 docs, 360 900 014 tokens (cl100k)**, 1 248 763 375 characters;
`dropped`: `wrong_language` 1129, `min_chars` 24 (registry `min_chars: 200`), all other counters 0. Parquet sha256
`c4ae6f1424dd45e482d43d7524bab5e3dbf44d44beb4acc7888ff769c0c2d4c5` (`wyniki/eksport_sha256.txt`).

Positive control: 19/19 planted documents got the expected reason (`wyniki/kontrola.json`, after annex 2026-11-25b).

Review of `dedup_slayer_8x3b_en` (annex 2026-11-25b, one reviewer, 100 dropped documents): 99 correct, 0 false,
1 doubtful; 20 random items (seed 20261125) checked by phrase search in the base itself: 19 with a copy, 1 probable
(bullet character differs).

Review of dropped documents (100 per reason, two reviewers A/B, false-drop thresholds ≤ 10% and Wilson 95% upper
bound ≤ 20%; `wyniki/przeglad_odrzuconych_1.json`):

| Reason | A false drops [Wilson] | B false drops [Wilson] | Verdict | Token cost |
|---|---|---|---|---|
| `walidacja_fabryki` | 0% [0; 3.7] | 0% [0; 3.7] | PASS | 0.03% |
| `domena_testow` | 0% [0; 3.7] | 0% [0; 3.7] | PASS | 1.18% |
| `ewal_13gram` | 33% [24.6; 42.7] | 44% [34.7; 53.8] | FAIL | 3.23% |
| `pii` | 9% [4.8; 16.2] | 13% [7.8; 21.0] | FAIL (B) | 6.35% |
| `mojibake` | 0% [0; 3.7] | 0% [0; 3.7] | PASS | 1.77% |
| `dedup_wewnatrz` | 3% [1.0; 8.5] | 1% [0.2; 5.4] | PASS | 1.06% |
| `dedup_slayer107` | 0% [0; 3.7] | 3% [1.0; 8.5] | PASS | 8.78% |

The precision FAILs are accepted unchanged (annex 2026-11-24b): these rules drop good text rather than let bad text
through; cost is recorded in tokens; privacy takes priority for `pii`. Rule changes need a new review sample and
are scheduled before part 2.

Review of 300 kept documents (`wyniki/przeglad_zachowanych_1.json`, preliminary aggregation): junk (SEO spam, pages
without mathematics, formulas lost in extraction) **13.0% [9.7; 17.3]** for both reviewers, FAIL of the 10%
threshold. Accepted (annex 2026-11-24c): it is a property of published FineMath-4+, and this shard is the
**comparison arm** against the rewritten CraneMath (arm C); an extra quality filter would change the arm. A quality
filter comes before part 2 if arm B wins. Missed PII 1–2/300 (OEIS `name(AT)domain` e-mails) led to
`pii_zaciemniony`. One missed-test flag (MATH) was not confirmed by grep against the MATH test.

## Personal data

- Our filters drop the whole document when it contains an e-mail address, phone number or IPv4 address (`pii`), or
  an obfuscated e-mail such as `name(AT)domain` (`pii_zaciemniony`). This is the only PII protection.
- Forum nicknames and signatures may remain (not detected by these rules).
- The Presidio pass of `shard.write` is **off** for this source (`no_masking()` in `src/mat_wybor.py`): measured on
  2026-11-24, Presidio's PhoneRecognizer tagged 403 spans in 300 FineMath-4+ documents, almost all of them numbers in
  the mathematics itself (percentages, ISBNs, decimals, physical constants), so masking would destroy the training
  signal. The `pii` record of `finemath_4plus_en.stats.json` stores `"pass": "none"` and this reason.
- Consequently `src/check.py` exits 1 for two expected reasons only: "stats.json pii has no presidio record", and the
  Presidio rescan of 200 documents flags 28 of them. Hit types checked 2026-11-25: CREDIT_CARD 3, UK_NHS 1,
  IP_ADDRESS 1, all numbers or ISBNs in the mathematics; no real personal data.
- Control sample of 200 kept documents: missed PII 0/200 for both reviewers (see `## Sample`).

## Sample

- Seed `20261124` (file permutation and export order).
- Manual review: 100 dropped documents per reason and 300 kept documents, first 3000 characters each; two
  independent reviewers A and B who did not build the set; Wilson 95% intervals as above.
- Control sample of 200 kept documents from the final selection, `default_rng(seed+2)` = `20261126`, two reviewers
  A and B, PII and missed-test fields only: missed PII **0/200** for both; missed test items: 0 confirmed (items 9636,
  84036 and 238166 were flagged and have no counterpart in the MATH test, grep over all T34_math test files 2026-11-25).
  Some reviewers read items partly (beginning plus a regex over the whole text), as they reported.
- The inline sample generated by `src/render_sample.py` from the built shard goes in the PR description.
