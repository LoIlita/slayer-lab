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
        "language": ["en"],
        "text_origin": "human",
        "legal_note": "Training basis: TDM exception (Art. 4 Directive 2019/790); no per-document licence, so the submission gate is unresolved. Takedown by url / WARC record.",
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
