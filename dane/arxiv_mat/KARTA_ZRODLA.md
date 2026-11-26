# Karta źródła: arXiv — matematyka, statystyka i logika (pełne teksty z otwartą licencją + abstrakty)

Zapisana 26.11.2026 przed pobraniem do budowy zbioru (pomiary na pełnych plikach źródła w `/tmp`, usunięte po
pomiarze). Rezerwacja: https://github.com/slayerlabs/benchmarks-fabryka-ai/issues/346. Przegląd kandydatów:
`dane/matematyka-wspolne/kandydaci_czyste.md` (A1–A3).

Cel: największa czysta prawnie porcja matematyki „wyższej” (prace badawcze w LaTeX) do zbioru matematyki v6 (~20 mld),
z myślą o Slayerze 1B i większych modelach. Wymóg właścicielki: licencje pozwalające sprzedawać model komercyjnie.
Oznaczenia: V = sprawdzone 26.11.2026 (URL, rewizja, sha256), I = wywnioskowane.

Części: **A1** pełne teksty na licencji otwartej (do zbioru), **A2** abstrakty prac spoza A1 (do zbioru),
**A3** pełne teksty na domyślnej licencji arXiv (ocena prawna, §2.3; nie do zbioru bez zgody).

## 1. Identyfikacja

- V: A1: `common-pile/arxiv_papers@963fe980c55b353980653f1a27c1dc0c8a2d7058`, 22 pliki `NNNNN_arxiv-papers.jsonl.gz`
  (sumy sha256 w §4). Karta: LaTeX z S3 arXiv → LaTeXML → HTML → Trafilatura; tylko CC BY, CC BY-SA, CC0.
- V: A2: `common-pile/arxiv_abstracts@828e35d1000f94579da8850f5f640c138279bdb5`, 4 pliki (sumy w §4); źródło OAI-PMH.
- V: kategorie i licencje arXiv: `librarian-bots/arxiv-metadata-snapshot@c428226b689a0e17db2cd55265133b9eca15d97f`
  (licencja CC0, 11 plików parquet, 3 224 542 prace; kolumny `id`, `categories`, `license`, `title`, `versions`).
  Snapshot z 10.2026 (I: data z `lastModified` repo 2026-10-27).
