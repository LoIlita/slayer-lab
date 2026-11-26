# Open textbooks: mathematics and statistics (LibreTexts, PressBooks)

Part 3 of the Slayer 1B mathematics and logic set (#357): chapters and sections of open mathematics and statistics
textbooks from LibreTexts and PressBooks (Common Pile), one document per page or chapter. Key `open_textbooks_math_en`,
one part `open_textbooks_math_en_p01`. Reservation: https://github.com/slayerlabs/benchmarks-fabryka-ai/issues/357
(source card filed under #346).

OpenStax-derived chapters are **excluded** (see `## Rights review`). Pages already present in FineMath-4+ part 2,
InfiWebMath-4+ or FineWeb-Edu 1.09 were removed.

Marks: **V** = verified 2026-11-26 at the cited source (URL, revision, hash, measurement); **I** = inferred.

## Source

- V: C1 https://huggingface.co/datasets/common-pile/libretexts @ `d4ce4b1edf95888b24992db3bbb2ae8e2bf6c22f`,
  `00000_libretext.json.gz` (sha256 `eee45504…c984`); C2 https://huggingface.co/datasets/common-pile/pressbooks @
  `29fa162fc78277b160a7010f18086b5189ffb761`, `00000_pressbooks.json.gz` (`67d1135a…9ff21`) and `00001_pressbooks.json.gz`
  (`cd3a4846…7c41`). Common Pile v0.1, https://arxiv.org/abs/2506.05209; texts collected from the HTML pages (03.2025).
  OERCommons (C3) rejected: selection precision 11/20 and 8/20.
- Selection (preregistered): C1 pages of `math.libretexts.org` and `stats.libretexts.org`; C2 books with a mathematics
  keyword in the book url or title and ≥ 3 LaTeX matches in the text (`skrypty/podr_pass.py`). Manual precision 20/20 for
  C1 and 20/20 for C2 (Wilson 95% 0.84–1.00).
- Normalisation (`skrypty/buduj_pule.py`, no models): LibreTexts navigation "Last updated Save as PDF Page ID" removed;
  PressBooks `[latex]x[/latex]` → `\(x\)`; blank lines collapsed.
- Build filter (preregistered, in this order): licence outside the SPDX map or NC/ND (0), exact duplicate (C1 515 /
  1 654 348 tokens; C2 1 293 / 8 937 721 — the same chapter under several `#chapter-…-section-N` ids), shorter than
  600 v6 tokens (C1 2 053 / 552 348; C2 34 / 14 703: tables of contents), OpenStax (C1 1 228 / 6 571 450; C2 206 /
  1 858 392).
- V: pool (`wyniki/budowa.json`, `wyniki/probka_pliki.json`): selected before the filter C1 9 733 / 31 638 141 and C2
  2 415 / 14 373 361; kept **6 819 documents, 26 422 540 v6 tokens** (C1 5 937 / 22 859 995; C2 882 / 3 562 545).
- Row id = source id (section url with fragment); `url` = id without the fragment; `author` from the source metadata.
- Tokens: v6 tokenizer (`tokenizer.json` sha256 `0640d3bd…815dd`), text tokens + 1 EOT.

## Rights review

- V: licence per row from `metadata.license`, mapped to SPDX (pool rows / v6 tokens): CC-BY-4.0 4 240 / 17 950 232,
  CC-BY-SA-4.0 1 611 / 5 496 494, GFDL-1.3-or-later 384 / 1 003 229, CC-BY-3.0 288 / 1 185 921, CC-BY-SA-3.0 152 /
  321 838, public domain (LicenseRef-PD) 144 / 464 826. No NC/ND in the three Common Pile sets (0 matches on 178 489
  documents). The Common Pile card warns about "license laundering".
- **Commercial use: allowed for every row.** CC BY, CC BY-SA, GFDL and public domain permit commercial use; share-alike
  (CC BY-SA) and GFDL copyleft apply to redistribution of the data itself: such rows keep their licence, and GFDL requires
  the licence text with redistributed copies. Attribution: `url` and `author` per row.
- **OpenStax excluded (conservative decision, preregistered).** V: on 2026-04-22 OpenStax announced moving new and
  updated versions of its library from CC BY to CC BY-NC-SA and named AI among the reasons (post of 2026-03-18). I: the
  Common Pile copies (03.2025) come from CC BY 4.0 versions and a CC licence cannot be revoked for released versions, so
  use would be lawful; the publisher's intent is a reputational risk. Rows whose url or the first/last 3000 characters
  (raw and normalised text, annex `aneks_2026_11_26_openstax_okno`) mention OpenStax are excluded: 1 434 documents,
  8 429 842 v6 tokens after the earlier build filters.
- **Gate "may TRAIN" (including commercial use): YES** (per-row open licence). Takedown: drop by `id` / url.
- **Gate "may SUBMIT": YES** (per-row licence without NC/ND; attribution, SA and GFDL kept in the export).
- **Decision: `admitted`.**

Not checked:
- Whether `metadata.license` matches the current page licence at LibreTexts/PressBooks.
- LibreTexts and PressBooks terms beyond the CC licences regarding AI training; robots.txt/TDMRep of these domains.
- OpenStax content not marked by the word "OpenStax" in url or the checked text windows.
- Text written with AI help in recent LibreTexts versions.

## Cleaning

Rules preregistered 2026-11-26 (`skrypty/preregistracja.json`) before building the pool, taken from InfiWebMath-4+ with
annexes 24.11, 24.11b, 24.11c, 25.11b, 25.11c, 25.11e; departures: Common Pile textbook pages with a selection rule
instead of a quality classifier, build filter before the detectors, added `dedup_infiwebmath4` and
`dedup_fineweb_edu_109`. Annexes: `aneks_2026_11_26_openstax_okno` (after the first build, before export: OpenStax
check also on the normalised text) and `aneks_2026_11_26_przeglad` (after the review, before export). Cascade in this
order; counts from `wyniki/agreguj.json` (`kaskada`; "independent" = documents with the reason regardless of order).

| # | Reason | Rule | dropped docs | dropped tokens (v6) |
|---|---|---|---|---|
| 1 | `walidacja_fabryki` | 13-gram sketch ≥ 0.5, MinHash ≥ 0.8, identical text or identical url vs Fabryka validation sets. | 0 | 0 |
| 2 | `domena_testow` | Domain hosting benchmark sources. | 0 | 0 |
| 3 | `ewal_13gram` | Non-trivial 13-gram from a strict math/code test at any df, or from another of ~60 tests at df < 5. | 140 | 842158 |
| 4 | `pii` | E-mail, phone number or IPv4 address → document dropped. | 33 | 211628 |
| 5 | `pii_zaciemniony` | Obfuscated e-mail → document dropped. | 0 | 0 |
| 6 | `pii_at_bez_nawiasow` | `name at domain.tld` → document dropped. | 119 | 701044 |
| 7 | `min_tresc` | Fewer than 50 normalised words. | 0 | 0 |
| 8 | `mojibake` | ≥ 3 matches of a strict mojibake regex. | 2 | 6220 |
| 9 | `dedup_wewnatrz` | Identical normalised text or MinHash (5-grams, 128 perm., LSH 32×4) J ≥ 0.8 within the pool (near copies C1↔C2 and between book versions). | 1597 | 6742284 |
| 10 | `dedup_finemath4` | Identical normalised url, MinHash J ≥ 0.8 or identical text vs FineMath-4+ part 2. | 1544 | 6875442 |
| 11 | `dedup_infiwebmath4` | Same vs InfiWebMath-4+. | 100 | 313897 |
| 12 | `dedup_slayer107` | 13-gram sketch ≥ 0.5 or MinHash ≥ 0.8 vs Slayer 1.07 English data. | 240 | 773959 |
| 13 | `dedup_slayer_8x3b_en` | MinHash J ≥ 0.8 or identical text vs the English part of Slayer 1.00–1.06. | 4 | 5882 |
| 14 | `dedup_english_technical` | MinHash J ≥ 0.8 or identical text vs `SlayerLab/english-technical-1b@3b833d36`. | 0 | 0 |
| 15 | `dedup_fineweb_edu_109` | Identical normalised url vs FineWeb-Edu urls in `SlayerLab/Slayer1B-Dataset@2d248a17` (1.09). | 51 | 70776 |

Pool 6 819 docs / 26 422 540 v6 tokens. Kept after all reasons (`uzysk`): **2 989 docs / 9 879 250 v6 tokens
(37.39%)**; near-duplicates within the pool (25.5 percentage points) and pages already in FineMath-4+ (26.0 points)
take most of the loss. One part (`wyniki/czesci.json`): `open_textbooks_math_en_p01`, 2 989 docs, 9 879 250 v6 tokens.

Export (`shard.write`): 2 986 docs, 8 954 754 `token_count` (the submissions repo's counter, not v6); `dropped`:
wrong_language 3. Parquet sha256 `eedae7b78eae5703ce53fb3a5a91a1c3051a8111656720fda5b723f8de50de21`.
Contract test: 1 passed. `src/check.py`: 21 lines, only the two expected causes (Presidio rescan, no presidio record).

Positive control: no result file for this source (not measured); rules and indexes as in InfiWebMath-4+.

Review (`wyniki/przeglad_1.json`, two independent reviewers A/B, full texts of kept documents; slices read incompletely
were finished; false-drop thresholds ≤ 10% and Wilson 95% upper bound ≤ 20%):

| Reason | n | A false drops [Wilson] | B false drops [Wilson] | Verdict A/B | Token cost (independent) |
|---|---|---|---|---|---|
| `ewal_13gram` | 91 | 88% [79.6; 93.1] | 92% [85.0; 96.2] | FAIL/FAIL | 3.19% |
| `pii` | 32 | 22% [11.0; 38.8] | 22% [11.0; 38.8] | FAIL/FAIL | 0.86% |
| `pii_at_bez_nawiasow` | 88 | 7% [3.2; 14.1] | 12.5% [7.1; 21.0] | PASS/FAIL | 2.88% |
| `mojibake` | 2 | 0% [0; 65.8] | 0% [0; 65.8] | FAIL/FAIL (small n) | 0.02% |
| `dedup_wewnatrz` | 94 | 0% [0; 3.9] | 0% [0; 3.9] | PASS/PASS | 28.53% |
| `dedup_finemath4` | 100 | 0% [0; 3.7] | 0% [0; 3.7] | PASS/PASS | 37.12% |
| `dedup_infiwebmath4` | 98 | 0% [0; 3.8] | 0% [0; 3.8] | PASS/PASS | 2.19% |
| `dedup_slayer107` | 96 | 0% [0; 3.8] | 0% [0; 3.8] | PASS/PASS | 5.08% |
| `dedup_slayer_8x3b_en` | 6 | 0% [0; 39.0] | 0% [0; 39.0] | FAIL/FAIL (small n) | 0.03% |
| `dedup_fineweb_edu_109` | 100 | 0% [0; 3.7] | 0% [0; 3.7] | PASS/PASS | 0.79% |

Accepted (annex `aneks_2026_11_26_przeglad`): `ewal_13gram` 88–92% false (formulas, definitions), cost 3.19%; `pii`
7/32 false (exercise numbers read as IPv4), the rest beyond the visible text, cost 0.80%; `pii_at_bez_nawiasow` (B)
11/88 false in the visible text, the rest beyond it ("available at …" phrases), cost 2.65%; `mojibake` 0/2 and
`dedup_slayer_8x3b_en` 0/6, failing only on small samples. These rules drop good text rather than let bad text through.
300 kept documents: junk **7/300** (A, 2.3% [1.1; 4.7]) and **6/300** (B, 2.0% [0.9; 4.3]) — LibreTexts navigation only,
chapters without mathematics — PASS.

## Personal data

- Documents with an e-mail address, phone number or IPv4 address (`pii`), an obfuscated e-mail (`pii_zaciemniony`) or
  `name at domain.tld` (`pii_at_bez_nawiasow`) are dropped whole. Detector classes in the pool: e-mail 5, phone 3, IP 27.
- Author names from the source metadata stay in `author` (attribution required by the licences).
- The Presidio pass of `shard.write` is off (`no_masking()` in `matematyka-wspolne/eksport/src/mat_wybor.py`): its
  PhoneRecognizer masks numbers in mathematics (403 spans in 300 FineMath-4+ documents, 2026-11-24). `check.py` result:
  21 lines, only "PII left after masking" and "no presidio record".
- Review of 300 kept documents: missed PII **0/300** for both reviewers.

## Sample

- Seed `20261126`.
- Manual review (`wyniki/przeglad_1.json`): up to 100 dropped documents per reason (n in the table above) and 300 kept
  documents; two independent reviewers A and B who did not build the set. Kept documents: junk 7/300 and 6/300, missed
  PII 0/300, missed test items 0/300.
- Selection precision (source card): C1 20/20, C2 20/20.
- The inline sample generated by `src/render_sample.py` from the built shard goes in the PR description.
