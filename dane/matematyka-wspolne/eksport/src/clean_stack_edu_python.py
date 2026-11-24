"""stack_edu_python: Stack-Edu Python files kept by the slayer-lab filters (dane/stackedu).

Usage: python src/clean_stack_edu_python.py <wybor.json> [pii_processes]
The file text is unchanged; shard.write masks PII (author e-mails in headers). id is the Software Heritage blob id;
license is the repository licence Stack v2 detected (metadata.license); author is the repository owner."""
import sys

import mat_wybor
import shard

KEY = "stack_edu_python"


def build(wybor: str):
    for r in mat_wybor.rows(wybor, ["text", "id", "repo_name", "license", "created"]):
        yield {"id": r["id"], "text": r["text"], "created": r["created"] or "unknown", "license": r["license"],
               "author": (r["repo_name"] or "unknown").split("/")[0], "language": "en", "text_origin": "human",
               "generator": None, "derived_from": None}


if __name__ == "__main__":
    mat_wybor.parallel_pii(int(sys.argv[2]) if len(sys.argv) > 2 else 8)
    print(shard.write(KEY, build(sys.argv[1])))
