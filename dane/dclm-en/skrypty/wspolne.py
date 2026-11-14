"""Wspólne dla DCLM-EN: rdzeń RPG v2 (normalizacja, hasze, MinHash) plus normalizacja url, domeny testów, PII."""
import hashlib
import os
import re
import sys
from urllib.parse import urlsplit

TU = os.path.dirname(os.path.abspath(__file__))
RPG = os.path.join(TU, "..", "..", "korpus-rpg-v2", "skrypty")
sys.path.insert(0, RPG)
import rdzen as r  # noqa: E402,F401
import rdzen2 as r2  # noqa: E402,F401

SEED = 20261114
DOMENY_TESTOW = ("wikihow.com", "instructables.com", "wikipedia.org", "wikinews.org", "wikivoyage.org", "wikibooks.org")


def host(url):
    try:
        h = (urlsplit(url if "//" in url else "//" + url).hostname or "").lower()
    except ValueError:
        return ""
    return h[4:] if h.startswith("www.") else h


def domena_testu(url):
    h = host(url)
    for d in DOMENY_TESTOW:
        if h == d or h.endswith("." + d):
            return d
    return None


def norm_url(url):
    u = url.strip()
    u = re.sub(r"^[a-zA-Z]+://", "", u)
    u = u.split("#", 1)[0]
    if "/" in u:
        h, p = u.split("/", 1)
        p = "/" + p
    else:
        h, p = u, ""
    h = h.lower()
    if h.startswith("www."):
        h = h[4:]
    h = h.split(":", 1)[0] if re.search(r":(80|443)$", h) else h
    u = h + p
    while u.endswith("/"):
        u = u[:-1]
    return u


def h64(s):
    return int.from_bytes(hashlib.blake2b(s.encode("utf-8", "surrogatepass"), digest_size=8).digest(), "little")


# ---- PII (preregistracja.json -> pii)
RX_EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Za-z]{2,})")
EMAIL_PRZYKLADOWE = {"example.com", "example.org", "example.net", "domain.com", "email.com", "yourdomain.com", "test.com"}
RX_TEL = re.compile(
    r"(?<![\w.+-])(?:\(\d{3}\)\s?\d{3}[-.\s]\d{4}|\d{3}-\d{3}-\d{4}|\d{3}\.\d{3}\.\d{4})(?![\w-])"
    r"|(?<![\w+])\+\d{1,3}(?:[\s.-]\(?\d{1,4}\)?){2,5}(?![\w-])"
)
RX_IP = re.compile(r"(?<![\d.])(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})(?![\d.])")


def pii(t):
    """Zwraca listę klas PII w tekście (email, telefon, ip)."""
    k = []
    for m in RX_EMAIL.finditer(t):
        if m.group(1).lower() not in EMAIL_PRZYKLADOWE:
            k.append("email")
            break
    for m in RX_TEL.finditer(t):
        if m.group(0).startswith("+") and sum(c.isdigit() for c in m.group(0)) < 9:
            continue
        k.append("telefon")
        break
    for m in RX_IP.finditer(t):
        o = [int(x) for x in m.groups()]
        if max(o) > 255 or o[0] in (0, 10, 127) or o == [255, 255, 255, 255] or (o[0] == 192 and o[1] == 168):
            continue
        k.append("ip")
        break
    return k
