"""Pobiera zbiory ewaluacyjne z testy.json przez parquety datasets-server (rewizja refs/convert/parquet) albo wskazane pliki.
Wyjście: <cel>/<id>/... oraz <wyniki>/status_pobran.json (status OK/BLOCKED z powodem per test)."""
import json
import os
import sys
import time

import requests
from huggingface_hub import HfApi
from huggingface_hub.utils import build_hf_headers

CEL, WYN, TESTY = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(CEL, exist_ok=True)
H = build_hf_headers()
sess = requests.Session()
sess.headers.update(H)
api = HfApi()
testy = json.load(open(TESTY, encoding="utf-8"))["testy"]


def wez(url, cel, proby=2):
    if os.path.exists(cel) and os.path.getsize(cel) > 0:
        return
    for p in range(proby):
        try:
            with sess.get(url, stream=True, timeout=120, allow_redirects=True) as r:
                r.raise_for_status()
                tmp = cel + ".tmp"
                with open(tmp, "wb") as f:
                    for k in r.iter_content(1 << 20):
                        f.write(k)
                os.replace(tmp, cel)
                return
        except Exception:  # noqa: BLE001
            if p + 1 == proby:
                raise
            time.sleep(5)


status = {}
if os.path.exists(f"{WYN}/status_pobran.json"):
    status = json.load(open(f"{WYN}/status_pobran.json", encoding="utf-8"))
for t in testy:
    tid = t["id"]
    if status.get(tid, {}).get("status") == "OK":
        continue
    if not t.get("repo"):
        status[tid] = {"status": "BLOCKED", "powod": t["powod_blocked"], "zrodlo": t.get("zrodlo")}
        continue
    d = f"{CEL}/{tid}"
    os.makedirs(d, exist_ok=True)
    st = {"repo": t["repo"], "pliki": [], "zrodlo": t.get("zrodlo", "tasks_50.json")}
    try:
        try:
            st["rewizja"] = api.dataset_info(t["repo"]).sha
        except Exception as e:  # noqa: BLE001
            st["rewizja"] = None
            st["info_blad"] = type(e).__name__ + ": " + str(e)[:200]
        if t.get("pliki"):
            for f in t["pliki"]:
                u = f"https://huggingface.co/datasets/{t['repo']}/resolve/main/{f}"
                c = f"{d}/{f.replace('/', '__')}"
                wez(u, c)
                st["pliki"].append({"plik": os.path.basename(c), "config": None, "split": "plik", "format": t.get("format")})
        else:
            r = sess.get("https://datasets-server.huggingface.co/parquet", params={"dataset": t["repo"]}, timeout=120)
            if r.status_code == 200:
                lista = r.json().get("parquet_files", [])
            else:
                wpisy = [p for p in api.list_repo_files(t["repo"], repo_type="dataset", revision="refs/convert/parquet") if p.endswith(".parquet")]
                if not wpisy:
                    raise RuntimeError(f"datasets-server HTTP {r.status_code}: {r.text[:200]}; brak gałęzi refs/convert/parquet")
                lista = [{"config": p.split("/")[0], "split": p.split("/")[-2], "filename": p.split("/")[-1], "url": f"https://huggingface.co/datasets/{t['repo']}/resolve/refs%2Fconvert%2Fparquet/{p}"} for p in wpisy]
                st["uwaga"] = "pobrane z gałęzi refs/convert/parquet (zbiór skryptowy, datasets-server niedostępny)"
            if not lista:
                raise RuntimeError("datasets-server: brak plików parquet (zbiór nieprzekonwertowany)")
            wybrane = []
            for f in lista:
                if t["configs"] != "*" and f["config"] not in t["configs"]:
                    continue
                sp = f["split"]
                if t["splits"] == "*" or (t["splits"] == "!train" and not sp.startswith("train")) or (isinstance(t["splits"], list) and sp in t["splits"]):
                    wybrane.append(f)
            if not wybrane:
                raise RuntimeError("brak plików pasujących do config/split; dostępne: " + ",".join(sorted({f['config'] + '/' + f['split'] for f in lista}))[:300])
            for f in wybrane:
                c = f"{d}/{f['config']}__{f['split']}__{f['filename']}"
                wez(f["url"], c)
                st["pliki"].append({"plik": os.path.basename(c), "config": f["config"], "split": f["split"], "format": "parquet"})
        st["status"] = "OK"
    except Exception as e:  # noqa: BLE001
        st["status"] = "BLOCKED"
        st["powod"] = f"{type(e).__name__}: {str(e)[:400]}"
    status[tid] = st
    json.dump(status, open(f"{WYN}/status_pobran.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(tid, st["status"], st.get("powod", ""), len(st.get("pliki", [])), flush=True)
json.dump(status, open(f"{WYN}/status_pobran.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("KONIEC", flush=True)
