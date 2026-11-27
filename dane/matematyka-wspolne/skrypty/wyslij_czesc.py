"""Wysyłka JEDNEJ ponownie wyeksportowanej części (albo ramienia) do repo HF jednym commitem: parquet, stats.json, datasheet
.md i (gdy jest w repo) .sha256; w tym samym commicie usuwa nieaktualnego bliźniaka tokenized/<tokenizer>/<klucz>.{bin,json}
(tokenizuj_hf.py zrobi go od nowa). Po commicie: sha256 LFS parquetu z API = plik .sha256 lokalnie; wypisuje id commitu.
Użycie: python wyslij_czesc.py <repo> <katalog_czesci> <katalog_w_repo> <opis_commitu> [<tokenizer>]
  katalog_czesci: wyjście remaskuj_czesc.sh (<klucz>.parquet, .stats.json, .md, .sha256); katalog_w_repo: data/<klucz> albo mikroanneal/<klucz>"""
import os
import sys

from huggingface_hub import CommitOperationAdd, CommitOperationDelete, HfApi

REPO, KAT, DOC, OPIS = sys.argv[1:5]
TOK = sys.argv[5] if len(sys.argv) > 5 else None
K = os.path.basename(KAT.rstrip("/"))
api = HfApi()
w_repo = set(api.list_repo_files(REPO, repo_type="dataset"))
ops = []
for ext in ("parquet", "stats.json", "md", "sha256"):
    cel = f"{DOC}/{K}.{ext}"
    if ext == "sha256" and cel not in w_repo:
        continue
    assert ext == "sha256" or cel in w_repo, f"{cel} nie ma w repo"
    ops.append(CommitOperationAdd(path_in_repo=cel, path_or_fileobj=os.path.join(KAT, f"{K}.{ext}")))
if TOK:
    for ext in ("bin", "json"):
        cel = f"tokenized/{TOK}/{K}.{ext}"
        if cel in w_repo:
            ops.append(CommitOperationDelete(path_in_repo=cel))
c = api.create_commit(REPO, operations=ops, repo_type="dataset", commit_message=OPIS)
lok = open(os.path.join(KAT, f"{K}.sha256")).read().split()[0]
info = api.get_paths_info(REPO, [f"{DOC}/{K}.parquet"], repo_type="dataset", revision=c.oid)[0]
assert info.lfs and info.lfs.sha256 == lok, (info.lfs, lok)
print(K, "commit", c.oid, "sha256 LFS = lokalny", lok, "operacje", len(ops), flush=True)
