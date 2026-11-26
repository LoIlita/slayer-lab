import re

# reguła 0: gęstość wzorów
def rule0(d):
    return d["s"] >= 10 and d["c"] >= 5


# reguła 1: reguła 0 + dziedzina z leadu (pierwsze 700 znaków): więcej sygnałów matematyki/logiki niż innych nauk
MATH = re.compile(r"\b(mathemat\w*|theorem\w*|lemma|conjecture|axiom\w*|algebra\w*|geometr\w*|topolog\w*|number theory|set theory|"
                  r"probability|statistic(s|al)\b|stochastic|combinatori\w*|graph theory|calculus|logic(al)?\b|logician|arithmetic|"
                  r"polynomial\w*|integers?\b|prime numbers?|matri(x|ces)|vector spaces?|manifolds?|homotop\w*|homolog\w*|"
                  r"measure theory|numerical analysis|interpolation|differential equations?|real analysis|complex analysis|"
                  r"functional analysis|group theory|ring theory|field theory|category theory|lie (group|algebra)\w*|"
                  r"riemann\w*|hilbert space|banach|eigen\w*|derivative|integral\b|series\b|sequence\w*|"
                  r"vertices|vertex|graph\b|geometric|trigonometr\w*|recursion|computab\w*|decidab\w*|proof\w*)", re.I)
OTHER = re.compile(r"\b(physic\w*|chemi\w*|thermodynamic\w*|astronom\w*|astrophysic\w*|engineering|aerospace|orbit(al)?\b|"
                   r"financ\w*|economic\w*|accounting|machine learning|neural network\w*|quantum|electromagnet\w*|"
                   r"mechanics|biolog\w*|medic\w*|climate|atmospher\w*|electrical|electronic\w*|signal processing|"
                   r"fluid|optic\w*|nuclear|particle|relativity|spacecraft|radiation|energy|molecul\w*|atom\w*|"
                   r"genetic\w*|ecolog\w*|psycholog\w*|linguistic\w*|music\w*)", re.I)


def domain(d):
    lead = d["text"][:700]
    return len(MATH.findall(lead)), len(OTHER.findall(lead))


def rule1(d):
    if not rule0(d):
        return False
    m, o = domain(d)
    return m >= 1 and m > 2 * o  # poprawka po ocenie 1. czterdziestki: m > o przepuszczało fizykę stat. i finanse
