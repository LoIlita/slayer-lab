# Karta źródła: Wikipedia EN i Wikibooks — artykuły matematyczne (Common Pile `wikimedia`)

Zapisana 26.11.2026 przed pobraniem do budowy zbioru (pełny przebieg strumieniowy po źródle w `/tmp`, zapisane tylko
wybrane dokumenty; usunięte po pomiarze). Rezerwacja: https://github.com/slayerlabs/benchmarks-fabryka-ai/issues/346.
Przegląd kandydatów: `dane/matematyka-wspolne/kandydaci_czyste.md` (D1, D2). Liczby per plik:
`wyniki/przeglad_zrodla.json`; oceny ręczne: `wyniki/ocena_precyzji.json`.

Cel: encyklopedyczne definicje, twierdzenia i dowody z matematyki i logiki (LaTeX) do zbioru matematyki v6.
Oznaczenia: V = sprawdzone 26.11.2026 (URL, rewizja, sha256), I = wywnioskowane.

## 1. Identyfikacja

- V: `common-pile/wikimedia@781b263a6546515543bec3968ad4743fbc152b72`; pliki `NNNNN_wikipedia.com.jsonl.gz`
  (187 plików, 26,80 GB gz) i `NNNNN_wikibooks.com.jsonl.gz` (2 pliki); sha256 wszystkich 189 w
  `wyniki/przeglad_zrodla.json` (np. `00000_wikipedia.com` `b31586888f49740783a55e6ee508c6e47b5d041ad5f2c155ba2e709d15553cdb`,
  `00000_wikibooks.com` `6d1a2f0080ba5999542df4cc79a261265e7d0fc1b0f7f1d97fba9ec605729372`).
- V: karta: zrzuty wiki EN z 03.2025, tylko najnowsza wersja strony, wikitext → tekst (wtf_wikipedia), „Before parsing,
  we converted wikitext math into LaTeX math using our custom code”; praca https://arxiv.org/abs/2506.05209.
- V: pola: `id` (`0-<page_id>`), `text` (tytuł w 1. linii), `source`, `added`, `created`, `metadata.license`,
  `metadata.authors` (lista [login, id]), `metadata.url` (`https://wikipedia.com/wiki/<Tytuł>`), `metadata.wiki`,
  `metadata.namespace`, `metadata.title`.

### Algorytm wyboru (do `preregistracja.json`)

1. `metadata.namespace == "0"` (artykuły; V: 6 855 964 z 46 691 214 dokumentów Wikipedii).
2. Reguła 0 (gęstość wzorów): ≥10 segmentów `\$\$?([^$\n]{1,300})\$\$?` zawierających któryś ze znaków `\ ^ _ =`
   ORAZ ≥5 komend LaTeX z listy (`\frac \sum \int \mathbb \mathcal \left \sqrt \alpha … \operatorname \begin`).
3. Reguła 1 (dziedzina z leadu, poprawka po ocenie): w pierwszych 700 znakach tekstu liczba trafień słownika
   MATEMATYKA (mathematics, theorem, lemma, axiom, algebra, geometry, topology, number/set theory, probability,
   statistics, stochastic, combinatorics, graph theory, calculus, logic, polynomial, integer, matrix, manifold,
   homotopy, eigen…, derivative, integral, series, sequence, vertex/vertices, graph, proof, computability…) jest
   **> 2 ×** liczba trafień słownika INNE (physics, chemistry, thermodynamic, astronomy, engineering, aerospace, orbit,
   finance, economic, machine learning, neural network, quantum, electromagnetic, mechanics, biology, medicine, climate,
   electrical/electronic, signal processing, fluid, optics, nuclear, particle, relativity, radiation, energy,
   molecule, atom, genetic, ecology, psychology, linguistics, music) i ≥1. Pełne wyrażenia: `skrypty/wiki_rules.py`
   (`rule0`, `rule1`); przebieg pomiarowy: `skrypty/wiki_pass.py` (ścieżki robocze `/tmp/karty`).
4. Dedup dokładny (md5 tekstu): V 0 kopii wśród wybranych.

## 2. Prawa

