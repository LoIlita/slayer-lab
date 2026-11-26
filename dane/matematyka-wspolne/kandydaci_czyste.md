# Kandydaci: czysta matematyka i logika matematyczna (~5–6 mld tokenów v6), bez StackExchange

Przegląd 26.11.2026 dla #346 (zbiór matematyki v6, ~20 mld). Gotowe: FineMath-4+ (7,0), Stack-Edu Python (4,8),
InfiWebMath-4+ (1,1). StackExchange ma osobną kartę. To jest przegląd przed kartami źródeł (krok 2 metodologii),
nie karta: każdy wybrany kandydat dostaje własną `KARTA_ZRODLA.md` przed pobraniem pełnych danych.

Oznaczenia: **V** = sprawdzone 26.11.2026 (URL, rewizja, sha256 pliku próbki); **I** = wywnioskowane albo
ekstrapolowane. Tokeny = tokenizer v6 (`dclm-en/robocze/pobrania/tokenizer_v6/tokenizer.json`, len(ids)+1),
liczone na próbkach w `/tmp/czyste` (usunięte po pomiarze). Skrypty pomiarowe były jednorazowe (`/tmp`).

Kryteria właścicielki: (1) bez tekstu modeli zamkniętych, (2) bez Llamy i ziaren przepisanych Llamą, (3) bez NC,
(4) jakość, (5) bez duplikatów ze Slayerem (1.07 en_mix: FineMath + open-web-math; 1.09: FineWeb-Edu) i z
FineMath-4+/InfiWebMath-4+/Stack-Edu.

## 1. Tabela kandydatów

