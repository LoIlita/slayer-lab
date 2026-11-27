# Stack-Edu Python (Common Pile v0.1, permissively licensed)

Part 2: the full Python pool of Stack-Edu for the combined set (target ≈ 20B v6 tokens), exported as five parts
`stack_edu_python_p01` … `stack_edu_python_p05`. Reservation: https://github.com/slayerlabs/benchmarks-fabryka-ai/issues/346.
Part 1 (arm D of the Slayer 1B microanneal) is described at the end of `## Cleaning`; it is a subset of part 2's pool
and **must not be added to part 2 in training**.

Marks: **V** = verified 2026-11-24/25 at the cited source (URL, revision, hash); **I** = inferred.

## Source

- V: https://huggingface.co/datasets/common-pile/stackv2_edu_filtered, revision
  `c354dbe88469a1153e97c6a63ac50591849654de` (97 `stack-edu-NNNN.json.gz` files, no access gate). Publisher Common
  Pile (EleutherAI et al.); paper Kandpal et al. 2025, https://arxiv.org/abs/2506.05209; code
  https://github.com/r-three/common-pile. "Edu" classifiers from SmolLM2 (https://arxiv.org/abs/2502.02737).
- V: the README at this revision describes raw Stack V2, not this subset; there is no own dataset card.
- V: whole source files from GitHub (Software Heritage / Stack v2), filtered by RedPajama V1 code heuristics and
  SmolLM2 "edu" classifiers at a lower threshold. Python rows (`metadata.language == "Python"`) are in files
  0073–0084.
- V: pool of part 2 = all 12 Python files 0073–0084 (same `numpy.default_rng(20261124)` permutation as part 1):
  7 218 355 Python rows, 11 140 913 173 v6 tokens; sha256 of every file in `wyniki/cz2/probka_pliki.json`. Export: all
  files kept by the rules.
- Row id `id` (= `blob_id`); source url `metadata.url` =
  `https://raw.githubusercontent.com/{repo_name}/{revision_id}{path}`.
- Tokens: v6 tokenizer (`tokenizer.json` sha256 `0640d3bd…815dd`), text tokens + 1 EOT.

## Rights review

- V: licence per file = `metadata.license` (one or more SPDX ids, detected by Stack v2 at repository level). In the
  Python of file 0084 (174 868 rows), all non-empty ids are on the Blue Oak Council list (v16, 225 licences);
  0.50% of rows have an empty `license` and only a repo licence in `gha_license_id`.
- V: no compilation licence on the HF repo (`cardData.license` = null). Common Pile's card warns that "license
  laundering and inaccurate metadata" can assign a wrong licence.
- I: the licence is the repository's, not necessarily the file's (vendored code, pasted snippets).
- **Gate "may TRAIN": YES** (V, 2026-11-24). Basis: per-file permissive licence (Blue Oak list); fallback TDM
  exception, art. 4 Directive 2019/790. Takedown: drop by `id` or `repo_name` in the next version.
- **Gate "may SUBMIT": YES, conditionally**: only rows with a non-empty permissive `metadata.license` (per-document
  licence, no NC/ND). Rows with an empty `license` are dropped (`licencja` rule). Attribution (MIT, BSD, Apache
  notices) is kept through `metadata.url`, `repo_name` and `license` in each row.
- **Decision: `admitted`** for rows passing the `licencja` rule; withheld: rows with an empty licence or a
  non-permissive `license_type`.
- Exported licences (top, part 2 total): MIT 2 460 101, Apache-2.0 573 192, BSD-3-Clause 224 976, BSD-2-Clause
  75 616, Unlicense 48 516, CC0-1.0 24 234, ISC 10 175.

Not checked:
- Whether all 12 Python files have only Blue Oak licences (the licence list was checked on file 0084; the `licencja`
  rule drops empty and non-permissive rows in all files).
- Stack v2 licence detection details (`bigcode/the-stack-v2` card is gated, not read) and the exact "edu" threshold
  used by Common Pile.
