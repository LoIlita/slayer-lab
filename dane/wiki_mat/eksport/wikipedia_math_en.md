# English Wikipedia and Wikibooks: mathematics articles

Part 3 of the Slayer 1B mathematics and logic set (#357): mathematics articles of English Wikipedia and Wikibooks from
the Common Pile Wikimedia dump, one document per article. Key `wikipedia_math_en`, one part `wikipedia_math_en_p01`.
Reservation: https://github.com/slayerlabs/benchmarks-fabryka-ai/issues/357 (source card filed under #346).

Articles already present as web pages in FineMath-4+ part 2, InfiWebMath-4+ or FineWeb-Edu 1.09 were removed
(`dedup_finemath4`, `dedup_infiwebmath4`, `dedup_fineweb_edu_109`).

Marks: **V** = verified 2026-11-26 at the cited source (URL, revision, hash, measurement); **I** = inferred.

## Source

- V: https://huggingface.co/datasets/common-pile/wikimedia, revision `781b263a6546515543bec3968ad4743fbc152b72`: 187
  `NNNNN_wikipedia.com.jsonl.gz` and 2 `NNNNN_wikibooks.com.jsonl.gz` files (sha256 of all 189 in
  `wyniki/przeglad_zrodla.json` and `wyniki/budowa.json`). Per the card: March 2025 dumps, latest revision of each page,
  wikitext rendered to text with wiki math converted to LaTeX. Paper https://arxiv.org/abs/2506.05209.
- Selection (rule 1 of the source card, preregistered): namespace 0 (articles); ≥ 10 `$…$` segments with `\ ^ _ =`
  and ≥ 5 LaTeX commands; mathematics vocabulary in the first 700 characters more than twice the vocabulary of other
  sciences (`skrypty/wiki_rules.py`). Measured precision (manual, "is it mathematics or logic"): 52/60 = 86.7% (Wilson
  95% 76–93%); the rest is mostly physics or engineering (I: acceptable as applied mathematics). Articles on logic and
  synthetic geometry with few formulas are systematically missed (recall on 20 core articles: 16/20).
- Normalisation (`skrypty/buduj_pule.py`, no models): `html.unescape`, removal of `{{Infobox …}}` blocks, collapse of
  blank lines.
- V: pool (`wyniki/budowa.json`, `wyniki/probka_pliki.json`): **9 990 documents, 30 824 027 v6 tokens**: Wikipedia
  8 521 / 26 769 474, Wikibooks 1 469 / 4 054 553; build filter (licence, exact duplicates) dropped 0.
- Row id `<wiki>:<source id>`; `url` `https://en.wikipedia.org/wiki/<Title>` or `https://en.wikibooks.org/wiki/<Title>`
  (canonical host, so that url dedup matches web sources); `author` = editor logins.
- Tokens: v6 tokenizer (`tokenizer.json` sha256 `0640d3bd…815dd`), text tokens + 1 EOT.

## Rights review

- V: `metadata.license` = CC BY-SA 4.0 in 9 990 / 9 990 rows ("Official Wikimedia wikis are released under a CC BY-SA
  license", Common Pile card). No NC/ND.
- **Commercial use: allowed.** CC BY-SA 4.0 permits commercial use; share-alike applies to redistribution of the data
  itself, which must stay under CC BY-SA 4.0. Attribution: article `url` and editor logins (`author`).
- I: a TDM opt-out does not matter when the basis is the licence; Wikimedia robots.txt not checked.
- **Gate "may TRAIN" (including commercial use): YES** (per-document licence). Takedown: drop by `id` / title.
- **Gate "may SUBMIT": YES** (CC BY-SA 4.0 per document, no NC/ND; SA and attribution kept in the export).
- **Decision: `admitted`.**

Not checked:
- Share of text edited with LLM help in 2023–2025 revisions.
- Wikimedia robots.txt / TDMRep.
- Recall of the selection rule beyond 20 control articles; precision on Wikibooks separately.

## Cleaning

Rules preregistered 2026-11-26 (`skrypty/preregistracja.json`) before building the pool, taken from InfiWebMath-4+ with
annexes 24.11, 24.11b, 24.11c, 25.11b, 25.11c, 25.11e; departures: Wikimedia dump with rule 1 instead of a quality
classifier, `domena_testow` without the "Wikimedia projects" rule (it would drop 100%; machine form in
`domena_testow_wylaczone`: wikipedia.org, wikinews.org, wikivoyage.org, wikibooks.org; test leaks from Wikipedia are
caught by `ewal_13gram`), added `dedup_infiwebmath4` and `dedup_fineweb_edu_109`, build filter before the detectors.
Annex `aneks_2026_11_26_przeglad` (after the review, before export) records the review result. Cascade in this order;
counts from `wyniki/agreguj.json` (`kaskada`; "independent" = documents with the reason regardless of order).

| # | Reason | Rule | dropped docs | dropped tokens (v6) |
|---|---|---|---|---|
| 1 | `walidacja_fabryki` | 13-gram sketch ≥ 0.5, MinHash ≥ 0.8, identical text or identical url vs Fabryka validation sets. | 1 | 536 |
| 2 | `domena_testow` | Domain hosting benchmark sources (without Wikimedia projects). | 0 | 0 |
| 3 | `ewal_13gram` | Non-trivial 13-gram from a strict math/code test at any df, or from another of ~60 tests at df < 5. | 200 | 999883 |
| 4 | `pii` | E-mail, phone number or IPv4 address → document dropped. | 8 | 59837 |
| 5 | `pii_zaciemniony` | Obfuscated e-mail → document dropped. | 0 | 0 |
| 6 | `pii_at_bez_nawiasow` | `name at domain.tld` → document dropped. | 3 | 6305 |
| 7 | `min_tresc` | Fewer than 50 normalised words. | 0 | 0 |
| 8 | `mojibake` | ≥ 3 matches of a strict mojibake regex. | 0 | 0 |
| 9 | `dedup_wewnatrz` | Identical normalised text or MinHash (5-grams, 128 perm., LSH 32×4) J ≥ 0.8 within the pool. | 86 | 100815 |
| 10 | `dedup_finemath4` | Identical normalised url, MinHash J ≥ 0.8 or identical text vs FineMath-4+ part 2. | 72 | 218577 |
| 11 | `dedup_infiwebmath4` | Same vs InfiWebMath-4+. | 230 | 628899 |
| 12 | `dedup_slayer107` | 13-gram sketch ≥ 0.5 or MinHash ≥ 0.8 vs Slayer 1.07 English data. | 361 | 1385742 |
| 13 | `dedup_slayer_8x3b_en` | MinHash J ≥ 0.8 or identical text vs the English part of Slayer 1.00–1.06. | 1 | 2615 |
| 14 | `dedup_english_technical` | MinHash J ≥ 0.8 or identical text vs `SlayerLab/english-technical-1b@3b833d36`. | 0 | 0 |
| 15 | `dedup_fineweb_edu_109` | Identical normalised url vs FineWeb-Edu urls in `SlayerLab/Slayer1B-Dataset@2d248a17` (1.09). | 2266 | 7686325 |

Pool 9 990 docs / 30 824 027 v6 tokens. Kept after all reasons (`uzysk`): **6 762 docs / 19 734 493 v6 tokens
(64.02%)**; `dedup_fineweb_edu_109` takes 24.9 percentage points (article page already in FineWeb-Edu 1.09). One part
(`wyniki/czesci.json`): `wikipedia_math_en_p01`, 6 762 docs, 19 734 493 v6 tokens.

Export (`shard.write`): 6 762 docs, 18 300 403 `token_count` (the submissions repo's counter, not v6); `dropped`: none.
Parquet sha256 `40348175d1f9276b0f3435ca847889d44940a8ea6d3c8ccb9516f0bc6fd05c6d`.
Contract test: 1 passed. `src/check.py`: 11 lines, only the two expected causes (Presidio rescan, no presidio record).

Positive control: no result file for this source (not measured); rules and indexes as in InfiWebMath-4+.

Review (`wyniki/przeglad_1.json`, two independent reviewers A/B, full texts of kept documents; slices read incompletely
were finished; false-drop thresholds ≤ 10% and Wilson 95% upper bound ≤ 20%):

| Reason | n | A false drops [Wilson] | B false drops [Wilson] | Verdict A/B | Token cost (independent) |
|---|---|---|---|---|---|
| `walidacja_fabryki` | 1 | 0% [0; 79.3] | 0% [0; 79.3] | FAIL/FAIL (upper bound at n = 1) | 0.002% |
| `ewal_13gram` | 93 | 71% [61.1; 79.2] | 68% [57.7; 76.4] | FAIL/FAIL | 3.24% |
| `pii` | 9 | 0% [0; 29.9] | 0% [0; 29.9] | FAIL/FAIL (small n) | 0.21% |
| `pii_at_bez_nawiasow` | 3 | 0% [0; 56.2] | 0% [0; 56.2] | FAIL/FAIL (small n) | 0.02% |
| `dedup_wewnatrz` | 87 | 0% [0; 4.2] | 0% [0; 4.2] | PASS/PASS | 0.33% |
| `dedup_finemath4` | 75 | 0% [0; 4.9] | 0% [0; 4.9] | PASS/PASS | 0.75% |
| `dedup_infiwebmath4` | 98 | 0% [0; 3.8] | 0% [0; 3.8] | PASS/PASS | 2.11% |
| `dedup_slayer107` | 97 | 0% [0; 3.8] | 0% [0; 3.8] | PASS/PASS | 4.57% |
| `dedup_slayer_8x3b_en` | 1 | 0% [0; 79.3] | 0% [0; 79.3] | FAIL/FAIL (upper bound at n = 1) | 0.01% |
| `dedup_fineweb_edu_109` | 100 | 0% [0; 3.7] | 0% [0; 3.7] | PASS/PASS | 29.30% |

Accepted (annex `aneks_2026_11_26_przeglad`): `ewal_13gram` false drops 66–68% (matrices, formulas), while the correct
28–31% are reading-test passages taken from Wikipedia (BoolQ, PAWS, ANLI, SQuAD2, Belebele), so the rule works as
intended here, cost 3.24%; `pii` 0/9 false in the visible text (all hits beyond it; full text: 2 real, the rest
numbers), cost 0.19%; `pii_at_bez_nawiasow` 0/3, all beyond the visible text, cost 0.02%; `walidacja_fabryki` and
`dedup_slayer_8x3b_en` 0/1. 300 kept documents: junk **1/300** for both reviewers (0.3% [0.1; 1.9]), PASS.

## Personal data

- Documents with an e-mail address, phone number or IPv4 address (`pii`), an obfuscated e-mail (`pii_zaciemniony`) or
  `name at domain.tld` (`pii_at_bez_nawiasow`) are dropped whole. Detector classes in the pool: e-mail 0, phone 0, IP 9.
- Editor logins stay in `author` (public user names; attribution required by CC BY-SA).
- The Presidio pass of `shard.write` is off (`no_masking()` in `matematyka-wspolne/eksport/src/mat_wybor.py`): its
  PhoneRecognizer masks numbers in mathematics (403 spans in 300 FineMath-4+ documents, 2026-11-24). `check.py` result:
  11 lines, only "PII left after masking" and "no presidio record".
- Review of 300 kept documents: missed PII **0/300** for both reviewers.

## Sample

- Seed `20261126`.
- Manual review (`wyniki/przeglad_1.json`): up to 100 dropped documents per reason (n in the table above) and 300 kept
  documents; two independent reviewers A and B who did not build the set. Kept documents: junk 1/300, missed PII 0/300,
  missed test items 0/300 for both.
- Selection precision (source card): 52/60 = 86.7% mathematics or logic.
- The inline sample generated by `src/render_sample.py` from the built shard goes in the PR description.
