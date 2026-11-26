# OEIS sequence entries (English, rendered as text)

Part 3 of the Slayer 1B mathematics and logic set (#357): entries of the On-Line Encyclopedia of Integer Sequences,
rendered from the OEIS source format as readable text, one document per A-number. Key `oeis_en`, one part
`oeis_en_p01`. Reservation: https://github.com/slayerlabs/benchmarks-fabryka-ai/issues/357.

Sequences whose page (`https://oeis.org/A<nr>`) is already in FineMath-4+ part 2 or InfiWebMath-4+ were removed
(`dedup_finemath4`, `dedup_infiwebmath4`), so the set holds no second version of the same page.

Marks: **V** = verified 2026-11-26 at the cited source (URL, revision, hash, measurement); **I** = inferred.

## Source

- V: https://github.com/oeis/oeisdata, revision `976b0c73e00453b1c1e6f16d83108cb9bb744c3b` (commit 2026-11-26T08:03:27Z,
  "oeis data export" by OEIS Robot); export of https://oeis.org/ in git form. Only `seq/A*/A*.seq` is used; `files/`
  (b-files, Git LFS) is not downloaded.
- V: 402 003 `.seq` files, 597 687 151 bytes, 0 UTF-8 errors (`wyniki/budowa.json`).
- Rendering (`dane/oeis/skrypty/buduj_pule.py`, deterministic parser, no models): name, first 60 terms, comments,
  formulas, examples, programs (Maple, Mathematica and others, with a language header), cross-references, author.
  Dropped fields: `%H` (links), `%I`, `%K`, `%O`, `%D` (bibliography), `%E` (extensions), `%V/%W/%X`.
- Build filter before the detectors (preregistered): no name, dead/recycled entries, no comments and no formulas,
  fewer than 200 characters without the terms line. Kept 311 925 documents, **191 127 613 v6 tokens** (median 533,
  p99 1 910, max 24 682 per document); dropped 90 078 documents (22.4%), 28 879 398 v6 tokens (13.1%): `bez_tresci`
  84 860, `krotka` 3 130, `martwa` 2 088 (`wyniki/budowa.json`, `wyniki/probka_pliki.json`).
- Row id `A<nr>`; `url` `https://oeis.org/A<nr>`; `created` = revision date for all rows.
- Tokens: v6 tokenizer (`tokenizer.json` sha256 `0640d3bd…815dd`), text tokens + 1 EOT.
- Human text written and edited by OEIS authors and editors. I: some recent comments may have been written with LLM
  help; the OEIS policy on such contributions and its enforcement were not checked.

## Rights review

- V: repository `LICENSE` at the revision: "The OEIS content is copyrighted by the OEIS Foundation, Inc. The content is
  made available under the terms of the CC-BY-SA-4.0 license"; README says the same. Licence per row `CC-BY-SA-4.0`
  in 311 925 / 311 925 rows, issued by the rights holder; no NC/ND.
- **Commercial use: allowed.** CC BY-SA 4.0 permits commercial use; share-alike applies to redistribution of the data
  itself, which must stay under CC BY-SA 4.0. Attribution: `url` per document and author names in the text.
- **Gate "may TRAIN": YES** (open licence). Takedown: drop by A-number / `url` in the next version.
- **Gate "may SUBMIT": YES** (per-document licence without NC/ND).
- **Decision: `admitted`.**

