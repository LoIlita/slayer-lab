"""Ręczna próbka (#346): podział na wycinki dla recenzentów i zliczenie ocen wobec progów preregistracji.
  dziel probka_przegladu.jsonl katalog rozmiar   -> katalog/wycinek_NN.jsonl
  licz zbior probka_przegladu.jsonl oceny_A.json oceny_B.json wyjscie.json
Werdykt per próg liczony osobno dla każdego recenzenta; obowiązuje gorszy (przegląd przechodzi, gdy przechodzi u obu).
Progi (aneks DCLM-EN z 15.11.2026, przejęte w preregistracjach): fałszywe odrzucenia per powód <= 10% i górna granica
Wilsona 95% <= 20%; śmieci w zachowanych <= 10% i górna <= 20%; przeoczenia PII / sekretów / testów 0 na wszystkich
zachowanych; cranemath: błędne przepisania (blad_matematyczny + sprzeczne) <= 10% i górna <= 20%."""
import json
import math
import os
import sys


def wilson(k, n, z=1.96):
    if n == 0:
        return [0.0, 0.0]
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(100 * max(0.0, c - h), 1), round(100 * min(1.0, c + h), 1)]


def wczytaj_jsonl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8")]


if sys.argv[1] == "dziel":
    poz, kat, roz = wczytaj_jsonl(sys.argv[2]), sys.argv[3], int(sys.argv[4])
    os.makedirs(kat, exist_ok=True)
    for i in range(0, len(poz), roz):
        with open(f"{kat}/wycinek_{i // roz:02d}.jsonl", "w", encoding="utf-8") as f:
            for x in poz[i:i + roz]:
                f.write(json.dumps(x, ensure_ascii=False) + "\n")
    print("pozycji", len(poz), "wycinkow", (len(poz) + roz - 1) // roz)
    sys.exit(0)

ZB, PROBKA, A, B, OUT = sys.argv[2:7]
poz = {x["nr"]: x for x in wczytaj_jsonl(PROBKA)}


def oceny(p):
    o = json.load(open(p, encoding="utf-8"))
    return {(x["nr"], x.get("powod")): x for x in o}


def prog(k, n, maks=10.0, gorna=20.0):
    w = wilson(k, n)
    st = round(100 * k / n, 1) if n else 0.0
    return {"k": k, "n": n, "stopa": st, "wilson95": w, "werdykt": "PASS" if n and st <= maks and w[1] <= gorna else ("NOT RUN" if not n else "FAIL")}


wyn = {"zbior": ZB, "recenzenci": {}}
for nazwa, plik in (("A", A), ("B", B)):
    oc = oceny(plik)
    brak = [k for k in ((x["nr"], x["powod"]) for x in poz.values()) if k not in oc]
    r = {"brakujace_oceny": len(brak), "powody": {}, "zachowane": {}}
    powody = sorted({x["powod"] for x in poz.values() if x["grupa"] == "odrzucony"})
    for p in powody:
        o = [oc[(x["nr"], p)] for x in poz.values() if x["grupa"] == "odrzucony" and x["powod"] == p and (x["nr"], p) in oc]
        r["powody"][p] = {**prog(sum(1 for x in o if x.get("trafny") == "nie"), len(o)),
                          "watpliwe": sum(1 for x in o if x.get("trafny") == "watpliwy")}
    z = [oc[(x["nr"], None)] for x in poz.values() if x["grupa"] == "zachowany" and (x["nr"], None) in oc]
    r["zachowane"]["smieci"] = {**prog(sum(1 for x in z if x.get("jakosc") == "nie"), len(z)),
                                "watpliwe": sum(1 for x in z if x.get("jakosc") == "watpliwy")}
    for pole in ("pii_przeoczone", "sekret_przeoczony", "test_przeoczony"):
        if any(pole in x for x in z):
            k = sum(1 for x in z if x.get(pole) == "tak")
            r["zachowane"][pole] = {"k": k, "n": len(z), "werdykt": "PASS" if k == 0 else "FAIL"}
    if ZB == "cranemath":
        zp = [x for x in z if "przepisanie" in x]
        r["zachowane"]["przepisanie_bledne"] = {**prog(sum(1 for x in zp if x["przepisanie"] in ("blad_matematyczny", "sprzeczne")), len(zp)),
                                                "watpliwe": sum(1 for x in zp if x["przepisanie"] == "watpliwe")}
    wyn["recenzenci"][nazwa] = r


def werdykty(r):
    return [v["werdykt"] for v in r["powody"].values()] + [v["werdykt"] for v in r["zachowane"].values()]


wsz = werdykty(wyn["recenzenci"]["A"]) + werdykty(wyn["recenzenci"]["B"])
wyn["werdykt"] = "PRZESZŁO" if all(w == "PASS" for w in wsz) else "NIE PRZESZŁO"
wyn["fail"] = sorted({f"{n}:{p}" for n, r in wyn["recenzenci"].items() for p, v in {**r["powody"], **r["zachowane"]}.items() if v["werdykt"] != "PASS"})
json.dump(wyn, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(wyn["werdykt"], wyn["fail"])
