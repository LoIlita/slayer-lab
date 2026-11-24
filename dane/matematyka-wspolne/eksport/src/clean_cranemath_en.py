"""cranemath_en: CraneMath rewrites (Qwen3-32B over FineMath-4+) kept by the slayer-lab filters (dane/cranemath).

Usage: python src/clean_cranemath_en.py <wybor.json> [pii_processes]
The rewritten text is unchanged; shard.write masks PII after generation. derived_from is the page the rewrite came from;
the row licence is the input's (FineMath compilation, page owner's rights)."""
import sys

import mat_wybor
import shard

KEY = "cranemath_en"
LICENSE = "ODC-By-1.0 (FineMath compilation); page text: rights of the page owner, used under the TDM exception"
GENERATOR = "Qwen/Qwen3-32B@unpublished prompt:cranemath_recipe.md"


def build(wybor: str):
    for r in mat_wybor.rows(wybor, ["text", "url", "id", "crawl"]):
        yield {"id": r["id"], "text": r["text"], "created": r["crawl"], "license": LICENSE, "author": "Ai2 (Qwen3-32B rewrite)",
               "language": "en", "text_origin": "synthetic", "generator": GENERATOR, "derived_from": r["url"]}


if __name__ == "__main__":
    mat_wybor.parallel_pii(int(sys.argv[2]) if len(sys.argv) > 2 else 8)
    print(shard.write(KEY, build(sys.argv[1])))
