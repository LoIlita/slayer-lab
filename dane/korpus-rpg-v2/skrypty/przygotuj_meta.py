"""Skrót poprzedniego manifestu i porównanie tokenizerów: sha, rozmiar słownika, stosunek liczby tokenów na próbce.
Argumenty: manifest_wejscie.json tokenizer_lokalny tokenizer_107 korpus.parquet katalog_kart wyjscie_tok.json."""
import hashlib
import json
import sys

import pyarrow.parquet as pq
from tokenizers import Tokenizer

M, TL, T107, KOR, KARTY, WY = sys.argv[1:7]
m = json.load(open(M, encoding="utf-8"))
sk = {k: m[k] for k in ("rpg", "parametry", "rodzina", "podciagi", "podzial_czesci", "minhash_czesci", "znaki", "dekontaminacja", "dedup_bazy", "bazy_poza_lista", "jakosc", "tagi_tresci", "liczby_scp", "liczby_gut_meta", "liczby_gut_teksty") if k in m}
sk["sha256"] = m["sha256"]
sk["ner_poprzednio"] = {"status": m["ner"]["status"], "powod": m["ner"]["powod"]}
json.dump(sk, open(f"{KARTY}/poprzedni_manifest_skrot.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

a, b = Tokenizer.from_file(TL), Tokenizer.from_file(T107)
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
pf = pq.ParquetFile(KOR)
t = pf.read_row_group(0, columns=["text", "tokeny"]).to_pylist()[:300]
la = sum(len(e.ids) for e in a.encode_batch([x["text"] for x in t], add_special_tokens=False)) + len(t)
lb = sum(len(e.ids) for e in b.encode_batch([x["text"] for x in t], add_special_tokens=False)) + len(t)
w = {"lokalny_do_licznikow": {"sha256": sha(TL), "rozmiar_slownika": a.get_vocab_size(with_added_tokens=True), "plik": "slayer-lab/tokenizer/tokenizer.json"},
     "karta_107_v6": {"sha256": sha(T107), "rozmiar_slownika": b.get_vocab_size(with_added_tokens=True), "zrodlo": "SlayerLab/slayer-1.07-pretrain (tokenizer.json)"},
     "zgodne": sha(TL) == sha(T107),
     "proba_300_wierszy": {"tokeny_lokalny_+1eot": la, "tokeny_v6_+1eot": lb, "stosunek_v6_do_lokalny": round(lb / la, 4), "licznik_n_tokens_wejscia": sum(x["tokeny"] for x in t)}}
json.dump(w, open(WY, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(w, ensure_ascii=False))