- V: `metadata.license` = „Creative Commons - Attribution Share-Alike - https://creativecommons.org/licenses/by-sa/4.0/”
  w 100% wybranych (8 521 + 1 469); karta: „Official Wikimedia wikis are released under a CC BY-SA license.”
- V: CC BY-SA 4.0 pozwala na użycie komercyjne; warunki: uznanie autorstwa (autorzy w `metadata.authors`, URL) i
  ShareAlike dla utworów zależnych. I: model nie jest utworem zależnym; wydawany zbiór tekstów jest — eksport z
  licencją CC BY-SA 4.0 i atrybucją.
- I: opt-out TDM nie ma znaczenia, gdy podstawą jest licencja; robots.txt Wikimedia nie sprawdzany.

**Bramka „można TRENOWAĆ” (komercyjnie): TAK** (licencja per dokument). Takedown: usunięcie po `id`/tytule.

**Bramka „można ZGŁOSIĆ”: TAK** (CC BY-SA 4.0 per dokument, bez NC/ND; obowiązek SA i atrybucji w eksporcie).

## 3. Zawartość

- V: angielski, tekst ludzki (I: od 2023 możliwe niewykrywalne fragmenty redagowane z pomocą LLM — polityka
  Wikipedii tego nie zakazuje wprost; nie sprawdzone). Wzory jako `$…$` i `$$…$$` w tekście; infoboksy częściowo
  jako surowy wikitext (V: np. „Complete graph” zaczyna się od `{{Infobox graph | …`), encje HTML (`&minus;`,
  `&thinsp;`) pozostawione (V).
