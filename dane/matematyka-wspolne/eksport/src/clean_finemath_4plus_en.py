"""finemath_4plus_en: FineMath-4+ pages kept by the slayer-lab filters (dane/finemath4).

Usage: python src/clean_finemath_4plus_en.py <wybor.json> [pii_processes] [key]
key: a part of the full pool registered as finemath_4plus_en_pNN (slayer-lab dane/matematyka-wspolne/skrypty/czesci.py).
The text is unchanged; Presidio is off (mat_wybor.no_masking). One row per page; id is the WARC file and record offset."""
import sys
from urllib.parse import urlsplit

import mat_wybor
import shard

KEY = sys.argv[3] if len(sys.argv) > 3 else "finemath_4plus_en"
LICENSE = "ODC-By-1.0 (FineMath compilation); page text: rights of the page owner, used under the TDM exception"


def build(wybor: str):
    for r in mat_wybor.rows(wybor, ["text", "url", "id", "crawl"]):
        yield {"id": r["id"], "text": r["text"], "created": r["crawl"], "license": LICENSE,
               "author": urlsplit(r["url"]).hostname or "unknown", "language": "en", "text_origin": "human",
               "generator": None, "derived_from": None}


if __name__ == "__main__":
    mat_wybor.no_masking()
    print(shard.write(KEY, build(sys.argv[1])))
