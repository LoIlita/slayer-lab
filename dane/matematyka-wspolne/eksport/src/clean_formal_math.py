"""formal_math: source files of formal mathematics libraries (Lean mathlib4, Isabelle AFP, HOL Light, Metamath set.mm,
Rocq stdlib, math-comp, UniMath, agda-stdlib, Stacks Project), kept by the slayer-lab filters (dane/formalna).

Usage: python src/clean_formal_math.py <wybor.json> [pii_processes] [key]
key: a part of the pool registered as formal_math_pNN (slayer-lab dane/matematyka-wspolne/skrypty/czesci.py).
Revisions predate the first commit that discloses LLM authorship (mathlib4, HOL Light); files touched by such commits are
excluded. Author e-mails in file headers are masked to [PII] before shard.write in every form seen in review (@, (at),
`name at domain.tld`, `name-at-domain`); set.mm proofs are replaced by `$= ? $.`. One row per file; license per file."""
import sys

import mat_wybor
import shard

KEY = sys.argv[3] if len(sys.argv) > 3 else "formal_math"


def build(wybor: str):
    for r in mat_wybor.rows(wybor, ["text", "id", "license", "created", "repo"]):
        yield {"id": r["id"], "text": mat_wybor.premask_emails(r["text"], bare_at=True), "created": r["created"],
               "license": r["license"], "author": r["repo"].split("/")[0] if r["repo"] else "unknown", "language": "en",
               "text_origin": "human", "generator": None, "derived_from": None}


if __name__ == "__main__":
    mat_wybor.no_masking(emails=True)
    print(shard.write(KEY, build(sys.argv[1])))
