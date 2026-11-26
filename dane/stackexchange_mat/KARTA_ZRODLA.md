# Karta źródła: Stack Exchange — serwisy matematyki i logiki (common-pile/stackexchange) dla Slayera 1B

Zapisana 26.11.2026 przed preregistracją i przebiegiem; pomiary na plikach pobranych do `/tmp` (usunięte po pomiarze).
Rezerwacja: https://github.com/slayerlabs/benchmarks-fabryka-ai/issues/346

Cel: część zbioru matematyki ~20 mld tokenów v6 (brakuje ~7 mld). Tekst pisany przez ludzi, licencja per dokument.
Oznaczenia: V = sprawdzone 2026-11-26 w podanym źródle (URL, rewizja, hash), I = wywnioskowane.

## 1. Identyfikacja

- V: URL https://huggingface.co/datasets/common-pile/stackexchange, rewizja `5ec3aa2e65b7c61b7c18f1ff18ccbc4d3279a23c`
  (API: lastModified 2025-06-06, bez bramki dostępu), 835 plików, 364 katalogi serwisów `<serwis>/documents/000NN_se.jsonl.gz`.
- V: **ta rewizja to wersja „raw”, nie „filtered”** — README: „This is the "raw" version of the StackExchange dataset”,
  33 415 400 dok., 103,7 GB UTF-8. Wersja filtrowana to osobne repo
  https://huggingface.co/datasets/common-pile/stackexchange_filtered @ `c0ac7373830c688a43fc12d1988c4b19ccd884ab`:
  44 pliki `stackexchange-dolma-00NN.json.gz` (34 925 454 063 B), 30 987 814 dok., bez katalogów per serwis (serwisy
  alfabetycznie: math.SE w plikach 0004–0006, mathoverflow.net w 0006). Link z README filtered do `stackexchange_raw`
  nie działa (API: brak repo).
- V: wydawca Common Pile (EleutherAI, Univ. of Toronto i in.), praca Kandpal i in. 2025, https://arxiv.org/abs/2506.05209;
  kod https://github.com/r-three/common-pile.
- V (README, praca §B.2): źródło to zrzuty społeczności z grudnia 2024 w Internet Archive plus pytania brakujące,
  wzięte z ostatniego oficjalnego zrzutu z lipca 2024. Dokument = pytanie + jego komentarze + odpowiedzi
  (zaakceptowana pierwsza, dalej wg głosów) + komentarze do odpowiedzi; Markdown → tekst przez PyMarkdown.
- V (praca, tab. 3): filtr wersji „filtered” dla StackExchange: język > 0,5 (FastText), redakcja PII regexem
  (e-mail, telefon, IP → `<EMAIL_ADDRESS>`, `<PHONE_NUMBER>`, `<IP_ADDRESS>`), bez filtra jakości, długości i toksyczności;
  potem globalny dedup (20-gramy, > 90%).

### Wybór serwisów

Zmierzono 14 serwisów (bez `*.meta.*`, które dotyczą spraw serwisu, nie matematyki). V: wszystkie istnieją w rewizji.

| serwis | decyzja | uzasadnienie (V: udział dok. z `$…$` w próbce pomiaru) |
|---|---|---|
| math.stackexchange.com | rdzeń | matematyka od szkoły do studiów (96%) |
| mathoverflow.net | rdzeń | matematyka badawcza (95%) |
| cstheory.stackexchange.com | rdzeń | informatyka teoretyczna: logika, złożoność, dowody (81%) |
| proofassistants.stackexchange.com | rdzeń | dowody formalne Lean/Coq/Isabelle, logika (37%, dużo kodu) |
| matheducators.stackexchange.com | rdzeń | dydaktyka matematyki (58%), mało |
| stats.stackexchange.com | rozszerzenie, zalecane | statystyka i prawdopodobieństwo (54%) |
| cs.stackexchange.com | rozszerzenie, zalecane | algorytmy, języki formalne (73%) |
| or.stackexchange.com | rozszerzenie, zalecane | optymalizacja, programowanie matematyczne (63%) |
| scicomp.stackexchange.com | rozszerzenie, zalecane | analiza numeryczna (71%) |
| quant.stackexchange.com | opcja | rachunek stochastyczny, ale dużo praktyki finansowej (49%) |
| crypto.stackexchange.com | opcja | teoria liczb i algebra, ale dużo inżynierii (62%) |
| physics.stackexchange.com | odrzucony | fizyka, nie matematyka (72%); kandydat do osobnego zbioru STEM |
| mathematica.stackexchange.com | odrzucony | pytania o oprogramowanie Wolfram, głównie kod (32%) |
| puzzling.stackexchange.com | odrzucony | zagadki i gry słowne (29%) |

