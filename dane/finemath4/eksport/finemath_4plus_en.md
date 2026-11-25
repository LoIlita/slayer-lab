# FineMath-4+ (English mathematical web text)

Part 2: the full FineMath-4+ pool for the Slayer 1B mathematics and code set (target ≈ 20B v6 tokens), exported as
seven parts `finemath_4plus_en_p01` … `finemath_4plus_en_p07`. Reservation:
https://github.com/slayerlabs/benchmarks-fabryka-ai/issues/346. Status: `held_for_review`.
Part 1 (arm B of the Slayer 1B microanneal) is described at the end of `## Cleaning`; it is a subset of part 2's pool
and **must not be combined with part 2 in training**. InfiWebMath-4+ and FineMath-3+ drop pages already in this
export (`dedup_finemath4` on their side).

Marks: **V** = verified 2026-11-24/25 at the cited source (URL, revision, hash); **I** = inferred.

## Source

- V: https://huggingface.co/datasets/HuggingFaceTB/finemath, revision
  `e92b25a616738fe95dc186b64dfb19f9c8525594`, subset `finemath-4plus` (64 parquet files, no access gate).
  Publisher Hugging Face (HuggingFaceTB); paper SmolLM2, Ben Allal et al. 2025, https://arxiv.org/abs/2502.02737.
