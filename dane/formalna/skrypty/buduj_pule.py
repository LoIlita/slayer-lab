"""Buduje pulę źródła 'formalna' (#357) z klonów w robocze/repo/<biblioteka> wg skrypty/preregistracja.json.

Wyjście: robocze/pula/<biblioteka>.parquet (row_group_size 5000), wyniki/probka_pliki.json, wyniki/budowa.json,
wyniki/duze_pliki.json, wyniki/hol_light_licencje.json.
Użycie: python buduj_pule.py   (venv dane/matematyka-wspolne/robocze/venv)
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import tomllib
from collections import Counter

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
from tokenizers import Tokenizer

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROB = f"{D}/robocze"
WYN = f"{D}/wyniki"
TOK_P = os.path.join(D, "..", "dclm-en", "robocze", "pobrania", "tokenizer_v6", "tokenizer.json")
TOK_SHA = "0640d3bd3674d7a6e59c540d945a2ad275a12e1bcaeb6007c37a90751f9815dd"
P = json.load(open(f"{D}/skrypty/preregistracja.json", encoding="utf-8"))
SEED = P["seed"]
LIB = P["zrodlo"]["biblioteki"]
REW = {k: P.get("aneks_2026_11_26c", {}).get("rewizje", {}).get(k, v["rewizja"]) for k, v in LIB.items()}
MAX_B = 1_000_000
MAX_FRAG = 50_000
RG = 5000

SPDX = {
    "mathlib4": "Apache-2.0", "hol_light": "BSD-2-Clause", "setmm": "CC0-1.0", "rocq_stdlib": "LGPL-2.1-only",
    "mathcomp": "CECILL-B", "unimath": "LicenseRef-UniMath", "agda_stdlib": "MIT",
    "stacks": "GFDL-1.2-no-invariants-or-later",
}
AFP_SPDX = {"bsd": "BSD-3-Clause", "lgpl": "LGPL-2.1-only"}
AFP_ZNACZNIK = re.compile(r"License:\s*(LGPL|LPGL|BSD)")


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def git(repo, *a):
    return subprocess.run(["git", "-C", repo, *a], check=True, capture_output=True).stdout


def daty(repo, rew):
    """Data ostatniego commita zmieniającego każdą ścieżkę (pierwsze wystąpienie w git log od rewizji)."""
    out = git(repo, "log", "--format=%x00%cI", "--name-only", "--no-renames", rew).decode("utf-8", "replace")
    d, cur = {}, None
    for ln in out.split("\n"):
        if ln.startswith("\x00"):
            cur = ln[1:]
        elif ln and ln not in d:
            d[ln] = cur
    return d


# aneks_2026_11_26b: commity z ujawnionym użyciem LLM
AI_WZORZEC = (r"\bClaude( Code| code| Opus| Sonnet| Fable| Haiku| [0-9]|\.|,|:| made| extracted| wrote| helped|"
              r" generated| was| did| has| had| and| to| for| in)|noreply@anthropic\.com|ChatGPT|\bGPT-?[0-9f]\b|"
              r"\bLLMs?\b|LLM-|Copilot|\bGemini\b|AlphaProof|DeepSeek|OpenAI|Anthropic|[Aa]utoformali[sz]|"
              r"[Ll]anguage [Mm]odels?\b|AI-generated|AI-assisted|[Gg]enerated (by|with|using) (an )?AI\b|by an AI\b|"
              r"\bAI systems?\b|\bCodex\b|Kimina|Goedel-Prover|\bAristotle\b|aristotle-harmonic|Gauss AI|Math Inc")
SETMM_AI = re.compile(r"Contributed by OpenAI|[Aa]sking Claude")


def pliki_ai(repo, rew):
    """{ścieżka: [hash, ...]} dla plików zmienianych przez commity pasujące do AI_WZORZEC; lista commitów."""
    out = git(repo, "log", "-P", f"--grep={AI_WZORZEC}", "--format=%H%x00%P%x00%cs%x00%s", rew).decode("utf-8", "replace")
    pl, kom = {}, []
    rx = re.compile(AI_WZORZEC)
    for ln in filter(None, out.split("\n")):
        h, par, d, subj = ln.split("\x00", 3)
        cia = git(repo, "log", "-1", "--format=%B", h).decode("utf-8", "replace")
        m = rx.search(cia)
        a = ["diff-tree", "-r", "--name-only", "--no-commit-id"]
        zm = git(repo, *(a + ([par.split()[0], h] if par else ["--root", h]))).decode("utf-8", "replace").split("\n")
        zm = [z for z in zm if z]
        kom.append({"commit": h, "data": d, "temat": subj[:200], "trafienie": cia[max(0, m.start() - 60): m.end() + 60] if m else "",
                    "plikow": len(zm)})
        for z in zm:
            pl.setdefault(z, []).append(h[:10])
    return pl, kom


# ---------- wybór plików ----------

def wybierz(lib, sciezki, repo):
    """Zwraca (wybrane, wykluczone: dict sciezka -> powód)."""
    wyk, wyb = {}, []
    for s in sciezki:
        powod = None
        if lib == "mathlib4":
            if not s.endswith(".lean"):
                continue
            if not s.startswith(("Mathlib/", "Archive/", "Counterexamples/")):
                powod = "poza_Mathlib_Archive_Counterexamples" if not s.startswith("MathlibTest/") else "testy"
            elif s.startswith(("Mathlib/Tactic/", "Mathlib/Util/", "Mathlib/Lean/")):
                powod = "metaprogramowanie"
        elif lib == "afp":
            if not s.endswith(".thy"):
                continue
            if not s.startswith("thys/"):
                powod = "poza_thys"
        elif lib == "hol_light":
            if not s.endswith(".ml"):
                continue
        elif lib == "setmm":
            if s not in ("set.mm", "iset.mm"):
                continue
        elif lib == "rocq_stdlib":
            if not s.endswith(".v"):
                continue
            if not s.startswith("theories/"):
                powod = "poza_theories"
        elif lib == "mathcomp":
            if not s.endswith(".v"):
                continue
            if s.startswith(("test-suite/", "docs/", "doc/", "etc/", ".nix/", ".github/")):
                powod = "testy_lub_pomocnicze"
        elif lib == "unimath":
            if not s.endswith(".v"):
                continue
            if not s.startswith("UniMath/"):
                powod = "poza_UniMath"
        elif lib == "agda_stdlib":
            if not (s.endswith(".agda") or s.endswith(".lagda.md")):
                continue
            if not s.startswith("src/"):
                powod = "poza_src"
        elif lib == "stacks":
            if not s.endswith(".tex"):
                continue
            if "/" in s:
                powod = "podkatalog"
            elif s in ("fdl.tex", "preamble.tex", "chapters.tex", "book.tex", "bibliography.tex"):
                powod = "licencja_lub_preambula"
        if powod:
            wyk[s] = powod
        else:
            wyb.append(s)
    return wyb, wyk


# ---------- HOL Light: licencje per plik ----------

LIC_RE = re.compile(r"GPL|\bMIT\b|Apache|Creative Commons|public domain|licen[cs]e", re.I)


def typ_licencji(t):
    """Licencja podkatalogu HOL Light z tekstu pliku licencji (aneks 2026-11-26)."""
    if t.lstrip().startswith("MIT License") or "Permission is hereby granted, free of charge" in t:
        return "MIT"
    if "Redistribution and use in source and binary forms" in t and "Neither the name" not in t \
            and "advertising" not in t.lower():
        return "BSD-2-Clause"
    return None


def hol_licencje(repo, wyb):
    pod = {}
    for s in git(repo, "ls-files").decode().split("\n"):
        b = os.path.basename(s).upper()
        if "/" in s and (b.startswith("LICEN") or b.startswith("COPYING")):
            t = open(f"{repo}/{s}", encoding="utf-8", errors="replace").read()
            pod[os.path.dirname(s)] = (s, typ_licencji(t), t[:300])
    zostaw, lic, wyk = [], {}, {}
    for s in wyb:
        katalogi = sorted((k for k in pod if s.startswith(k + "/")), key=len)
        l = "BSD-2-Clause"
        if katalogi:
            k = katalogi[-1]
            l = pod[k][1]
            if l is None:
                wyk[s] = {"powod": "podkatalog_z_inna_licencja", "plik_licencji": pod[k][0], "poczatek": pod[k][2]}
                continue
        nag = open(f"{repo}/{s}", encoding="utf-8", errors="replace").read(3000)
        m = LIC_RE.search(nag)
        if m and "HOL Light" not in nag[max(0, m.start() - 300): m.end() + 300]:
            i = nag.rfind("\n", 0, m.start())
            wyk[s] = {"powod": "naglowek_z_inna_licencja", "fragment": nag[max(0, i): m.end() + 200]}
            continue
        zostaw.append(s)
        lic[s] = l
    return zostaw, lic, wyk, {k: {"plik": v[0], "licencja": v[1]} for k, v in pod.items()}


# ---------- set.mm ----------

MARK = re.compile(r"^\s*(#{4,}|#\*#\*|=-=-|-\.-\.)")
PROOF = re.compile(r"\$=\s.*?\s\$\.", re.S)


def bez_dowodow(t):
    return PROOF.sub("$= ? $.", t)


def fragmenty_mm(lines):
    """Granice: wiersz '$(' przed wierszem znacznika sekcji. Zwraca [(od, do)] (0-based, do wyłącznie)."""
    gr = [0]
    for i in range(1, len(lines) - 1):
        if lines[i].strip() == "$(" and MARK.match(lines[i + 1]) and i != gr[-1]:
            gr.append(i)
    gr.append(len(lines))
    jednostki = []
    for a, b in zip(gr, gr[1:]):
        dl = len(bez_dowodow("".join(lines[a:b])))
        if dl <= MAX_FRAG:
            jednostki.append((a, b, dl))
            continue
        # sekcja za długa: podział na końcach instrukcji ('$.' kończący wiersz)
        s = a
        acc = 0
        for i in range(a, b):
            if lines[i].rstrip().endswith("$.") or i == b - 1:
                kaw = len(bez_dowodow("".join(lines[s:i + 1])))
                jednostki.append((s, i + 1, kaw))
                s = i + 1
        if s < b:
            jednostki.append((s, b, len(bez_dowodow("".join(lines[s:b])))))
    return grupuj(jednostki)


def grupuj(jednostki):
    out, cur, dl = [], None, 0
    for a, b, n in jednostki:
        if cur is not None and dl + n > MAX_FRAG:
            out.append(cur)
            cur, dl = None, 0
        cur = (cur[0], b) if cur else (a, b)
        dl += n
    if cur:
        out.append(cur)
    return out


def fragmenty_tex(lines):
    gr = [0] + [i for i in range(1, len(lines)) if lines[i].startswith("\\section{")] + [len(lines)]
    return grupuj([(a, b, len("".join(lines[a:b]))) for a, b in zip(gr, gr[1:])])


# ---------- budowa ----------

def czytaj(p):
    b = open(p, "rb").read()
    t = b.decode("utf-8")
    if t.startswith("\ufeff"):
        t = t[1:]
    return t.replace("\r\n", "\n").replace("\r", "\n")


def main():
    assert sha256(TOK_P) == TOK_SHA, "zły tokenizer"
    tok = Tokenizer.from_file(TOK_P)
    os.makedirs(f"{ROB}/pula", exist_ok=True)
    os.makedirs(WYN, exist_ok=True)
    tylko = set(sys.argv[1:])
    budowa, duze, pliki, hol, ai = {}, [], [], {}, {}
    for lib, cfg in LIB.items():
        if tylko and lib not in tylko:
            continue
        repo = f"{ROB}/repo/{lib}"
        rew = REW[lib]
        head = git(repo, "rev-parse", "HEAD").decode().strip()
        assert head == rew, f"{lib}: HEAD {head} != {rew}"
        gh = cfg["repo"].replace("https://github.com/", "")
        rew_data = git(repo, "log", "-1", "--format=%cI", rew).decode().strip()
        sciezki = sorted(git(repo, "ls-files").decode().split("\n")[:-1])
        wyb, wyk = wybierz(lib, sciezki, repo)
        lic = {}
        if lib == "afp":
            ok = []
            for s in wyb:
                wpis = s.split("/")[1]
                tp = f"{repo}/metadata/entries/{wpis}.toml"
                if not os.path.exists(tp):
                    wyk[s] = "afp_brak_toml"
                    continue
                l = tomllib.load(open(tp, "rb")).get("license")
                if l not in AFP_SPDX:
                    wyk[s] = f"afp_licencja_{l}"
                    continue
                m = AFP_ZNACZNIK.search(open(f"{repo}/{s}", encoding="utf-8", errors="replace").read(3000))
                lic[s] = AFP_SPDX[l] if not m else ("BSD-3-Clause" if m.group(1) == "BSD" else "LGPL-2.1-only")
                ok.append(s)
            wyb = ok
        if lib == "hol_light":
            wyb, lic, wh, pod = hol_licencje(repo, wyb)
            hol = {"wykluczone": wh, "podkatalogi_z_licencja": pod, "zostawione": len(wyb),
                   "licencje": dict(Counter(lic.values()))}
            wyk.update({s: v["powod"] for s, v in wh.items()})
        ai_pl, ai_kom = pliki_ai(repo, rew)
        ai_wyk = []
        if lib != "setmm":
            ok = []
            for s in wyb:
                if s in ai_pl:
                    wyk[s] = "ai_commit"
                    ai_wyk.append(s)
                else:
                    ok.append(s)
            wyb = ok
        ai_frag = []
        dat = daty(repo, rew)
        rng = np.random.default_rng(SEED)
        wyb = [wyb[i] for i in rng.permutation(len(wyb))]
        wiersze = []
        for s in wyb:
            pth = f"{repo}/{s}"
            rozm = os.path.getsize(pth)
            try:
                t = czytaj(pth)
            except UnicodeDecodeError:
                wyk[s] = "nie_utf8"
                continue
            base = dict(license=lic.get(s, SPDX.get(lib)), created=dat.get(s) or rew_data,
                        repo=cfg["repo"], path=s, biblioteka=lib)
            url0 = f"https://github.com/{gh}/blob/{rew}/{s}"
            id0 = f"formalna/{lib}/{s}"
            if lib == "setmm" or (lib == "stacks" and rozm > MAX_B):
                lines = t.splitlines(keepends=True)
                fr = fragmenty_mm(lines) if lib == "setmm" else fragmenty_tex(lines)
                if lib == "stacks":
                    duze.append({"biblioteka": lib, "plik": s, "bajty": rozm, "decyzja": f"podzielony na {len(fr)} fragmentów"})
                for a, b in fr:
                    tx = "".join(lines[a:b])
                    r = f"#L{a + 1}-L{b}"
                    if lib == "setmm":
                        tx = bez_dowodow(tx)
                        if SETMM_AI.search(tx):
                            ai_frag.append({"id": id0 + r, "znaki": len(tx), "tokeny_v6": len(tok.encode(tx, add_special_tokens=False).ids) + 1,
                                            "trafienie": SETMM_AI.search(tx).group(0)})
                            continue
                    wiersze.append(dict(base, text=tx, url=url0 + r, id=id0 + r))
                continue
            if rozm > MAX_B:
                wyk[s] = "powyzej_1MB"
                duze.append({"biblioteka": lib, "plik": s, "bajty": rozm, "decyzja": "wykluczony"})
                continue
            wiersze.append(dict(base, text=t, url=url0, id=id0))
        # tokeny
        tk = []
        for i in range(0, len(wiersze), 2000):
            enc = tok.encode_batch([w["text"] for w in wiersze[i:i + 2000]], add_special_tokens=False)
            tk += [len(e.ids) + 1 for e in enc]
        for w, n in zip(wiersze, tk):
            w["tokeny_v6"] = n
        ai_tok = {}
        for s in ai_wyk:
            try:
                ai_tok[s] = len(tok.encode(czytaj(f"{repo}/{s}"), add_special_tokens=False).ids) + 1
            except UnicodeDecodeError:
                ai_tok[s] = None
        ai[lib] = {"commitow": len(ai_kom), "plikow_wykluczonych": len(ai_wyk),
                   "tokeny_v6_wykluczonych": int(sum(v for v in ai_tok.values() if v)),
                   "fragmenty_setmm": ai_frag, "commity": ai_kom,
                   "pliki": {s: {"tokeny_v6": ai_tok[s], "commity": ai_pl[s]} for s in sorted(ai_wyk)}}
        kol = ["text", "url", "id", "license", "created", "repo", "path", "biblioteka", "tokeny_v6"]
        tab = pa.table({k: [w[k] for w in wiersze] for k in kol},
                       schema=pa.schema([(k, pa.int64() if k == "tokeny_v6" else pa.string()) for k in kol]))
        out = f"{ROB}/pula/{lib}.parquet"
        pq.write_table(tab, out, row_group_size=RG, compression="zstd")
        T = int(sum(tk))
        pliki.append({"plik": lib, "repo": cfg["repo"], "rewizja": rew, "rozmiar": os.path.getsize(out),
                      "sha256": sha256(out), "wiersze": len(wiersze), "tokeny_v6": T, "lokalnie": out})
        budowa[lib] = {
            "repo": cfg["repo"], "rewizja": rew, "data_rewizji": rew_data,
            "plikow_wybranych": len({w["path"] for w in wiersze}), "wiersze": len(wiersze), "tokeny_v6": T,
            "znaki": int(sum(len(w["text"]) for w in wiersze)),
            "bajty_plikow_zrodlowych": int(sum(os.path.getsize(f"{repo}/{p}") for p in {w["path"] for w in wiersze})),
            "licencje_wierszy": dict(Counter(w["license"] for w in wiersze)),
            "licencje_tokeny": {l: int(sum(w["tokeny_v6"] for w in wiersze if w["license"] == l))
                                for l in sorted({w["license"] for w in wiersze})},
            "wykluczone_powody": dict(Counter(wyk.values())),
            "wykluczone_przyklady": {p: [s for s, v in wyk.items() if v == p][:10] for p in set(wyk.values())},
            "tokeny_max": int(max(tk)) if tk else 0,
            "tokeny_mediana": int(np.median(tk)) if tk else 0,
            "ai_plikow_wykluczonych": len(ai_wyk) + len(ai_frag),
            "ai_tokeny_v6_wykluczonych": ai[lib]["tokeny_v6_wykluczonych"] + int(sum(f["tokeny_v6"] for f in ai_frag)),
        }
        print(lib, json.dumps({k: budowa[lib][k] for k in ("wiersze", "tokeny_v6", "wykluczone_powody")}, ensure_ascii=False), flush=True)
    if tylko:
        return
    W = sum(p["wiersze"] for p in pliki)
    T = sum(p["tokeny_v6"] for p in pliki)
    json.dump({"repo": "formalna (9 repozytoriów git; repo i rewizja per plik w pliki[])",
               "rewizja": "per biblioteka, pliki[].rewizja = skrypty/preregistracja.json zrodlo.biblioteki",
               "seed": SEED, "wiersze": W, "tokeny_v6": T, "pliki": pliki},
              open(f"{WYN}/probka_pliki.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump({"tokenizer_sha256": TOK_SHA, "wiersze": W, "tokeny_v6": T, "biblioteki": budowa},
              open(f"{WYN}/budowa.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(duze, open(f"{WYN}/duze_pliki.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(hol, open(f"{WYN}/hol_light_licencje.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(ai, open(f"{WYN}/ai_wykluczone.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("KONIEC", W, T)


if __name__ == "__main__":
    main()