- V: wydawca A1/A2: Common Pile v0.1 (Kandpal i in. 2025, https://arxiv.org/abs/2506.05209); kod
  https://github.com/r-three/common-pile.

### Algorytm wyboru (do `preregistracja.json`)

1. Łączenie: `doc["id"]` z Common Pile = identyfikator arXiv bez wersji (np. `0704.3395`, `2101.00001`); V: na
   wszystkich 304 048 dokumentach A1 `metadata.url == "https://arxiv.org/abs/" + id` i każdy `id` ma wiersz w
   snapshocie metadanych (§4: liczby). Kategorie bierzemy z `categories` snapshotu, nie z Common Pile (brak tam pola).
2. Kategoria główna = pierwszy element `categories.split()`. Wybór: `^(math\.|math-ph$|stat\.|cs\.LO$|cs\.DM$|cs\.CC$|cs\.FL$|cs\.SC$|cs\.IT$|cs\.GT$|cs\.NA$)`.
   Wariant ścisły (rekomendowany do pierwszej wersji): `^(math\.|math-ph$|cs\.LO$|cs\.DM$)`.
3. A1: wszystkie dokumenty `common-pile/arxiv_papers` spełniające 2 (licencja już otwarta, sprawdzić per dokument:
   `metadata.license` ∈ {CC BY 3.0/4.0, CC BY-SA 4.0, CC0, „Public Domain”}).
4. A2: dokumenty `common-pile/arxiv_abstracts`, których `id` spełnia 2 i **nie** należy do zbioru id A1.
5. Dedup: A1 wobec peS2o (prace arXiv są też w peS2o, `metadata.pdf_src` ∈ {Arxiv, ArXiv}) i wobec TeX z GitHub;
   A2 wobec A1 rozwiązany przez krok 4.

## 2. Prawa

### 2.1 A1 — pełne teksty na licencji otwartej

- V: `metadata.license` prac A1 (wszystkie 22 pliki): CC BY 4.0 63 056, CC0 4 190, CC BY-SA 4.0 3 796, CC BY 3.0
  1 794, „Public Domain” 484 — zero NC/ND. Zgodność z licencją w snapshocie arXiv: §4.
- V: arXiv (https://info.arxiv.org/help/license/index.html): CC BY 4.0 „allows for commercial use”, CC BY-SA 4.0
  też; licencja wybrana dla wersji jest nieodwołalna.
- **Bramka „można TRENOWAĆ” (komercyjnie): TAK** — licencje per dokument pozwalają na użycie komercyjne
  (atrybucja; SA dla utworów zależnych). Takedown: usunięcie po `id`.
- **Bramka „można ZGŁOSIĆ”: TAK** — licencja per dokument, bez NC/ND; obowiązek atrybucji (`author` = autorzy z
  `metadata.authors`, URL abs). Ryzyko: „license laundering” (karta Common Pile) i niezgodności z §4.

### 2.2 A2 — abstrakty

- V: Terms of Use for arXiv APIs (https://info.arxiv.org/help/api/tou.html): „You are free to use descriptive
  metadata about arXiv e-prints under the terms of the Creative Commons Universal (CC0 1.0) Public Domain
  Declaration”, przypis: „Descriptive metadata includes … title, abstract, authors…”.
- V: `metadata.license` w A2 = „Creative Commons Zero - Public Domain”, osobne pole `full_text_license`.
- **TRENOWAĆ (komercyjnie): TAK. ZGŁOSIĆ: TAK** (CC0).

### 2.3 A3 — pełne teksty na domyślnej licencji arXiv (`nonexclusive-distrib`)

Pytanie: czy trening modelu sprzedawanego komercyjnie na pracach z licencją domyślną da się oprzeć na art. 4
dyrektywy 2019/790 (eksploracja tekstów i danych, TDM, również komercyjna; w Polsce I: art. 26³ pr. aut. — numer
przepisu nie sprawdzony u źródła). Warunki
art. 4: (1) zgodny z prawem dostęp do utworu, (2) brak zastrzeżenia praw przez uprawnionego „w odpowiedni sposób,
np. za pomocą środków nadających się do odczytu maszynowego” (art. 4 ust. 3); (3) art. 7 ust. 1 chroni przed
umownym wyłączeniem tylko wyjątki z art. 3, 5, 6 — **umowa może ograniczyć TDM z art. 4**.

Ustalenia:

- V: licencja domyślna (https://arxiv.org/licenses/nonexclusive-distrib/1.0/license.html): „I grant arXiv.org a
  perpetual, non-exclusive license to distribute this article.” — prawa ma tylko arXiv, nie osoby trzecie.
- V: strona bulk data (https://info.arxiv.org/help/bulk_data.html) i S3 (…/bulk_data_s3.html): licencja domyślna
  „does not assign copyright to arXiv, nor grant arXiv the right to grant any specific rights to others. We are thus
  unable to grant others the right to distribute arXiv articles.”; „Please do not attempt to download the complete
  corpus programmatically. The Amazon S3 buckets are the accepted mechanism”.
- V: Terms of Use for arXiv APIs (obejmują wprost „bulk data downloads”, czyli S3): „By using arXiv APIs, you are
  agreeing to the terms and conditions outlined on this page.” Dozwolone: „Retrieve, store, and use the content of
  arXiv e-prints for your own personal use, or for research purposes.” Zakazane: „Store and serve arXiv e-prints
  (PDFs, source files, or other content) from your servers, unless you have the permission of the copyright holder
  or are permitted to do so by the license”. Użycia komercyjnego (np. trenowania produktu) regulamin nie wymienia
  wśród dozwolonych.
- V: S3 requester-pays: dostęp płatny po stronie pobierającego (opłata transferu AWS); arXiv kieruje do Terms of Use
  for arXiv APIs; osobnego regulaminu S3 arXiv nie ma (I: obowiązuje też AWS Customer Agreement, bez wpływu na prawa
  do treści).
- V: robots.txt arxiv.org (sha256 `eda2bc852443f3f29d31eb04d37b26476654dc33b29256fb882819da23d189a5`, 341 linii):
  10 sekcji `User-agent` (`*`, Googlebot, bingbot, Baiduspider, ToutiaoSpider, YandexBot, Applebot, Yahoo! Slurp,
  SemrushBot, SQUID…); **0 wpisów** dla GPTBot, CCBot, ClaudeBot, Google-Extended, `Content-signal`/`ai-train`;
  `User-agent: *` ma `Allow: /abs /pdf /html`, `Disallow: /e-print /src …`, `Crawl-delay: 15`, komentarz
  „Indiscriminate automated downloads from this site are not permitted”.
- V: `https://arxiv.org/.well-known/tdmrep.json` → HTTP 404; nagłówki odpowiedzi `/abs/2101.00001` (arxiv.org i
  export.arxiv.org) bez `tdm-reservation`/`X-Robots-Tag`.
- V: Proof-Pile-2 `arxiv/` (`EleutherAI/proof-pile-2@901a9273a770e9d4138c5ddd91802f9c5c6cdc4b`) = podzbiór arXiv z
  RedPajama-Data-1T (karta PP2). Karta `togethercomputer/RedPajama-Data-1T@398f92572e94f4793e41c22ab7ea2a788d9e7de4`:
  „ArXiv data is downloaded from Amazon S3 in the `arxiv` requester pays bucket. We only keep latex source files and
  remove preambles, comments, macros and bibliographies.”; licencja: „Please refer to the licenses of the data
  subsets you use … ArXiv Terms of Use” — **bez filtra licencji** (V: w shardzie `arXiv_000` 10 724/13 066 prac ma
  licencję domyślną, 455 NC/ND, 1 887 otwartą).

Ocena:

- (1) Zgodny z prawem dostęp: S3/API — tak, ale na warunkach Terms of Use („personal use, or for research
  purposes”); kopia RedPajama/PP2 na HF — I: wątpliwy, bo jej udostępnienie narusza zakaz „store and serve” z ToU
  i brak zgody autorów (redystrybucja pełnych tekstów bez licencji). Pobranie publicznej strony `/pdf` — dostęp
  zgodny z prawem, ale robots.txt i strona bulk data zakazują masowego pobierania (I: naruszenie warunków
  technicznych/umownych, nie praw autorskich).
- (2) Zastrzeżenie maszynowe: V brak (robots.txt bez agentów AI, brak TDMRep). I: Terms of Use to zastrzeżenie w
  języku naturalnym arXiv (nie autorów); I (z pamięci, orzeczenie nie przeczytane): LG Hamburg (310 O 227/23,
  27.09.2024, LAION) w obiter dictum dopuścił zastrzeżenie w regulaminie pisanym językiem naturalnym jako „maszynowo
  czytelne” — linia orzecznicza niepewna.
  Autorzy prac nie składają zastrzeżeń (I: brak mechanizmu w arXiv).
- (3) Umowa: kto pobiera z S3/API, akceptuje ToU; art. 7 ust. 1 nie chroni art. 4 → trening produktu komercyjnego
  na tych danych to I: naruszenie umowy z arXiv (ograniczenie do użytku osobistego/badawczego), niezależnie od
  wyjątku TDM wobec autorów.

**Werdykt A3: TRENOWAĆ (komercyjnie): NIE** bez zgody (arXiv na dostęp poza ToU albo autorów na użycie). Podstawa:
jedyna zgodna z wytycznymi arXiv droga pobrania (S3/API) wiąże się z ToU ograniczającym użycie do celów osobistych
i badawczych, a umowa może wyłączyć art. 4; kopie stron trzecich (RedPajama, Proof-Pile-2) są redystrybucją bez
licencji. Wariant „WARUNKOWO” istnieje tylko dla modelu badawczego (art. 3 dyrektywy nie dotyczy nas, bo nie jesteśmy
organizacją badawczą/instytucją dziedzictwa — I) albo po pisemnej zgodzie arXiv. **ZGŁOSIĆ: NIE.**

- V: skala A3 (snapshot): prace na licencji domyślnej lub bez licencji (sprzed 2004), bez NC/ND: kategorie ścisłe
  535 810 (do 2304, zakres RedPajama: 447 792), wszystkie docelowe 629 937 (do 2304: 523 518).
- V (shard PP2 `arxiv/train/arXiv_000.jsonl.zst`, sha256
  `44afbfe594b8a289fd54e9937461b26629c6c5632dcfb64f78ba65bfbc1edecc`, 13 066 prac; pola `meta`: `arxiv_id`,
  `language`, `timestamp`, `url`, `yymm`): 3 050 prac w kategoriach ścisłych, z nich 2 578 na licencji domyślnej;
  średnio 31 165 tok. v6 na pracę (2,44 B/tok; tekst to oczyszczony LaTeX).
- I: tokeny v6 A3 ścisłe w PP2 ≈ 2 578 × 100 shardów × 31,2 tys. ≈ **~8 mld** (jeden shard ze 100; shardy mogą
  różnić się składem); górna granica z metadanych 447 792 × 31,2 tys. ≈ 14 mld.

## 3. Zawartość

- V: angielski (w zdecydowanej większości), tekst ludzki: prace badawcze; tekst z LaTeXML+Trafilatura w Markdownie
  (`#` tytuły, `######` „Abstract”), wzory `$…$` / `$$…$$` w LaTeX. Pola dokumentu (V, wszystkie 304 048): `id`,
  `text`, `source` (`arxiv-papers`), `created` (data v1), `added`, `metadata.license`, `metadata.authors` (napis),
  `metadata.submitter`, `metadata.url`. Format `id`: nowy `YYMM.NNNNN` 303 936, stary (`math/0601001`) 112.
- V: kategorie główne A1: math.\* 54 209, stat.\* 8 332 (w tym stat.ML 2 629), cs.IT 3 385, cs.LO 2 138, math-ph
  2 104, cs.GT 1 178, cs.CC 704, cs.FL 622, cs.DM 502, cs.SC 146 (cs.NA 0 — od 2019 alias math.NA).
- V: lata `created` A1: 2021–2024 = 61 677 z 73 320 (A1 to głównie prace z ostatnich lat).
- V: przeczytane ręcznie 6 prac z losowej próby 97 (seed 11): artykuły z math.CA, NT, GR, CO, stat.ME — tekst
  czytelny, nagłówek z afiliacjami i e-mailami; 1/6 (`1304.2314`) to pusty dokument (`"\n\n"`, błąd konwersji).
- Artefakty (V, na 73 320 pracach A1; wyrażenia w `skrypty/arxiv_pass.py`):
  - adres e-mail w tekście: **53 792 (73,4%)** — nagłówki autorów; maskowanie obowiązkowe;
  - sklejone znaczniki przypisów (`…action111As we will…`, regex `[a-z]1{3,}[A-Z ]`): 11 602 (15,8%);
  - puste grupy LaTeXML `~{}` (`$12~{}\mu_{g}$`): 13 913 (19,0%) — nieszkodliwe, do normalizacji;
  - nierozwiązane odnośniki `[?]`/`??`: 444 (0,6%);
  - mojibake (`\ufffd`, `Ã…`, `â€…`): 162 (0,22%);
  - znaczniki HTML: 10; dokumenty < 5 kB (w tym puste): 843 (1,15%).
  - Miara „pusty wzór” (`\$\s*\$`) okazała się błędna (łapie otwarcie `$$`) — nie raportowana.

## 4. Skala i dostęp

| część | dokumenty (V) | bajty UTF-8 (V) | tokeny v6 |
|---|---|---|---|
| A1 wszystkie kategorie docelowe | 73 320 z 304 048 | 6 110 534 698 | **~2,40 mld** (I: 2,54 B/tok, V z 1 498 losowych prac ze wszystkich plików) |
| A1 ścisłe (math.\*, math-ph, cs.LO, cs.DM) | 58 953 | 4 970 935 928 | ~1,96 mld (I) |
| A2 abstrakty prac spoza A1 | 579 097 (z 652 417 docelowych; 73 320 = A1) | 431 442 492 | **~0,111 mld** (I: 3,88 B/tok z 5% próby; śr. 192 tok.) |
| A3 (nie do zbioru) | §2.3 | | ~8 mld ścisłe w PP2 (I) |

- V: łączenie A1 z metadanymi: 304 048/304 048 dokumentów (`url == https://arxiv.org/abs/<id>` w 100%); A2: każdy
  abstrakt docelowy połączony (pole „bez_meta” = 0 dla docelowych; wybór robi snapshot).
- V: zgodność licencji Common Pile ↔ snapshot arXiv w A1: zgodne 72 632 (99,06%); niezgodne 688, w tym snapshot
  **bardziej restrykcyjny**: `nonexclusive-distrib` przy CC BY/CC0/BY-SA w Common Pile — 385, BY-NC-ND/BY-NC-SA przy
  CC BY — 158 (V, 10 najczęstszych par). Reguła: brać licencję bardziej restrykcyjną → odrzucić te ≥543 prace.
- V: sha256 plików A1 (22) i A2 (4): `wyniki/przeglad_zrodla.json`; np. A1 `00000` `0bac07f4441c5bd38bdb1c5c246a030355e466b1e00c4c707ed98eeca03bc365`,
  A2 `00000` `1a6c475ff4af00e9abaf57919d01c3f27ec04670370f79585db2debb2d3abdb8`.
- V: dostęp bez bramki, `hf_hub_download` po rewizji; pełny przebieg A1+A2 ~56 min.

## 5. Ryzyka

- Prawa: niezgodne licencje (≥543 prace, wyżej); „license laundering” (karta Common Pile); A3 poza zbiorem.
- PII: e-maile w 73,4% prac A1, 23 abstraktach A2 (V); nazwiska i afiliacje autorów to dane publiczne związane z
  publikacją (I), ale maskowanie e-maili obowiązkowe.
- Testy: I: prace z math.HO/stat mogą cytować zadania konkursowe (MATH ma źródła olimpijskie) — 13-gramy testów;
  miniF2F/ProofNet bywają omawiane w cs.LO.
- Konwersja: puste i bardzo krótkie dokumenty (843 < 5 kB), artefakty przypisów; wzory, których LaTeXML nie
  przetworzył, znikają (I: urwane zdania w ~1/6 przeczytanych prac).
- Syntetyczne: I: prace z 2023–2024 mogą zawierać tekst pisany z LLM; nie mierzone.
- Wpływ przy 1B: DeepSeekMath (2402.03300 §5.1.2, Tab. 8): „arXiv papers seem ineffective in improving mathematical
  reasoning” (1.3B, 150 mld tok.: MMLU-STEM 19,5→9,0); MathPile (2312.17120 Tab. 4, Mistral-7B, +arXiv 0,38 mld):
  MATH 10,08→7,50. Autorzy DeepSeekMath nie badali większej skali ani mieszania.

## 6. Nowość

- V: nakładanie z peS2o (`common-pile/peS2o@2caeba1585aaafa3c965410d80af85b09ed11cd9`, 2 z 102 plików: `peS2o-0001`
  `8bf759b5d6ec8cad115921af0fe1ac85d2141893a3501599ecc171adc28fa2ed`, `peS2o-0051`
  `7044ba18f93a0aa2de080b766cf65f6d1506073d1f318dfef71d897774877cb2`; 136 605 dok.): 118 prac A1 (dopasowanie po
  znormalizowanym tytule; po id z `oa_url` tylko 3, bo `oa_url` rzadko wskazuje arXiv — 26 dok.); `pdf_src` = Arxiv
  w 3 691 dok. I: w całym peS2o ~5–6 tys. prac A1 (~8%) — dedup A1↔peS2o po tytule + MinHash.
- I: FineMath-4+/InfiWebMath-4+ to web: strony `arxiv.org` w próbce eksportu FineMath-4+ 1/266 351 — nakładanie
  pomijalne (strony abstraktów, nie pełne teksty). Slayer 1.07/1.09 bez arXiv (wg kart składów).
- V: Llemma (2310.10631 Tab. 5) trenuje Proof-Pile-2 z arXiv:web:code = 2:4:1 (proporcja dobrana perpleksją na
  zbiorze treningowym MATH, różnice między mieszankami ~0,01); osobnej ablacji samego arXiv w tej pracy nie ma.

## Nie sprawdzone

- Licencje u źródła dla próbki prac (strona `arxiv.org/abs/<id>`), poza porównaniem ze snapshotem.
- Odsetek tekstu nieangielskiego (Common Pile arXiv nie ma pola języka).
- Nakładanie 13-gramów z testami Fabryki; tekst syntetyczny w pracach 2023–2024.
- Nakładanie z peS2o na wszystkich 102 plikach (2 sprawdzone, dopasowanie tylko po tytule).
- A3: orzeczenie LG Hamburg i polski przepis (art. 26³) nie przeczytane u źródła; stanowisko arXiv wobec
  komercyjnego trenowania (brak pisemnej odpowiedzi); stanowisko autorów; skład pozostałych 99 shardów PP2 `arxiv/`.
- Regulamin AWS dla requester-pays (tylko strona arXiv).