Niemierzone, poza zakresem (I): datascience, economics, quantumcomputing, codegolf, tex, dsp, electronics.

## 2. Prawa

- V: każdy dokument ma `metadata.license`; we wszystkich 14 serwisach (pełne pliki) 100% to CC BY-SA:
  math.SE 3.0 52,1% / 4.0 47,5% / 2.5 0,4% (1 686 834 dok.); mathoverflow 3.0 45,6% / 4.0 46,1% / 2.5 8,3%;
  or i proofassistants 4.0 100%. Brak NC/ND.
- I: `license` to licencja pytania; V: licencje wszystkich postów dokumentu są w `metadata.all_licenses`: math.SE
  (plik 00000) ~86% dok. jedna wersja, reszta mieszanka 2.5/3.0/4.0. Licencja nie wynika z daty pytania (np.
  pytanie 1906380 z 2016 ma 4.0); I: to `ContentLicense` z zrzutu, liczone od ostatniej edycji posta.
- V: **luka**: w ostatnim pliku każdego serwisu (I: dopełnienie ze zrzutu z lipca 2024) `all_licenses` zawiera `'None'`
  w 63–100% dokumentów (math.SE `00006`: 73 189 z 87 430 dok., 90% znaków; mathoverflow `00001`: 4 244 z 5 251).
  To ~4,3% dokumentów math.SE i ~2,7% mathoverflow. W pozostałych pobranych plikach `'None'` nie występuje; math.SE
  00001–00005 czytane bez `all_licenses`, ale w wersji filtered (cały math.SE) `'None'` ma 72 359 z 1 661 912 dok.
  (4,35%), wszystkie w pliku 0006 (V). I: post bez `ContentLicense`
  w zrzucie; regulamin SE daje CC BY-SA na każdy wkład, ale per wiersz tego nie potwierdzimy.
- V: atrybucja: `metadata.url` (`https://<serwis>/questions/<id>`, 100% dok., id = id pytania) i `metadata.authors`:
  nazwy wyświetlane i adresy profili (`https://<serwis>/users/<n>`) w równych liczbach. Pusta lista autorów:
  math.SE 14,2% dok., mathoverflow 12,4%, stats 18,0% (I: konta usunięte). Atrybucję zapewnia wtedy URL.