| # | źródło | repo @ rewizja (plik próbki, sha256) | licencja per dokument | tekst | tokeny v6 | jakość (5+ dok. przeczytanych) | nakładanie | dowód wpływu |
|---|---|---|---|---|---|---|---|---|
| A1 | arXiv pełne teksty, licencje otwarte, kategoria główna math.\*, math-ph, stat.\*, cs.LO/DM/CC/FL/SC/IT/GT/NA | `common-pile/arxiv_papers@963fe980c55b353980653f1a27c1dc0c8a2d7058` (22 pliki `.jsonl.gz`, shard `00000` = `0bac07f4…bc365`; sumy wszystkich w §2.1a); kategorie z `librarian-bots/arxiv-metadata-snapshot@c428226b689a0e17db2cd55265133b9eca15d97f` (CC0, 3 224 542 prac) | V (wszystkie 22 pliki): `metadata.license` prac docelowych: CC BY 4.0 63 056, CC0 4 190, CC BY-SA 4.0 3 796, CC BY 3.0 1 794, „Public Domain” 484; zero NC/ND | ludzki; LaTeX→LaTeXML→HTML→Trafilatura, wzory jako `$…$` | V: 73 320 prac docelowych z 304 048, 6,11 GB UTF-8; ścisłe (math.\*, math-ph, cs.LO, cs.DM) 58 953 prac, 4,97 GB. Przelicznik V z próbki 1 500 prac shardu 0: 2,49 B/tok → **~2,45 mld** (ścisłe ~2,0 mld) | dobra: prawdziwe prace (math.OC, AP, NT, CA, PR), LaTeX czytelny; artefakty: znaczniki przypisów „111”, `~{}~{}`, e-maile autorów (PII), czasem urwane zdania po usuniętym wzorze | niskie (I): FineMath/OWM to web; strony `arxiv.org` w próbce eksportu FineMath-4+: 1/266 351. peS2o ma te same prace (`pdf_src` Arxiv) — dedup obowiązkowy | DeepSeekMath (2402.03300 §5.1.2, Tab. 8): „arXiv papers seem ineffective in improving mathematical reasoning” — 1.3B po 150 mld tok. ArXiv-RedPajama: GSM8K 2,9→3,3, MATH 3,0→3,4, MMLU-STEM 19,5→9,0; 7B: MATH 12,5→11,1. Autorzy zastrzegają: nie badali większej skali ani mieszania. MathPile (2312.17120 Tab. 4, Mistral-7B): +arXiv 0,38 mld: MATH 10,08→7,50. Llemma (2310.10631 Tab. 5) trenuje arXiv:web:code = 2:4:1 (dobór perpleksją na MATH train) |
| A2 | arXiv abstrakty tych kategorii | `common-pile/arxiv_abstracts@828e35d1000f94579da8850f5f640c138279bdb5` (shard `00000`, `1a6c475f…3abdb8`) | V: `metadata.license` = CC0 (polityka arXiv dla metadanych wg karty), `full_text_license` osobno | ludzki | V: shard 0 (z 4): 218 104 abstraktów w kategoriach, 39,5 mln tok., śr. 156. I: całość ~0,1 mld; nowe (prace spoza A1) ~0,09 mld | dobra, krótkie | abstrakty prac z A1 są w ich pełnych tekstach → brać tylko prace bez otwartej licencji | brak osobnego |
| A3 | arXiv licencja domyślna (`nonexclusive-distrib`), bez NC/ND, te same kategorie | metadane jw.; tekst np. `EleutherAI/proof-pile-2@901a9273a770e9d4138c5ddd91802f9c5c6cdc4b` → `arxiv/` (RedPajama, do 04.2023) albo własny LaTeX z S3 arXiv | V: 495 525 prac docelowych ≤09.2024 z licencją domyślną + 65 003 bez licencji (przed 2004); licencja domyślna NIE daje praw osobom trzecim | ludzki | I: ~560 tys. × ~27 tys. ≈ **~15 mld** | jak A1 | jak A1 | jak A1 |
| B1 | Lean 4 mathlib4 | `github.com/leanprover-community/mathlib4@e54979a532247ae4eb9d5578a8fd40a1bc332101` | V: Apache-2.0 (LICENSE + nagłówek pliku) | ludzki (I: polityka mathlib wobec kodu z AI nie sprawdzona) | V: 9 351 plików `.lean`, 104,2 MB, ~45 mln (2,31 B/tok) | bardzo dobra: docstringi, twierdzenia, dowody taktyczne | I: znikome (w eksporcie FineMath 0 trafień `leanprover`) | Llemma Tab. 4: Lean formal-to-formal miniF2F-test 20,49 (Code Llama 7B) → 26,23 (Llemma 7B) po AlgebraicStack (1,5 mld tok. formalnej mat.); bez ablacji samego Lean |
| B2 | Isabelle AFP | `github.com/isabelle-prover/mirror-afp-devel@02fd3c6b5326d1c53704c52c09cabb3fd2a772f5` | V: per wpis w `metadata/entries/*.toml`: 1 017 × `bsd`, 26 × `lgpl` | ludzki | V: 10 562 `.thy`, 303,4 MB, ~135 mln (2,25 B/tok) | bardzo dobra (np. Bernoulli.thy: lematy + Isar) | I: znikome (`isa-afp.org` 1 trafienie w InfiWebMath) | Llemma Tab. 4: Isabelle informal-to-formal miniF2F-test 17,62 → 22,13 (7B) |
| B3 | HOL Light | `github.com/jrh13/hol-light@096417cac706ff0818f739bbc19f2ed499e43283` | V: licencja typu BSD-2 („Redistribution and use… permitted”); V: „Some files… other licenses” — per plik do sprawdzenia | ludzki | V: 980 `.ml`, 87,1 MB, ~44 mln (1,98 B/tok) | dobra (OCaml + twierdzenia), sporo tabel liczbowych | znikome | brak osobnego |
| B4 | Metamath set.mm + iset.mm | `github.com/metamath/set.mm@ce7f29d6bb49ca66913cc4adae72bb4df5bcb854` | V: CC0 (LICENSE) | ludzki | V: 64,2 MB, 35 mln z dowodami; V: 59,9%/55% bajtów to skompresowane dowody (`$= … $.`, ciąg liter) → bez nich ~14 mln (I) | definicje i komentarze dobre; dowody skompresowane = śmieci | `metamath.org` 320/266 351 w próbce FineMath-4+ (I: ~8 tys. stron w pełnym) | brak |
| B5 | Rocq stdlib, math-comp, UniMath, agda-stdlib, Stacks Project | `rocq-prover/stdlib@9657c750…`, `math-comp/math-comp@656cdbcf…`, `UniMath/UniMath@11e01f09…`, `agda/agda-stdlib@119d1761…`, `stacks/stacks-project@a04446e5…` | V: LGPL-2.1 / CeCILL-B / MIT-podobna / MIT / GFDL 1.2 | ludzki | V: 3,0 / 2,8 / 10,8 / 2,2 / 11,0 mln = **~30 mln** | dobra; Stacks = LaTeX geometrii algebraicznej | Stacks: 21/266 351 w FineMath-4+ | brak |
| B6 | Proof-Pile-2 AlgebraicStack: `isa_proofsteps`, `lean_proofsteps` | `EleutherAI/proof-pile-2@901a9273a770e9d4138c5ddd91802f9c5c6cdc4b` | I: pochodne AFP+Isabelle (BSD/LGPL) i mathlib4 `c779bd5` (Apache-2.0); karta: „We do not alter the license” | wyekstrahowane narzędziem (PISA, lean-training-data), nie LLM (V: praca, dod. B.1.2–B.1.3) | V: isa 258 108 dok., 1 766,8 MB, ~923 mln; lean 3 396 dok., ~81 mln. I: po dedupie stanów ~0,3–0,5 mld | dobra, ale powtarzalna (stan → krok) | nakłada się z B1/B2 treściowo (inna forma) | Llemma Tab. 4 jw. |
| B7 | Proof-Pile-2 AlgebraicStack: `github-lean/coq/isabelle` | jw. | **V: brak pola licencji** (`meta`: author, repo, sha, path); pobrane przez GitHub API bez filtra licencji (praca, B.1.1) | ludzki + autoport (`mathlib3port`, `Mathlib4_auto`) | V: lean ~222 mln, coq ~288 mln, isabelle ~342 mln | mieszana: dużo kopii i portów automatycznych | z B1/B2 | Llemma jw. |
| B8 | Proof-Pile-2 AlgebraicStack: `tex` | jw. | V (plik `tex0002`): `max_stars_repo_licenses` per plik z The Stack v1: MIT 2 789, Apache 640, BSD-3 373, CC-BY-4.0 351, CC0 258… (licencja repo, nie tekstu) | ludzki | V: tex0002: 5 156 dok., 83,8 MB, 28,3 mln (2,96 B/tok). I: całość (0,55 GB zst) ~0,5 mld | mieszana: notatki, prace, dokumentacja programów | I: część to źródła prac z arXiv → dedup z A1 | brak |
| C1 | LibreTexts math + stats | `common-pile/libretexts@d4ce4b1edf95888b24992db3bbb2ae8e2bf6c22f` (cały zbiór, `eee45504…c984`) | V: `metadata.license` per sekcja: CC-BY 7 080, CC-BY-SA 1 876, GFDL 564, PD 213; brak NC | ludzki (V: część to OpenStax, np. Introductory Statistics) | V: 9 733 dok. (host math./stats.), 95,2 MB, **~32 mln** (3,01 B/tok) | dobra; nagłówki nawigacji „Last updated / Save as PDF”, wzory `\(…\)` | **wysokie**: `libretexts.org` 1 230/266 351 w próbce FineMath-4+ (I: ~31 tys. stron w pełnym), 1 365/196 757 w InfiWebMath | MathPile Tab. 4 (Mistral-7B): +Textbooks 0,56 mld: MATH 10,08→12,10, SAT 47,27→56,36, MMLU-Math 44,92→48,93 |
| C2 | PressBooks math | `common-pile/pressbooks@29fa162fc78277b160a7010f18086b5189ffb761` (2 pliki: `67d1135a…`, `cd3a4846…`) | V: CC-BY 1 262, CC-BY-SA 1 153 w wycinku; całość bez NC | ludzki | V: 2 415 dok. (słowo kluczowe w tytule/URL + ≥3 wzory), 48,8 MB, **~16 mln** | dobra (Trigonometry, Algebra and Trigonometry OpenStax); wzory jako `[latex]…[/latex]`, linki wideo | `pressbooks` 122/266 351 w FineMath-4+ | jw. (podręczniki) |
| C3 | OERCommons math | `common-pile/oercommons@9b3305165b01bec541b6a6baaba2b5b8566dfe29` (`6582d00a…27b8`) | V: CC-BY 332, CC-BY-SA 19, PD 3 | ludzki | V: 354 dok., **~1,6 mln** | słaba: opisy lekcji, standardy, tabele | `oercommons.org` 38/266 351 | brak |
| C4 | DOAB (książki OA) gęste matematycznie | `common-pile/doab@89e7a35935045f2b268a2229347e38f16fbeb729` (shard `00000` z 13, `38da5ce3…a9d3`) | V: CC-BY 33 947, CC-BY-SA 32 w shardzie; brak NC (filtr źródła) | ludzki; PDF→Marker (OCR/konwersja) | V: shard 0: 352 rozdziały (≥100 komend LaTeX i ≥2/1000 zn.), 43,5 MB, 14,2 mln. I: całość **~0,18 mld** | mieszana: dużo inżynierii (CFD, robotyka, MDPI), artefakty Marker („Rynð Þ”, `<sup>`) | niskie (PDF-y) | brak |
| D1 | Wikipedia EN, artykuły ze wzorami | `common-pile/wikimedia@781b263a6546515543bec3968ad4743fbc152b72` (`00000_wikipedia` `b3158688…3cdb`) | V: CC BY-SA 4.0 w każdym dok. | ludzki (I: od 2023 możliwe fragmenty pisane z LLM, niewykrywalne) | V: shard 0: 632 art. (≥10 wzorów `$…$` z `\ ^ _ =` i ≥5 komend), 4,19 mln; shard 93: 75 tys.; shard 170: 51 tys. (187 shardów, gęstość spada z id strony). I: **~0,1–0,3 mld**; MathPile: Wikipedia mat. po czyszczeniu 0,18 mld (Llama) | dobra (Galois group, Pell's equation, Peano axioms); filtr łapie też fizykę/chemię | I: FineWeb-Edu (1.09) może mieć strony en.wikipedia — nie mierzone; w FineMath-4+ 3/266 351 | MathPile Tab. 4/5 (Mistral-7B): +Wikipedia 0,18 mld: GSM8K 47,38→49,96, MMLU-Math 44,92→47,16, MATH 10,08→9,96; surowa Wikipedia 2,18 mld: GSM8K →32,30 (czyszczenie LaTeX kluczowe) |
| D2 | Wikibooks math | jw. (`00000_wikibooks.com`) | V: CC BY-SA 4.0 | ludzki | V: 2 111 dok., ~6,2 mln (z 2 shardów; drugi 39 MB) → I: ~7 mln | dobra (Calculus, Commutative Algebra, A-level) | `wikibooks.org` 396/196 757 w InfiWebMath | brak |
| D3 | ProofWiki | strona; dumpy wikiteam (archive.org); I: możliwie w `common-pile/wikiteam` — nie znalezione (datasets-server 503) | V: CC BY-SA 3.0 + GFDL (proofwiki.org/wiki/ProofWiki:Copyrights, oldid 326045); strony dyskusji i użytkowników wyłączone | ludzki | nie zmierzone (I: ~30–50 mln) | I: dobra (dowody) | **wysokie**: `proofwiki.org` 605/266 351 w FineMath-4+ (I: ~15 tys. stron), 800/196 757 w InfiWebMath | brak osobnego |
| D4 | PlanetMath | `github.com/planetmath` (64 repo, LaTeX wg MSC) | V: GFDL (planetmath.org/planetmath) | ludzki | nie zmierzone (I: ~10 mln) | I: dobra | `planetmath.org` 137/266 351 FineMath-4+, 330/196 757 InfiWebMath | brak |
| D5 | nLab | ncatlab.org | **V: brak formalnej licencji** („no consensus on a more formal license statement”) | ludzki | nie zmierzone | dobra | `ncatlab.org` 30/266 351 | — |
| E1 | OEIS | `github.com/oeis/oeisdata@976b0c73e00453b1c1e6f16d83108cb9bb744c3b` (`seq/`) | V: CC BY-SA 4.0 (LICENSE repo + EULA oeis.org) | ludzki | V: 402 003 `.seq`, 597,7 MB, ~308 mln (1,94 B/tok). I: bez `%H` (linki, 13% bajtów), `%I/%K/%O/%U` ~0,22 mld | średnia: nazwy, komentarze, wzory (`%F`), przykłady (`%e`), kod Mathematica/PARI (`%t/%o`); dużo ciągów liczb; e-maile autorów | **wysokie**: `oeis.org` 2 966/266 351 w FineMath-4+ (I: ~75 tys. stron), 578/196 757 w InfiWebMath | brak |
| E2 | peS2o, `s2fieldsofstudy` ∋ Mathematics, bez `pdf_src` Arxiv | `common-pile/peS2o@2caeba1585aaafa3c965410d80af85b09ed11cd9` (`v0/documents/peS2o-0001`, `8bf759b5…a2ed`) | V: `oa_license` CCBY 1 459, CCBYSA 51, CC0 15, pd 6 w wycinku | ludzki; PDF→Grobid | V: shard 1: 1 531/68 188 dok. (2,2%), ~10,9 mln, bez arXiv ~8,2 mln. I: 93 shardy → **~0,75 mld** | słaba dla matematyki: wzory spłaszczone („f 1 (u 1 , u 2 ) = Au 1 (1 − u 1 /K)”), sporo modelowania stosowanego | z A1 (376/1 531 to arXiv) | brak (Common Pile ważył źródła po modelach 1,7B na 28 mld tok., wag w HTML nie ma) |
| — | odrzucone z góry | `GAIR/MathPile` (CC-BY-NC-SA-4.0, V API) — NC; `math-ai/AutoMathText` (web pokrywa OWM; nie sprawdzane głębiej); Lean Workbook / DeepSeek-Prover (LLM) | | | | | | |

## 2. Pomiary szczegółowe

### 2.1 arXiv (A1–A3)

- V: metadane arXiv (snapshot CC0, 3 224 542 prac): kategoria główna docelowa: 135 066 otwartych, 660 359 innych.
  Licencje prac docelowych: `nonexclusive-distrib` 565 017, CC BY 4.0 120 194, brak 64 920, BY-NC-ND 4.0 17 285,
  BY-NC-SA 4.0 10 829, CC0 6 832, BY-SA 4.0 6 070, BY 3.0 1 970.
- V: do 09.2024 (zakres Common Pile, I): 80 062 otwarte prace docelowe z 365 072 otwartych (21,9%).
- I: tekst A1 to sprawdzony wycinek, A3 (licencja domyślna) liczony tylko z metadanych.

### 2.1a Pełny przebieg arXiv (V, 26.11.2026)

- Wszystkie 22 pliki `common-pile/arxiv_papers@963fe980…` przeczytane: **304 048 prac** (karta podaje 321 336 dla
  wersji „raw”; 304 048 to liczba z tabeli 4 pracy dla wersji filtrowanej — repo „raw” ma tyle samo wierszy, V).
  Wszystkie prace mają kategorie w snapshocie metadanych (0 braków w shardzie 0).
- Kategoria główna docelowa: 73 320 prac, 6 110 534 698 B; ścisła: 58 953 prace, 4 970 935 928 B; całość 20,7 GB.
- Lata (`created`) prac docelowych: 2021–2024 = 61 677 z 73 320 (I: arXiv zaczął szeroko oferować CC BY 4.0 ok. 2020).
- sha256 plików: shard `00000` `0bac07f4441c5bd38bdb1c5c246a030355e466b1e00c4c707ed98eeca03bc365`, `00001`
  `db1a144d0a86ff3415810b611670680fcc69889595c340955edcbf01d2c5b56d`, `00002`
  `e2f12073e35e1c31daff1eac2c12e2a7267185d81f843bab15702f10713cff74` (pozostałe policzone, nie przepisane tutaj).
- Tokeny: 6,11 GB / 2,49 B/tok ≈ 2,45 mld v6 (I: przelicznik z 1 500 prac shardu 0, starszych niż średnia).

### 2.2 Formalna matematyka (B1–B8)

- Rdzeń bibliotek z jawną licencją (B1–B5): ~45 + 135 + 44 + 14 + 30 ≈ **~0,27 mld** v6. To mało; więcej daje
  tylko B6 (stany dowodów, ~0,3–0,5 mld po dedupie, I) i B8 (TeX z GitHub, ~0,5 mld, I).
- B7 (GitHub Lean/Coq/Isabelle z AlgebraicStack) — bramka ZGŁOSIĆ nie przejdzie (brak licencji per plik); zamiast tego
  własny klon wybranych repo z licencją (B1–B5 plus np. CoqGym/VST po sprawdzeniu).
- AlgebraicStack Python (6,1 mld Llama) pominięty: pokrywa się ze Stack-Edu Python.

### 2.3 Podręczniki i wiki (C, D)

- C1–C4 razem ~0,23 mld, z czego 0,18 to DOAB (słabsza konwersja). LibreTexts i PressBooks to w dużej części OpenStax
  (CC BY 4.0); rejestr wyklucza OpenStax **Polska** za zakaz trenowania AI — dla OpenStax (US) taki zapis nie był
  sprawdzany.
- Wycinek matematyki w C2–C4 i D1 to heurystyka (słowa w tytule + gęstość LaTeX); precyzja nie mierzona (D1 łapie
  fizykę i chemię).

## 3. Ranking

Skala: jakość × czystość praw × nowość wobec FineMath/Slayera × skala.

| miejsce | kandydat | bramka TRENOWAĆ | bramka ZGŁOSIĆ | uzasadnienie |
|---|---|---|---|---|
| 1 | A1 arXiv otwarte, math | TAK (licencja) | TAK (CC BY/BY-SA/CC0 per dok.; I: ryzyko „license laundering” wg karty) | jedyne czyste źródło >1 mld; nowe wobec web; słaby dowód wpływu przy 1B |
| 2 | B1+B2+B3+B5 biblioteki formalne | TAK | TAK (Apache/BSD/LGPL/MIT/CeCILL-B/GFDL; HOL Light per plik) | najczystsze pochodzenie, nowe, dowód Llemma; małe (~0,26 mld) |
| 3 | D1+D2 Wikipedia/Wikibooks math | TAK | TAK (CC BY-SA 4.0) | dobra jakość, dowód MathPile; nakładanie z FineWeb-Edu niezmierzone |
| 4 | C1+C2 LibreTexts/PressBooks math | TAK | TAK | najlepszy dowód (MathPile Textbooks), ale małe i mocno w FineMath (dedup zje część) |
| 5 | B6 proofsteps Isabelle/Lean | TAK | NIEROZSTRZYGNIĘTY (licencja pochodna, I) | duże, bez LLM, powtarzalne |
| 6 | E1 OEIS | TAK | TAK (CC BY-SA 4.0) | ~0,22 mld po czyszczeniu; duże nakładanie z FineMath; specyficzny format |
| 7 | A2 abstrakty arXiv (prace bez otwartej licencji) | TAK | TAK (CC0) | ~0,09 mld, krótkie |
| 8 | B8 TeX z GitHub (Stack v1) | TAK | NIEROZSTRZYGNIĘTY (licencja repo ≠ licencja tekstu; I) | ~0,5 mld, jakość mieszana |
| 9 | E2 peS2o math | TAK | TAK (oa_license per dok.) | ~0,75 mld, ale Grobid niszczy wzory |
| 10 | C4 DOAB math | TAK | TAK | ~0,18 mld, artefakty konwersji, dużo inżynierii |
| 11 | B4 set.mm (bez skompresowanych dowodów) | TAK | TAK (CC0) | ~14 mln |
| 12 | D3 ProofWiki, D4 PlanetMath | TAK | TAK (CC BY-SA 3.0 / GFDL) | nie zmierzone; ProofWiki mocno w FineMath |
| — | A3 arXiv licencja domyślna | TAK tylko przez wyjątek TDM | **NIE** (brak licencji dla osób trzecich) | ~15 mld; jedyna droga do pełnych 5–6 mld z arXiv |
| — | B7 GitHub formal bez licencji, D5 nLab | TDM | NIE | brak licencji |

## 4. Propozycja składu (~5,5 mld v6, wszystko z bramką ZGŁOSIĆ = TAK albo NIEROZSTRZYGNIĘTY)

Unikalnych czystych tokenów (po wyłączeniu A3, B7, D5) jest ~5,1 mld (I) przed dedupem. Do 5–6 mld dochodzi się
powtórzeniem małych źródeł (Common Pile powtarzał małe źródła do 6×; tu najwyżej 2×).

| składnik | unikalne (I) | epoki | w zbiorze | licencja |
|---|---|---|---|---|
| A1 arXiv otwarte, math/stat/logika | ~2,45 mld (V bajty, I przelicznik) | 1 | 2,45 | CC BY / BY-SA / CC0 per dok. |
| A2 abstrakty arXiv (bez prac z A1) | ~0,09 | 1 | 0,09 | CC0 |
| B1–B5 biblioteki formalne | ~0,27 | 2 | 0,54 | Apache-2.0, BSD/LGPL (AFP), BSD-2 (HOL Light), CC0, LGPL-2.1, CeCILL-B, MIT, GFDL |
| B6 proofsteps Isabelle+Lean (po dedupie) | ~0,4 | 1 | 0,4 | pochodne BSD/LGPL/Apache (I) |
| D1+D2 Wikipedia+Wikibooks math | ~0,2 | 2 | 0,4 | CC BY-SA 4.0 |
| C1+C2+C3 podręczniki | ~0,05 | 2 | 0,1 | CC BY / BY-SA / GFDL / PD |
| C4 DOAB math | ~0,18 | 1 | 0,18 | CC BY / BY-SA |
| E1 OEIS (po czyszczeniu i dedupie z FineMath) | ~0,2 | 1 | 0,2 | CC BY-SA 4.0 |
| E2 peS2o math bez arXiv | ~0,75 | 1 | 0,75 | CC BY / BY-SA / CC0 per dok. |
| B8 TeX z GitHub (po dedupie z A1) | ~0,45 | 1 | 0,45 | MIT/Apache/BSD/CC per repo (I) |
| D3+D4 ProofWiki, PlanetMath (po zmierzeniu) | ~0,04 | 2 | 0,08 | CC BY-SA 3.0, GFDL |
| **razem** | **~5,1** | | **~5,6** | |

Wariant dla Slayera 1B: A1 ma najsłabszy dowód przy ~1B (DeepSeekMath); jeśli zbiór idzie najpierw do 1B, zmniejszyć
A1 do ~1 mld i podnieść epoki B/C/D. Wariant „pełne 6 mld z samego arXiv” wymaga A3 (tylko wyjątek TDM, nie do
zgłoszenia) — wtedy osobny podzbiór z flagą `TDM`, poza eksportem do `dataset-team-submissions`.

Obowiązkowo w każdym wariancie: dedup 13-gramów i MinHash wobec FineMath-4+, InfiWebMath-4+ (LibreTexts, ProofWiki,
OEIS, PlanetMath, Wikipedia mają tam tysiące stron), en_mix 1.07, FineWeb-Edu 1.09; dedup A1↔E2↔B8; 13-gramy testów
(MATH, GSM8K, MMLU, miniF2F, PISA, ProofNet); PII (e-maile autorów w A1, E1, AFP).

## Nie sprawdzone

- Przelicznik B/tok dla A1 tylko z shardu 0 (prace starsze); kategorie z dzisiejszego snapshotu metadanych (prace
  przeklasyfikowane po 2024 mogą się różnić).
- Czy licencje w Common Pile arXiv zgadzają się z metadanymi arXiv per praca (porównanie per id nie zrobione).
- Tokeny D1 w całej Wikipedii (zmierzone 3 z 187 shardów, gęstość nierówna) i nakładanie z FineWeb-Edu 1.09.
- Precyzja heurystyk wycinka (C2–C4, D1, E2) — brak ręcznej oceny ≥40 dok. na warstwę.
- Dedup wewnątrz B6 (powtórzenia stanów) i realny uzysk; licencja `isa_proofsteps` (dystrybucja Isabelle) u źródła.
- B8: czy filtr AlgebraicStack dla TeX jest matematyczny; tylko 1 z 3 plików.
- ProofWiki i PlanetMath: rozmiar, dumpy, obecność w `common-pile/wikiteam` (datasets-server zwrócił 503).
- OpenStax (US) a trenowanie AI (rejestr wyklucza OpenStax Polska); regulaminy LibreTexts/PressBooks poza licencją.
- Polityka mathlib4/AFP wobec wkładu generowanego przez LLM; HOL Light: pliki na innych licencjach.
- Opt-out TDM (robots.txt, TDMRep) dla stron i dla arXiv (A3).
- Wagi mieszanki Comma z pracy Common Pile (tabela nie wyrenderowana w HTML).
- Dowód wpływu dla OEIS, DOAB, peS2o, B8 — nie znaleziony.
