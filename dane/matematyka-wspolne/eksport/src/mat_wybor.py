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
# obfuscated author e-mails in source-code headers (stack_edu_python, aneks 2026-11-27 in dane/stackedu; final check found
# 'name_at_domain.tld'): forms without '@' that EMAIL_AT does not cover; the domain must end in a listed TLD, so that code
# like `obj_at_index` or prose "look at self.x" is left alone (scan dane/matematyka-wspolne/skrypty/skan_zaciemnione.py)
_CODE_TLD = r"(?:com|org|net|edu|gov|mil|info|io|biz|de|uk|fr|ch|it|ac|au|nz|ca|jp|nl|be|at|cz|pl|dk|se|fi|no|es|pt|us|cn|in|br|ru|il|kr|tw|sg|hk|ie|hu|gr|ro|sk|si|lt|lv|ee|mx|ar|cl|za|tr|ir)"
_CODE_SEPD = r"(?:\.|_dot_|\(dot\)|\[dot\]|\{dot\}|<dot>| dot | DOT )"
EMAIL_CODE_OBF = [
    re.compile(r"[A-Za-z0-9.+-]+_at_([A-Za-z0-9-]+(?:" + _CODE_SEPD + r"[A-Za-z0-9-]+)*" + _CODE_SEPD + _CODE_TLD + r")\b"),
    re.compile(r"[A-Za-z0-9._%+-]+ ?[\{<] ?(?:at|AT) ?[\}>] ?([A-Za-z0-9-]+(?:" + _CODE_SEPD + r"[A-Za-z0-9-]+)*" + _CODE_SEPD + _CODE_TLD + r")\b"),
    re.compile(r"[A-Za-z0-9._%+-]+ (?:at|AT) ([A-Za-z0-9-]+(?: (?:dot|DOT) [A-Za-z0-9-]+)* (?:dot|DOT) " + _CODE_TLD + r")\b"),
    re.compile(r"[A-Za-z0-9._%+-]+ AT ([A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\." + _CODE_TLD + r")\b"),
    re.compile(r"[A-Za-z0-9._%+-]*[._][A-Za-z0-9._%+-]+ at ([A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\." + _CODE_TLD + r")\b(?![/\w.])"),
]
# the same forms in web text (finemath_4plus_en, infiwebmath_4plus_en, stackexchange_math, cranemath_en; aneks 2026-11-27
# zaciemnione_proza in dane/<set>/skrypty/preregistracja.json): mailing-list archives ("From: Name <login_at_uni.edu>",
# pipermail headers "Name login at uni.edu" over the date line, "<login at uni.edu> wrote:"), letter headers and page
# footers. Narrower than EMAIL_CODE_OBF where prose would trip it, wider where the archives write addresses differently:
# - `_at_`: '_' allowed in the name ("R_dot_Lyons_at_ieee_dot_org"), a second-level ccTLD is taken along ("uni.ac.th");
# - `at … dot`: the first domain label has 2+ characters and is not a determiner ("arrive at a dot in", "at the dot in"),
#   a leading "first dot last" is taken along;
# - `AT domain.tld`: the name has a lowercase letter or digit ("FIND ME AT dansmath.com" is a site, not an address);
# - `x.y at domain.tld`: a valid name (no trailing '.', so "e.g. at amazon.com" is left alone);
# - `<login at domain.tld>` filling a whole <…>, (…) or […], `login at <mail provider>.tld` and a pipermail header line
#   (also "login at domain login at domain" when the poster gave no name): the name may lack '.' there; a common word as the
#   name ("(available at amazon.com)", "account at gmail.com", any case) is left alone;
# - `login at domain.tld` right after an address label ("Email:", "mailto:", "To: ", "From: ", "Reply-to: ", "e-mail to "),
#   in a signature line (alone on its line or at its end after a gap) and in a quote header ("login at uni.edu wrote:");
#   in <…>, signatures and quote headers the TLD may be upper case ("<name at RELAY.CS.NET>").
_PROSE_TLD = r"(?:" + _CODE_TLD[3:-1] + r")(?:\.[a-z]{2})?"
_PROSE_DOMAIN = r"[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\." + _PROSE_TLD
_PROSE_DOMAIN_CI = r"[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.(?i:" + _PROSE_TLD + r")"  # "<name%host at RELAY.CS.NET>", "[name at UGA.EDU]"
_PROSE_WORDS = (r"(?!(?i:and|or|nor|but|also|as|even|only|both|not|just|either|neither|then|to|"
                r"available|found|located|look|looking|see|here|there|online|posted|published|sold|buy|bought|"
                r"purchased|hosted|open|now|it|me|us|you|him|her|them|this|that|which|one|account|accounts|address|mail|"
                r"email|e-mail|inbox|sign|signed|registered|login|log|user|users|someone|people|everyone|anyone|"
                r"free|cheaper|cheap|price|prices|sale|deals|info|information|details|more|less|work|works|job|jobs|"
                r"page|site|website|blog|link|links|copy|copies|book|books|download|downloads|order|orders|store|shop)"
                r" (?:at|AT) )")
