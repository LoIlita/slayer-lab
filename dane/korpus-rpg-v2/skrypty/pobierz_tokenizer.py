"""Pobiera tokenizer v6 z repo slayer-1.07-pretrain przez huggingface_hub (uwierzytelnia sama biblioteka) i sprawdza sha256 oraz rozmiar słownika.
Argumenty: katalog_docelowy oczekiwany_sha256."""
import hashlib
import json
import sys

from huggingface_hub import hf_hub_download
from tokenizers import Tokenizer

CEL, OCZ = sys.argv[1], sys.argv[2]
p = hf_hub_download(repo_id="SlayerLab/slayer-1.07-pretrain", repo_type="dataset", filename="tokenizer.json", local_dir=CEL)
sha = hashlib.sha256(open(p, "rb").read()).hexdigest()
t = Tokenizer.from_file(p)
wyn = {"sha256": sha, "rozmiar_slownika": t.get_vocab_size(with_added_tokens=True), "token_0": t.id_to_token(0)}
print(json.dumps(wyn, ensure_ascii=False))
if sha != OCZ or wyn["rozmiar_slownika"] != 32768 or wyn["token_0"] != "<|endoftext|>":
    raise SystemExit("tokenizer niezgodny z oczekiwanym")
