"""open_textbooks_math_en: open textbook chapters on mathematics and statistics from LibreTexts and PressBooks (Common Pile), kept by the
slayer-lab filters (dane/podreczniki_mat): OpenStax-derived chapters excluded, exact duplicate chapters removed.

Usage: python src/clean_open_textbooks_math_en.py <wybor.json> [pii_processes] [key]
key: a part of the pool registered as open_textbooks_math_en_pNN (slayer-lab dane/matematyka-wspolne/skrypty/czesci.py).
One row per page or chapter; licence per row (CC BY, CC BY-SA, GFDL, public domain); author from the source metadata.
Documents with an e-mail, phone or IPv4 were dropped upstream; Presidio is off (mat_wybor.no_masking)."""
import sys

import mat_wybor
import shard

KEY = sys.argv[3] if len(sys.argv) > 3 else "open_textbooks_math_en"


def build(wybor: str):
    for r in mat_wybor.rows(wybor, ["text", "id", "license", "created", "author"]):
        yield {"id": r["id"], "text": r["text"], "created": r["created"] or "unknown", "license": r["license"],
               "author": r["author"] or "unknown", "language": "en", "text_origin": "human", "generator": None,
               "derived_from": None}


if __name__ == "__main__":
    mat_wybor.no_masking()
    print(shard.write(KEY, build(sys.argv[1])))
