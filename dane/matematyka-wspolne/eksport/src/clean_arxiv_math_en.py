"""arxiv_math_en: arXiv papers (full text) and abstracts in mathematics, mathematical physics, statistics and theoretical
computer science, openly licensed only, kept by the slayer-lab filters (dane/arxiv_mat).

Usage: python src/clean_arxiv_math_en.py <wybor.json> [pii_processes] [key]
key: a part of the pool registered as arxiv_math_en_pNN (slayer-lab dane/matematyka-wspolne/skrypty/czesci.py).
Full texts (id `arXiv:<id>`): common-pile/arxiv_papers, papers whose primary category is math.*, math-ph, stat.*, cs.LO,
cs.DM, cs.CC, cs.FL, cs.SC, cs.IT, cs.GT or cs.NA and whose licence (the stricter of Common Pile and arXiv metadata) is
CC BY, CC BY-SA, CC0 or public domain. Abstracts (id `arXiv-abs:<id>`, CC0): the same categories, papers not in the
full-text part. Author e-mails were masked at pool build and are masked again here before shard.write, including brace
lists "{a, b}@uni.edu" and hyphen-wrapped addresses (slayer-lab aneks 2026-11-26 arxiv_mat, after the sample review)."""
import sys

import mat_wybor
import shard

KEY = sys.argv[3] if len(sys.argv) > 3 else "arxiv_math_en"


def build(wybor: str):
    for r in mat_wybor.rows(wybor, ["text", "id", "license", "created", "author"]):
        yield {"id": r["id"], "text": mat_wybor.premask_emails(r["text"], wrapped=True), "created": r["created"] or "unknown",
               "license": r["license"], "author": r["author"] or "unknown", "language": "en", "text_origin": "human",
               "generator": None, "derived_from": None}


if __name__ == "__main__":
    mat_wybor.no_masking(emails=True)
    print(shard.write(KEY, build(sys.argv[1])))
