# arXiv mathematics: openly licensed full texts and CC0 abstracts

Part 3 of the Slayer 1B mathematics and logic set (#357): research papers from arXiv in mathematics, mathematical
physics, statistics and theoretical computer science. Full texts only where the author chose an open licence (CC BY,
CC BY-SA, CC0, public domain); for the other papers of the same categories only the title and abstract (CC0 under the
arXiv API terms). Key `arxiv_math_en`, parts `arxiv_math_en_pNN` (the pool split in pool order by v6 tokens).
Reservation: https://github.com/slayerlabs/benchmarks-fabryka-ai/issues/357 (source card filed under #346).

Marks: **V** = verified 2026-11-26 at the cited source (URL, revision, hash, measurement); **I** = inferred.

## Source

- V: full texts (A1): https://huggingface.co/datasets/common-pile/arxiv_papers, revision
  `963fe980c55b353980653f1a27c1dc0c8a2d7058`, 22 files `NNNNN_arxiv-papers.jsonl.gz`. Common Pile v0.1 (Kandpal et
  al. 2025, https://arxiv.org/abs/2506.05209): LaTeX sources converted with LaTeXML to HTML and with Trafilatura to
  text (Markdown headings, formulas as `$…$` LaTeX).
- V: abstracts (A2): https://huggingface.co/datasets/common-pile/arxiv_abstracts, revision
  `828e35d1000f94579da8850f5f640c138279bdb5`, 4 files (OAI-PMH metadata).
- V: categories and licences: https://huggingface.co/datasets/librarian-bots/arxiv-metadata-snapshot, revision
  `c428226b689a0e17db2cd55265133b9eca15d97f` (CC0). sha256 of all source files in `wyniki/przeglad_zrodla.json`.
- Selection (preregistered, `skrypty/preregistracja.json`): primary category (first of `categories`) matching
  `^(math\.|math-ph$|stat\.|cs\.LO$|cs\.DM$|cs\.CC$|cs\.FL$|cs\.SC$|cs\.IT$|cs\.GT$|cs\.NA$)`. A1: every full text of
  these categories; A2: abstracts of papers of these categories that are not in A1 (id duplicates in the abstracts
  source: first occurrence kept, 8 rows skipped).
- V: build filter (`skrypty/buduj_pule.py`, `wyniki/budowa.json`): 563 papers dropped for licence (the stricter of the
  Common Pile and arXiv-snapshot licences is not open: arXiv default licence, NC, ND or none; their abstracts are in
  A2), 496 empty conversions. One reviewer checked 40 per reason: 40/40 and 40/40 correct
  (`robocze/przeglad/oceny_filtra_budowy.json`).
- V: pool: **652 409 documents, 2 532 068 972 v6 tokens**: A1 72 261 / 2 410 548 069 (median 24 998 tokens per
  paper, max 9.9 M), A2 580 148 / 121 520 903 (median 191).
- Row id `arXiv:<id>` (full text) or `arXiv-abs:<id>` (abstract); `url` `https://arxiv.org/abs/<id>`; `author` =
  arXiv author list; `created` = date of v1. A2 text = title, blank line, abstract.
- Text is not cleaned beyond e-mail masking: conversion artefacts are a property of the source (glued footnote marks
  like `action111As` in ~16% of papers, empty LaTeXML groups `~{}` ~19%, unresolved references `[?]`, formulas lost
  by LaTeXML leaving broken sentences).
- Tokens: v6 tokenizer (`tokenizer.json` sha256 `0640d3bd…815dd`), text tokens + 1 EOT.

## Rights review

- V: row licences, kept in `license` per row: A1 CC-BY-4.0 62 163, CC0-1.0 4 074, CC-BY-SA-4.0 3 807, CC-BY-3.0
  1 747, CC-PDDC 470 (pool counts); A2 CC0-1.0 580 148. No NC/ND, no arXiv default licence.
- V: arXiv licences (https://info.arxiv.org/help/license/index.html): CC BY 4.0 and CC BY-SA 4.0 allow commercial
  use; a licence chosen for a version is irrevocable. Terms of Use for arXiv APIs
  (https://info.arxiv.org/help/api/tou.html): descriptive metadata, including title and abstract, under CC0 1.0.
- Papers under the arXiv default licence (`nonexclusive-distrib`) are **excluded**: the arXiv bulk-data terms allow
  personal or research use only (source card §2.3).
- **Commercial use: allowed.** Attribution: `url` and `author`; share-alike (CC BY-SA rows) applies to
  redistribution of the data itself.
- **Gate "may TRAIN" (including commercial use): YES. Gate "may SUBMIT": YES. Decision: `admitted`.**
- Risk (Common Pile card): "license laundering" — a licence declared by the submitter may not match the rights of
  all authors; mitigated by taking the stricter of two licence records.

Not checked:
- Licences at `arxiv.org/abs/<id>` for a sample of papers (only the metadata snapshot).
- Share of non-English text; share of text written with LLM help in 2023–2025 papers.
- Overlap with peS2o (not part of this set or of Slayer data; card §6 estimates ~8% of A1).

## Cleaning

Rules preregistered 2026-11-26 (`skrypty/preregistracja.json`) before building the pool, taken from InfiWebMath-4+ with
annexes 24.11, 24.11b, 24.11c, 25.11b, 25.11c, 25.11e; departures: PII mode `maskuj_email_usun_telefon_ip` (author
e-mails masked, documents with a phone number or IPv4 address dropped), build filter before the detectors, added
`dedup_infiwebmath4`, no `dedup_fineweb_edu_109` (the source is not web pages; the url `arxiv.org/abs/<id>` still
meets web sources in `dedup_finemath4` / `dedup_infiwebmath4`). Annex `aneks_2026_11_26_przeglad` (after the review,
before export) records the review result and widens e-mail masking at export. Cascade in this order; counts from
`wyniki/agreguj.json` (`kaskada`).

| # | Reason | Rule | dropped docs | dropped tokens (v6) |
|---|---|---|---|---|
| 1 | `walidacja_fabryki` | 13-gram sketch ≥ 0.5, MinHash ≥ 0.8, identical text or url vs Fabryka validation sets. | 2 | 328 |
| 2 | `domena_testow` | Domain hosting benchmark sources. | 0 | 0 |
| 3 | `ewal_13gram` | Non-trivial 13-gram from a strict math/code test at any df, or from another of ~60 tests at df < 5. | 624 | 28 909 335 |
| 4 | `pii` | Phone number or IPv4 address (DCLM-EN detector) → document dropped; e-mails are masked, not dropped. | 1 277 | 69 711 230 |
| 5 | `min_tresc` | Fewer than 50 normalised words (short abstracts). | 47 065 | 3 003 353 |
| 6 | `mojibake` | ≥ 3 matches of a strict mojibake regex. | 30 | 1 263 777 |
| 7 | `dedup_wewnatrz` | Identical normalised text or MinHash (5-grams, 128 perm., LSH 32×4) J ≥ 0.8 within the pool (A1 and A2 together). | 378 | 409 951 |
| 8 | `dedup_finemath4` | Identical url, MinHash J ≥ 0.8 or identical text vs FineMath-4+ part 2. | 2 | 1 195 |
| 9 | `dedup_infiwebmath4` | Same vs InfiWebMath-4+. | 2 | 905 |
| 10 | `dedup_slayer107` | 13-gram sketch ≥ 0.5 or MinHash ≥ 0.8 vs Slayer 1.07 English data. | 3 236 | 787 338 |
| 11 | `dedup_slayer_8x3b_en` | MinHash J ≥ 0.8 or identical text vs the English part of Slayer 1.00–1.06. | 2 | 578 |
| 12 | `dedup_english_technical` | MinHash J ≥ 0.8 or identical text vs `SlayerLab/english-technical-1b@3b833d36`. | 0 | 0 |

Pool 652 409 docs / 2 532 068 972 v6 tokens. Kept after all reasons (`uzysk`): **599 791 docs / 2 427 980 982 v6
tokens (95.89%)**: full texts 70 226 / 2 310 331 144, abstracts 529 565 / 117 649 838. Parts (`wyniki/czesci.json`):
8 parts of ~303 M v6 tokens each (`arxiv_math_en_p01..p08`; p01–p07 full texts, p08 the remaining full texts and all
abstracts); smaller than the ~1 bn parts of other sources because `shard.write` and `check.py` count tokens of a whole
part in memory and full papers are long.

Review (`wyniki/przeglad_1.json`; 841 positions: up to 100 dropped per reason and 300 kept; two independent reviewers
A and B; false-drop thresholds ≤ 10% and Wilson 95% upper bound ≤ 20%; for `pii` and `mojibake` the reviewers also
saw every detector match with ±300 characters of the full text, `skrypty/trafienia_probki.py`):

| Reason | n | A false drops [Wilson] | B false drops [Wilson] | Verdict A/B | Token cost (independent) |
|---|---|---|---|---|---|
| `walidacja_fabryki` | 2 | 0% [0; 65.8] | 0% [0; 65.8] | FAIL/FAIL (upper bound at n = 2) | 0.00% |
| `ewal_13gram` | 100 | 100% [96.3; 100] | 100% [96.3; 100] | FAIL/FAIL | 1.14% |
| `pii` | 100 | 89% [81.4; 93.7] | 89% [81.4; 93.7] | FAIL/FAIL | 2.84% |
| `min_tresc` | 100 | 0% [0; 3.7] | 0% [0; 3.7] | PASS/PASS | 0.12% |
| `mojibake` | 33 | 0% [0; 10.4] | 0% [0; 10.4] | PASS/PASS | 0.06% |
| `dedup_wewnatrz` | 100 | 0% [0; 3.7] | 0% [0; 3.7] | PASS/PASS | 0.02% |
| `dedup_finemath4` | 2 | 0% [0; 65.8] | 0% [0; 65.8] | FAIL/FAIL (upper bound at n = 2) | 0.00% |
| `dedup_infiwebmath4` | 2 | 0% [0; 65.8] | 0% [0; 65.8] | FAIL/FAIL (upper bound at n = 2) | 0.00% |
| `dedup_slayer107` | 100 | 0% [0; 3.7] | 0% [0; 3.7] | PASS/PASS | 0.03% |
| `dedup_slayer_8x3b_en` | 2 | 0% (2 doubtful: no index score in the sample) | same | FAIL/FAIL (upper bound at n = 2) | 0.00% |

Accepted (annex `aneks_2026_11_26_przeglad`, conservative rules whose cost is < 5%): `ewal_13gram` 100/100 false
(shared LaTeX formulas such as matrices and standard definitions, not test items), cost 1.14%; `pii` 89/100 false
(section numbers like `8.2.3.1` and version numbers read as IPv4; 11 real phone or fax numbers in author headers),
cost 2.84% — privacy first; n = 2 reasons FAIL only on the Wilson upper bound. 300 kept documents: junk **0/300**
for both reviewers (5 and 2 doubtful: proceedings prefaces and applied-statistics abstracts), missed test items
**0/300**, missed PII **2/300** (see Personal data).

## Personal data

- Author e-mails (73% of full texts, in author headers) are masked to `[PII]`, not dropped: at pool build
  (`nazwa@domena.tld`, `name(AT)domain`, `name at domain.tld`; 117 796 + 114 + 714 matches, 0 left of these three
  forms) and again before `shard.write` (`premask_emails(..., wrapped=True)` in
  `matematyka-wspolne/eksport/src/mat_wybor.py`, called from `src/clean_arxiv_math_en.py`).
- The review found 2/300 kept documents with an address the build masking missed: a brace list
  `{a.b, c.d}@uni.edu` and an address broken by a line wrap at a hyphen (`name@wias-\nberlin.de`). Annex
  `aneks_2026_11_26_przeglad` widens the export masking (`EMAIL_LATEX`, `EMAIL_BRACED`, `EMAIL_WRAPPED`): local parts
  in LaTeX math (`$name$@uni.edu`), brace or bracket lists over up to 3 lines, addresses broken by a line wrap before,
  after or inside the domain, spaces around `@`, doubled `@@`. After it: 0 addresses in the 300 kept documents and 0
  documents in the whole pool with a local part before `@domain.tld`. What remains are bare domains whose name the
  source already lost (`mailto:@uni.edu`), not personal data. The wider patterns may also mask one word before
  `\n@domain` or up to 200 characters of a `$…$` group right before `@domain`.
- Documents with a phone number or IPv4 address (DCLM-EN detector) are dropped (`pii`): IP 1 112, phone 184 documents
  in the pool, most of them numbering, not personal data (review above).
- Author names stay as required attribution (CC BY / CC BY-SA).
- The Presidio pass of `shard.write` is off (`no_masking(emails=True)`): its PhoneRecognizer masks numbers in
  mathematical text (403 spans in 300 FineMath-4+ documents, 2026-11-24).

## Sample

- Seed `20261126`.
- Manual review (`wyniki/przeglad_1.json`): up to 100 dropped documents per reason (all there were for
  `walidacja_fabryki`, `mojibake`, `dedup_finemath4`, `dedup_infiwebmath4`, `dedup_slayer_8x3b_en`) and 300 kept
  documents, each shown in full up to 3000 characters plus detector matches from the full text; two independent
  reviewers A and B who did not build the set.
- The inline sample generated by `src/render_sample.py` from the built shard goes in the PR description.
