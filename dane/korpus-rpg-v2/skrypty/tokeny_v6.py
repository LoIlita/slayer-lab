"""Liczy tokeny v6 dla każdego wiersza wejścia: n = tokeny bez znaków specjalnych + 1 (EOT po dokumencie). Zapisuje n_NNNN.npy per grupa wierszy
oraz listę wierszy, w których tekst sam koduje się na id 0 (EOT w środku dokumentu psułby granice paczki).
Argumenty: wejscie.parquet tokenizer.json katalog_wyjscia procesy."""
import json
import multiprocessing as mp
import os
import sys

os.environ["TOKENIZERS_PARALLELISM"] = "false"
import numpy as np  # noqa: E402
import pyarrow.parquet as pq  # noqa: E402
from tokenizers import Tokenizer  # noqa: E402

P, TOK, OUT, PROC = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
TK = None


def init():
    global TK
    TK = Tokenizer.from_file(TOK)


def grupa(g):
    t = pq.ParquetFile(P).read_row_group(g, columns=["text"]).column(0).to_pylist()
    n, zera, mx = [], [], 0
    for i, e in enumerate(TK.encode_batch(t, add_special_tokens=False)):
        ids = e.ids
        n.append(len(ids) + 1)
        if ids:
            mx = max(mx, max(ids))
        if 0 in ids:
            zera.append([g, i, ids.count(0)])
    np.save(f"{OUT}/.tmp_{g:04d}.npy", np.asarray(n, dtype=np.int64))
    os.replace(f"{OUT}/.tmp_{g:04d}.npy", f"{OUT}/n_{g:04d}.npy")
    json.dump({"zera": zera, "max_id": mx}, open(f"{OUT}/z_{g:04d}.json", "w"))
    return g


def main():
    os.makedirs(OUT, exist_ok=True)
    pf = pq.ParquetFile(P)
    gr = [g for g in range(pf.num_row_groups) if not os.path.exists(f"{OUT}/n_{g:04d}.npy") or not os.path.exists(f"{OUT}/z_{g:04d}.json")]
    print("do policzenia grup:", len(gr), flush=True)
    with mp.get_context("fork").Pool(PROC, initializer=init) as p:
        for k, g in enumerate(p.imap_unordered(grupa, gr, chunksize=1), 1):
            if k % 10 == 0:
                print(k, "/", len(gr), flush=True)
    razem, zera, mx = 0, [], 0
    for g in range(pf.num_row_groups):
        razem += int(np.load(f"{OUT}/n_{g:04d}.npy").sum())
        d = json.load(open(f"{OUT}/z_{g:04d}.json"))
        zera += d["zera"]
        mx = max(mx, d["max_id"])
    wyn = {"tokeny_wejscia_v6_z_eot": razem, "wiersze_z_id_0_w_tekscie": len(zera), "przyklady": zera[:20], "max_id": mx}
    json.dump(wyn, open(f"{OUT}/podsumowanie.json", "w", encoding="utf-8"), indent=1)
    print(json.dumps(wyn), flush=True)


if __name__ == "__main__":
    main()
