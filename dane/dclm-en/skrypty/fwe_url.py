"""Próbka url FineWeb-Edu: kolumna url z losowych plików data/ (czytana zakresami HTTP, bez tekstu), hasze znormalizowanych url.
Liczbę wierszy całego FWE (config default) bierze z datasets-server. Argumenty: wyjscie liczba_plikow."""
import json
import os
import sys
import numpy as np
import pyarrow.parquet as pq
import requests
from huggingface_hub import HfApi, HfFileSystem
from huggingface_hub.utils import build_hf_headers

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wspolne as w  # noqa: E402

OUT, ILE = sys.argv[1], int(sys.argv[2])
REPO, REW = "HuggingFaceFW/fineweb-edu", "87f09149ef4734204d70ed1d046ddc9ca3f2b8f9"
os.makedirs(OUT, exist_ok=True)
fs = HfFileSystem()
pliki = sorted(f for f in HfApi().list_repo_files(REPO, repo_type="dataset", revision=REW) if f.startswith("data/") and f.endswith(".parquet"))
B = f"datasets/{REPO}@{REW}/"


# liczba wierszy całego FWE z datasets-server (odczyt stopek ok. 1550 plików przez HfFileSystem trwał ponad 20 min bez wyniku)
s = requests.Session()
s.headers.update(build_hf_headers())
rozm = s.get("https://datasets-server.huggingface.co/size", params={"dataset": REPO}, timeout=120).json()
razem = next(c["num_rows"] for c in rozm["size"]["configs"] if c["config"] == "default")
brak = []
wyb = sorted(np.random.default_rng(w.SEED).choice(len(pliki), ILE, replace=False).tolist())
hs, info = [], []
for i in wyb:
    p = pliki[i]
    with fs.open(B + p, "rb") as h:
        u = pq.read_table(h, columns=["url"]).column(0).to_pylist()
    hs.append(np.unique(np.fromiter((w.h64(w.norm_url(x)) for x in u), dtype=np.uint64, count=len(u))))
    info.append({"plik": p, "wiersze": len(u)})
    print(p, len(u), flush=True)
cale = np.concatenate(hs)
uniq, ile = np.unique(cale, return_counts=True)
np.save(f"{OUT}/fwe_url_h.npy", uniq)
wyn = {"repo": REPO, "rewizja": REW, "plikow_data": len(pliki), "wiersze_fwe_data": razem, "pliki_bez_metadanych": brak,
       "probka": info, "wiersze_probki": sum(x["wiersze"] for x in info), "url_unikalne_probki": int(len(uniq)),
       "url_w_wielu_plikach_probki": int((ile > 1).sum()), "udzial_probki_w_fwe": sum(x["wiersze"] for x in info) / razem}
json.dump(wyn, open(f"{OUT}/fwe_url.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(json.dumps({k: v for k, v in wyn.items() if k != "probka"}), flush=True)
