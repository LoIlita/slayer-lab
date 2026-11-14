"""Pobiera angielskie części SlayerLab/slayer-1.07-pretrain (en_mix, en_fineweb_edu: train.bin + docs.idx) oraz korpus technika-i-nauka."""
import json
import os
import sys
import time

import requests
from huggingface_hub.utils import build_hf_headers

CEL = sys.argv[1]
sess = requests.Session()
sess.headers.update(build_hf_headers())


def wez(url, cel):
    os.makedirs(os.path.dirname(cel), exist_ok=True)
    if os.path.exists(cel) and os.path.getsize(cel) > 0:
        print("jest", cel, flush=True)
        return
    for p in range(3):
        try:
            with sess.get(url, stream=True, timeout=300, allow_redirects=True) as r:
                r.raise_for_status()
                with open(cel + ".tmp", "wb") as f:
                    for k in r.iter_content(1 << 22):
                        f.write(k)
                os.replace(cel + ".tmp", cel)
                print("ok", cel, os.path.getsize(cel), flush=True)
                return
        except Exception as e:  # noqa: BLE001
            print("blad", url, type(e).__name__, str(e)[:200], flush=True)
            time.sleep(10)
    raise SystemExit("nie pobrano: " + url)


B = "https://huggingface.co/datasets/SlayerLab/slayer-1.07-pretrain/resolve/main"
for d in ("en_mix", "en_fineweb_edu"):
    for f in ("docs.idx", "train.bin"):
        wez(f"{B}/{d}/{f}", f"{CEL}/slayer107/{d}/{f}")
T = "https://huggingface.co/datasets/SlayerLab/technika-i-nauka/resolve/main/data"
for f in ("train.parquet", "validation.parquet", "test.parquet"):
    wez(f"{T}/{f}", f"{CEL}/technika/{f}")
print("KONIEC", flush=True)