- TDM opt-out and "Am I in the Stack" opt-outs after the Software Heritage snapshot.
- Whether the repository licence matches each file (vendoring, copies from other projects).
- Decontamination against code tests by Common Pile/SmolLM2.
- Overlap with Slayer 1.08b data (self-oss-instruct, OpenCodeReasoning).
- `revision_date` as a filter for LLM-written code.

## Cleaning

Rules preregistered 2026-11-24 (`skrypty/preregistracja.json`) before any count, with annexes; part 2
(`czesc_2`, written 2026-11-25 before downloading the remaining files, commit `380e7f0`) keeps them unchanged.
Applied as a cascade in this order; counts from `wyniki/cz2/agreguj.json` (`kaskada`; "independent" = documents
with the reason regardless of order, `niezaleznie`).

| # | Reason | Rule | dropped docs | dropped tokens (v6) |
|---|---|---|---|---|
| 1 | `licencja` | Empty `metadata.license` or `license_type` ≠ `permissive` → row dropped. | 37976 | 59580580 |
| 2 | `walidacja_fabryki` | 13-gram sketch ≥ 0.5, MinHash ≥ 0.8, identical text or identical url vs Fabryka validation sets. | 19198 | 9983175 |
| 3 | `ewal_13gram` | Non-trivial 13-gram from a strict math/code test (MathQA, MMLU, GSM8K, MATH, BBH, HumanEval, MBPP, GSM-Plus, GSM1k) at any df, or from another of ~60 tests at df < 5. | 5930 | 14665069 |
| 4 | `sekrety` | AWS key, Google API key, private key block, Slack or GitHub token pattern → file dropped. | 3254 | 15450727 |
| 5 | `haslo_w_kodzie` | Hard-coded `password`/`passwd`/`pwd` string literal of ≥ 4 chars → file dropped (annex 2026-11-24c). | 43141 | 85495814 |
| 6 | `wygenerowany` | "auto-generated", "generated by" or "do not edit" in the first 1000 characters → file dropped. | 44529 | 150438674 |
| 7 | `min_tresc` | Fewer than 50 normalised words (empty `__init__.py`, licence-only files; annex 2026-11-24b). | 450825 | 41463792 |
| 8 | `int_score` | Edu classifier `int_score` < 3 (SmolLM2 threshold). Independent: 54.3% of tokens. | 2974444 | 5796572174 |
| 9 | `mojibake` | ≥ 3 matches of a strict mojibake regex. | 404 | 1855568 |
| 10 | `dedup_wewnatrz` | Identical normalised text or MinHash (5-grams, 128 perm., LSH 32×4) J ≥ 0.8 within the whole part 2 pool (includes part 1). | 4204 | 6515276 |
| 11 | `dedup_slayer107` | 13-gram sketch ≥ 0.5 or MinHash ≥ 0.8 vs Slayer 1.07 English data. | 4502 | 2070622 |
| 12 | `dedup_slayer_8x3b_en` | MinHash J ≥ 0.8 or identical text vs the English part of Slayer 1.00–1.06, `SlayerLab/slayer-pl-8x3b@d50df04a` `shared/en.parquet` (sha256 `f3d451b7…`, 2 384 000 docs; annex 2026-11-25b). | 12 | 10560 |
| 13 | `dedup_english_technical` | MinHash J ≥ 0.8 or identical text vs `SlayerLab/english-technical-1b@3b833d36` (1.08 data, includes code). | 140 | 249311 |
| 14 | `dedup_fineweb_edu_109` | Identical normalised url vs FineWeb-Edu urls in `SlayerLab/Slayer1B-Dataset@2d248a17` (kept for uniformity). | 0 | 0 |

Pool 7 218 355 docs / 11 140 913 173 v6 tokens. Kept after all reasons (`uzysk`): **3 629 796 docs /
4 956 561 831 v6 tokens (44.49%)**; `int_score` < 3 takes most of the loss.

Parts (`wyniki/cz2/czesci.json`, `matematyka-wspolne/skrypty/czesci.py`): five parts of ≈ 0.99B v6 tokens each.

