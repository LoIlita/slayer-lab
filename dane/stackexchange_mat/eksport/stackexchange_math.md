# Stack Exchange mathematics and logic Q&A (Common Pile)

Part 3 of the Slayer 1B mathematics and logic set (#357): questions with their comments and answers from nine Stack
Exchange sites about mathematics and logic, one document per question. Key `stackexchange_math`, one part
`stackexchange_math_p01`. Reservation: https://github.com/slayerlabs/benchmarks-fabryka-ai/issues/357.
Status: `held_for_review`.

Questions already present as web pages in FineMath-4+ part 2 or InfiWebMath-4+ were removed (`dedup_se_strony`,
`dedup_finemath4`, `dedup_infiwebmath4`), so the set holds no second copy of the same question.

Marks: **V** = verified 2026-11-26 at the cited source (URL, revision, hash, measurement); **I** = inferred.

## Source

- V: https://huggingface.co/datasets/common-pile/stackexchange, revision `5ec3aa2e65b7c61b7c18f1ff18ccbc4d3279a23c`, the
  "raw" version (the "filtered" version masks PII with placeholders that also replace numbers in mathematics).
  Publisher Common Pile (Kandpal et al. 2025, https://arxiv.org/abs/2506.05209). Per the README and paper §B.2: community
  dumps of December 2024 on the Internet Archive plus missing questions from the official dump of July 2024. Document =
  question + comments + answers (accepted first, then by votes) + answer comments, Markdown rendered to text.
- Sites (preregistered): math.stackexchange.com, mathoverflow.net, cstheory, matheducators, proofassistants, stats, cs,
  scicomp, or. Not taken: physics, mathematica, puzzling, quant, crypto, meta sites (`KARTA_ZRODLA.md`).
- Row selection before the pool (preregistered): question `created` < 2022-12-01 (answers after that may contain
  ChatGPT text; answer dates are not available), and every post licensed (`metadata.all_licenses` without `'None'`).
- V: pool (`wyniki/probka_pliki.json`): 23 files, **1 938 345 documents, 1 667 484 804 v6 tokens**; math.SE
  `00005_se.jsonl.gz` has no row left after selection (field `puste`). Per site (docs / v6 tokens): math.SE 1 528 962 /
  1 264 279 214; mathoverflow 139 833 / 158 746 924; stats 194 855 / 172 863 100; cs 45 097 / 36 789 139; cstheory
  12 068 / 12 327 267; scicomp 10 500 / 11 552 078; matheducators 3 423 / 6 935 484; or 3 085 / 3 288 406;
  proofassistants 522 / 703 192.
- Row id `<site>/<question id>`; `url` `https://<site>/questions/<id>`; `created` = question date.
- Tokens: v6 tokenizer (`tokenizer.json` sha256 `0640d3bd…815dd`), text tokens + 1 EOT.

## Rights review

- V: every document carries a CC BY-SA licence from the authors of its posts (`metadata.license` of the question:
  CC BY-SA 2.5, 3.0 or 4.0; `metadata.all_licenses` for all posts; documents with an unlicensed post are not in the
  pool). No NC/ND. Attribution: `url` per question and display names of all posters (`author`).
- **Commercial use: allowed.** CC BY-SA permits commercial use; share-alike applies to redistribution of the data
  itself, which must stay under CC BY-SA.
- V: since 2024 the platform declares an AI-training opt-out: `Content-signal: search=no, ai-train=no` in robots.txt of
  math.SE and mathoverflow, and the data-dump download form ("for projects that do not include training a large language
  model (LLM)"; sanction: no access to future downloads) (`KARTA_ZRODLA.md` §2).
- I: the platform does not own the rights to the posts and cannot revoke the authors' CC BY-SA licence; the dump form is
  an agreement with the downloader, not a content licence.
- Risk, NOT CHECKED: the Common Pile copy comes from community dumps uploaded in December 2024 and from the official
  dumps of July 2024; whether the original downloader accepted the new download terms is unknown.
- **Gate "may TRAIN" (including commercial use): YES**, on the authors' CC BY-SA licence (fallback: TDM exception,
  art. 4 Directive 2019/790); the platform opt-out is a note, not a veto. Takedown: drop by site and question id.
- **Gate "may SUBMIT": UNRESOLVED**, for the team's rights review: per-row licence without NC/ND, but the platform signals
  an opt-out and the repository rule excludes TDM opt-outs.
- **Decision: `held_for_review`.**

Not checked:
- robots.txt as served to ordinary crawlers (our client got HTTP 418 with `ai-train=no`, `Disallow: /`); TDMRep and
  ai.txt only for math.SE (404).
- Whether the downloader of the dumps behind the Common Pile copy accepted the post-2024 terms.
- LLM text in answers to questions asked before 2022-12-01 (no answer dates).
- Copies of SE pages on other domains (only `url`-based and MinHash dedup against our sources).

## Cleaning

Rules preregistered 2026-11-26 (`skrypty/preregistracja.json`, commit `805bf5b`) before download, taken from
InfiWebMath-4+ with annexes 24.11, 24.11b, 24.11c, 25.11b, 25.11c; departures: row selection by date and licence, new
reason `dedup_se_strony`, no `dedup_fineweb_edu_109` (urls without slug never match FineWeb-Edu). Annex
`aneks_2026_11_26_przeglad` (commit `3865ee2`, after the review, before export) records the review result. Cascade in this
order; counts from `wyniki/agreguj.json` (`kaskada`; "independent" = documents with the reason regardless of order).

| # | Reason | Rule | dropped docs | dropped tokens (v6) |
|---|---|---|---|---|
| 1 | `walidacja_fabryki` | 13-gram sketch ≥ 0.5, MinHash ≥ 0.8, identical text or identical url vs Fabryka validation sets. | 72 | 69725 |
| 2 | `domena_testow` | Domain hosting benchmark sources. | 0 | 0 |
| 3 | `ewal_13gram` | Non-trivial 13-gram from a strict math/code test at any df, or from another of ~60 tests at df < 5. | 5783 | 7783924 |
| 4 | `pii` | E-mail, phone number or IPv4 address → document dropped. | 2729 | 4777218 |
| 5 | `pii_zaciemniony` | Obfuscated e-mail (`name(AT)domain(DOT)tld`) → document dropped. | 79 | 178577 |
| 6 | `pii_at_bez_nawiasow` | `name at domain.tld` → document dropped. | 1607 | 2798551 |
| 7 | `min_tresc` | Fewer than 50 normalised words. | 4525 | 311696 |
| 8 | `mojibake` | ≥ 3 matches of a strict mojibake regex. | 6 | 8842 |
| 9 | `dedup_wewnatrz` | Identical normalised text or MinHash (5-grams, 128 perm., LSH 32×4) J ≥ 0.8 within the pool (cross-posts). | 531 | 456247 |
| 10 | `dedup_finemath4` | Identical normalised url, MinHash J ≥ 0.8 or identical text vs FineMath-4+ part 2. | 170589 | 197320547 |
| 11 | `dedup_infiwebmath4` | Same vs InfiWebMath-4+. | 13966 | 14500140 |
| 12 | `dedup_se_strony` | Question (site, id) present as a web page in the FineMath-4+ part 2 or InfiWebMath-4+ export (`matematyka-wspolne/skrypty/se_strony.py`; index of 386 409 questions). | 108541 | 125253635 |
| 13 | `dedup_slayer107` | 13-gram sketch ≥ 0.5 or MinHash ≥ 0.8 vs Slayer 1.07 English data. | 14947 | 16731779 |
| 14 | `dedup_slayer_8x3b_en` | MinHash J ≥ 0.8 or identical text vs the English part of Slayer 1.00–1.06. | 13 | 8033 |
| 15 | `dedup_english_technical` | MinHash J ≥ 0.8 or identical text vs `SlayerLab/english-technical-1b@3b833d36`. | 0 | 0 |

Pool 1 938 345 docs / 1 667 484 804 v6 tokens. Kept after all reasons (`uzysk`): **1 614 957 docs / 1 297 285 890 v6
tokens (77.80%)**; dedup against our earlier sources (FineMath-4+, InfiWebMath-4+, SE pages) takes 20.9 percentage points.
One part (`wyniki/czesci.json`): `stackexchange_math_p01`, 1 614 957 docs, 1 297 285 890 v6 tokens.

Export (`shard.write`): 1 614 905 docs, 1 187 714 477 `token_count` (the submissions repo's counter, not v6); `dropped`:
wrong_language 52. Parquet sha256 `78f6efd26679d307acae8920e111ddc7857b2c4d461da8c9fe6697435d2bb79c`.
Contract test: 1 passed. `src/check.py`: 8 lines, only the two expected causes (Presidio rescan, no presidio record).

Positive control: no result file for this source (not measured); rules and indexes as in InfiWebMath-4+ / FineMath-4+.

Review (`wyniki/przeglad_1.json`, two independent reviewers A/B, full texts; five slices repeated after a model-provider
refusal; false-drop thresholds ≤ 10% and Wilson 95% upper bound ≤ 20%):

| Reason | n | A false drops [Wilson] | B false drops [Wilson] | Verdict A/B | Token cost (independent) |
|---|---|---|---|---|---|
| `walidacja_fabryki` | 72 | 0% [0; 5.1] | 0% [0; 5.1] | PASS/PASS | 0.004% |
| `ewal_13gram` | 100 | 95% [88.8; 97.8] | 85% [76.7; 90.7] | FAIL/FAIL | 0.47% |
| `pii` | 100 | 45% [35.6; 54.8] | 44% [34.7; 53.8] | FAIL/FAIL | 0.29% |
| `pii_zaciemniony` | 82 | 2% [0.7; 8.5] | 2% [0.7; 8.5] | PASS/PASS | 0.01% |
| `pii_at_bez_nawiasow` | 100 | 66% [56.3; 74.5] | 67% [57.3; 75.4] | FAIL/FAIL | 0.17% |
| `min_tresc` | 100 | 0% [0; 3.7] | 0% [0; 3.7] | PASS/PASS | 0.02% |
| `mojibake` | 6 | 0% [0; 39.0] | 0% [0; 39.0] | FAIL/FAIL (upper bound at n = 6) | 0.001% |
| `dedup_wewnatrz` | 100 | 0% [0; 3.7] | 0% [0; 3.7] | PASS/PASS | 0.03% |
| `dedup_finemath4` | 99 | 0% [0; 3.7] | 0% [0; 3.7] | PASS/PASS | 11.86% |
| `dedup_infiwebmath4` | 100 | 0% [0; 3.7] | 0% [0; 3.7] | PASS/PASS | 0.88% |
| `dedup_se_strony` | 100 | 0% [0; 3.7] | 0% [0; 3.7] | PASS/PASS | 19.49% |
| `dedup_slayer107` | 100 | 0% [0; 3.7] | 0% [0; 3.7] | PASS/PASS | 1.02% |
| `dedup_slayer_8x3b_en` | 17 | 0% [0; 18.4] | 0% [0; 18.4] | PASS/PASS | 0.001% |

The FAILs are accepted (annex `aneks_2026_11_26_przeglad`): `ewal_13gram` drops common expressions (identity matrix,
tan(a+b), Fibonacci) and 5–6 verbatim MATH/MathQA problems, cost 0.47%; `pii` drops theorem section numbers read as IPv4,
cost 0.29%; `pii_at_bez_nawiasow` drops phrases such as "at stats.stackexchange.com", cost 0.17%; `mojibake` 0/6 false,
failing only on the Wilson upper bound. These rules drop good text rather than let bad text through. 300 kept documents:
junk **0/300** for both reviewers (1–2 doubtful: formulas in images), PASS.

## Personal data

- Documents with an e-mail address, phone number or IPv4 address (`pii`), an obfuscated e-mail (`pii_zaciemniony`) or
  `name at domain.tld` (`pii_at_bez_nawiasow`) are dropped whole. Detector classes in the pool: e-mail 1 269, phone 34,
  IP 1 448.
- Display names of posters stay in `author` and `@nick` mentions in the text (public pseudonyms; attribution required by
  CC BY-SA). Profile links are not exported (`clean_stackexchange_math.py` keeps names only).
- The Presidio pass of `shard.write` is off (`no_masking()` in `matematyka-wspolne/eksport/src/mat_wybor.py`): its
  PhoneRecognizer masks numbers in mathematics (403 spans in 300 FineMath-4+ documents, 2026-11-24). `check.py` result:
  8 lines, only "PII left after masking" and "no presidio record".
- Review of 300 kept documents: missed PII **0/300** for both reviewers.

## Sample

- Seed `20261127`.
- Manual review (`wyniki/przeglad_1.json`): up to 100 dropped documents per reason (n in the table above) and 300 kept
  documents, full texts; two independent reviewers A and B who did not build the set. Kept documents: junk 0/300,
  missed PII 0/300, missed test items 0/300 for both.
- The inline sample generated by `src/render_sample.py` from the built shard goes in the PR description.