_DAYS = r"(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)(?:,? \d{1,2})? (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) "
_LABELS = [lab + sp for lab in ("mailto:", "email:", "Email:", "EMAIL:", "e-mail:", "E-mail:", "E-Mail:", "E-MAIL:")
           for sp in ("", " ")] + ["To: ", "From: ", "Cc: ", "CC: ", "Sender: ", "Reply-To: ", "Reply-to: ", "email : ",
                                   "e-mail : ", "email to ", "e-mail to ", "Email to ", "E-mail to "]
_PROSE_MAIL_HOSTS = _MAIL_HOSTS[:-1] + r"|comcast|verizon|att|earthlink|btinternet|cox|sbcglobal|netscape|mindspring|bigfoot|alltel|juno|bellsouth|netcom)"
EMAIL_PROSE_OBF = [
    re.compile(r"(?<![A-Za-z0-9._+-])[A-Za-z0-9._+-]+_at_([A-Za-z0-9-]+(?:" + _CODE_SEPD + r"[A-Za-z0-9-]+)*" + _CODE_SEPD + _PROSE_TLD + r")\b"),
    re.compile(r"(?<![A-Za-z0-9._%+-])[A-Za-z0-9._%+-]+ ?[\{<] ?(?:at|AT) ?[\}>] ?([A-Za-z0-9-]+(?:" + _CODE_SEPD + r"[A-Za-z0-9-]+)*" + _CODE_SEPD + _PROSE_TLD + r")\b"),
    re.compile(r"(?<![A-Za-z0-9._%+-])(?:[A-Za-z0-9._%+-]+ (?:dot|DOT) )*[A-Za-z0-9._%+-]+ (?:at|AT) (?!(?:the|a|an|this|that|each|every|one|any|its|his|her|our|their|my|your)\b)"
               r"([A-Za-z0-9-]{2,}(?: (?:dot|DOT) [A-Za-z0-9-]+)* (?:dot|DOT) " + _CODE_TLD + r")\b"),
    re.compile(r"(?<![A-Za-z0-9._%+-])(?=[A-Za-z0-9._%+-]*[a-z0-9])[A-Za-z0-9._%+-]+ AT (" + _PROSE_DOMAIN + r")\b"),
    re.compile(r"(?<![A-Za-z0-9._%+-])[A-Za-z0-9%+-]+(?:[._][A-Za-z0-9%+-]+)+ at (" + _PROSE_DOMAIN + r")\b(?!\.?[/\w])"),
    re.compile(r"(?<=[<(\[])" + _PROSE_WORDS + r"[A-Za-z0-9._%+-]+ (?:at|AT) (" + _PROSE_DOMAIN_CI + r")(?= ?[>)\]]| ?<mailto)"),
    re.compile(r"(?<=>)" + _PROSE_WORDS + r"[A-Za-z0-9._%+-]+ (?:at|AT) (" + _PROSE_DOMAIN_CI + r")(?=<mailto)"),
    re.compile(r"(?<![\w.@-])" + _PROSE_WORDS + r"[A-Za-z0-9_%+-]+ (?:at|AT) (" + _PROSE_MAIL_HOSTS + r"\.(?:com|net|org|de|fr|it|es|ru|cn|ca|nl|pl)(?:\.[a-z]{2})?)\b(?!\.?[/\w])"),
    re.compile(r"(?m)^[A-Za-z0-9._%+-]+ at ([A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,})(?= [A-Za-z0-9._%+-]+ at [A-Za-z0-9.-]+\n" + _DAYS + r")"),
    re.compile(r"(?m)(?<=[^\n] )[A-Za-z0-9._%+-]+ at ([A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,})(?=\n(?:> ?)*" + _DAYS + r")"),
    re.compile(r"(?:" + "|".join(f"(?<={re.escape(lab)})" for lab in _LABELS) + r")[A-Za-z0-9._%+-]+ (?:at|AT) "
               r"([A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,})\b(?!\.?[/\w])"),
    # signature lines: the address alone on a line (also quoted "> "), or at the end of a line after a tab, 2+ spaces or
    # ": ", followed by nothing, a "(note)", a link or a wide gap ("Jon Perry\nperry at uni.co.uk\nhttp://…"); a capitalised
    # word as the name is a site phrase, not a login ("Created at edHelper.Com", "Crossposted at Math.SE")
    re.compile(r"(?m)(?:^|(?<=^> )|(?<=^>> )|(?<=^> > )|(?<=  )|(?<=\t)|(?<=\xa0)|(?<=: ))(?![A-Z][a-z])" + _PROSE_WORDS + r"[A-Za-z0-9._%+-]+ (?:at|AT) ("
               + _PROSE_DOMAIN_CI + r")(?=[ \t]*(?:$|\(|https?://|www\.)|[ \t]{2,})"),
    # quote headers: "login at uni.edu wrote:", "login at uni.edu (Jan\n> Kowal) writes:"
    re.compile(r"(?<![A-Za-z0-9._%+-])" + _PROSE_WORDS + r"[A-Za-z0-9._%+-]+ (?:at|AT) (" + _PROSE_DOMAIN_CI
               + r")(?=[\s>]+(?:\([^()\n]{1,40}(?:\n[> ]*[^()\n]{0,40})?\)\s+)?(?:wrote|writes|said)\b)"),
]
# cheap necessary condition of each EMAIL_PROSE_OBF pattern (same result, the full pattern runs only where it can match:
# almost every web page has " at "). Every pattern starts at the beginning of a run of name characters (look-behind), so
# a page with a long run of letters or digits (digits of pi, base64) costs linear, not quadratic time.
_PROSE_GUARDS = [re.compile(g) for g in (r"_at_", r"[\{<] ?(?:at|AT) ?[\}>]", r" (?:dot|DOT) ", r" AT ", r"[._][A-Za-z0-9%+-]+ at ",
                                         r" (?:at|AT) [A-Za-z0-9.-]+ ?[<>)\]]", r" (?:at|AT) [A-Za-z0-9.-]+<mailto",
                                         r" (?:at|AT) " + _PROSE_MAIL_HOSTS + r"\.",
                                         r"\n" + _DAYS, r"\n(?:> ?)*" + _DAYS, r"(?::|to) ?[A-Za-z0-9._%+-]+ (?:at|AT) [A-Za-z0-9-]+\.",
                                         r" (?:at|AT) [A-Za-z0-9-]+\.", r" (?:wrote|writes|said)\b")]
