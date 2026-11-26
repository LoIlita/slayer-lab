"""stackexchange_math: questions with comments and answers from Stack Exchange sites about mathematics and logic (Common Pile
raw dump), kept by the slayer-lab filters (dane/stackexchange_mat): questions created before 2022-12-01, every post licensed,
no question already present as a web page in finemath_4plus_en or infiwebmath_4plus_en.

Usage: python src/clean_stackexchange_math.py <wybor.json> [pii_processes] [key]
key: a part of the pool registered as stackexchange_math_pNN (slayer-lab dane/matematyka-wspolne/skrypty/czesci.py).
id is `<site>/<question id>`; license is the question's CC BY-SA version (metadata.license); author lists the display names
of all posters (metadata.authors). Documents with an e-mail, phone or IPv4 were dropped upstream; Presidio is off."""
import ast
import sys

import mat_wybor
import shard

KEY = sys.argv[3] if len(sys.argv) > 3 else "stackexchange_math"
SPDX = {"by-sa/2.5": "CC-BY-SA-2.5", "by-sa/3.0": "CC-BY-SA-3.0", "by-sa/4.0": "CC-BY-SA-4.0"}


def spdx(lic: str) -> str:
    return next((v for k, v in SPDX.items() if k in (lic or "")), lic)


def authors(a: str) -> str:
    try:
        names = [n for n in ast.literal_eval(a or "[]") if not str(n).startswith("http")]
    except (ValueError, SyntaxError):
        names = []
    return ", ".join(names) or "unknown"


def build(wybor: str):
    for r in mat_wybor.rows(wybor, ["text", "id", "license", "created", "authors"]):
        yield {"id": r["id"], "text": r["text"], "created": r["created"], "license": spdx(r["license"]),
               "author": authors(r["authors"]), "language": "en", "text_origin": "human", "generator": None,
               "derived_from": None}


if __name__ == "__main__":
    mat_wybor.no_masking()
    print(shard.write(KEY, build(sys.argv[1])))
