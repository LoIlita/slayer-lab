import re

KW = re.compile(r"\b(math|maths|mathemat\w*|calculus|algebra\w*|geometr\w*|trigonometr\w*|precalculus|pre-calculus|statistic\w*|probabilit\w*|arithmetic|number theory|topology|combinatori\w*|differential equations?|linear algebra|discrete|logic|proofs?|real analysis|complex analysis|derivatives?|integrals?|functions?|equations?|fractions?|vectors?|matri(x|ces))\b", re.I)
NEG = re.compile(r"\b(standards?|syllabus|esl|economics|macroeconomics|microeconomics|antiracism|lesson plan|editor|resource to)\b", re.I)


# OER, reguła 1: słowo matematyczne w tytule, bez słów wykluczających, co najmniej 800 tokenów
def oer1(d):
    t = d.get("title") or ""
    return bool(KW.search(t)) and not NEG.search(t) and d["tok"] >= 800
