import gzip, json, hashlib, re
from tokenizers import Tokenizer
TOK = Tokenizer.from_file("/Users/lolita/Documents/GitHub/slayer-lab/dane/dclm-en/robocze/pobrania/tokenizer_v6/tokenizer.json")


def ntok_batch(ts):
    return [len(e.ids) + 1 for e in TOK.encode_batch(ts, add_special_tokens=False)]


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 24), b""):
            h.update(b)
    return h.hexdigest()


def it(p):
    with gzip.open(p, "rt") as f:
        for l in f:
            yield json.loads(l)


EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")
MOJI = re.compile(r"(\ufffd|Ã[\u0080-\u00bf©¨¶¼ª«´³]|â€[\u0080-\u00bf™œ\x9d“”˜¢¦]|Â[\u00a0-\u00bf])")
SEG = re.compile(r"\$\$?([^$\n]{1,300})\$\$?")
MATHY = re.compile(r"[\\^_=]")
CMD = re.compile(r"\\(frac|sum|int|mathbb|mathcal|left|sqrt|alpha|beta|gamma|delta|theta|lambda|sigma|omega|pi|cdot|leq|geq|in|subset|forall|exists|infty|partial|nabla|lim|log|sin|cos|binom|mathrm|operatorname|begin)\b")


def math_feats(t):
    s = sum(1 for m in SEG.finditer(t) if MATHY.search(m.group(1)))
    c = len(CMD.findall(t))
    return s, c
