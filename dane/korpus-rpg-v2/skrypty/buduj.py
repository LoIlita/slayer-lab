"""Buduje config default i cc-by-sa: mapowanie schematu, podział po work_family, zapis shardów ~500 MB.
Argumenty: wejscie.parquet usuniecia.json katalog_wyjscia procesy(nieużywane; zapis sekwencyjny).
Tekst nie jest zmieniany: wiersz wyjściowy to wiersz wejściowy minus usunięcia i po przemapowaniu kolumn."""
import hashlib
import json
import os
import re
import sys

import pyarrow as pa
import pyarrow.parquet as pq

import numpy as np  # noqa: E402

WEJ, USUN, OUT, V6 = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
SHARD = 500 * 1024 * 1024
GRUPA = 2000

SCHEMAT = pa.schema([
    ("document_id", pa.string()),
    ("source_id", pa.string()),
    ("text", pa.string()),
    ("register", pa.string()),
    ("license", pa.string()),
    ("license_url", pa.string()),
    ("is_share_alike", pa.bool_()),
    ("author", pa.string()),
    ("provenance", pa.string()),
    ("work_family", pa.string()),
    ("first_pub_year", pa.int32()),
    ("content_tag", pa.string()),
    ("n_tokens", pa.int64()),
])

REJ = {"fikcja": "fiction", "dramat": "drama", "poezja": "poetry", "swiaty": "history-travel-folklore"}
TAG = {"przemoc_drastyczna": "graphic_violence", "rasistowski_jezyk": "racist_language", "samobojstwo": "suicide", "seksualne": "sexual"}
LIC = {"CC BY-SA 3.0": ("CC-BY-SA-3.0", "https://creativecommons.org/licenses/by-sa/3.0/"), "CC-BY-3.0": ("CC-BY-3.0", None), "CC-BY-4.0": ("CC-BY-4.0", None), "CC-BY-SA-4.0": ("CC-BY-SA-4.0", None)}
AUT_RPG = {"blades-srd": "John Harper (One Seven Design)", "dnd-srd-5.2.1": "Wizards of the Coast LLC", "fate": "Evil Hat Productions, LLC and credited contributors", "cairn": "Yochai Gal"}
ZM_G = {"usunięte nagłówki/stopki PG i noty transkrypcji; złamania wierszy prozy złączone; podkreślenia kursywy zdjęte": "edition headers and footers and transcription notes removed; hard-wrapped prose lines rejoined; underscore italic markers removed"}
ZM_S = {"znaczniki Wikidot usunięte; boilerplate szablonu usunięty; tekst bez zmian redakcyjnych": "Wikidot markup and template boilerplate removed; no editorial changes to the text"}
UW_S = {"licencja obrazów nieobjęta; tylko tekst strony": "image licenses not covered; page text only"}
POCH = {"Doslownie z naglowka pliku SRD.": "verbatim from the SRD file header", "Doslownie z 1. strony dokumentu.": "verbatim from page 1 of the document", "Doslownie ze strony Licensing wydawcy.": "verbatim from the publisher's Licensing page", "Zlozona z noty pliku i README repozytorium; wydawca nie podaje gotowej formuly.": "composed from the file notice and repository README; the publisher gives no ready-made statement"}


def z_slownika(s, d, nazwa):
    if s in d:
        return d[s]
    raise SystemExit(f"nieznana wartość {nazwa}: {s!r}")


def zamien(w):
    a = json.loads(w["atrybucja"])
    z = w["zrodlo"]
    lic = w["licencja"]
    if z == "gutenberg":
        m = re.fullmatch(r"domena publiczna \(autor zm\. (\d{1,4})( p\.n\.e\.)?(?:, tłumacz zm\. (\d{4}))?\)", lic)
        if not m:
            raise SystemExit("zła licencja gutenberg: " + repr(lic))
        rok = -int(m.group(1)) if m.group(2) else int(m.group(1))
        prov = {"source": "gutenberg", "title": a["tytul"], "url": a["url"], "ebook": a["numer_ksiazki"], "authors": a["autor"], "translators": a["tlumacz"],
                "other_contributors": a["inne_osoby"], "pg_release_date": a["wydano"], "rights_statement": a["prawa_rdf"], "author_death_year": rok, "translator_death_year": int(m.group(3)) if m.group(3) else None,
                "groups": a["grupy"], "changes": z_slownika(a["zmiany"], ZM_G, "zmiany g"), "source_revision": w["rewizja_zrodla"]}
        licencja, url, sa = "public-domain", None, False
        rejestr = z_slownika(a["kategoria"], REJ, "kategoria")
        autor = "; ".join(a["autor"]) if a["autor"] else None
    elif z == "scp":
        prov = {"source": "scp-wiki", "title": a["tytul"], "url": a["url"], "author": a["autor"], "license_box_author": a["autor_licencji_box"], "page_creator": a["tworca_strony"],
                "page_history_authors": a["autorzy_historii"], "rating": a["rating"], "license_tags": a["tagi_licencji"], "changes": z_slownika(a["zmiany"], ZM_S, "zmiany s"),
                "note": z_slownika(a["uwaga"], UW_S, "uwaga"), "source_revision": w["rewizja_zrodla"]}
        licencja, url = LIC[lic]
        sa = True
        rejestr = "shared-world-fiction"
        autor = a["autor"]
    elif z in ("rpg_cc_by", "rpg_sa"):
        prov = {"source": z, "attribution_statement": a["formula"], "attribution_origin": z_slownika(a["pochodzenie_formuly"], POCH, "poch"), "license_url": a["licencja_url"], "source_url": a["zrodlo_url"], "source_revision": w["rewizja_zrodla"]}
        if a.get("zakaz"):
            prov["publisher_restriction"] = a["zakaz"]
        licencja, url = LIC[lic][0], a["licencja_url"]
        sa = z == "rpg_sa"
        rejestr = "rpg-rules"
        autor = AUT_RPG[w["id_zrodla"].split("/")[0]]
    else:
        raise SystemExit("nieznane źródło: " + z)
    tagi = [t for t in (w["tag_tresci"] or "").split(",") if t]
    return {"document_id": f"{z}:{w['id_zrodla']}", "source_id": z, "text": w["text"], "register": rejestr, "license": licencja, "license_url": url, "is_share_alike": sa,
            "author": autor, "provenance": json.dumps(prov, ensure_ascii=False, sort_keys=True), "work_family": w["rodzina_dziela"], "first_pub_year": w["rok_wydania"],
            "content_tag": ",".join(z_slownika(t, TAG, "tag") for t in tagi), "n_tokens": w["tokeny"]}


