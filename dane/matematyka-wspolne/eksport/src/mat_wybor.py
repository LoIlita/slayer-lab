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
# name at domain tld with a space instead of the dot ("norbert.schirmer at web de", AFP header, review 26.11)
EMAIL_SPACE_TLD = re.compile(r"[A-Za-z0-9._%+-]+ (?:at|AT) [A-Za-z0-9-]{2,} (?:com|org|net|edu|de|uk|fr|ch|it|nl|at|au|ca|jp)\b")


def _mask_emails(text: str, bare_at: bool = False) -> tuple[str, int]:
    n = 0

    def sub(m):
        nonlocal n
        if m.lastindex and m.group(1).lower() in EXAMPLE_DOMAINS:
            return m.group(0)
        n += 1
        return "[PII]"
    text = EMAIL_AT.sub(sub, EMAIL.sub(sub, text))
    return (EMAIL_SPACE_TLD.sub(sub, EMAIL_DASH_AT.sub(sub, EMAIL_BARE_AT.sub(sub, text))) if bare_at else text), n


MASKED = {"pii": 0}  # e-mails masked by premask_emails before shard.write


def premask_emails(text: str, bare_at: bool = False) -> str:
    """Mask e-mails BEFORE shard.write: its language gate then sees the same text check.py rescans. Masking inside
    shard.write ran after the gate, and 8 Python files whose gate vote flipped on the masked text failed check.py
    (independent check, 2026-11-25). bare_at: also `name at domain.tld` (formalna, aneks 26.11d)."""
    masked, n = _mask_emails(text, bare_at)
    MASKED["pii"] += n
    return masked


def no_masking(emails: bool = False) -> None:
    """Presidio off (see module docstring). emails=True (stack_edu_python): rows arrive pre-masked by premask_emails, and the
    count of masked e-mails goes into stats.json."""
    pii.mask = lambda texts, language, *, names=False: (list(texts), dict(MASKED) if emails else {})
    pii.record = lambda languages, *, names: {"pass": "regex e-mail only, before the language gate" if emails else "none",
                                              "reason": REASON}
