"""Helpers for the slayer-lab maths sources (finemath_4plus_en, cranemath_en, stack_edu_python).

Rows come from the filtered pool built in slayer-lab (dane/<set>/skrypty/odtworz.sh: pula, przebieg, agreguj): `wybor.json`
lists the global row numbers kept after every filter and chosen up to the export token target, and the pool units
(parquet path, row group) they live in. The text is passed to shard.write unchanged.

`no_masking()` replaces the Presidio pass of shard.write for these three sources. Measured on FineMath-4+ on 2026-11-24:
Presidio's PhoneRecognizer tagged 403 spans in 300 documents, almost all of them numbers in the maths itself
("80% = [PHONE] × 50", ISBNs, decimals, the Planck constant), so masking destroys the training signal. Personal data is
handled upstream instead: slayer-lab drops every document with an e-mail, phone, IP or obfuscated e-mail (finemath4,
cranemath) and every file with a secret or hard-coded password (stackedu); see dane/<set>/skrypty/preregistracja.json.
stats.json records the opt-out and the reason, so check.py's PII rescan failure is expected and explained in the datasheet."""
import json
import re

import pyarrow.parquet as pq

import pii


def rows(wybor_path: str, columns: list[str]):
    """Kept pool rows in pool order, as dicts with the requested columns."""
    w = json.load(open(wybor_path, encoding="utf-8"))
    starts, units = w["poczatki"], w["jednostki"]
    by_unit: dict[int, list[int]] = {}
    u = 0
    for g in w["dokumenty_globalne"]:
        while starts[u + 1] <= g:
            u += 1
        by_unit.setdefault(u, []).append(g - starts[u])
    for u in sorted(by_unit):
        path, rg = units[u]
        t = pq.ParquetFile(path).read_row_group(rg, columns=columns).to_pylist()
        for i in by_unit[u]:
            yield t[i]


REASON = ("Presidio not run: its phone recognizer masks numbers in mathematical text and code (403 spans in 300 FineMath-4+ "
          "documents, 2026-11-24). Documents with an e-mail, phone, IPv4 or obfuscated e-mail are dropped whole upstream "
          "(slayer-lab dane/<set>/skrypty/preregistracja.json, reasons pii, pii_zaciemniony, sekrety, haslo_w_kodzie).")
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Za-z]{2,})")
EXAMPLE_DOMAINS = {"example.com", "example.org", "example.net", "domain.com", "email.com", "yourdomain.com", "test.com"}
# e-mail written as name(AT)domain(DOT)tld / name [at] domain.tld: slayer-lab pattern pii_zaciemniony (aneks 24.11c)
EMAIL_AT = re.compile(r"[A-Za-z0-9._%+-]+\s?[\(\[]\s?(?:AT|at)\s?[\)\]]\s?[A-Za-z0-9.-]+\s?(?:[\(\[]\s?(?:DOT|dot)\s?[\)\]]|\.)\s?[A-Za-z]{2,}")
# e-mail written as name at domain.tld: slayer-lab pattern pii_at_bez_nawiasow (aneks 25.11c); masked only where the
# preregistration says so (formalna, aneks 26.11d): in web text the pattern also hits phrases like "available at Amazon.com"
EMAIL_BARE_AT = re.compile(r"[A-Za-z0-9._%+-]+ (?:at|AT) [A-Za-z0-9-]{2,}(?:(?:\.| (?:dot|DOT) )[A-Za-z0-9-]+)*(?:\.| (?:dot|DOT) )(?:com|org|net|edu|gov|mil|info|io|biz|[a-z]{2})\b")
# name-at-domain.tld (AFP headers, review 26.11): masked together with EMAIL_BARE_AT
EMAIL_DASH_AT = re.compile(r"[A-Za-z0-9._%+]+-at-[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}\b")
# name at domain tld with a space instead of the dot ("norbert.schirmer at web de", AFP header, review 26.11); the local
# part must contain '.' or '_' so that prose ("look at this de facto") is left alone
EMAIL_SPACE_TLD = re.compile(r"[A-Za-z0-9%+-]*[._][A-Za-z0-9._%+-]+ (?:at|AT) [A-Za-z0-9-]{2,} (?:com|org|net|edu|de|uk|fr|ch|it|nl|at|au|ca|jp)\b")
# arXiv author headers (aneks 26.11 arxiv_mat, review and pool residue scan 26.11): a list of local parts in braces,
# brackets or LaTeX braces sharing one domain, also wrapped over up to 3 lines ("{a.b,\nc.d}@uni.edu",
# "$\{a,b\}$@uni.edu", "<a,b>@uni.edu", "–a,b˝@uni.edu" with braces mangled by the conversion); an address broken by
# the line wrap at a hyphen, before or after '@' ("name@wias-\nberlin.de", "name\n@uni.edu", "name@\nuni.edu"); spaces
# around '@' ("name @ uni.edu"); a doubled '@@' (conversion artefact); local parts typeset in LaTeX math right before
# '@' ("$name$@uni.edu", "$\big{\{}$a, b$\big{\}}$@uni.edu"; from the first '$' within 200 characters, no blank line)
_DOMAIN = r" ?\n?((?:[A-Za-z0-9-]+-\n)?[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,})"
EMAIL_BRACED = re.compile(r"[\{\(\[<–][^{}()\[\]<>@\n–˝]{0,300}(?:\n[^{}()\[\]<>@\n–˝]{0,300}){0,2}[\}\)\]>˝] ?\n?(?:\$ ?)?@@?"
                          + _DOMAIN)