class Zapis:
    def __init__(self, config, split):
        self.k = f"{OUT}/data/{config}"
        os.makedirs(self.k, exist_ok=True)
        self.config, self.split = config, split
        self.nr, self.bufor, self.wr, self.pl, self.pliki, self.wierszy, self.tok = 0, [], None, None, [], 0, 0

    def _otworz(self):
        self.pl = f"{self.k}/.tmp-{self.split}-{self.nr:05d}.parquet"
        self.wr = pq.ParquetWriter(self.pl, SCHEMAT, compression="zstd")

    def dodaj(self, w):
        self.bufor.append(w)
        self.wierszy += 1
        self.tok += w["n_tokens"]
        if len(self.bufor) >= GRUPA:
            self.oproznij()

    def oproznij(self):
        if not self.bufor:
            return
        if self.wr is None:
            self._otworz()
        self.wr.write_table(pa.Table.from_pylist(self.bufor, schema=SCHEMAT), row_group_size=GRUPA)
        self.bufor = []
        if os.path.getsize(self.pl) >= SHARD:
            self.wr.close()
            self.pliki.append(self.pl)
            self.wr = None
            self.nr += 1

    def koniec(self):
        self.oproznij()
        if self.wr is not None:
            self.wr.close()
            self.pliki.append(self.pl)
            self.wr = None
        n = len(self.pliki)
        out = []
        for i, p in enumerate(self.pliki):
            cel = f"{self.k}/{self.split}-{i:05d}-of-{n:05d}.parquet"
            os.replace(p, cel)
            out.append(os.path.relpath(cel, OUT))
        return {"pliki": out, "wierszy": self.wierszy, "tokeny": self.tok}


def czy_val(rodzina):
    return int(hashlib.sha1(rodzina.encode("utf-8")).hexdigest(), 16) % 200 == 0


def main():
    us = json.load(open(USUN, encoding="utf-8"))
    do_usun = {tuple(k[:2]) for k in us["wiersze"]}
    pf = pq.ParquetFile(WEJ)
    z = {("default", "train"): Zapis("default", "train"), ("default", "validation"): Zapis("default", "validation"), ("cc-by-sa", "train"): Zapis("cc-by-sa", "train"), ("cc-by-sa", "validation"): Zapis("cc-by-sa", "validation")}
    wej, usunieto = 0, 0
    for g in range(pf.num_row_groups):
        t = pf.read_row_group(g).to_pylist()
        n_v6 = np.load(f"{V6}/n_{g:04d}.npy")
        if len(n_v6) != len(t):
            raise SystemExit(f"grupa {g}: {len(n_v6)} liczników v6 na {len(t)} wierszy")
        for i, w in enumerate(t):
            wej += 1
            if (g, i) in do_usun:
                usunieto += 1
                continue
            r = zamien(w)
            r["n_tokens"] = int(n_v6[i])
            cfg = "default" if w["zrodlo"] in ("gutenberg", "rpg_cc_by") else "cc-by-sa"
            if cfg == "default" and r["is_share_alike"]:
                raise SystemExit("wiersz SA w default: " + r["document_id"])
            z[(cfg, "validation" if czy_val(r["work_family"]) else "train")].dodaj(r)
        print("grupa", g, "wej", wej, "usun", usunieto, flush=True)
    wyn = {f"{a}/{b}": v.koniec() for (a, b), v in z.items()}
    wyn["wejscie_wierszy"] = wej
    wyn["usunieto_wierszy"] = usunieto
    json.dump(wyn, open(f"{OUT}/liczby_budowy.json", "w", encoding="utf-8"), indent=1)
    print(json.dumps(wyn, indent=1), flush=True)
    print("KONIEC", flush=True)


if __name__ == "__main__":
    main()