| key | docs | v6 tokens | parquet sha256 |
|---|---|---|---|
| `stack_edu_python_p01` | 722 555 | 991 310 853 | `8e0a40ab3d829ab526ac4b499cad4a13cd101af02ef3fd4e249cf9c8e46c7c9d` |
| `stack_edu_python_p02` | 729 634 | 991 312 955 | `0a2a596e3e30c0bf69ab4d85fae665194c912dd7e375c9733b14c98ee4bfa66c` |
| `stack_edu_python_p03` | 728 181 | 991 312 869 | `582896c2bb8ff00c5e288fd96163e2e65b7ccee9fae47a661396437ce4705c09` |
| `stack_edu_python_p04` | 726 339 | 991 308 269 | `2455ab6a61c849f41d42c09a300b285409b47610eda611c8ac58c1614ec5afca` |
| `stack_edu_python_p05` | 723 087 | 991 316 885 | `ccfb85dbd6dd2d13e7e133f6b193229f43932c722a32cf36766be5f108d8cf8f` |

Docs and v6 tokens above are the selection before `shard.write`. Export of all five parts (`eksport_czesci.sh`):
**3 516 755 docs, 3 744 422 806 tokens** by the submissions repo counter (`token_count`, a different tokenizer from
v6); 113 041 rows dropped by the `shard.write` language gate (3 629 796 − 113 041 = 3 516 755); 185 412 e-mails
masked to `[PII]` before the language gate. Each part: contract test 1 passed.

Review of dropped documents (part 1 sample, rules unchanged in part 2; 100 per reason, two reviewers A/B,
false-drop thresholds ≤ 10% and Wilson 95% upper bound ≤ 20%; `wyniki/przeglad_odrzuconych_1.json`):

| Reason | A false drops [Wilson] | B false drops [Wilson] | Verdict | Token cost (part 1) |
|---|---|---|---|---|
| `licencja` | 0% [0; 3.7] | 0% [0; 3.7] | PASS | 0.54% |
| `walidacja_fabryki` | 49% [39.4; 58.7] | 0% [0; 3.7] | FAIL (A) | 0.09% |
| `ewal_13gram` | 88% [80.2; 93.0] | 85% [76.7; 90.7] | FAIL | 0.15% |
| `sekrety` | 16% [10.1; 24.4] | 13% [7.8; 21.0] | FAIL | 0.10% |
| `wygenerowany` | 34% [25.5; 43.7] | 34% [25.5; 43.7] | FAIL | 1.38% |
| `int_score` | 0% [0; 3.7] | 0% [0; 3.7] | PASS | 54.48% |
| `mojibake` | 1.7% [0.3; 9.1] | 0% [0; 6.2] | PASS | 0.10% |
| `dedup_wewnatrz` | 0% [0; 4.8] | 0% [0; 4.8] | PASS | 0.01% |
| `dedup_slayer107` | 0% [0; 3.7] | 0% [0; 3.7] | PASS | 0.12% |
| `dedup_english_technical` | 0% [0; 15.5] | 0% [0; 15.5] | PASS | 0.003% |

The precision FAILs are accepted unchanged (annex 2026-11-24b): these rules drop good code rather than let bad code
through, at ≈ 1.7% of tokens in total. Causes: `walidacja_fabryki` matches shared licence headers, `ewal_13gram`
matches code idioms (loops, `Node` classes, bubble sort), `wygenerowany` matches the phrase in comments, `sekrety`
matches example keys from documentation. A review of dropped documents on the part 2 pool was not run.

Review of 300 kept documents in part 1 (`wyniki/przeglad_zachowanych_1.json`): junk 0.3% [0.1; 1.9] (A) and 0.7%
[0.2; 2.4] (B), PASS; missed tests 0/300, PASS; missed secret 1/300 for both reviewers (a local database password in
a `connect` call), FAIL of the 0 threshold → rule `haslo_w_kodzie` (annex 2026-11-24c).

