"""cranemath_en: CraneMath rewrites (Qwen3-32B over FineMath-4+) kept by the slayer-lab filters (dane/cranemath).

Usage: python src/clean_cranemath_en.py <wybor.json> [pii_processes]
The rewritten text is unchanged; PII handling: mat_wybor.no_masking (documents with PII are dropped upstream). derived_from
is the page the rewrite came from: its URL when Ai2 kept one with a scheme, otherwise the Common Crawl WARC record it was
extracted from (about 1.3% of rows carry only a bare host in metadata.url). The row licence is the input's."""
import sys

import mat_wybor
import shard

KEY = "cranemath_en"
LICENSE = "ODC-By-1.0 (FineMath compilation); page text: rights of the page owner, used under the TDM exception"
GENERATOR = "Qwen/Qwen3-32B@unpublished prompt:cranemath_recipe.md"


def derived_from(r: dict) -> str:
    if (r["url"] or "").startswith(("http://", "https://")):
        return r["url"]
    return f"https://data.commoncrawl.org/{r['warc_filename']}#offset={r['warc_record_offset']}"


def build(wybor: str):
    for r in mat_wybor.rows(wybor, ["text", "url", "id", "crawl", "warc_filename", "warc_record_offset"]):
        yield {"id": r["id"], "text": r["text"], "created": r["crawl"], "license": LICENSE, "author": "Ai2 (Qwen3-32B rewrite)",
               "language": "en", "text_origin": "synthetic", "generator": GENERATOR, "derived_from": derived_from(r)}


if __name__ == "__main__":
    mat_wybor.no_masking()
    print(shard.write(KEY, build(sys.argv[1])))
