# Karta źródła: otwarte podręczniki matematyki (LibreTexts, PressBooks, OERCommons) z Common Pile

Zapisana 26.11.2026 przed pobraniem do budowy zbioru (pomiary na pełnych plikach źródła w `/tmp`, usunięte po
pomiarze). Rezerwacja: https://github.com/slayerlabs/benchmarks-fabryka-ai/issues/346. Przegląd kandydatów:
`dane/matematyka-wspolne/kandydaci_czyste.md` (C1–C3).

Cel: mała, czysta prawnie porcja podręcznikowej matematyki szkolnej i akademickiej (wyjaśnienia, przykłady,
ćwiczenia) do zbioru matematyki v6. Oznaczenia: V = sprawdzone 26.11.2026 (URL, rewizja, sha256), I = wywnioskowane.

## 1. Identyfikacja

| część | repo @ rewizja | pliki (sha256) |
|---|---|---|
| C1 LibreTexts | V: `common-pile/libretexts@d4ce4b1edf95888b24992db3bbb2ae8e2bf6c22f` | `00000_libretext.json.gz` `eee45504dab26b692653943a8528ead0d0361bce3b5255ed07b69da3fbd3c984` (cały zbiór, 62 269 dok.) |
| C2 PressBooks | V: `common-pile/pressbooks@29fa162fc78277b160a7010f18086b5189ffb761` | `00000_pressbooks.json.gz` `67d1135ad65d3c1f2f4d88d44ad35d37a4e381cb518c1bd878e4d2c350c9ff21`, `00001_pressbooks.json.gz` `cd3a484605b52654a3a1b022bd125091fa15739b243d8b9967c97454e1227c41` (106 881 dok.) |
| C3 OERCommons | V: `common-pile/oercommons@9b3305165b01bec541b6a6baaba2b5b8566dfe29` | `00000_oercommons.json.gz` `6582d00a93ffcddad76beace4866e42ff9f1c5bc1f3985cc8f117d51271027b8` (9 339 dok.) |

- V: wydawca: Common Pile v0.1 (EleutherAI i in.), praca https://arxiv.org/abs/2506.05209; kod
  https://github.com/r-three/common-pile. Teksty zebrane z HTML stron źródeł (karty: LibreTexts 03.2025,
  PressBooks i OERCommons 03.2025 wg pola `added`).
- V: pola dokumentu: `id` (URL sekcji), `text`, `source`, `added`, `created`, `metadata.license`, `metadata.url`;
  PressBooks dodatkowo `metadata.title` (tytuł książki), `metadata.book_url`; OERCommons `metadata.title`,
  `metadata.author`.

### Algorytm wyboru (do `preregistracja.json`)

1. C1: `metadata.url` (gdy brak: `id`) pasuje do `^https?://(math|stats)\.libretexts\.org`.
2. C2: `KW` (słowo matematyczne: math, mathematics, calculus, algebra, geometry, trigonometry, statistics,
   probability, … — wyrażenia `KW` i `LATEX` w `skrypty/podr_pass.py`) w `metadata.book_url + " " + metadata.title`
   ORAZ ≥3 trafienia wzoru LaTeX w tekście (`\frac`, `\sqrt`, `\begin{`, `$…$`, …). Wyniki: `wyniki/przeglad_zrodla.json`.
3. Wszystkie: deduplikacja dokładna po md5 tekstu (V: konieczna, niżej); odrzucenie dokumentów < 600 tokenów v6
   (V: to w C1 głównie strony-spisy treści rozdziałów).
4. C3 odrzucone w całości (precyzja < 55%, niżej).

## 2. Prawa

- V: licencja per dokument w `metadata.license`; w żadnym z trzech zbiorów nie ma licencji NC ani ND (0 dopasowań
  `nc|noncommercial|nd|noderiv` na 178 489 dokumentach).
- V: licencje w wybranej części po dedupie i progu 600 tok.: C1 (7 165 dok.): CC BY 4.0 4 916, CC BY-SA 4.0 1 281,
  GFDL 384, CC BY 3.0 288, CC BY-SA 3.0 152, PD 144. C2 (1 101 dok.): CC BY 4.0 726, CC BY-SA 4.0 375.
- V: karta Common Pile: licencja sprawdzana per sekcja (LibreTexts) lub z wyszukiwarki źródła (OERCommons); autorzy
  ostrzegają przed „license laundering” (błędnie oznaczone licencje).