- **Precyzja (ręczna ocena: czy artykuł to matematyka/logika, z prawdopodobieństwem, statystyką i teorią
  obliczeń; fizyka, chemia, inżynieria, finanse, ML = nie; „wątpliwe” liczone jako nie)**:
  - Reguła 0, 40 losowych (seed 101, shardy 0, 1, 4, 8): **23/40 = 57,5%** (Wilson 95%: 42–71%). Błędy: fizyka
    (Luminosity, Fine-structure constant, Wien's law, Elastic collision, Cavendish experiment, Fluctuation theorem,
    State function, Greenhouse effect), inżynieria (Propellant mass fraction, Orbital inclination change, Damköhler
    numbers, CRC), finanse/ekonomia (Net present value, Bond convexity, Minimum wage), ML (Multi-task learning),
    wątpliwe: Buckingham π theorem.
  - Reguła 1 (ten sam próg 2× wynikał z tej czterdziestki: przy `m > o` przechodziły Fluctuation theorem, Bond
    convexity, Buckingham) na **nowych** 40 (seed 202, te same shardy, bez dokumentów z próby 1): **35/40 = 87,5%**
    (Wilson 95%: 74–95%). Błędy: Penrose–Hawking singularity theorems, Characteristic impedance; wątpliwe:
    Elliptic-curve cryptography, Rhumb line, Reed–Solomon error correction.
  - Reguła 1, kontrola na późnych shardach (≥50, seed 303, 20 dok.): **17/20** (błędy: Two-dimensional filter,
    Siacci's theorem, Non-expanding horizon). Łącznie reguła 1: **52/60 = 86,7%** (Wilson 95%: 76–93%).
- Recall (V, kontrola na 20 hasłach podstawowych): reguła 1 łapie 16/20; tracone: Logarithm (lead 1:1 matematyka:inne),
  Euclidean geometry, Mathematical logic, Gödel's incompleteness theorems (poza nadzbiorem: mało wzorów LaTeX). I:
  artykuły z logiki i geometrii syntetycznej (mało wzorów) są systematycznie pomijane; w próbie 1 reguła 1 zgubiła
  1 z 23 trafnych (Orbit (dynamics)).

## 4. Skala i dostęp

Pełny przebieg (V, wszystkie 189 plików, ~70 min, 4 procesy; tokeny v6 policzone na każdym wybranym dokumencie):

| | Wikipedia | Wikibooks |
|---|---|---|
| dokumenty / bajty UTF-8 | 46 691 214 / 76,5 GB | 261 588 / 0,70 GB |
| namespace 0 | 6 855 964 / 20,46 GB | 89 958 / 0,44 GB |
| nadzbiór (≥5 wzorów, ≥3 komendy) | 19 466 dok., 57,7 mln tok. | 3 560 dok., 8,6 mln |
| reguła 0 | 14 687 dok., 49,4 mln tok. | 2 624 dok., 7,37 mln |
| **reguła 1** | **8 521 dok., 26,80 mln tok.** (88,7 MB) | **1 469 dok., 4,06 mln** |

- I: **razem ~30,9 mln tokenów v6** (reguła 1), z czego ~41% Wikipedii jest już w InfiWebMath-4+ (§6) → nowych
  ~18–20 mln. To o rząd wielkości mniej niż szacunek w przeglądzie kandydatów (0,1–0,3 mld) i niż Wikipedia
  matematyczna MathPile (0,18 mld tok. Llamy, dobór po kategoriach, nie po wzorach).
- V: dostęp bez bramki, `hf_hub_download` po rewizji.

## 5. Ryzyka

- Precyzja ~87% (wyżej): ~13% fizyki/inżynierii przechodzi; dopuszczalne dla „matematyki stosowanej”, do decyzji.
- PII: V 0 dokumentów z adresem e-mail wśród wybranych (reguła 1). Loginy autorów tylko w `metadata.authors`.
- Testy: I: hasła Wikipedii są cytowane w MMLU (np. pytania z definicji) — 13-gramy testów obowiązkowe.
- Kopie: V 0 dokładnych; I: te same treści w FineMath-4+ i InfiWebMath-4+ jako strony WWW (§6).
- Format: infoboksy w wikitexcie, encje HTML, brak części wzorów inline (I: wzory zapisane w Unicode zamiast
  `<math>` nie są w LaTeX, np. `π1`); do normalizacji (`html.unescape`, wycięcie `{{Infobox …}}`).
- Syntetyczne: I niskie, nie mierzone.

## 6. Nowość

Nakładanie URL (URL znormalizowany: `en.wikipedia.org`/`wikipedia.com` → `wikipedia`, bez fragmentu i zapytania,
`%XX` zdekodowane, małe litery):

| | InfiWebMath-4+ (V, lokalna kopia `dane/infiwebmath4/robocze/pobrania/lok`, 32 pliki, 6 296 212 wierszy) | FineMath-4+ (V, kolumna `url` 4 z 64 shardów `HuggingFaceTB/finemath@e92b25a6…`, 418 720 wierszy) |
|---|---|---|
| Wikipedia, reguła 1 (8 521) | 3 043 dok., 10,95 mln tok. (41%) | 434 dok., 1,54 mln |
| Wikibooks, reguła 1 (1 469) | 636 dok., 1,24 mln tok. (31%) | 67 dok., 0,14 mln |

- I: FineMath-4+ (w Slayerze 1.07 i w gotowym zbiorze) ma prawdopodobnie znaczną część tych artykułów (434 trafienia
  w 1/16 zbioru; ekstrapolacja liniowa niemożliwa, bo te same strony występują w wielu zrzutach CC). FineWeb-Edu
  (Slayer 1.09) nie sprawdzony.
- Dowód wpływu: MathPile (arXiv 2312.17120, Tab. 4/5, Mistral-7B): „+ Wikipedia (0.18B)” (oczyszczona): GSM8K
  47,38→49,96, MMLU-Math 44,92→47,16, SAT-MATH 47,27→53,63, MATH 10,08→9,96; surowa Wikipedia 2,18 mld: GSM8K →32,30
  („correct LaTeX display in documents is vital”).

## Nie sprawdzone

- Nakładanie z FineMath-4+ na pełnych 64 shardach i z FineWeb-Edu (1.09); 13-gramy testów.
- Recall reguły 1 poza 20 hasłami kontrolnymi; artykuły z logiki i geometrii bez wzorów (np. przez kategorie
  Wikipedii — Common Pile ich nie ma, potrzebny osobny zrzut `categorylinks`).
- Udział tekstu redagowanego z LLM w wersjach z 2023–2025.
- robots.txt/TDMRep Wikimedia (nieistotne przy licencji, ale nie sprawdzone).
- Wikibooks: precyzja nie oceniana osobno (ta sama reguła; tylko 1 469 dok.).
