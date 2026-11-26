"""Registry of sources in this repo. Plain data only: parsed with ast.literal_eval, never imported for its values.

Each entry maps a source key to a dict with these fields:

Required:
  pretty        display name
  upstream      URL, or list of URLs
  license       license name as the source states it
  license_spdx  SPDX identifier
  domain        content domain
  added         YYYY-MM-DD
  created       creation date or range of the texts
  provenance    how the texts were obtained
  traceable     whether each text can be traced to its upstream
  is_ocr        bool
  language      non-empty list drawn from "pl", "en", "pl+en"
  text_origin   "human", "translated", "synthetic" or "mixed"
  legal_note    non-empty string

Optional:
  min_chars                  int >= 1
  dynaword_overlap_reviewed  non-empty str
"""

SOURCES: dict[str, dict] = {
    "oeis_en": {
        "pretty": "OEIS sequence entries (English, rendered as text)",
        "upstream": "https://github.com/oeis/oeisdata",
        "license": "CC BY-SA 4.0 (OEIS End-User License Agreement and repository LICENSE)",
        "license_spdx": "CC-BY-SA-4.0",
        "domain": "mathematics",
        "added": "2026-11-26",
        "created": "1964-2026 (entry history); text as of commit 976b0c73 (2026-11-26)",
        "provenance": "oeis/oeisdata@976b0c73, seq/*.seq rendered as text (name, terms, comments, formulas, examples, programs, cross-references; no links, no e-mails, authors by name) by slayer-lab dane/oeis; filtered there (13-gram decontamination, dedup vs Slayer 1.07 EN, finemath_4plus_en and infiwebmath_4plus_en)",
        "traceable": True,
        "is_ocr": False,
        "language": ["en"],
        "text_origin": "human",
        "legal_note": "CC BY-SA 4.0 per entry; attribution by A-number URL and author names in the text. Share-alike applies to redistributions of this source.",
    },
    "formal_math": {
        "pretty": "Formal mathematics libraries (Lean, Isabelle AFP, HOL Light, Metamath, Rocq, math-comp, UniMath, Agda, Stacks Project)",
        "upstream": ["https://github.com/leanprover-community/mathlib4", "https://github.com/isabelle-prover/mirror-afp-devel", "https://github.com/jrh13/hol-light", "https://github.com/metamath/set.mm", "https://github.com/rocq-prover/stdlib", "https://github.com/math-comp/math-comp", "https://github.com/UniMath/UniMath", "https://github.com/agda/agda-stdlib", "https://github.com/stacks/stacks-project"],
        "license": "per file: Apache-2.0, BSD-3-Clause, BSD-2-Clause, LGPL-2.1-only, CECILL-B, MIT, CC0-1.0, GFDL-1.2-or-later, UniMath licence (MIT text)",
        "license_spdx": "LicenseRef-per-file",
        "domain": "mathematics",
        "added": "2026-11-26",
        "created": "1990-2025 (commit dates)",
        "provenance": "pinned revisions (mathlib4 and HOL Light before the first commit disclosing LLM authorship; files touched by such commits excluded), one row per source file, set.mm proofs replaced by `$= ? $.`, built and filtered by slayer-lab dane/formalna (13-gram decontamination, dedup vs Slayer 1.07 EN and earlier sources)",
        "traceable": True,
        "is_ocr": False,
        "language": ["en"],
        "text_origin": "human",
        "legal_note": "Licence per file from the library's LICENSE, file header or AFP entry metadata; copyleft files (LGPL, GFDL) keep their licence on redistribution. Author e-mails masked to [PII].",
    },
    "stackexchange_math": {
        "pretty": "Stack Exchange mathematics and logic Q&A (Common Pile)",
        "upstream": "https://huggingface.co/datasets/common-pile/stackexchange",
        "license": "CC BY-SA 2.5 / 3.0 / 4.0 per question (all posts in a document licensed)",
        "license_spdx": "CC-BY-SA-4.0",
        "domain": "mathematics",
        "added": "2026-11-26",
        "created": "2008-2022 (questions before 2022-12-01)",
        "provenance": "common-pile/stackexchange@5ec3aa2e (raw), sites math, mathoverflow, cstheory, matheducators, proofassistants, stats, cs, scicomp, or; one document per question with comments and answers; filtered by slayer-lab dane/stackexchange_mat (13-gram decontamination, PII, dedup vs Slayer 1.07 EN, finemath_4plus_en and infiwebmath_4plus_en including the same question as a web page)",
        "traceable": True,
        "is_ocr": False,
        "language": ["en"],
        "text_origin": "human",
        "legal_note": "Licence per question (CC BY-SA version of the question; all_licenses checked, documents with an unlicensed post dropped). Stack Exchange states an AI-training opt-out on the platform since 2024; training relies on the authors' CC BY-SA licence, as the Common Pile does. Takedown by site and question id.",
    },
    "finemath_3_en": {
        "pretty": "FineMath-3+ score 3 (English mathematical web text, pages outside FineMath-4+)",
        "upstream": "https://huggingface.co/datasets/HuggingFaceTB/finemath",
        "license": "ODC-By 1.0 (compilation); page texts from Common Crawl, rights of each page owner",
        "license_spdx": "ODC-By-1.0",
        "domain": "mathematics",
        "added": "2026-11-25",
        "created": "2013-2024 (Common Crawl snapshots)",
        "provenance": "HuggingFaceTB/finemath@e92b25a6, subset finemath-3plus, rows with int_score == 3; random files, filtered by slayer-lab dane/finemath3 (13-gram decontamination, PII, dedup vs Slayer 1.07 EN, finemath_4plus_en and infiwebmath_4plus_en)",
        "traceable": True,
        "is_ocr": False,
        "min_chars": 200,  # as finemath_4plus_en
        "language": ["en"],
        "text_origin": "human",
        "legal_note": "Training basis: TDM exception (Art. 4 Directive 2019/790); no per-document licence, so the submission gate is unresolved. Takedown by url / WARC record.",
    },
    "finemath_4plus_en": {
        "pretty": "FineMath-4+ (English mathematical web text)",
        "upstream": "https://huggingface.co/datasets/HuggingFaceTB/finemath",
        "license": "ODC-By 1.0 (compilation); page texts from Common Crawl, rights of each page owner",
        "license_spdx": "ODC-By-1.0",
        "domain": "mathematics",
        "added": "2026-11-24",
        "created": "2013-2024 (Common Crawl snapshots)",
        "provenance": "HuggingFaceTB/finemath@e92b25a6, subset finemath-4plus; random files, filtered by slayer-lab dane/finemath4 (13-gram decontamination, PII, dedup vs Slayer 1.07 EN)",
        "traceable": True,
        "is_ocr": False,
        "min_chars": 200,  # short rows are mostly bare formulas that langid cannot place; check.py's short-row gate fails at 82%
        "language": ["en"],
        "text_origin": "human",
        "legal_note": "Training basis: TDM exception (Art. 4 Directive 2019/790); no per-document licence, so the submission gate is unresolved. Takedown by url / WARC record.",
    },
    "infiwebmath_4plus_en": {
        "pretty": "InfiWebMath-4+ (English mathematical web text, pages outside FineMath-4+)",
        "upstream": "https://huggingface.co/datasets/HuggingFaceTB/finemath",
        "license": "ODC-By 1.0 (compilation); page texts from Common Crawl via InfiMM-WebMath-40B, rights of each page owner",
        "license_spdx": "ODC-By-1.0",
        "domain": "mathematics",
        "added": "2026-11-25",
        "created": "2019-2023 (Common Crawl snapshots, WARC dates)",
        "provenance": "HuggingFaceTB/finemath@e92b25a6, subset infiwebmath-4plus; all files, filtered by slayer-lab dane/infiwebmath4 (13-gram decontamination, PII, dedup vs Slayer 1.07 EN and vs finemath_4plus_en)",
        "traceable": True,
        "is_ocr": False,
        "min_chars": 200,  # as finemath_4plus_en
        "language": ["en"],
        "text_origin": "human",
        "legal_note": "Training basis: TDM exception (Art. 4 Directive 2019/790); no per-document licence, so the submission gate is unresolved. Takedown by url / WARC-Record-ID.",
    },
    "cranemath_en": {
        "pretty": "CraneMath (FineMath-4+ rewritten by Qwen3-32B, Dolma 3 Dolmino)",
        "upstream": "https://huggingface.co/datasets/allenai/dolma3_dolmino_mix-100B-1125",
        "license": "ODC-By 1.0 (compilation); inputs are Common Crawl page texts; generator Qwen3-32B under Apache-2.0",
        "license_spdx": "ODC-By-1.0",
        "domain": "mathematics",
        "added": "2026-11-24",
        "created": "2025 (rewrite); inputs 2013-2024",
        "provenance": "allenai/dolma3_dolmino_mix-100B-1125@f23aa129, data/ingredient1-cranemath; random files, filtered by slayer-lab dane/cranemath (13-gram decontamination on text and original_text, truncated <think>, PII, dedup)",
        "traceable": True,
        "is_ocr": False,
        "min_chars": 200,  # as finemath_4plus_en
        "language": ["en"],
        "text_origin": "synthetic",
        "legal_note": "Rewrites of web pages; the input pages carry no per-document licence, so the submission gate is unresolved. Training basis: TDM exception. Ai2 does not publish the Qwen3-32B revision.",
    },
    "stack_edu_python": {
        "pretty": "Stack-Edu Python (Common Pile v0.1, permissively licensed)",
        "upstream": "https://huggingface.co/datasets/common-pile/stackv2_edu_filtered",
        "license": "per file: permissive licences from the Blue Oak Council list (metadata.license)",
        "license_spdx": "LicenseRef-per-file-permissive",
        "domain": "code",
        "added": "2026-11-24",
        "created": "2008-2023 (commit dates)",
        "provenance": "common-pile/stackv2_edu_filtered@c354dbe8, files 0073-0084, language Python; filtered by slayer-lab dane/stackedu (licence, int_score >= 3, secrets, generated code, 13-gram decontamination, dedup)",
        "traceable": True,
        "is_ocr": False,
        "language": ["en"],
        "text_origin": "human",
        "legal_note": "Stack v2 detects the licence per repository, not per file; rows with an empty licence are dropped. Takedown by blob id or repository.",
    },
}