Not checked:
- TDM opt-out of oeis.org (would concern crawling the site, not the licence).
- Whether every entry (including those imported from Sloane's older books) is covered by the licence beyond the
  general `LICENSE` statement.
- OEIS policy on LLM-written contributions.

## Cleaning

Rules preregistered 2026-11-26 (`skrypty/preregistracja.json`, commit `4215d12`) before cloning, taken from
InfiWebMath-4+ with its annexes (24.11, 24.11b, 24.11c, 25.11b, 25.11c, 25.11e); departures: PII mode
`maskuj_email_usun_telefon_ip`, build filter, added `dedup_infiwebmath4`, no `dedup_fineweb_edu_109` (not web pages).
Annex `aneks_2026_11_26_przeglad` (after the review, before export) records the review result. Cascade in this order;
counts from `wyniki/agreguj.json` (`kaskada`; "independent" = documents with the reason regardless of order).

| # | Reason | Rule | dropped docs | dropped tokens (v6) |
|---|---|---|---|---|
| 1 | `walidacja_fabryki` | 13-gram sketch ≥ 0.5, MinHash ≥ 0.8, identical text or identical url vs Fabryka validation sets. | 36 | 14011 |
| 2 | `domena_testow` | Domain hosting benchmark sources. | 0 | 0 |
| 3 | `ewal_13gram` | Non-trivial 13-gram from a strict math/code test at any df, or from another of ~60 tests at df < 5. | 205 | 195012 |
| 4 | `pii` | Phone number or IPv4 address (DCLM-EN detector) → document dropped; e-mails are masked, not dropped. | 136 | 148393 |
| 5 | `pii_zaciemniony` | Obfuscated e-mail after masking (control, expected 0). | 0 | 0 |
| 6 | `pii_at_bez_nawiasow` | `name at domain.tld` after masking (control, expected 0). | 0 | 0 |
| 7 | `min_tresc` | Fewer than 50 normalised words. | 691 | 94809 |
| 8 | `mojibake` | ≥ 3 matches of a strict mojibake regex. | 0 | 0 |
| 9 | `dedup_wewnatrz` | Identical normalised text or MinHash (5-grams, 128 perm., LSH 32×4) J ≥ 0.8 within the pool. | 843 | 698542 |
| 10 | `dedup_finemath4` | Identical normalised url, MinHash J ≥ 0.8 or identical text vs FineMath-4+ part 2. | 43051 | 32029028 |
| 11 | `dedup_infiwebmath4` | Same vs InfiWebMath-4+. | 1487 | 1405761 |
| 12 | `dedup_slayer107` | 13-gram sketch ≥ 0.5 or MinHash ≥ 0.8 vs Slayer 1.07 English data. | 4009 | 2265803 |
| 13 | `dedup_slayer_8x3b_en` | MinHash J ≥ 0.8 or identical text vs the English part of Slayer 1.00–1.06. | 0 | 0 |
| 14 | `dedup_english_technical` | MinHash J ≥ 0.8 or identical text vs `SlayerLab/english-technical-1b@3b833d36`. | 0 | 0 |

Pool 311 925 docs / 191 127 613 v6 tokens. Kept after all reasons (`uzysk`): **261 467 docs / 154 276 254 v6 tokens
(80.72%)**; `dedup_finemath4` takes 16.8% of pool tokens. One part (`wyniki/czesci.json`): `oeis_en_p01`, 261 467
docs, 154 276 254 v6 tokens.

Export (`shard.write`, docs, `token_count`, `dropped`), parquet sha256 and `src/check.py`: in progress.

Positive control: no result file for this source (not measured); `buduj_pule.py` asserts the e-mail masking on lines
with `(AT)`, `@` and ` at ` before building.

Review (`wyniki/przeglad_1.json`, two independent reviewers A/B, full texts; false-drop thresholds ≤ 10% and Wilson
95% upper bound ≤ 20%):

| Reason | n | A false drops [Wilson] | B false drops [Wilson] | Verdict A/B | Token cost (independent) |
|---|---|---|---|---|---|
| `walidacja_fabryki` | 34 | 0% [0; 10.2] | 0% [0; 10.2] | PASS/PASS | 0.01% |
| `ewal_13gram` | 100 | 100% [96.3; 100] | 100% [96.3; 100] | FAIL/FAIL | 0.10% |
| `pii` | 100 | 92% [85.0; 95.9] | 92% [85.0; 95.9] | FAIL/FAIL | 0.08% |
| `min_tresc` | 100 | 0% [0; 3.7] | 0% [0; 3.7] | PASS/PASS | 0.05% |
| `dedup_wewnatrz` | 100 | 0% [0; 3.7] | 0% [0; 3.7] | PASS/PASS | 0.37% |
| `dedup_finemath4` | 100 | 0% [0; 3.7] | 0% [0; 3.7] | PASS/PASS | 16.77% |
| `dedup_infiwebmath4` | 100 | 0% [0; 3.7] | 0% [0; 3.7] | PASS/PASS | 0.74% |
| `dedup_slayer107` | 100 | 0% [0; 3.7] | 0% [0; 3.7] | PASS/PASS | 1.22% |

The FAILs are accepted (annex `aneks_2026_11_26_przeglad`): `ewal_13gram` drops formulae (Python loops, prime
lists, recurrences) and `pii` drops tiling symbols (3.4.6.4) and Knuth section numbers read as IPv4; both cost ≈ 0.1%
of tokens and drop good text rather than let bad text through. 300 kept documents: junk **0/300** for both reviewers
(Wilson upper 1.3%), PASS.

## Personal data

- Author e-mails (mostly `name(AT)domain.com` in old entries) are removed at build time: 13 744 obfuscated, 12 plain
  and 18 `name at domain` matches; 0 / 0 / 0 left in the pool (`wyniki/budowa.json`). They are masked again to
  `[PII]` before `shard.write` (`premask_emails` in `matematyka-wspolne/eksport/src/mat_wybor.py`, called from
  `src/clean_oeis_en.py`).
- Documents with a phone number or IPv4 address (DCLM-EN detector) are dropped (`pii`): 136 documents (IP 129,
  phone 7 in the pool), almost all of them sequences of numbers, not personal data (review above).
- Author names stay in the text as required attribution (CC BY-SA); `_Name_` markers are unwrapped outside program
  lines.
- The Presidio pass of `shard.write` is off (`no_masking(emails=True)`): its PhoneRecognizer masks numbers in
  mathematical text (403 spans in 300 FineMath-4+ documents, 2026-11-24). `check.py` result: in progress.
- Review of 300 kept documents: missed PII **0/300** for both reviewers.

## Sample

- Seed `20261126`.
- Manual review (`wyniki/przeglad_1.json`): up to 100 dropped documents per reason (34 for `walidacja_fabryki`, all
  there were) and 300 kept documents, full texts; two independent reviewers A and B who did not build the set; one
  slice of reviewer A was repeated after an incomplete read. Kept documents: junk 0/300, missed PII 0/300, missed test
  items 0/300 for both.
- The inline sample generated by `src/render_sample.py` from the built shard goes in the PR description.
