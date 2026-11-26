"""wikipedia_math_en: English Wikipedia and Wikibooks articles on mathematics (Common Pile wikimedia), kept by the slayer-lab filters
(dane/wiki_mat): selection rule 1 of the source card (formula density and a mathematics vocabulary test, precision 87%).

Usage: python src/clean_wikipedia_math_en.py <wybor.json> [pii_processes] [key]
key: a part of the pool registered as wikipedia_math_en_pNN (slayer-lab dane/matematyka-wspolne/skrypty/czesci.py).
One row per article; licence CC BY-SA 4.0; author = editor logins from the source metadata. Documents with an e-mail,
phone or IPv4 were dropped upstream; Presidio is off (mat_wybor.no_masking)."""
import sys

import mat_wybor
import shard

KEY = sys.argv[3] if len(sys.argv) > 3 else "wikipedia_math_en"


def build(wybor: str):
    for r in mat_wybor.rows(wybor, ["text", "id", "license", "created", "author"]):
        yield {"id": r["id"], "text": r["text"], "created": r["created"] or "unknown", "license": r["license"],
               "author": r["author"] or "unknown", "language": "en", "text_origin": "human", "generator": None,
               "derived_from": None}


if __name__ == "__main__":
    mat_wybor.no_masking()
    print(shard.write(KEY, build(sys.argv[1])))
