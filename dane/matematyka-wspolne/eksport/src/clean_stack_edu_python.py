"""stack_edu_python: Stack-Edu Python files kept by the slayer-lab filters (dane/stackedu).

Usage: python src/clean_stack_edu_python.py <wybor.json> [pii_processes] [key]
key: a part of the full pool registered as stack_edu_python_pNN (slayer-lab dane/matematyka-wspolne/skrypty/czesci.py).
The file text is unchanged except author e-mails, masked to [PII] before shard.write (mat_wybor.premask_emails). id is the Software Heritage blob id;
license is the repository licence Stack v2 detected (metadata.license); author is the repository owner."""
import sys

import mat_wybor
import shard

KEY = sys.argv[3] if len(sys.argv) > 3 else "stack_edu_python"


def build(wybor: str):
    for r in mat_wybor.rows(wybor, ["text", "id", "repo_name", "license", "created"]):
        yield {"id": r["id"], "text": mat_wybor.premask_emails(r["text"]), "created": r["created"] or "unknown", "license": r["license"],
               "author": (r["repo_name"] or "unknown").split("/")[0], "language": "en", "text_origin": "human",
               "generator": None, "derived_from": None}


if __name__ == "__main__":
    mat_wybor.no_masking(emails=True)
    print(shard.write(KEY, build(sys.argv[1])))
