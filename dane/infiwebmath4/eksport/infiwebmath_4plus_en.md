# InfiWebMath-4+ (English mathematical web text, pages outside FineMath-4+)

Part 2 of the Slayer 1B mathematics and code set (target ≈ 20B v6 tokens), one part `infiwebmath_4plus_en_p01`.
Reservation: https://github.com/slayerlabs/benchmarks-fabryka-ai/issues/346. Status: `held_for_review`.

These are mathematical web pages **not already in FineMath-4+ part 2**: every page whose normalised url, MinHash
signature (J ≥ 0.8) or normalised text matches a FineMath-4+ part 2 document was removed (`dedup_finemath4`).

Marks: **V** = verified 2026-11-25 at the cited source (URL, revision, hash, measurement); **I** = inferred.

## Source

- V: https://huggingface.co/datasets/HuggingFaceTB/finemath, revision
  `e92b25a616738fe95dc186b64dfb19f9c8525594` (same revision as FineMath-4+), config `infiwebmath-4plus` (32 parquet
  files, no access gate). Per the finemath card: the filtered English text-only portion of InfiMM-WebMath-40B
  (https://huggingface.co/datasets/Infi-MM/InfiMM-WebMath-40B @ `0fb36b9d`, paper arXiv 2409.12568), re-classified with
  the FineMath classifier (https://huggingface.co/HuggingFaceTB/finemath-classifier, MIT), kept at score ≥ 4.
- V: human web text from Common Crawl snapshots 2019–2023, extracted from HTML by InfiMM; images were removed from
  `text` (their notation is lost). Nothing generated.
- V: pool = all 32 files in a `numpy.default_rng(20261125)` permutation: 6 296 212 documents, 9 310 103 443 v6 tokens;
  sha256 of every file in `wyniki/probka_pliki.json`. Export: every document kept by the rules.
- Row id: `WARC-Record-ID` from `metadata.WARC_HEADER`; `url` present in 100% of rows (V on shard 0). There are no
  `warc_filename`/`offset` columns as in FineMath-4+.
- Tokens: v6 tokenizer (`tokenizer.json` sha256 `0640d3bd…815dd`), text tokens + 1 EOT.

## Rights review

- V: licence of the config ODC-By 1.0 + Common Crawl Terms of Use (finemath README, one licence for all configs);
  InfiMM-WebMath-40B is also ODC-By 1.0 + CC ToU and "does not alter the license of any of the underlying data".
  Both licence the compilation, not the texts; pages keep their publishers' rights; no per-row licence field.
- I: the Llama 3.1 licence does not attach: Llama-3.1-70B only produced scores for training the classifier.
- **Gate "may TRAIN": YES** (2026-11-25). Basis: TDM exception, art. 4 Directive 2019/790, for the texts; ODC-By for the
  compilation. Takedown: drop by `url` or `WARC-Record-ID` in the next version. Condition: TDM opt-out, not checked.
- **Gate "may SUBMIT": UNRESOLVED.** No per-document licence; some domains carry SA licences or restrictive terms
  (V in the sample: gradesaver, byjus, geeksforgeeks); TDM opt-out not checked.
- **Decision: `held_for_review`.** Withheld: the whole set until per-document rights are resolved.

Not checked:
- TDM opt-out (robots.txt, TDMRep) and terms of use of the top domains.
- Contents of `finemath_contamination_report` for the infiwebmath configs.
- Domain, e-mail and snapshot distribution beyond shard 0 (`KARTA_ZRODLA.md`).

## Cleaning

Rules preregistered 2026-11-25 (`skrypty/preregistracja.json`, commit `05447f8`) before download, taken from
FineMath-4+ with annexes 24.11, 24.11b, 24.11c, 25.11b, plus the new reason `dedup_finemath4`; annex 25.11c (commit
`601e1bc`, before aggregation) added `pii_at_bez_nawiasow`; annex 25.11e (commit `3c13221`, after the review, before
export) records the review result. Cascade in this order; counts from `wyniki/agreguj.json` (`kaskada`;
"independent" = documents with the reason regardless of order, `niezaleznie`).

| # | Reason | Rule | dropped docs | dropped tokens (v6) |
|---|---|---|---|---|
| 1 | `walidacja_fabryki` | 13-gram sketch ≥ 0.5, MinHash ≥ 0.8, identical text or identical url vs Fabryka validation sets. | 1968 | 2491853 |
| 2 | `domena_testow` | Page from a domain that hosts benchmark sources (wikihow, instructables, Wikimedia projects). | 46217 | 108310030 |
| 3 | `ewal_13gram` | Non-trivial 13-gram from a strict math/code test (MathQA, MMLU, GSM8K, MATH, BBH, HumanEval, MBPP, GSM-Plus, GSM1k) at any df, or from another of ~60 tests at df < 5. | 74411 | 223125410 |
| 4 | `pii` | E-mail, phone number or IPv4 address found → document dropped. | 105498 | 354221501 |
| 5 | `pii_zaciemniony` | Obfuscated e-mail (`name(AT)domain(DOT)tld`) → document dropped. | 2733 | 6310070 |
| 6 | `pii_at_bez_nawiasow` | E-mail written as `name at domain.tld` without brackets → document dropped (annex 2026-11-25c). | 33686 | 141360017 |
| 7 | `min_tresc` | Fewer than 50 normalised words. | 42737 | 3728135 |
| 8 | `mojibake` | ≥ 3 matches of a strict mojibake regex. | 20761 | 93153939 |
| 9 | `dedup_wewnatrz` | Identical normalised text or MinHash (5-grams, 128 perm., LSH 32×4) J ≥ 0.8 within the pool (many crawl snapshots of the same page). | 2372245 | 3625482832 |
| 10 | `dedup_finemath4` | Identical normalised url, MinHash J ≥ 0.8 or identical text vs documents selected for export in FineMath-4+ part 2 (page already in FineMath-4+). | 2156847 | 3112315778 |
| 11 | `dedup_slayer107` | 13-gram sketch ≥ 0.5 or MinHash ≥ 0.8 vs Slayer 1.07 English data. | 226479 | 278871641 |
| 12 | `dedup_slayer_8x3b_en` | MinHash J ≥ 0.8 or identical text vs the English part of Slayer 1.00–1.06 (`SlayerLab/slayer-pl-8x3b@d50df04a` `shared/en.parquet`). | 3571 | 4173754 |
| 13 | `dedup_english_technical` | MinHash J ≥ 0.8 or identical text vs `SlayerLab/english-technical-1b@3b833d36` (1.08 data). | 2 | 10294 |
| 14 | `dedup_fineweb_edu_109` | Identical normalised url vs FineWeb-Edu urls in `SlayerLab/Slayer1B-Dataset@2d248a17` (1.09). | 182030 | 214563336 |

Pool 6 296 212 docs / 9 310 103 443 v6 tokens. Kept after all reasons (`uzysk`): **1 027 027 docs / 1 141 984 853 v6
tokens (12.27%)**. Most of the loss is deduplication: within the pool (38.9% of pool tokens in the cascade, 43.3%
independently; 1 503 028 identical texts and 1 018 778 MinHash matches) and against FineMath-4+ part 2 (a further 33.4%
in the cascade, 63.2% independently). One part (`wyniki/czesci.json`): `infiwebmath_4plus_en_p01`, 1 027 027 docs,
1 141 984 853 v6 tokens.

Export (`shard.write`): 1 025 440 docs, 1 049 426 401 `token_count` (the submissions repo's counter, not v6); `dropped`:
wrong_language 1 515, min_chars 72. Parquet sha256 `b854ae40fd66dbaf9509614f65db5c14d3d601a82587ff55b2731ddc6af5bbec`.
Contract test: 1 passed. `src/check.py`: 21 lines, only the two expected causes (Presidio rescan, no presidio record).

Positive control: not run on this source; rules and indexes are the same as for FineMath-4+, whose positive control
passed 19/19 (`dane/finemath4/wyniki/kontrola.json`).

Review (`wyniki/przeglad_1.json`, 1610 items, two independent reviewers A/B reading full texts; false-drop thresholds
≤ 10% and Wilson 95% upper bound ≤ 20%; `dedup_finemath4` judged with its FineMath-4+ pair from
`matematyka-wspolne/skrypty/para_wlasne.py`; a first judgement without the pair was discarded):

| Reason | n | A false drops [Wilson] | B false drops [Wilson] | Verdict A/B | Token cost (independent) |
|---|---|---|---|---|---|
| `walidacja_fabryki` | 100 | 9% [4.8; 16.2] | 0% [0; 3.7] | PASS/PASS | 0.03% |
| `domena_testow` | 100 | 0% [0; 3.7] | 0% [0; 3.7] | PASS/PASS | 1.17% |
| `ewal_13gram` | 100 | 42% [32.8; 51.8] | 44% [34.7; 53.8] | FAIL/FAIL | 2.44% |
| `pii` | 100 | 15% [9.3; 23.3] | 4% [1.6; 9.8] | FAIL/PASS | 3.97% |
| `pii_zaciemniony` | 100 | 4% [1.6; 9.8] | 1% [0.2; 5.4] | PASS/PASS | 0.08% |
| `pii_at_bez_nawiasow` | 100 | 80% [71.1; 86.7] | 34% [25.5; 43.7] | FAIL/FAIL | 1.71% |
| `min_tresc` | 100 | 0% [0; 3.7] | 0% [0; 3.7] | PASS/PASS | 0.04% |
| `mojibake` | 100 | 0% [0; 3.7] | 0% [0; 3.7] | PASS/PASS | 1.23% |
| `dedup_wewnatrz` | 100 | 0% [0; 3.7] | 0% [0; 3.7] | PASS/PASS | 43.31% |
| `dedup_finemath4` | 100 | 0% [0; 3.7] | 0% [0; 3.7] | PASS/PASS | 63.21% |
| `dedup_slayer107` | 100 | 0% [0; 3.7] | 0% [0; 3.7] | PASS/PASS | 6.32% |
| `dedup_slayer_8x3b_en` | 100 | 0% [0; 3.7] | 0% [0; 3.7] | PASS/PASS | 0.19% |
| `dedup_english_technical` | 10 | 0% [0; 27.8] | 0% [0; 27.8] | FAIL/FAIL (upper bound at n = 10) | 0.00% |
| `dedup_fineweb_edu_109` | 100 | 0% [0; 3.7] | 0% [0; 3.7] | PASS/PASS | 8.24% |

The FAILs are accepted (annex 2026-11-25e): `ewal_13gram` drops formulae, Asymptote code and Python idioms (fix
deferred); `pii` false drops are digits of π, ISBNs and chapter numbers read as IPs, and 46–57% of hits lie beyond the
visible 3000 characters; `pii_at_bez_nawiasow` drops phrases such as "here at Shaalaa.com" — privacy takes priority
for both; `dedup_english_technical` has 0/10 false drops and fails only on the Wilson upper bound of a tiny population.
These rules drop good text rather than let bad text through.

Review of 300 kept documents: junk **8.7% [6.0; 12.4]** (A, PASS) and **10.3% [7.4; 14.3]** (B, FAIL of the 10%
threshold). Accepted (annex 2026-11-25e): junk (SEO spam, pages without mathematics, formulas lost in extraction) at
≈ 9–10% is a property of the source, as for FineMath-4+; a quality filter is deferred.

## Personal data

- Our filters drop the whole document when it contains an e-mail address, phone number or IPv4 address (`pii`), an
  obfuscated e-mail such as `name(AT)domain` (`pii_zaciemniony`) or `name at domain.tld` (`pii_at_bez_nawiasow`).
  This is the only PII protection. Detector classes in the pool: e-mail 83 361, phone 14 053, IP 15 457.
- `metadata.WARC_HEADER` holds the server IP (not a person's); only `WARC-Record-ID` and `WARC-Date` are taken from it.
- Forum nicknames and signatures may remain (not detected by these rules).
- The Presidio pass of `shard.write` is **off** for this source, as for FineMath-4+ (`no_masking()` in
  `matematyka-wspolne/eksport/src/mat_wybor.py`): on 2026-11-24 Presidio's PhoneRecognizer tagged 403 spans in 300
  FineMath-4+ documents, almost all of them numbers in the mathematics itself, so masking would destroy the training
  signal. The `pii` record of `stats.json` stores `"pass": "none"` and this reason; `src/check.py`'s Presidio rescan is
  therefore expected to report a mismatch (result for this source: 21 lines of that kind, nothing else).
- Review of 300 kept documents: missed PII **0/300** for both reviewers.

## Sample

- Seed `20261125` (file permutation).
- Manual review: 100 dropped documents per reason (10 for `dedup_english_technical`, all there were) and 300 kept
  documents, 1610 items in total; two independent reviewers A and B who did not build the set, full texts; Wilson 95%
  intervals as above. Kept documents: missed PII 0/300 and missed test items 0/300 for both.
- The inline sample generated by `src/render_sample.py` from the built shard goes in the PR description.