# second, targeted pass of prose_obf (aneks 2026-11-27 zaciemnione_proza, field `resztki_maskowane`): person addresses the
# generic patterns leave on purpose (all-caps name, no label, '!' before the login), found by the broad 'x at domain' scan
# of the text AFTER the mask and reviewed by hand; exact strings, so the generic patterns stay narrow
EMAIL_PERSON_EXACT = ("MIKE AT IMAPENGUIN.COM", "jhefferon at smcvt.edu", "gindrup at okway.okstate.edu",
                      "jkuangATvcccd.edu", "cking at lyon.k12.nv.us", "hongy... at gmail.com", "lap at mantr.com",
                      "Kim at mathisFigureOutAble.com")
# EMAIL and EMAIL_AT tried from every position are quadratic on such runs (first met in FineMath-4+ text, 27.11): the same
# patterns anchored at the start of a run find a match exactly when the originals find one (the leftmost match of the
# originals always starts there), so they decide cheaply whether the original has to run at all
_EMAIL_FIND = re.compile(r"(?<![A-Za-z0-9._%+-])" + EMAIL.pattern)
_EMAIL_AT_FIND = re.compile(r"(?<![A-Za-z0-9._%+-])" + EMAIL_AT.pattern)


def _mask_emails(text: str, bare_at: bool = False, wrapped: bool = False, code_obf: bool = False,
                 prose_obf: bool = False) -> tuple[str, int]:
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
    if _EMAIL_FIND.search(text):
        text = EMAIL.sub(sub, text)
    if _EMAIL_AT_FIND.search(text):
        text = EMAIL_AT.sub(sub, text)
    if code_obf:
        for rx in EMAIL_CODE_OBF:
            text = rx.sub(sub, text)
    if prose_obf:
        for guard, rx in zip(_PROSE_GUARDS, EMAIL_PROSE_OBF):
            if guard.search(text):
                text = rx.sub(sub, text)
        for s in EMAIL_PERSON_EXACT:
            if s in text:
                n += text.count(s)
                text = text.replace(s, "[PII]")
    return (EMAIL_SPACE_TLD.sub(sub, EMAIL_DASH_AT.sub(sub, EMAIL_BARE_AT.sub(sub, text))) if bare_at else text), n