EMAIL_WRAPPED = re.compile(r"[A-Za-z0-9._%+-]+(?:-\n[A-Za-z0-9._%+-]+)?(?:\$\d+\$)?[\}\)\]>˝]? ?\n?@@?" + _DOMAIN)
EMAIL_LATEX = re.compile(r"\$(?:[^@\n]|\n(?!\n)){0,200}?\$ ?@@?" + _DOMAIN)
AT_AFTER_DOLLAR = re.compile(r"\$ ?@")
AT_AFTER_BRACE = re.compile(r"[\}\)\]>˝] ?\n?(?:\$ ?)?@")
# residue scan of the exported parts (27.11): "name{at}gmail.com", "name [at] amazon dot com", "name{at}gmail{dot}com",
# "first.last AT\nuni.fr" (local part with '.' or '_' so that prose is left alone)
_OBF_TLD = r"(?:com|org|net|edu|gov|info|io|de|uk|fr|ch|it|ac|au|nz|ca|jp|nl|be|at|cz|pl|dk|se|fi|no|es|pt|us|cn|in|br|ru|il|kr|tw|sg|hk|ie)\b"
EMAIL_OBF = re.compile(r"[A-Za-z0-9._%+-]+ ?[\{\[\(] ?(?:at|AT) ?[\}\]\)] ?([A-Za-z0-9-]+(?:(?: ?[\{\[\(] ?(?:dot|DOT) ?[\}\]\)] ?|\.| dot | DOT )[A-Za-z0-9-]+)*(?: ?[\{\[\(] ?(?:dot|DOT) ?[\}\]\)] ?|\.| dot | DOT )"
                       + _OBF_TLD + ")")
EMAIL_AT_NL = re.compile(r"[A-Za-z0-9%+-]*[._][A-Za-z0-9._%+-]+ (?:at|AT)\n([A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\." + _OBF_TLD + r")(?![/\w.])")
# full residue scan after the 27.11 re-export (27.11, second annex): logins without '.' wrapped after a lowercase "at":
# "login at\ngmail dot com", "login at\ngmail.com"; narrow on purpose: the domain is a mail provider, or is spelled with
# " dot " (prose like "available at\ngithub.com" or "contributors at\nmathoverflow.net" is left alone)
_MAIL_HOSTS = r"(?:gmail|googlemail|yahoo|ymail|hotmail|outlook|live|msn|icloud|aol|gmx|protonmail|proton|yandex|mail|qq|163|126|sina|web|t-online|orange|free|libero|naver|hanmail|rediffmail|zoho)"
EMAIL_AT_NL_MAIL = re.compile(r"(?:[A-Za-z0-9._%+-]+ dot )*[A-Za-z0-9._%+-]+ at\n(" + _MAIL_HOSTS + r"(?:\.| dot )[a-z]{2,3}(?:(?:\.| dot )[a-z]{2})?\b(?![/\w])"
                              r"|[A-Za-z0-9-]+(?: dot [A-Za-z0-9-]+)* dot " + _OBF_TLD + ")")


def _mask_emails(text: str, bare_at: bool = False, wrapped: bool = False) -> tuple[str, int]:
    n = 0

    def sub(m):
        nonlocal n
        if m.lastindex and m.group(1).lower() in EXAMPLE_DOMAINS:
            return m.group(0)
        n += 1
        return "[PII]"
    if wrapped and "@" in text:
        if AT_AFTER_DOLLAR.search(text):  # guard: EMAIL_LATEX tries every '$' of a paper
            text = EMAIL_LATEX.sub(sub, text)
        if AT_AFTER_BRACE.search(text):
            text = EMAIL_BRACED.sub(sub, text)
        text = EMAIL_WRAPPED.sub(sub, text)
    if wrapped:
        text = EMAIL_AT_NL_MAIL.sub(sub, EMAIL_AT_NL.sub(sub, EMAIL_OBF.sub(sub, text)))
    text = EMAIL_AT.sub(sub, EMAIL.sub(sub, text))
    return (EMAIL_SPACE_TLD.sub(sub, EMAIL_DASH_AT.sub(sub, EMAIL_BARE_AT.sub(sub, text))) if bare_at else text), n


MASKED = {"pii": 0}  # e-mails masked by premask_emails before shard.write


def premask_emails(text: str, bare_at: bool = False, wrapped: bool = False) -> str:
    """Mask e-mails BEFORE shard.write: its language gate then sees the same text check.py rescans. Masking inside
    shard.write ran after the gate, and 8 Python files whose gate vote flipped on the masked text failed check.py
    (independent check, 2026-11-25). bare_at: also `name at domain.tld` (formalna, aneks 26.11d). wrapped: also brace
    lists and hyphen-wrapped addresses (arxiv_math_en, aneks 26.11 arxiv_mat)."""
    masked, n = _mask_emails(text, bare_at, wrapped)
    MASKED["pii"] += n
    return masked


def no_masking(emails: bool = False) -> None:
    """Presidio off (see module docstring). emails=True (stack_edu_python): rows arrive pre-masked by premask_emails, and the
    count of masked e-mails goes into stats.json."""
    pii.mask = lambda texts, language, *, names=False: (list(texts), dict(MASKED) if emails else {})
    pii.record = lambda languages, *, names: {"pass": "regex e-mail only, before the language gate" if emails else "none",
                                              "reason": REASON}