**Part 1 (historical, microanneal arm D).** Pool `stack-edu-0080.json.gz` only (639 779 rows, 988 588 081 v6
tokens), same rules; kept 321 688 docs / 439 111 541 v6 tokens (44.418%); export target 250M v6 tokens: 186 072
docs selected, exported 180 275 docs, 188 819 386 tokens (cl100k), `wrong_language` 5797, 9 484 e-mails masked;
key `stack_edu_python`, parquet sha256 `4ccfbb8c3e483192545a2264cb813c88d21bfd5e4f9abd5b525884fdeadd2d83`; positive
control 22/22 (`wyniki/kontrola.json`). File 0080 is also in part 2's pool and `dedup_wewnatrz` runs over the whole
pool, so part 1 is a subset of part 2: do not train on both. Rebuilt 2026-11-27 after annex
`aneks_2026_11_27_zaciemnione`: the same ids in the same order taken from the re-exported `stack_edu_python_p01`
(`source` kept as `stack_edu_python`; `matematyka-wspolne/skrypty/przebuduj_ramie.py`, `wyniki/mikroanneal_aneks.json`):
91 files changed (109 obfuscated addresses → `[PII]`), other columns identical except `token_count` in those rows;
**180 275 docs, 188 818 786 tokens (cl100k)**, 9 593 e-mails masked, parquet sha256
`c928eaec8101cdb6d69808a2280ff613ccd4b3e2cf956568227a8e0200d2f901`.

## Personal data

- Files are dropped whole for secrets: recognisable key formats (`sekrety`; part 2 by class: Google API key 2013,
  private key 566, AWS key 443, Slack token 225, GitHub token 39) and hard-coded passwords (`haslo_w_kodzie`).
- E-mail addresses are masked, not dropped (code with an author's address is good code): plain addresses and the
  `name(AT)domain(DOT)tld` form are replaced with `[PII]` using the slayer-lab detector's patterns, example domains
  excepted, **before** `shard.write` (`premask_emails` in `src/mat_wybor.py`), so the language gate sees the same text
  that `src/check.py` checks. Part 2: 185 412 e-mails masked. Phone numbers and IPs are only counted by our detector,
  not masked.
- The Presidio pass of `shard.write` is **off** for this source: measured on 2026-11-24, Presidio's PhoneRecognizer
  tagged 403 spans in 300 FineMath-4+ documents, almost all of them numbers, and code is equally dense in numeric
  literals, so masking would corrupt the code. The `pii` record of each part's `stats.json` stores
  `"pass": "regex e-mail only, before the language gate"` and this reason.
- Consequently `src/check.py` exits 1 for each part only with the expected lines ("PII left after masking" from the
  Presidio rescan and "stats.json pii has no presidio record"): p01 15, p02 13, p03 16, p04 9, p05 17 lines. Hit types
  were checked on 2026-11-25 on part 1 (local or example IP addresses in code, a `{LOGIN_INFO}@github.com` template,
  constants and hashes; no real personal data); not checked per hit for part 2.
- Control sample of 200 kept files of part 2: missed secrets, PII and test items 0/200 for both reviewers (see
  `## Sample`).

## Sample

- Seed `20261124` (file permutation).
- Part 2 control sample: 200 kept files from the part 2 selection, `default_rng(seed+3)`, two independent reviewers
  A and B, both declared reading the full 3000 characters (`wyniki/cz2/przeglad_kontrolny.json`): missed secrets
  **0/200**, missed PII **0/200**, missed test items **0/200** for both; quality "yes" 196/200 (A, 4 doubtful) and
  195/200 (B, 5 doubtful). Card numbers in item 6015718 are public payment-gateway test numbers (comment "test card
  numbers"), checked 2026-11-25.
- Part 1 manual review: 100 dropped files per reason and 300 kept files, first 3000 characters each; two independent
  reviewers A and B who did not build the set; Wilson 95% intervals as above. Part 1 control sample of 200 kept
  files, `default_rng(seed+2)`: missed secrets 0/200 and missed test items 0/200 for both.
- The inline sample generated by `src/render_sample.py` from the built shard goes in the PR description.