MASKED = {"pii": 0}  # e-mails masked by premask_emails before shard.write


def premask_emails(text: str, bare_at: bool = False, wrapped: bool = False, code_obf: bool = False,
                   prose_obf: bool = False) -> str:
    """Mask e-mails BEFORE shard.write: its language gate then sees the same text check.py rescans. Masking inside
    shard.write ran after the gate, and 8 Python files whose gate vote flipped on the masked text failed check.py
    (independent check, 2026-11-25). bare_at: also `name at domain.tld` (formalna, aneks 26.11d). wrapped: also brace
    lists and hyphen-wrapped addresses (arxiv_math_en, aneks 26.11 arxiv_mat). code_obf: obfuscated forms in code
    headers, `name_at_domain.tld`, `name <at> domain`, `name at domain dot tld`, `name AT domain.tld` (stack_edu_python,
    aneks 2026-11-27 dane/stackedu). prose_obf: the same forms in web text and mailing-list archives (EMAIL_PROSE_OBF,
    aneks 2026-11-27 zaciemnione_proza)."""
    masked, n = _mask_emails(text, bare_at, wrapped, code_obf, prose_obf)
    MASKED["pii"] += n
    return masked


def no_masking(emails: bool = False) -> None:
    """Presidio off (see module docstring). emails=True (stack_edu_python): rows arrive pre-masked by premask_emails, and the
    count of masked e-mails goes into stats.json."""
    pii.mask = lambda texts, language, *, names=False: (list(texts), dict(MASKED) if emails else {})
    pii.record = lambda languages, *, names: {"pass": "regex e-mail only, before the language gate" if emails else "none",
                                              "reason": REASON}