- V: texts are pages from Common Crawl (CC-MAIN 2013–2024) extracted with the OpenWebMath pipeline, kept when the
  FineMath classifier (https://huggingface.co/HuggingFaceTB/finemath-classifier @ `bd0b0e33`, MIT) scores ≥ 4.
  English, Markdown + LaTeX: step-by-step solutions, Q&A forums (math.stackexchange, physicsforums, mathhelpforum,
  jiskha, socratic, …).
- V: pool of part 2 = all 64 files in the same `numpy.default_rng(20261124)` permutation as part 1: 6 699 493
  documents, 10 552 288 210 v6 tokens; sha256 of every file in `wyniki/cz2/probka_pliki.json`. Export: every document
  kept by the rules.
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
- **Decision: `held_for_review`.** Withheld: the whole set until per-document rights are resolved.

Not checked:
- TDM opt-out (robots.txt, TDMRep, ai.txt) and terms of use of the top domains.
- Content of `HuggingFaceTB/finemath_contamination_report` @ `3dc3725b` (counts, exact tests).
- Number of FineMath documents and subset (3+/4+) in Slayer 1.07 `en_mix`; overlap is handled by `dedup_slayer107`.
- Full Llama 3.1 licence text against classifier-only use (conclusion above is I).
- Domain, e-mail and `snapshot_type` distribution beyond the first 20 000 rows of shard 0.

## Cleaning

Rules preregistered 2026-11-24 (`skrypty/preregistracja.json`) before any count, with annexes. Part 2 (`czesc_2`,
written 2026-11-25 before downloading the remaining files, commit `380e7f0`) keeps the rules of part 1 (annexes up to
25.11b) and deliberately defers the quality filter (annex 24.11c) and the precision fixes of the conservative rules
(annex 24.11b); both only drop documents, so they can be applied later to this export. Annex 25.11c (commit
`601e1bc`, after the first part 2 control sample missed one `name at domain.org` e-mail) adds `pii_at_bez_nawiasow`.
Cascade in this order; counts from `wyniki/cz2/agreguj.json` (`kaskada`; "independent" = documents with the reason
regardless of order, `niezaleznie`).

| # | Reason | Rule | dropped docs | dropped tokens (v6) |
|---|---|---|---|---|
| 1 | `walidacja_fabryki` | 13-gram sketch ≥ 0.5, MinHash ≥ 0.8, identical text or identical url vs Fabryka validation sets. | 4083 | 4186642 |
| 2 | `domena_testow` | Page from a domain that hosts benchmark sources (wikihow, instructables, Wikimedia projects). | 47827 | 127765691 |
| 3 | `ewal_13gram` | Non-trivial 13-gram from a strict math/code test (MathQA, MMLU, GSM8K, MATH, BBH, HumanEval, MBPP, GSM-Plus, GSM1k) at any df, or from another of ~60 tests at df < 5. | 80983 | 285728794 |
| 4 | `pii` | E-mail, phone number or IPv4 address found → document dropped. | 140063 | 627830112 |
| 5 | `pii_zaciemniony` | Obfuscated e-mail (`name(AT)domain(DOT)tld`) → document dropped (annex 2026-11-24c). | 5995 | 10103504 |
| 6 | `pii_at_bez_nawiasow` | E-mail written as `name at domain.tld` without brackets → document dropped (annex 2026-11-25c). Before the rule: 29 350 of 4 814 480 selected documents (0.61%), `wyniki/cz2/wzorzec_email_at_bez_nawiasow.json`. | 41030 | 139638162 |
| 7 | `min_tresc` | Fewer than 50 normalised words → document dropped (annex 2026-11-24b). | 42275 | 3709604 |
| 8 | `mojibake` | ≥ 3 matches of a strict mojibake regex. | 56514 | 160473284 |
| 9 | `dedup_wewnatrz` | Identical normalised text or MinHash (5-grams, 128 perm., LSH 32×4) J ≥ 0.8 within the whole part 2 pool (includes part 1). | 640521 | 1017809945 |
| 10 | `dedup_slayer107` | 13-gram sketch ≥ 0.5 or MinHash ≥ 0.8 vs Slayer 1.07 English data (FineMath, open-web-math, FineWeb-Edu). | 501565 | 717139748 |
| 11 | `dedup_slayer_8x3b_en` | MinHash J ≥ 0.8 or identical text vs the English part of Slayer 1.00–1.06, `SlayerLab/slayer-pl-8x3b@d50df04a` `shared/en.parquet` (sha256 `f3d451b7…`, 2 384 000 docs; annex 2026-11-25b). | 6560 | 7667216 |
| 12 | `dedup_english_technical` | MinHash J ≥ 0.8 or identical text vs `SlayerLab/english-technical-1b@3b833d36` (1.08 data). | 2 | 10290 |
| 13 | `dedup_fineweb_edu_109` | Identical normalised url vs FineWeb-Edu files in `SlayerLab/Slayer1B-Dataset@2d248a17` (1.09). | 346945 | 423124444 |

Pool 6 699 493 docs / 10 552 288 210 v6 tokens. Kept after all reasons (`uzysk`): **4 785 130 docs / 7 027 100 774
v6 tokens (66.59%)**.

Parts (`wyniki/cz2/czesci.json`): seven parts of ≈ 1.004B v6 tokens each. Export (`eksport_czesci.sh`, `KONIEC 7`);
"docs" below are exported rows, the selection before `shard.write` is in `czesci.json`:

| key | docs | expected `check.py` lines | parquet sha256 |
|---|---|---|---|
| `finemath_4plus_en_p01` | 676 355 | 27 | `51b6e67d1e215b99822ac7f083507da89aa5a12c43b1165581ef990d59a645e5` |
| `finemath_4plus_en_p02` | 674 766 | 26 | `3532ded4b92449de3575bd069b0900e01bca5fade78d6b486586e6d42c4e27c8` |
| `finemath_4plus_en_p03` | 680 572 | 30 | `6362c45b0c35f6821c9e9d9373341dcdee7f0b1899ea5592cf1e41ef43fd645c` |
| `finemath_4plus_en_p04` | 682 556 | 21 | `f80fab9efc1dceea7275cf9f77cfac28791ef7fe92cd6897047bdfa110131463` |
| `finemath_4plus_en_p05` | 680 148 | 21 | `017ef971d727237590ebbf1fb0bb21660b8032fc08e2f423385074c65e7e37f3` |
| `finemath_4plus_en_p06` | 685 711 | 33 | `c9a195d565165a528c66476b5b3a48a92109b6064e3e728445f0c3d82e4a19a9` |
| `finemath_4plus_en_p07` | 683 199 | 19 | `4a67a117cddda85588d96d6c12767fce6343adb6408884734eca15df896cd3af` |

Export total: **4 763 307 docs, 6 337 631 742 tokens** by the submissions repo counter (`token_count`, not v6);
`dropped`: `wrong_language` 21 289, `min_chars` 534 (registry `min_chars: 200`); 4 785 130 − 21 823 = 4 763 307.

Positive control: not run on the part 2 pool; rules and indexes are those of part 1, where it passed 19/19
(`wyniki/kontrola.json`); `pii_at_bez_nawiasow` has no planted case.

Review of dropped documents: not run on the part 2 pool. The rules are those of part 1 (review below), except
`pii_at_bez_nawiasow`, which was reviewed on InfiWebMath-4+ (`dane/infiwebmath4/wyniki/przeglad_1.json`: false drops
80% (A) and 34% (B), e.g. "here at Shaalaa.com"; accepted as a conservative privacy rule, annex 2026-11-25e there).

Part 1 review of dropped documents (100 per reason, two reviewers A/B, false-drop thresholds ≤ 10% and Wilson 95%
upper bound ≤ 20%; `wyniki/przeglad_odrzuconych_1.json`; token cost in part 1):

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
through; privacy takes priority for `pii`. `dedup_slayer_8x3b_en` (part 1, one reviewer, 100 dropped): 99 correct,
0 false, 1 doubtful.

Junk: part 1, 300 kept documents (`wyniki/przeglad_zachowanych_1.json`): 13.0% [9.7; 17.3] for both reviewers; part 2
control sample (below): 10.5% (A) and 9.0% (B). Junk (SEO spam, pages without mathematics, formulas lost in
extraction) is a property of published FineMath-4+; the quality filter is deferred (`czesc_2.reguly`).

**Part 1 (historical, microanneal arm B).** Pool of 4 files (`train-00063`, `-00013`, `-00018`, `-00042`; 418 718
docs, 660 554 470 v6 tokens), same rules without `pii_at_bez_nawiasow`; kept 329 712 docs / 492 093 320 v6 tokens;
export target 400M v6 tokens: 267 504 docs selected, exported **266 351 docs, 360 900 014 tokens (cl100k)**; key
`finemath_4plus_en`, parquet sha256 `c4ae6f1424dd45e482d43d7524bab5e3dbf44d44beb4acc7888ff769c0c2d4c5`. Its four
files are in part 2's pool and `dedup_wewnatrz` runs over the whole pool, so part 1 is a **subset** of part 2: do
not combine them in training.

## Personal data

- Our filters drop the whole document when it contains an e-mail address, phone number or IPv4 address (`pii`), an
  obfuscated e-mail such as `name(AT)domain` (`pii_zaciemniony`) or `name at domain.tld` (`pii_at_bez_nawiasow`).
  This is the only PII protection. Detector classes in the part 2 pool: e-mail 116 352, phone 20 396, IP 16 956.
- Forum nicknames and signatures may remain (not detected by these rules).
- The Presidio pass of `shard.write` is **off** for this source (`no_masking()` in `src/mat_wybor.py`): measured on
  2026-11-24, Presidio's PhoneRecognizer tagged 403 spans in 300 FineMath-4+ documents, almost all of them numbers in
  the mathematics itself (percentages, ISBNs, decimals, physical constants), so masking would destroy the training
  signal. The `pii` record of each part's `stats.json` stores `"pass": "none"` and this reason.
- Consequently `src/check.py` exits 1 for each part only with the expected lines ("PII left after masking" from the
  Presidio rescan and "stats.json pii has no presidio record"): p01 27, p02 26, p03 30, p04 21, p05 21, p06 33,
  p07 19. Hit types were checked on 2026-11-25 on part 1 (CREDIT_CARD 3, UK_NHS 1, IP_ADDRESS 1, all numbers or
  ISBNs); not checked per hit for part 2.
- Part 2 control sample: missed PII **0/200** for both reviewers (see `## Sample`); the first part 2 control sample,
  before annex 25.11c, missed one e-mail written as `name at domain.org`.

## Sample

- Seed `20261124` (file permutation).
- Part 2 control sample (`wyniki/cz2/przeglad_kontrolny.json`): 200 kept documents from the part 2 selection after
  annex 25.11c, `default_rng(seed+3)`, two independent reviewers A and B; both declared reading the full 3000
  characters plus a pattern search for e-mail/phone/IP. Missed PII **0/200** and missed test items **0/200** for both;
  quality yes / doubtful / no: 143 / 36 / 21 (A) and 149 / 33 / 18 (B); junk 10.5% [7.0; 15.5] (A) and 9.0% [5.8;
  13.8] (B).
- Part 1 manual review: 100 dropped documents per reason and 300 kept documents, first 3000 characters each; two
  independent reviewers A and B who did not build the set. Part 1 control sample of 200, `default_rng(seed+2)`:
  missed PII 0/200 for both; flagged test items 9636, 84036 and 238166 have no counterpart in the MATH test (grep
  2026-11-25).
- The inline sample generated by `src/render_sample.py` from the built shard goes in the PR description.
