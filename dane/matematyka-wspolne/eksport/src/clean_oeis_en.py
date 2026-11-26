"""oeis_en: OEIS sequence entries rendered as readable text, kept by the slayer-lab filters (dane/oeis).

Usage: python src/clean_oeis_en.py <wybor.json> [pii_processes] [key]
key: a part of the pool registered as oeis_en_pNN (slayer-lab dane/matematyka-wspolne/skrypty/czesci.py).
Text built in slayer-lab dane/oeis/skrypty/buduj_pule.py from oeis/oeisdata (no %H links, no e-mails, authors by name);
e-mails are masked again here before shard.write. One row per A-number; Presidio is off (mat_wybor.no_masking)."""
import sys

import mat_wybor
import shard

KEY = sys.argv[3] if len(sys.argv) > 3 else "oeis_en"


def build(wybor: str):
    for r in mat_wybor.rows(wybor, ["text", "id", "license", "created"]):
        yield {"id": r["id"], "text": mat_wybor.premask_emails(r["text"]), "created": r["created"], "license": r["license"],
               "author": "OEIS contributors (names in the text)", "language": "en", "text_origin": "human",
               "generator": None, "derived_from": None}


if __name__ == "__main__":
    mat_wybor.no_masking(emails=True)
    print(shard.write(KEY, build(sys.argv[1])))