- V: regulamin pobrania zrzutu od lipca/sierpnia 2024 (cytat formularza w https://meta.stackexchange.com/q/402501):
  „I understand that this file is being provided to me for my own use and for projects that do not include training
  a large language model (LLM), and that should I distribute this file for the purpose of LLM training, Stack Overflow
  reserves the right to decline to allow me access to future downloads”. W tym samym zrzucie `license.txt`: „All
  content contributed to Stack Exchange sites is licensed under the Creative Commons CC BY-SA license”.
  I: to umowa z pobierającym (sankcja: odcięcie od kolejnych zrzutów), nie licencja treści. Licencję dają autorzy.
- V: `https://math.stackexchange.com/robots.txt` i `https://mathoverflow.net/robots.txt` (odpowiedź HTTP 418 dla
  naszego klienta, 113 B): `License: https://stackoverflow.com/license.xml`, `Content-signal: search=no, ai-train=no`,
  `Disallow: /`. `license.xml` (RSL) wskazuje CC BY-SA 4.0 dla `/`. Czy zwykły crawler dostaje ten sam plik:
  NIE SPRAWDZONE.
- Bramka „można TRENOWAĆ”: **TAK**. Podstawa: CC BY-SA per dokument od autorów, zapasowo TDM art. 4 dyr. 2019/790.
  Sygnał `ai-train=no` i formularz zrzutu to uwagi, nie weto (metodologia §2). Takedown: usunięcie po `metadata.url` / `id`.
- Bramka „można ZGŁOSIĆ”: **NIEROZSTRZYGNIĘTY**. Za: licencja per wiersz, CC BY-SA bez NC/ND, autor i URL w danych.
  Przeciw: (a) wydawca platformy sygnalizuje opt-out (`ai-train=no` w robots.txt, formularz zrzutu), a reguła repo
  zgłoszeń wyklucza opt-out TDM. I: opt-out platformy nad licencją autorów przypomina LESSONS §4 odwrotnie: autorzy
  dali licencję, platforma jej nie odwoła. To decyzja dla przeglądu praw (krok 11). (b) Dokumenty z `'None'`
  w `all_licenses` zgłaszać tylko po decyzji, inaczej odrzucić. (c) SA: eksport w BY-SA z kolumną `license` i `author`.

## 3. Zawartość

- V: pola: `id` (id pytania, = końcówka `url`), `text`, `source` („Stack Exchange”), `added` (2025-03), `created`
  (data pytania), `metadata` {`license`, `all_licenses`, `site`, `url`, `authors`, `sort` = „votes”, `include_comments`
  = true}. To samo w obu wersjach; filtered ma dodatkowo `provenance`.
- V: format: tytuł w 1. wierszu, treść pytania, potem komentarze i odpowiedzi rozdzielone pustą linią, bez znaczników
  „pytanie/odpowiedź/komentarz”. LaTeX zachowany (`$…$`, `$$…$$`, `\begin{align}`), obrazki giną (tekst typu „Here I
  add the two pages” bez treści).
- V (ręczna próbka, seed 20261126): 10 dok. math.SE (6 z pliku 00000, 4 z 00006, lata 2011–2023) i 5 mathoverflow
  (2010–2021). Wszystkie to prawdziwe pytania matematyczne z odpowiedziami ludzi: szeregi Maclaurina, ideały
  w F[[X]], dedukcja naturalna, teoria krat, równanie Lapunowa, automorficzność, partycje płaskie. Spamu i tekstu
  z modelu nie było. Jeden dokument (math.SE 4755162) to samo pytanie bez odpowiedzi. Są podpisy („Thanks, FGH”,
  „Best regards, Gabriel”), wzmianki `@nick` i pomyłki w odpowiedziach poprawiane w komentarzach.
  Ocena jednego czytelnika (ja), bez progów.
- V: krótkie dokumenty (< 300 znaków): math.SE 0,5% (pliki 00000+00006), mathoverflow 0,25%.
- V: rozkład lat math.SE: pliki 00000 (2010–2014) i 00001–00005 rosnąco do 2024; 00006 to dopełnienie 2010–2024.
  ID nie powtarzają się między plikami (math.SE, mathoverflow, stats, physics: 0 duplikatów id).

## 4. Skala i dostęp

Tokeny v6 = `len(ids)+1`, tokenizer v6 z `dclm-en/robocze/pobrania/tokenizer_v6`. sha256 każdego pobranego pliku
zgodne z LFS (V), np. math.SE `00000_se.jsonl.gz` `2192f16e2cc89b0cd0207c74fc7f01baa8c0c8949c912d46c2a962981385eb53`,
mathoverflow `00000_se.jsonl.gz` `3b49c223e55d1c1fe0c558123a453ff1874162263a4a6d37933925824b239d10`.

| serwis | pliki | B (gz) | dok. | tokeny v6 | tok./dok. |
|---|---|---|---|---|---|
| math.stackexchange.com | 7 | 1 622 793 038 | 1 686 834 | ~1 385 mln (I) | ~821 |
| mathoverflow.net | 2 | 231 185 412 | 159 926 | 179 558 061 | 1 123 |
| cstheory | 2 | 19 029 302 | 13 213 | 13 284 215 | 1 005 |
| proofassistants | 2 | 2 073 112 | 1 237 | 1 600 602 | 1 294 |
| matheducators | 2 | 12 686 534 | 3 896 | 7 981 909 | 2 049 |
| stats | 2 | 272 073 616 | 220 450 | 195 611 932 | 887 |
| cs | 2 | 56 907 711 | 49 746 | 40 060 258 | 805 |
| or | 2 | 6 032 308 | 4 492 | 4 705 989 | 1 048 |
| scicomp | 2 | 17 211 280 | 11 696 | 12 931 096 | 1 106 |
| quant | 2 | 25 847 503 | 23 340 | 18 296 712 | 784 |
| crypto | 2 | 44 016 079 | 31 442 | 30 512 488 | 970 |
| physics (odrzucony) | 3 | 337 285 378 | 243 973 | 235 427 215 | 965 |
| mathematica (odrzucony) | 2 | 126 707 151 | 96 388 | 119 161 912 | 1 236 |
| puzzling (odrzucony) | 2 | 47 064 692 | 28 537 | 34 084 296 | 1 194 |

- V: wszystkie serwisy poza math.SE zmierzone w całości (wszystkie pliki, tokenizacja każdego dokumentu).
- math.SE: V tokeny zmierzone na plikach 00000 i 00006: 363 663 dok., 316 689 635 tokenów v6 przy 936 167 795 znakach
  (0,3383 tok./znak). V pliki 00001–00005 przeczytane strumieniowo (bez tokenizacji): 1 323 171 dok., 3 159 430 870
  znaków. I: ekstrapolacja 0,3383 × znaki → ~1 069 mln, razem ~1 385 mln. Kontrola V: wersja filtered, math.SE
  zmierzona w całości (pliki 0004–0006): 1 661 912 dok., 1 379 007 641 tokenów v6.
- V: filtered vs raw: math.SE 98,5% dok. (≈99,5% tokenów), mathoverflow 158 923 dok. / 178 260 937 tok. (99,4% /
  99,3%), matheducators 100%, mathematica 97,7% dok. Filtr niemal nic nie usuwa w matematyce.
- Rdzeń (5 serwisów) przed dedupem: ~1 588 mln tokenów v6; z rozszerzeniem zalecanym (+4): ~1 841 mln; z opcjami (+2): ~1 890 mln.

## 5. Ryzyka

- Nakładanie z już zbudowanymi źródłami (V, po znormalizowanym `(serwis, id pytania)` z URL `/questions/<n>`, `/q/<n>`,
  `/feeds/question/<n>`; flagi z `powody.npz` przebiegów FineMath-4+ cz. 2 i InfiWebMath-4+, waga = znaki SE):

  | serwis | pytania w eksporcie FM-4+ ∪ Infi-4+ | dok. / znaki SE | + flagi `dedup_slayer107` / `fineweb_edu_109` | do usunięcia: dok. / znaki |
  |---|---|---|---|---|
  | math.SE (cały) | 255 139 dok. | 15,1% / 20,3% | +9 386 dok. | 264 525 / 21,1% |
  | mathoverflow | 13 850 | 8,7% / 11,3% | 0,56% / 0,09% zn. | 14 313 / 11,8% |
  | cstheory | 1 306 | 9,9% / 11,8% | 0,44% / 0,09% | 12,2% zn. |
  | proofassistants | 79 | 6,8% zn. | 0,06% / 0 | 6,9% zn. |
  | matheducators | 965 | 29,5% zn. | 0,98% / 3,68% | 31,4% zn. |
  | stats | 20 124 | 12,4% zn. | 0,41% / 0,23% | 12,9% zn. |
  | cs | 11 803 | 28,0% zn. | 0,90% / 0,96% | 29,3% zn. |
  | or / scicomp / quant / crypto | — | 16,2 / 18,9 / 13,3 / 8,8% zn. | — | 16,8 / 19,7 / 13,7 / 9,2% zn. |

  V: w puli FineMath-4+ jest 250 449 różnych pytań math.SE (281 016 wierszy), w eksporcie 238 331 (279 256 092 tok. v6
  stron www); InfiWebMath-4+ eksport: 20 487 pytań. V: 98,8% pytań math.SE z eksportu FM-4+ ∪ Infi-4+ o id ≤ 882 946
  ma dokument w zrzucie (91 124 z 92 269); mathoverflow 98,0%. Strony www są starsze i z resztkami nawigacji, więc
  dokument SE jest czystszy (I). Alternatywa: zostawić SE, a z eksportu FM-4+ usunąć strony SE (eksport już wysłany).
- Slayer 1.07 / open-web-math: V (karta `SlayerLab/minimal-en-corpus-5b@bb3aec23`, `manifests/mixture.json`): korpus
  ma 86 717 dok. open-web-math, 152 782 FineMath i osobne źródło „stackexchange” (746 732 dok., 447 mln tok.). Karta
  1.07 (`slayer-1.07-pretrain@6a337bbf`) opisuje `en_mix` (1 249 258 dok.) jako FineWeb-Edu, FineMath, open-web-math
  i DCLM, bez StackExchange. I: górna granica dla math.SE w `en_mix` przez OWM: 86 717 × 18% (notatka zespołu) ≈ 15,6 tys.
  stron SE wszystkich serwisów; przez FineMath 152 782 × ~4% ≈ 6 tys.; razem ≤ ~1–1,3% pytań math.SE. Zgodne
  z pomiarem V: `dedup_slayer107` zaznaczył 7 600 pytań math.SE w pulach FM-4+/Infi-4+ i 1,19% znaków w plikach
  00000+00006. Czy pakiet `en_mix` naprawdę nie ma źródła stackexchange z minimal-en: NIE SPRAWDZONE na tokenach.
- Tekst z modeli (warunek 1): I: odpowiedzi po 30.11.2022 mogą zawierać tekst ChatGPT mimo zakazów SE. Mamy tylko datę
  pytania. V: udział dokumentów z `created` ≥ 2022-12-01: mathoverflow 12,6% dok. / 11,0% zn., stats 11,5% zn.,
  cstheory 6,9% zn., proofassistants 54% zn.; math.SE ~9% dok. (I: pliki 00001–00005 mają 140 952 dok. z lat
  2023–2024 + część 2022). Odcięcie po dacie pytania nie wyłapie nowych odpowiedzi do starych pytań.
- PII: V e-mail (regex) w math.SE 0,05% dok., mathoverflow 0,22%, mathematica 0,55%, reszta ≤ 0,4%. Nicki: `@nick`
  w treści, nazwy wyświetlane i profile w `authors` (dane osobowe pod pseudonimem, publiczne). Redakcja PII w wersji
  filtered psuje liczby: V w pierwszych 89 321 wierszach pliku 0005 12 z 14 pierwszych trafień `<PHONE_NUMBER>`
  / `<IP_ADDRESS>` to liczby lub numery wzorów (np. „$<PHONE_NUMBER> \bmod 2^5$”, „π(10^12) is<PHONE_NUMBER>8”);
  dotyczy ~0,5% dok. math.SE i 1,4% mathoverflow. Wniosek: brać raw i własne reguły PII. Uwaga: reguły telefon/IP
  w naszym detektorze (DCLM) też trafią w długie liczby; fałszywe odrzucenia zmierzyć na tym źródle.
- Kontaminacja: I math.SE ma pytania z zadań MATH, GSM8K, MMLU i podręczników (uczniowie wklejają zadania); twórcy nie
  dekontaminowali. 13-gramy wobec testów Fabryki obowiązkowe (w FM-4+ `ewal_13gram` zabrał 2,8% tokenów).
- Kopie wewnątrz SE: pytania przenoszone między serwisami (math.SE ↔ mathoverflow) i duplikaty pytań: NIE ZMIERZONE
  (I: mało; MinHash wewnątrz).
- Licencja `'None'` (sekcja 2): ~4,7% tokenów math.SE (I: 90% znaków pliku 00006).

## 6. Nowość

- V (karty 1.07, 1.09, rejestr `slayer-pl-8x3b` → `en` = fineweb-edu + finemath): Stack Exchange jako osobne źródło
  nie występuje w historii Slayera. Pośrednio strony SE są w FineMath, open-web-math, DCLM i FineWeb-Edu (wyżej:
  ~1–2% znaków).
- V: najwięcej nakładania jest z naszym własnym eksportem FineMath-4+: 20% znaków math.SE. Reszta, ok. 79% znaków
  math.SE i 88% mathoverflow, jest nowa po dedupie URL.
- Szacunek po dedupie URL (V udziały × tokeny z tab. 4):

  | zestaw | tokeny v6 po dedupie URL | szacunek po kaskadzie (I, ×0,85–0,95: 13-gramy, MinHash wobec stron-kopii SE, PII, min. treść) |
  |---|---|---|
  | rdzeń: math.SE 1 093 + mathoverflow 158 + cstheory 11,7 + matheducators 5,5 + proofassistants 1,5 | ~1 270 mln | ~1,08–1,21 mld |
  | + stats 170 + cs 28 + scicomp 10 + or 3,9 | ~1 483 mln | ~1,26–1,41 mld |
  | + quant 15,8 + crypto 27,7 | ~1 527 mln | ~1,30–1,45 mld |
  | odrzucone: physics 194, mathematica 105, puzzling 23 | (322 mln) | — |

  I: bez dokumentów z `'None'` w `all_licenses` −~4% rdzenia. Z odcięciem pytań od 2022-12-01 jeszcze ~−8%.
  Wtedy rdzeń to ~0,95–1,1 mld.

## Nie sprawdzone

- Prawdziwy robots.txt dla zwykłych crawlerów (nasz klient dostał HTTP 418 z `ai-train=no`, `Disallow: /`); TDMRep
  (`/.well-known/tdmrep.json` 404), ai.txt (404) — sprawdzone tylko dla math.SE.
- Co znaczy `'None'` w `all_licenses` (który post, komentarz czy odpowiedź) i czy kod common-pile przypisuje licencje
  komentarzom.
- Tokeny v6 math.SE plików 00001–00005 (ekstrapolacja ze znaków; kontrola: wersja filtered zmierzona w całości daje 1,379 mld).
- Nakładanie treści (MinHash/13-gram) z FM-4+, Infi-4+, en_mix 1.07 i FineWeb-Edu 1.09, w tym strony-kopie SE na innych
  domenach; tu tylko nakładanie po id pytania.
- Nakładanie z FineMath-3+ i innymi źródłami #346 w budowie (CraneMath, Stack-Edu Python: I, pomijalne).
- Czy `en_mix` 1.07 zawiera źródło „stackexchange” z minimal-en-corpus-5b (karta mówi, że nie).
- Udział tekstu z modeli w odpowiedziach po 2022-11 (brak dat postów; tylko data pytania).
- Ręczna próbka szersza niż 15 dok. i drugi czytelnik; serwisy rozszerzenia nie czytane.
- Kontaminacja testami Fabryki (13-gramy) i fałszywe odrzucenia reguł PII telefon/IP na liczbach.
- Duplikaty i przeniesienia pytań między serwisami.