- **OpenStax (US)** — V: 1 229 dokumentów C1 (6,57 mln tok.) i 205 dokumentów C2 (2,09 mln tok.) to treści OpenStax
  (słowo „OpenStax” w URL albo na początku/końcu tekstu).
  - V: regulamin OpenStax (https://openstax.org/tos, API CMS strona 115, opublikowany 2016-11-08): „Each individual
    work in the Service is offered for license to you by the author of that work on the terms and conditions set forth
    in the Creative Commons license associated with that individual work” — brak zapisu o AI/trenowaniu modeli (V:
    0 trafień `artificial|AI|machine|train|scrap|crawl` w treści regulaminu).
  - V: 22.04.2026 OpenStax ogłosił przejście całej biblioteki z CC BY na CC BY-NC-SA „for all newly released and
    updated versions”, z dopiskiem „No action is needed by anyone who has previously created derivatives of CC BY
    content” (https://openstax.org/blog/openstax-licensing). Powód (V, wpis z 18.03.2026 „When open resources meet a
    changing landscape”): komercyjne ponowne użycie, „Emerging technologies like artificial intelligence (AI) have
    accelerated this shift”.
  - I: kopie w Common Pile pochodzą z 03.2025, sprzed zmiany, z wersji na CC BY 4.0; licencja CC jest nieodwołalna dla
    już udostępnionych wersji, więc te kopie wolno wykorzystywać komercyjnie z uznaniem autorstwa. Wola wydawcy jest
    jednak jasna (ryzyko reputacyjne, nie prawne). Formularz OpenStax „content reuse request” wymienia „AI-related
    project” (wynik wyszukiwania, strona nie przeczytana — I).
  - Rozjazd z rejestrem: OpenStax **Polska** ma jawny zakaz trenowania AI (rejestr, sekcja 4); OpenStax US takiego
    zakazu w regulaminie nie ma (V).

**Bramka „można TRENOWAĆ” (także komercyjnie): TAK.** Podstawa: licencje CC BY / CC BY-SA / GFDL / PD per dokument
(wszystkie pozwalają na użycie komercyjne; BY-SA i GFDL — copyleft dla utworów zależnych, I: model nie jest utworem
zależnym tekstu, ale wydawany zbiór tak). Ścieżka takedown: usunięcie po `id` (URL sekcji).

**Bramka „można ZGŁOSIĆ”: TAK** dla C1 i C2 (licencja per dokument, bez NC/ND), z obowiązkiem atrybucji (autor/URL w
kolumnie `author`) i zachowaniem SA/GFDL w części na tych licencjach. Zastrzeżenie: treści OpenStax oznaczyć w
datasheet (zmiana licencji wydawcy w 2026).

## 3. Zawartość

- V: angielski; tekst ludzki (podręczniki akademickie i szkolne, ćwiczenia, przykłady z rozwiązaniami); wzory jako
  `\(…\)` / `\[…\]` (C1) albo `[latex]…[/latex]` (C2, znaczniki WordPress do normalizacji).
- V: C1 hosty: math.libretexts.org 7 600, stats.libretexts.org 2 133 (przed dedupem); C2 najczęstsze książki:
  Trigonometry 83, Algebra and Trigonometry OpenStax 79, Introductory Statistics 73, Mathematics for the Liberal
  Arts 67, Introduction to Statistics 65, Statistics for the Social Sciences 58, Informal Calculus 50.
- V: artefakty: C1 3 277 dokumentów zaczyna się od nawigacji „Last updated / Save as PDF” (do wycięcia regexem);
  2 170 dokumentów C1 < 600 tok. to spisy treści rozdziałów; C2 ma linki wideo i „[latex]”.
- **Precyzja wycinka (ręczna ocena, „czy to matematyka/statystyka”)**:
  - C1: 20/20 (V, seed 31; Wilson 95%: 0,84–1,00). Uwagi: 4/20 to krótkie spisy treści (usuwa próg 600 tok.),
    1/20 matematyka finansowa (liczona jako matematyka).
  - C2: 20/20 (V, seed 32; 0,84–1,00). Uwagi: dużo matematyki elementarnej (Adult Literacy Fundamental Mathematics).
  - C3 reguła 0 (`KW` w tytule albo ≥5 wzorów): 11/20 (V, seed 33; 0,34–0,74); błędy: lekcja ESL „Modal Verbs –
    Probability”, makroekonomia, sylabusy, standardy stanowe, puste strony. Reguła 1 (`KW` w tytule, bez
    standards/syllabus/ESL/economics, ≥800 tok.) na nowych 20: 8/20 (V, seed 34; 0,22–0,61), do tego pula tylko 63
    dok. / 0,2 mln tok. **C3 odrzucone.**

## 4. Skala i dostęp

| część | wybrane (V) | po dedupie dokładnym | po progu 600 tok. (do zbioru) |
|---|---|---|---|
| C1 | 9 733 dok., 31,64 mln tok. v6, 95,2 MB | 9 234 dok., 29,99 mln | **7 165 dok., 29,43 mln** |
| C2 | 2 415 dok., 16,06 mln, 48,8 MB | 1 122 dok., 5,97 mln | **1 101 dok., 5,96 mln** |
| C3 (odrzucone) | 356 dok., 1,59 mln | 224 dok., 0,95 mln | 143 dok., 0,94 mln |

- V: C2 ma 1 293 kopie dokładne (10,09 mln tok., 63% tokenów wycinka): ten sam rozdział pod kilkoma `id`
  z różnym fragmentem `#chapter-…-section-N` (1 134 unikalne URL-e bez fragmentu na 2 415 dok.).
- I: razem **~35 mln tokenów v6** po dedupie dokładnym; po dedupie rozmytym C1↔C2 (te same książki OpenStax w obu)
  i wobec FineMath/InfiWebMath mniej (§6).
- V: dostęp bez bramki, `hf_hub_download` po rewizji.

## 5. Ryzyka

- Kopie: V dokładne (wyżej); I: bliskie kopie między C1 i C2 (OpenStax „Algebra and Trigonometry”, „Introductory
  Statistics” są w obu) — MinHash obowiązkowy.
- Testy: I: ćwiczenia podręcznikowe mogą pokrywać się z MATH/GSM8K/MMLU (zadania typu „Yoonie is a personnel
  manager…” z OpenStax Introductory Statistics krążą po sieci) — 13-gramy testów obowiązkowe.
- PII: V: e-mail w 11 dok. C1 i 1 dok. C2 (po progu); maskowanie.
- Syntetyczne: I: niskie (podręczniki sprzed 2023 w większości); nowsze wersje LibreTexts mogą mieć fragmenty z AI —
  nie sprawdzone.
- OCR: nie dotyczy (HTML).
- Prawa: OpenStax (wyżej); „license laundering” wg karty Common Pile.

## 6. Nowość

- I: wysokie nakładanie z FineMath-4+ (w Slayerze 1.07 i w gotowym zbiorze): w próbce eksportu FineMath-4+
  (266 351 wierszy) `libretexts.org` 1 230, `pressbooks` 122, `openstax.org` 99; w InfiWebMath-4+ (196 757 wierszy)
  `libretexts.org` 1 365. Pomiar URL: §6a.
- Dowód wpływu: MathPile (arXiv 2312.17120, Tab. 4, Mistral-7B, ciągły pretrening): „+ Textbooks (0.56B)”: GSM8K
  47,38→48,97, MATH 10,08→12,10, SAT-MATH 47,27→56,36, MMLU-Math 44,92→48,93. Inne podręczniki niż nasze, model 7B.

### 6a. Nakładanie URL z FineMath-4+ i InfiWebMath-4+

Metoda: URL znormalizowany (bez schematu, `www.`, fragmentu `#`, zapytania, końcowego `/`, z dekodowaniem `%XX`,
małe litery). InfiWebMath-4+: V lokalna kopia `dane/infiwebmath4/robocze/pobrania/lok/*.parquet` (32 pliki,
6 296 212 wierszy). FineMath-4+: V kolumna `url` 4 z 64 shardów `HuggingFaceTB/finemath@e92b25a6…/finemath-4plus`
(418 720 wierszy; pełne pobranie kolumny trwało ~6 min/shard).

| wycinek (przed dedupem) | w InfiWebMath-4+ (V) | w FineMath-4+ (V, 4/64 shardów) | FineMath ×16 (I) |
|---|---|---|---|
| C1 LibreTexts 9 733 dok. | 944 dok., 4,68 mln tok. | 81 dok., 0,30 mln | ~1 300 dok., ~4,8 mln |
| C2 PressBooks 2 415 dok. | 254 dok., 1,98 mln | 33 dok., 0,25 mln | ~530 dok., ~4,0 mln |

I: część C1/C2 (rzędu 15–30% tokenów) jest już w gotowym zbiorze przez FineMath-4+ i InfiWebMath-4+ jako strony
WWW tych samych sekcji; dedup URL + MinHash przed użyciem. Ekstrapolacja ×16 zakłada równy rozkład domen w
shardach FineMath.

## Nie sprawdzone

- Licencje per dokument u źródła (zgodność `metadata.license` z bieżącą stroną LibreTexts/PressBooks) — próbka nie
  sprawdzona.
- Regulaminy LibreTexts i PressBooks (poza licencją CC) wobec trenowania AI; robots.txt/TDMRep tych domen.
- Pełna treść artykułu pomocy OpenStax „Using OpenStax Content with AI Tools” i formularza „content reuse request”
  (strony JS, nieczytelne dla narzędzia).
- Precyzja reguły C2 tylko na 20 dok.; recall reguły C2 (książki bez słowa matematycznego w tytule) nie mierzony.
- Bliskie kopie C1↔C2 i nakładanie 13-gramów z testami.
