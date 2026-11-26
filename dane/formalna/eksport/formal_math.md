# Formal mathematics libraries (Lean, Isabelle AFP, HOL Light, Metamath, Rocq, math-comp, UniMath, Agda, Stacks Project)

Part 3 of the Slayer 1B mathematics and logic set (#357): source files of nine formal mathematics libraries, one
document per file. Key `formal_math`, one part `formal_math_p01`. Reservation:
https://github.com/slayerlabs/benchmarks-fabryka-ai/issues/357.

Human-written only: mathlib4 and HOL Light are taken at revisions before the first commit that discloses LLM
authorship, and files touched by such commits are excluded in every library.

Marks: **V** = verified 2026-11-26 at the cited source (URL, revision, file, measurement); **I** = inferred.

## Source

- V: nine git repositories at pinned revisions (`dane/formalna/KARTA_ZRODLA.md`, `skrypty/preregistracja.json`):

| library | repository | revision | files | rows | v6 tokens | licence (rows) |
|---|---|---|---|---|---|---|
| mathlib4 | github.com/leanprover-community/mathlib4 | `9bed6a56` (2025-03-31) | `.lean` | 5 892 | 30 775 066 | Apache-2.0 |
| afp | github.com/isabelle-prover/mirror-afp-devel | `02fd3c6b` | `.thy` | 10 557 | 129 985 322 | BSD-3-Clause 10 238; LGPL-2.1-only 319 |
| hol_light | github.com/jrh13/hol-light | `b9a430b8` (2025-12-11) | `.ml` | 541 | 12 555 462 | BSD-2-Clause |
| setmm | github.com/metamath/set.mm | `ce7f29d6` | `set.mm`, `iset.mm` (sections) | 621 | 11 155 284 | CC0-1.0 |
| rocq_stdlib | github.com/rocq-prover/stdlib | `9657c750` | `.v` | 583 | 2 605 422 | LGPL-2.1-only |
| mathcomp | github.com/math-comp/math-comp | `656cdbcf` | `.v` | 149 | 2 776 193 | CECILL-B |
| unimath | github.com/UniMath/UniMath | `11e01f09` | `.v` | 1 659 | 10 183 276 | LicenseRef-UniMath (MIT text) |
| agda_stdlib | github.com/agda/agda-stdlib | `119d1761` | `.agda`, `.lagda.md` | 1 190 | 2 156 221 | MIT |
| stacks | github.com/stacks/stacks-project | `a04446e5` | `.tex` | 193 | 11 027 028 | GFDL-1.2-no-invariants-or-later |
| **total** | | | | **21 385** | **213 219 274** | |

- Document = one file. set.mm/iset.mm are split into Metamath sections of up to 50 000 characters, with compressed
  proofs replaced by `$= ? $.` (statements, hypotheses, definitions and comments stay); Stacks files > 1 MB are split
  on `\section`; files > 1 MB in other libraries are excluded. Excluded directories: mathlib4 `Mathlib/{Tactic,Util,Lean}`
  and `MathlibTest`, tests and helper directories, licence files, LaTeX preambles.
- `url` = `github.com/<repo>/blob/<revision>/<path>` (with `#L<from>-L<to>` for fragments); `created` = date of the last
  commit touching the file. Contract check `wyniki/kontrakt.json`: PASS (21 385 unique ids, v6 tokens recomputed).
- Tokens: v6 tokenizer (`tokenizer.json` sha256 `0640d3bd…815dd`), text tokens + 1 EOT.
- Model-written text (annexes 26.11b, 26.11c): files changed by a commit whose message discloses an AI tool (pattern in
  `skrypty/buduj_pule.py`, `AI_WZORZEC`) are excluded. On the final revisions this removes mathlib4 1 file, UniMath 49
  files (578 161 tokens); set.mm fragments "Contributed by OpenAI" / "asking Claude" are excluded (2 fragments). The pool
  built on the November 2026 revisions of mathlib4 and HOL Light was discarded (`wyniki/budowa_odrzucona_rewizje_listopad.json`).

## Rights review

- V: licence per row from the library's LICENSE, the file header or the AFP entry metadata (table above). AFP:
  `License: LGPL` in a file overrides the entry's `bsd` (57 files); HOL Light files with another licence are excluded
  (2); Stacks `introduction.tex`: GFDL 1.2 or later, no invariant sections; UniMath `LICENSE.md` is the MIT text with
  "UniMath" (I: equivalent to MIT).
- **Commercial use: allowed for every row.** Apache-2.0, BSD-2/3-Clause, MIT, CC0-1.0, CeCILL-B, LGPL-2.1 and
  GFDL-1.2 all permit commercial use. Copyleft (LGPL, GFDL) applies to redistribution of the data itself: such files
  keep their licence, and GFDL requires the licence text to accompany redistributed copies. File headers with
  copyright notices stay in the text.
- **Gate "may TRAIN": YES** (open licences without NC/ND). Takedown: drop by `url` / `path` in the next version.
- **Gate "may SUBMIT": YES** for rows with a licence from the table (per-row licence).
- **Decision: `admitted`.**

Not checked:
- LLM use not disclosed in commit messages (AFP mirror messages are terse; 0 hits there proves nothing; AFP is 61% of
  pool tokens).
- Files renamed after an AI commit (the rule does not follow renames).
- Library policies on LLM contributions; mapping of `LicenseRef-UniMath` to the licences accepted by `check.py`.
- Overlap of mathlib4 `Archive/Imo` and AFP with miniF2F/ProofNet (not in the Fabryka test index).
- HOL Light files > 1 MB excluded by the rule although hand-written (I: ≈ 6–7M v6 tokens).

## Cleaning

Rules preregistered 2026-11-26 14:23 CET (`skrypty/preregistracja.json`) before cloning, taken from InfiWebMath-4+ with
its annexes; departures: PII mode `maskuj_email_usun_telefon_ip` (as Stack-Edu), `dedup_infiwebmath4` added, no
`dedup_fineweb_edu_109` (urls are GitHub blobs), document = file. Annexes: 26.11 (licences after cloning, before the
first count), 26.11b (exclusion of files touched by disclosed AI commits), 26.11c (mathlib4 and HOL Light revisions
before AI commits), 26.11d (e-mails masked instead of dropping files; `pii_zaciemniony` and `pii_at_bez_nawiasow`
removed from the cascade), `aneks_2026_11_26_przeglad` (review result, before export). Cascade in this order; counts
from `wyniki/agreguj.json` (`kaskada`; "independent" = files with the reason regardless of order).

| # | Reason | Rule | dropped files | dropped tokens (v6) |
|---|---|---|---|---|
| 1 | `walidacja_fabryki` | 13-gram sketch ≥ 0.5, MinHash ≥ 0.8, identical text or identical url vs Fabryka validation sets. | 0 | 0 |
| 2 | `domena_testow` | Domain hosting benchmark sources. | 0 | 0 |
| 3 | `ewal_13gram` | Non-trivial 13-gram from a strict math/code test at any df, or from another of ~60 tests at df < 5. | 5 | 374277 |
| 4 | `pii` | Phone number or IPv4 address → file dropped; e-mails are masked, not dropped. | 37 | 1211156 |
| 5 | `min_tresc` | Fewer than 50 normalised words. | 576 | 49683 |
| 6 | `mojibake` | ≥ 3 matches of a strict mojibake regex. | 0 | 0 |
| 7 | `dedup_wewnatrz` | Identical normalised text or MinHash (5-grams, 128 perm., LSH 32×4) J ≥ 0.8 within the pool (copies across libraries). | 253 | 2715768 |
| 8 | `dedup_finemath4` | MinHash J ≥ 0.8 or identical text vs FineMath-4+ part 2 (no url match). | 3 | 58434 |
| 9 | `dedup_infiwebmath4` | Same vs InfiWebMath-4+. | 0 | 0 |
| 10 | `dedup_slayer107` | 13-gram sketch ≥ 0.5 or MinHash ≥ 0.8 vs Slayer 1.07 English data. | 32 | 74635 |
| 11 | `dedup_slayer_8x3b_en` | MinHash J ≥ 0.8 or identical text vs the English part of Slayer 1.00–1.06. | 0 | 0 |
| 12 | `dedup_english_technical` | MinHash J ≥ 0.8 or identical text vs `SlayerLab/english-technical-1b@3b833d36`. | 0 | 0 |

Pool 21 385 files / 213 219 274 v6 tokens. Kept after all reasons (`uzysk`): **20 479 files / 208 735 321 v6 tokens
(97.90%)**. One part (`wyniki/czesci.json`): `formal_math_p01`, 20 479 files, 208 735 321 v6 tokens.

Export (`shard.write`, rows, `token_count`, `dropped`), parquet sha256 and `src/check.py`: in progress.

Positive control: no result file for this source (not measured); planned cases in the preregistration
(`kontrole_dodatnie`).

Review (`wyniki/przeglad_1.json`, two independent reviewers A/B, full texts; dedups judged with their pair from
`matematyka-wspolne/skrypty/probka_z_parami.py`; false-drop thresholds ≤ 10% and Wilson 95% upper bound ≤ 20%):

| Reason | n | A false drops [Wilson] | B false drops [Wilson] | Verdict A/B | Token cost (independent) |
|---|---|---|---|---|---|
| `ewal_13gram` | 5 | 100% [56.6; 100] | 100% [56.6; 100] | FAIL/FAIL | 0.18% |
| `pii` | 36 | 44% [29.5; 60.4] | 44% [29.5; 60.4] | FAIL/FAIL | 0.57% |
| `min_tresc` | 100 | 0% [0; 3.7] | 0% [0; 3.7] | PASS/PASS | 0.02% |
| `dedup_wewnatrz` | 95 | 0% [0; 3.9] | 0% [0; 3.9] | PASS/PASS | 1.29% |
| `dedup_finemath4` | 3 | 0% [0; 56.2] | 0% [0; 56.2] | FAIL/FAIL (upper bound at n = 3) | 0.03% |
| `dedup_slayer107` | 49 | 0% [0; 7.3] | 0% [0; 7.3] | PASS/PASS | 0.04% |

Accepted (annex `aneks_2026_11_26_przeglad`): `ewal_13gram` 5/5 false (formulae, a Goldbach quotation), cost 0.18%;
`pii` 16/36 false (version numbers, example RFC addresses; 3 correct public institutional addresses), cost 0.57%;
`dedup_finemath4` 0/3, failing only on the Wilson upper bound. Kept files (300, stratified by library tokens, at least
20 per library): junk **3.7% [2.1; 6.4]** (A) and **3.0% [1.6; 5.6]** (B), PASS; missed test items 0/300.

## Personal data

- Author e-mails in file headers (mostly AFP theories) are masked to `[PII]` before `shard.write`
  (`premask_emails(..., bare_at=True)` in `matematyka-wspolne/eksport/src/mat_wybor.py`, called from
  `src/clean_formal_math.py`) in every form seen: `name@domain`, `name(AT)domain(DOT)tld`, `name at domain.tld`,
  `name-at-domain.tld`, `name at web de`. Files are not dropped for e-mails (annex 26.11d).
- Review of 300 kept files on the text before masking: 17/300 with an author e-mail for both reviewers; after the
  masking was extended with the forms found in the review, `matematyka-wspolne/skrypty/resztki_email.py` on the whole
  pool after masking found **0 documents with e-mail remnants out of 21 385**; the 1 131 hits of the `bare_at` patterns
  on the whole pool were reviewed: all are addresses.
- Files with a phone number or IPv4 address (DCLM-EN detector) are dropped (`pii`, 37 files). Author names stay in
  headers (attribution required by the licences).
- The Presidio pass of `shard.write` is off (`no_masking(emails=True)`): its PhoneRecognizer masks numbers in
  mathematics and code (403 spans in 300 FineMath-4+ documents, 2026-11-24). `check.py` result: in progress.

## Sample

- Seed `20261126`.
- Manual review (`wyniki/przeglad_1.json`): up to 100 dropped files per reason (n per reason in the table above),
  and 300 kept files stratified by library; full texts; two independent reviewers A and B who did not build the set.
  Kept files: junk 3.7% / 3.0%, missed test items 0/300, e-mails handled by masking (above).
- The inline sample generated by `src/render_sample.py` from the built shard goes in the PR description.
