# Dziennik zbioru: DCLM-baseline 1.0 EN

Przepis: [`METODOLOGIA.md` w repo zespołu](https://github.com/slayerlabs/benchmarks-fabryka-ai/blob/main/research/slayer-1b/dane/METODOLOGIA.md). Tu wynik każdego kroku tego zbioru: data, komenda, kod
wyjścia, liczby, link. Karta źródła: [`KARTA_ZRODLA.md`](KARTA_ZRODLA.md). Do 15.11.2026 plik nazywał się
`METODOLOGIA.md` (tak odsyłają do niego `skrypty/preregistracja.json` i starsze commity).

## Bramki praw

| bramka | wynik |
|---|---|
| Można TRENOWAĆ | TAK (wyjątek TDM, takedown po `url`/`id`) |
| Można ZGŁOSIĆ do `dataset-team-submissions` | **NIEROZSTRZYGNIĘTY**: CC-BY-4.0 dotyczy kompilacji, teksty z Common Crawl bez licencji per dokument; decyduje Ania |

## 1. Rezerwacja

| | DCLM-EN |
|---|---|
| Co | issue [#197](https://github.com/slayerlabs/benchmarks-fabryka-ai/issues/197); cel ≥5 mld tokenów v6 pod HellaSwag, PIQA, ARC-C, WinoGrande |
| Sprawdzenie | `open`; wiersz 2026-11-14 „w budowie” istnieje |

## 2. Karta źródła i bramka praw

| | DCLM-EN |
|---|---|
| Co | [`KARTA_ZRODLA.md`](KARTA_ZRODLA.md), 14.11.2026 |
| Prawa | CC-BY-4.0 kompilacji; teksty Common Crawl; karta: „research use only”; opt-out TDM: NIE SPRAWDZONE |
| Sprawdzenie | trenować: TAK; zgłosić: NIEROZSTRZYGNIĘTY |
| Pułapki | DCLM jest już w EN 1.07 (`minimal-en-corpus-5b`, 577 998 dok.) |

## 3. Preregistracja

| | DCLM-EN |
|---|---|
| Co | [`skrypty/preregistracja.json`](skrypty/preregistracja.json): seed 20261114, 8 powodów w kaskadzie |
| Sprawdzenie | zmiana 15→8 plików FWE dopisana przed wynikiem FWE |

## 4. Środowisko

| | DCLM-EN |
|---|---|
| Co | Python 3.12.2; od 14.11 także `torch==2.15.0`, `transformers==5.23.0` (krok `edu`, 4 wątki CPU) |

## 5. Pobranie z rewizją i sumą

| | DCLM-EN |
|---|---|
| Co | `odtworz.sh tokenizer`, `probka`, `testy`, `baza107`, `walidacja_pobierz` |
| Źródła | DCLM `mlfoundations/dclm-baseline-1.0-parquet@817d6752…`; tokenizer v6 sha `0640d3bd…`; EN 1.07 `SlayerLab/slayer-1.07-pretrain@6a337bbf`; walidacje `minimal-en-corpus-5b@bb3aec23`, `minimal-en-corpus-2b-v2@ef0ab069` |
| Pułapki | wykluczone 31 plików ([`skrypty/wykluczone.json`](skrypty/wykluczone.json)) |

## 6. Indeksy i kontrole

| | DCLM-EN |
|---|---|
| Co | `odtworz.sh ewal`, `idx107`, `idx_wal`, `idx_ivme`, `kontrola` |
| Sprawdzenie | `ewal`: `ogolem 32411348`; `idx107`: 3 278 603 dok., 158 680 048 próbek; `idx_wal` = [`wyniki/indeks_walidacja.json`](wyniki/indeks_walidacja.json) bajt w bajt; `idx_ivme` = [`wyniki/indeks_ivme.json`](wyniki/indeks_ivme.json); kontrola: 14/14 wg [`wyniki/kontrole_dodatnie.json`](wyniki/kontrole_dodatnie.json) |
| Pułapki | brak w zakresie: segmenty c01–c10 i gold (niedostępne) |

## 7. Przebieg

| | DCLM-EN |
|---|---|
| Co | `odtworz.sh przebieg`, 6 procesów, `nice -n 10` |
| Sprawdzenie | 216/216 `u_*.npz`, `KONIEC 1570s`, 14.11.2026 |

## 8. Po przebiegu

| | DCLM-EN |
|---|---|
| Co | `odtworz.sh fwe_url` (8 plików FWE), `edu` (50 000 dok., cpu float32), `agreguj` |
| Sprawdzenie | 14-15.11.2026: **`fwe_url`** kod 0, 2765 s, szczyt RSS 837 MB; 8/8 plików, 4 829 900 wierszy (0,317% z 1 525 223 056 wierszy FWE), 4 748 572 unikalnych url ([`wyniki/fwe_url.json`](wyniki/fwe_url.json)). **`edu`** kod 0, 5414 s, szczyt RSS 7318 MB, cpu float32, **4 wątki** (`EDU_WATKI`, `OMP_NUM_THREADS`, `torch.set_num_threads`), `KONIEC 50000`; int_score 0-5: 2608 / 24 007 / 15 931 / 6270 / 1180 / 4; próg ≥2 = 49,52% tokenów, ≥3 = 15,79%. **`agreguj`** kod 0, 30 s (RSS niezmierzony: krótszy niż okres próbki 30 s); 1 051 235 dok., 1 470 704 495 tokenów v6; kaskada 376 + 6738 + 2611 + 29 333 + 2279 + 3679 + 11 741 + 1895 = 58 652 odrzuconych, suma z zachowanymi = dokumenty próbki; **zostaje 992 583 dok. (94,42%), 1 345 901 642 tokenów v6 (91,51%)** (stan przed aneksem 15.11; po aneksie 993 878 dok., 1 352 267 245 tokenów v6, sekcja „Aneks do preregistracji”; aneks 2 cofnięty aneksem 3, stan końcowy = stan po aneksie 1: 993 878 dok., 1 352 267 245 tokenów v6, 37 shardów (33-43), sekcja „Aneks 3”); `niedostepne` puste; FWE url: 7826 trafień (0,74%); szacunek do 5 mld v6: 38 shardów (34-43) z 27 838, dolna granica ([`wyniki/agreguj.json`](wyniki/agreguj.json)); ręczna próbka 200 wierszy w `robocze/wyniki/probki_reczne.jsonl`, oceniona 15.11.2026: **NIE PRZESZŁO** (sekcja „Ręczny przegląd próbki” niżej) |

## Ręczny przegląd próbki

Data 15.11.2026, recenzent: agent niezależny (nie budował zbioru). Próbka: `robocze/wyniki/probki_reczne.jsonl`
(100 zachowanych + 100 odrzuconych, rng 20261114, powód = pierwszy w kaskadzie). Ocena per dokument:
`robocze/przeglad_probki.json` (zostaje w `robocze/`, bo opisuje dokumenty z PII; wartości PII nie są w nim zapisane).

Metoda: odczyt 1500 znaków każdego dokumentu. Dla `pii` i `mojibake` pełny tekst z `robocze/pobrania/dclm`
(dopasowanie po `url` i zgodności 1500 znaków, 200/200 znalezione), klasa i kontekst trafienia z zamaskowaną
wartością. Dla `ewal_13gram` odtworzone trafiające 13-gramy z `robocze/wyniki/ewal/*__13.npy` funkcjami `rdzen.py`.
Zachowane przeskanowane w pełnym tekście także poszerzonymi wzorcami PII (e-mail zaciemniony, adres ulicy,
telefon bez myślników): 0 trafień. Przedziały: Wilson 95%.

**Fałszywe odrzucenia** (dobry tekst odrzucony), osobno dla każdego powodu:

| Powód | n w próbce | Wynik | Stopa [Wilson 95%] | Brakuje do 100 odrzuconych |
|---|---|---|---|---|
| `pii`: trafienie nie jest e-mailem/telefonem/IP | 53 | 0 | 0,0% [0,0; 6,8] | 47 |
| `pii`: dobry tekst, trafienie to kontakt firmy lub instytucji, bez osoby prywatnej | 53 | 29 | **54,7% [41,5; 67,3]** | 47 |
| `ewal_13gram` | 5 | 4 (+1 wątpliwy) | **80,0% [37,6; 96,4]** | 95 |
| `domena_testow` (wg reguły) | 9 | 0 | 0,0% [0,0; 29,9] | 91 |
| `mojibake` | 2 | 0 | 0,0% [0,0; 65,8] | 98 |
| `dedup_wewnatrz` | 10 | 2 sprawdzone słuszne (identyczny szablon w próbce), 8 NOT RUN | — | 90 |
| `dedup_slayer107` | 15 | NOT RUN (wymaga indeksu i pary dopasowania) | — | 85 |
| `dedup_ivme` | 4 | NOT RUN | — | 96 |
| `walidacja_fabryki` | 2 | NOT RUN | — | 98 |

Trafienia `ewal_13gram` to powszechne cytaty i ciągi, nie przeciek pytań: tytuł „Wealth of Nations” (TriviaQA),
ciąg „1 2 3 … 13” (MATH, HumanEval, MBPP, LLMzSzŁ), tekst II poprawki USA (BoolQ, ReCoRD), wers Emmy Lazarus
(TriviaQA); piąty to zdanie prasowe z ReCoRD cytowane w blogu (wątpliwy). Żadne nie dotyczy HellaSwag, PIQA,
ARC-C ani WinoGrande. `pii`: 21 z 53 to kontakt przypisany osobie (słusznie), 3 to spam/SEO (odrzucenie słuszne
z innego powodu), 29 to dobry tekst z telefonem lub adresem e-mail firmy, urzędu, policji, uczelni.

**Przeoczenia** (100 zachowanych; jedna próbka zachowanych dla wszystkich powodów):

| Kategoria | Wynik | Stopa [Wilson 95%] |
|---|---|---|
| PII w zakresie detektora (e-mail, telefon, IP) i poszerzone wzorce | 0 | 0,0% [0,0; 3,7] |
| `mojibake` (2 dopasowania, poniżej progu 3) | 1 | 1,0% [0,2; 5,4] |
| `domena_testow` wg reguły | 0 | 0,0% [0,0; 3,7] |
| `domena_testow` wg uzasadnienia (wikisource.org, projekt Wikimedia spoza listy) | 1 | 1,0% [0,2; 5,4] |
| `ewal_13gram`, dedupy, walidacja | NOT RUN: z tekstu nie da się ocenić, wymaga indeksu | — |
| śmieci poza zakresem filtrów: spam/SEO, tekst maszynowy (spinning), zepsute tłumaczenie z wtrętami nie-EN | 5 (+3 wątpliwe) | 5,0% [2,2; 11,2]; z wątpliwymi 8,0% [4,1; 15,0] |

Treści testów, boilerplate'u bez treści ani dokumentów w całości nie-EN wśród zachowanych nie znaleziono.

**Werdykt wobec preregistracji: NIE PRZESZŁO.**

1. Preregistracja (`reczna_probka`) i notatka `komplet-kontroli-zbioru` §6 wymagają 100 zachowanych i 100
   odrzuconych przy KAŻDYM powodzie; jest 100/100 łącznie. Do dobrania: **700 odrzuconych** (walidacja_fabryki 98,
   domena_testow 91, ewal_13gram 95, pii 47, mojibake 98, dedup_wewnatrz 90, dedup_slayer107 85, dedup_ivme 96),
   losowanych w widoku niezależnym (dokument z danym powodem, nie tylko pierwszym w kaskadzie); zachowanych 0,
   jeśli jedna próbka 100 zachowanych liczy się dla wszystkich powodów, inaczej 700. Dla dedupów i walidacji
   próbka musi pokazywać parę dopasowania, bez niej ocena zostaje NOT RUN.
2. Ani preregistracja, ani notatka nie podają progu stopy przeoczeń i fałszywych odrzuceń, więc PASS nie da się
   ogłosić nawet przy pełnej próbce. Próg trzeba dopisać do preregistracji PRZED doborem próbki.
3. `ewal_13gram` odrzuca dobre teksty na powszechnych cytatach (4/5); reguła „każde trafienie usuwa” wymaga
   decyzji (np. lista dozwolonych ciągów albo próg liczby trafień) przed eksportem. `pii` usuwa 29/53 dobrych
   tekstów z kontaktem firmowym; w kroku 9 repo zgłoszeń i tak maskuje PII, więc to decyzja o zakresie usuwania.

### Aneks do preregistracji, 15.11.2026 (przed drugą próbką)

Zapisany w [`skrypty/preregistracja.json`](skrypty/preregistracja.json), pole `aneks_2026_11_15`, PO pierwszym
przeglądzie i PRZED doborem drugiej próbki. Powód: trzy punkty werdyktu wyżej.

**Progi.** Notatka `komplet-kontroli-zbioru` i `zasady-raportowania-benchmarkow` progów stóp ręcznej próbki nie
podają (sprawdzone 15.11.2026), więc obowiązują progi tego aneksu:

| Miara | Próg |
|---|---|
| fałszywe odrzucenia, KAŻDY powód osobno (dokument nie ma cechy, którą opisuje powód) | ≤10% i górna granica Wilsona 95% ≤20% |
| przeoczenia PII w 100 zachowanych (e-mail, telefon, IP) | ≤1% |
| śmieci bez filtra w 100 zachowanych (ocena „nie”; wątpliwe obok) | ≤10% |
| przeoczenia `mojibake` i `domena_testow` w 100 zachowanych | ≤10% każdy |
| przeoczenia `ewal_13gram`, dedupów, walidacji | z tekstu nieocenialne: mierzy kontrola dodatnia |

NOT RUN albo BLOCKED przy którymkolwiek powodzie to brak PASS.

**PII: reguła bez zmian, świadomy koszt.** Dokument z e-mailem, telefonem albo IP odpada w całości, także z
kontaktem firmy lub instytucji, jak w wersjach 1.08 i 1.09. W pierwszym przeglądzie 29 z 53 odrzuceń `pii`
(54,7% [41,5; 67,3]) to dobre teksty z kontaktem firmowym: ten koszt jest przyjęty, nie liczy się jako fałszywe
odrzucenie i jest raportowany osobno.

**`ewal_13gram`: wykluczenie 13-gramów powszechnych.** Krok `ewal_czeste` ([`skrypty/ewal_czeste.py`](skrypty/ewal_czeste.py))
odtwarza trafiające 13-gramy 2821 dokumentów z trafieniem i liczy, w ilu dokumentach próbki występuje każdy z
33 823 n-gramów. Najczęstsze: ciągi `1 2 3 … 13` i alfabet (df do 312), II poprawka USA (80), I poprawka (67),
Deklaracja Niepodległości (56), formułka trynitarna (44), szablon spisu ludności z Wikipedii (55), notka copyright
(38), wiersz Emmy Lazarus (33). Reguła: z indeksu wypada 13-gram o **df ≥ 5** dokumentów próbki albo **trywialny**
(każde słowo to liczba lub pojedynczy znak); dokument odpada, gdy ma choć jedno trafienie spoza listy. Lista
budowana raz z próbki głównej: [`skrypty/ewal_13gram_wykluczone.json`](skrypty/ewal_13gram_wykluczone.json).
Próg 5: wszystkie n-gramy HellaSwag z df ≥ 5 to cytaty liturgiczne i biblijne, PIQA, ARC-C i WinoGrande nie mają
n-gramu z df ≥ 2; 339 nietrywialnych n-gramów z df ≥ 5 przejrzanych ręcznie, same cytaty i formułki. Ryzyko:
treść testu skopiowana w ≥5 dokumentach próbki przestaje być łapana 13-gramem.

**Druga próbka.** `default_rng(20261115)`, 100 dokumentów na KAŻDY powód w widoku niezależnym (wszystkie, gdy
powód ma <100) plus 100 zachowanych wspólnych dla wszystkich powodów; dedupy i walidacja z parą dopasowania.

**Przeliczenie po aneksie (15.11.2026).**

| Krok | Wynik |
|---|---|
| `ewal_czeste` (kod 0, 30 s) | lista 1285 wykluczonych 13-gramów (394 z df ≥ 5, w tym 55 trywialnych, + 891 trywialnych z df < 5); z 2821 dokumentów z trafieniem odpada nadal **1344** (15 098 522 → 7 071 298 tokenów v6) |
| kontrola dodatnia, wstawione (`ewal_czeste` na `kontrola/przebieg`) | K_hellaswag, K_piqa, K_arc_c, K_winogrande: `ewal_13gram` przed i po zmianie; pozostałe 10 bez zmian (4/4 + 10/10) |
| kontrola dodatnia, prawdziwe dokumenty próbki | trafienie PIQA: 4/4 nadal odpada; ARC-C: 2/2; WinoGrande: brak dokumentów z trafieniem (0/0); HellaSwag: 84/129 nadal odpada, 45 trafiało wyłącznie n-gramami z listy (formułka trynitarna, 1 P 3,15 i inne cytaty) |
| `agreguj` (kod 0, 30 s) | kaskada `ewal_13gram` 2611 → 1224 dok.; **zostaje 993 878 dok. (94,544%), 1 352 267 245 tokenów v6 (91,947%)**, czyli +1295 dok. i **+6 365 603 tokeny v6** wobec 992 583 / 1 345 901 642; szacunek do 5 mld v6: 37 shardów (33-43) ([`wyniki/agreguj.json`](wyniki/agreguj.json), pole `ewal_13gram_aneks`) |
| `probka_przegladu` (kod 0, ok. 3 min, szczyt RSS ok. 11 GB) | 900 dokumentów w `robocze/probka_przegladu_2.jsonl`: po 100 na każdy z 8 powodów (każdy ma ≥100 w całej próbce: walidacja 376, domena 6746, ewal 1344, pii 29 482, mojibake 2424, dedup_wewnatrz 3819, dedup_slayer107 12 931, dedup_ivme 3509) + 100 zachowanych; pary znalezione 400/400 ([`skrypty/probka_przegladu.py`](skrypty/probka_przegladu.py): walidacja z tekstów indeksu, 1.07 i Ivme skanem okien 12 tokenów) |

### Drugi przegląd, 15.11.2026: wynik

Recenzenci: trzech niezależnych agentów (nie budowali zbioru), każdy na 300 dokumentach z `robocze/probka_przegladu_2.jsonl`
według jednej instrukcji (`robocze/instrukcja_przegladu_2.md`). Progi aneksu czytali dopiero po policzeniu stóp. Ocena
per dokument: `robocze/przeglad_probki_2_{a,b,c}.json` (bez wartości PII). Przedziały: Wilson 95%.

| Powód | n | Fałszywe odrzucenia | Stopa [Wilson 95%] | Wątpliwe | Dobry tekst usunięty | Werdykt |
|---|---|---|---|---|---|---|
| `walidacja_fabryki` | 100 | 3 | 3,0% [1,0; 8,5] | 22 (strony z szablonu z innymi danymi; z nimi 25,0% [17,6; 34,3]) | 34 | PASS |
| `domena_testow` | 100 | 0 | 0,0% [0,0; 3,7] | 0 | 97 | PASS |
| `ewal_13gram` | 100 | **51** | **51,0% [41,4; 60,6]** | 15 | 87 (45 dobrych z nietrafnym powodem) | **FAIL** |
| `pii` | 100 | 4 | 4,0% [1,6; 9,8] | 3 | 85 (kontakt: osoba 42, firma/instytucja 50, inne 8) | PASS |
| `mojibake` | 100 | 0 | 0,0% [0,0; 3,7] | 1 | 49 | PASS |
| `dedup_wewnatrz` | 100 | 0 | 0,0% [0,0; 3,7] | 0 | 74 | PASS |
| `dedup_slayer107` | 100 | 4 | 4,0% [1,6; 9,8] | 9 (z nimi 13,0% [7,8; 21,0]) | 73 | PASS |
| `dedup_ivme` | 100 | 4 | 4,0% [1,6; 9,8] | 12 (z nimi 16,0% [10,1; 24,4]) | 46 | PASS |

| Zachowane (100) | Wynik | Stopa [Wilson 95%] | Próg | Werdykt |
|---|---|---|---|---|
| przeoczenia PII | 0 | 0,0% [0,0; 3,7] | ≤1% | PASS |
| przeoczenia `mojibake` | 1 | 1,0% [0,2; 5,5] | ≤10% | PASS |
| przeoczenia `domena_testow` | 0 | 0,0% [0,0; 3,7] | ≤10% | PASS |
| śmieci (ocena „nie”) | 5 | 5,0% [2,2; 11,2]; z 14 wątpliwymi 19,0% [12,5; 27,8] | ≤10% | PASS |

**Werdykt wobec aneksu: NIE PRZESZŁO** — `ewal_13gram` ma 51% fałszywych odrzuceń przy progu 10%. Po wykluczeniu
n-gramów z df ≥ 5 filtr nadal odrzuca na cytatach i formułkach z df 1-4: Patrick Henry, Churchill, M. L. King,
„Wielki Gatsby”, Manifest komunistyczny, preambuła i klauzule Konstytucji USA, art. 5 NATO, tytuły („Harry Potter
and the…”), frazy typu „leading cause of death for both men and women”. Trafień prawdziwych ok. 34 na 100 (wklejona
Wikipedia/OpenStax, artykuły CNN z ReCoRD, RACE, wikiHow pod HellaSwag, quiz TriviaQA). Progu df nie zmieniam po
tym wyniku: dobór progu pod wynik przeglądu to próg dobrany po zobaczeniu danych. Następna zmiana reguły
`ewal_13gram` wymaga nowego aneksu i trzeciej, świeżej próbki tego powodu. Pozostałe 7 powodów i zachowane
przechodzą. Uwagi recenzentów: `walidacja_fabryki` ma 22 wątpliwe pary (strony z jednego szablonu, np. Ancestry, grouply,
z innymi danymi); śmieci z wątpliwymi w zachowanych to 19%; recenzent `pii` widział e-maile zamaskowane przez hook sesji
(`[REDACTED:email]`) i oceniał je po kontekście.

Zastrzeżenia, które mogą zmienić werdykt (do rozstrzygnięcia w aneksie przed kolejną próbką):

- **Definicja kopii przy dedupach.** Recenzent dedupów liczył stronę bez własnej treści, różniącą się od pary tylko
  podstawioną nazwą lub numerem (regulamin phpBB z inną nazwą forum, ogłoszenie z inną dzielnicą), jako bliską kopię.
  Przy ostrzejszym czytaniu („nie tylko wspólny szablon”) `dedup_slayer107` ma 12% [7,0; 19,8], a `dedup_ivme` 22%
  [15,0; 31,1], czyli oba FAIL. Recenzent `walidacja_fabryki` zaliczył takie strony do wątpliwych (22).
- **PII w zachowanych.** Próg ≤1% jest spełniony stopą punktową (0/100), ale górna granica Wilsona to 3,7%: n = 100
  nie wykazuje stopy ≤1% statystycznie.
- Zachowane długie dokumenty (28 ponad 5000 znaków) recenzent przeczytał na początku i końcu, PII w środku sprawdził
  wzorcami.

### Aneks 2 do preregistracji, 15.11.2026 (przed trzecią próbką)

Zapisany w [`skrypty/preregistracja.json`](skrypty/preregistracja.json), pole `aneks_2026_11_15b`, PO drugim
przeglądzie (1e5a152, 430703d) i PRZED budową indeksu wspólnego z FWE, przeliczeniem i trzecią próbką. Powód:
`ewal_13gram` nie przeszedł, a trzy zastrzeżenia wyżej mogły zmienić werdykt. Rozstrzygnięcia:

1. **Kopia w dedupach.** Strona różniąca się od pary tylko podmienioną nazwą, liczbą albo inną wartością w tym samym
   szablonie (regulamin phpBB, ogłoszenie z inną dzielnicą) to KOPIA. Taką definicję realizuje MinHash ≥ 0,8, a
   FineWeb traktuje szablony jako duplikaty. Werdykty `dedup_*` i `walidacja_fabryki` z drugiego przeglądu zostają
   (fałszywe odrzucenia 0-4%).
2. **Przeoczenia PII.** Próg ≤1% wymaga wykazania górnej granicy. Reguła trzech: 0 trafień na n = 300 daje górną
   granicę ok. 1% (Clopper-Pearson, jednostronnie 95%: 0,994%). Dobór 200 nowych zachowanych (do 100 z drugiego
   przeglądu), tylko do kontroli PII, ocenia niezależny recenzent. PASS tylko przy 0/300.
3. **`ewal_13gram`: wspólne z niezależnym korpusem sieciowym.** Zamiast progu df (który dostroiłby się do wyniku
   przeglądu) z indeksu wypada 13-gram testu obecny choć raz w próbce FineWeb-Edu z kroku `fwe_url` (8 plików,
   4 829 900 wierszy, rewizja `87f09149…`): fragment obecny w sieci niezależnie od testu nie świadczy o
   zanieczyszczeniu. Reguła z aneksu 1 (df ≥ 5 i ciągi) zostaje jako dodatkowa; dokument odpada przy trafieniu spoza
   sumy obu list. Ryzyko: kopia testu z Common Crawl obecna i w DCLM, i w FWE przestaje być łapana; mierzy to kontrola
   dodatnia (4 wstawione dokumenty i prawdziwe trafienia PIQA, ARC-C, WinoGrande, HellaSwag).

**Trzecia próbka.** `default_rng(2026111502)`: 100 dokumentów `ewal_13gram` po zmianie (wszystkie, gdy jest ich mniej)
plus 200 nowych zachowanych do PII. Progi bez zmian (fałszywe odrzucenia ≤10%, górna granica Wilsona ≤20%). Jeśli
`ewal_13gram` znów nie przejdzie, reguły nie stroi się dalej w tym przebiegu: wynik zostaje otwarty.

**Przeliczenie po aneksie 2 (15.11.2026).**

| Krok | Wynik |
|---|---|
| `ewal_fwe` ([`skrypty/ewal_wspolne_z_fwe.py`](skrypty/ewal_wspolne_z_fwe.py); kod 0, 1835 s, w tym pobranie 8 plików FWE ok. 14 GB do `robocze/pobrania/fwe`, liczenie 248 s na 6 procesach, szczyt RSS 6598 MB) | 4 829 900/4 829 900 wierszy FWE, strumieniowo po 4834 grupach wierszy; 21 714 dokumentów FWE z trafieniem; **243 317 z 32 411 348 13-gramów testów występuje w FWE** (HellaSwag 5954 z 3 208 403, PIQA 409 z 134 393, ARC-C 109 z 40 190, WinoGrande 0 z 50 713) ([`wyniki/ewal_wspolne_fwe.json`](wyniki/ewal_wspolne_fwe.json)); lista zamrożona w [`skrypty/ewal_13gram_wspolne_fwe.npz`](skrypty/ewal_13gram_wspolne_fwe.npz) |
| `ewal_czeste_fwe` (kod 0, 90 s) | suma list 243 881 13-gramów, z tego 13 377 trafiających w próbkę; z 2821 dokumentów z trafieniem odpada nadal **750** (aneks 1: 1344), 3 579 936 tokenów v6 ([`wyniki/ewal_13gram_aneks2.json`](wyniki/ewal_13gram_aneks2.json): per test dokumenty z trafieniem i ile nadal odpada) |
| kontrola dodatnia, wstawione | K_hellaswag, K_piqa, K_arc_c, K_winogrande: `ewal_13gram` przed i po zmianie; pozostałe 10 bez zmian (4/4 + 10/10) |
| kontrola dodatnia, prawdziwe dokumenty próbki | PIQA 4/4 nadal odpada (aneks 1: 4/4); **ARC-C 0/2** (aneks 1: 2/2; oba trafienia ARC-C są w FWE); WinoGrande 0/0; HellaSwag 61/129 (aneks 1: 84/129) |
| 100 dokumentów `ewal_13gram` z drugiego przeglądu (oceny recenzenta b) | z 34 trafnych nadal odpada 21, **13 trafnych przestaje odpadać**; z 51 fałszywych nadal odpada 20; z 15 wątpliwych 11 |
| `agreguj` (kod 0, 30 s) | kaskada `ewal_13gram` 1224 → 665 dok.; **zostaje 994 398 dok. (94,593%), 1 355 128 923 tokenów v6 (92,141%)**, czyli +520 dok. i **+2 861 678 tokenów v6** wobec aneksu 1 (993 878 / 1 352 267 245); szacunek do 5 mld v6 bez zmian: 37 shardów (33-43) ([`wyniki/agreguj.json`](wyniki/agreguj.json)) |
| `probka_przegladu_3` ([`skrypty/probka_przegladu_3.py`](skrypty/probka_przegladu_3.py), kod 0, 30 s), wylosowana po commicie aneksu 93ca7ff | `robocze/probka_przegladu_3.jsonl`: 100 z 750 dokumentów `ewal_13gram` + 200 z 994 298 zachowanych (bez 100 z drugiego przeglądu) |

### Trzeci przegląd, 15.11.2026: wynik

Recenzenci: dwóch niezależnych agentów (nie budowali zbioru), instrukcja `robocze/instrukcja_przegladu_3.md`,
progi czytane po policzeniu stóp. Oceny per dokument: `robocze/przeglad_probki_3_{d,e}.json` (bez wartości PII). Wilson 95%.

| Miara | n | Wynik | Stopa [Wilson 95%] | Próg | Werdykt |
|---|---|---|---|---|---|
| `ewal_13gram`: fałszywe odrzucenia | 100 | 28 (+17 wątpliwych) | **28,0% [20,1; 37,5]**; z wątpliwymi 45,0% [35,6; 54,8] | ≤10%, górna ≤20% | **FAIL** |
| przeoczenia PII w zachowanych (200 nowych + 100 z drugiego przeglądu) | 300 | 0 (+1 wątpliwy) | 0,0% [0,0; 1,26]; Clopper-Pearson jednostronnie 0,994% | 0/300 | **PASS** |

`ewal_13gram`: `do_treningu` tak 80, wątpliwe 16, nie 4. Spadek z 51% do 28% nie wystarcza; nawet dolna granica (20,1%) jest
powyżej progu. PII: wątpliwy to archiwum listy mailingowej (winehq.org) z samymi loginami „login at” bez domeny, czyli bez
adresu w zakresie detektora; uznany za trafienie dałby 1/300 i górną granicę 1,57% (FAIL). 147 z 200 dokumentów
przeczytanych w całości, 53 dłuższe sprawdzone wzorcami na całym tekście plus początek i koniec ręcznie.

**Werdykt: `ewal_13gram` NIE PRZESZEDŁ — OTWARTE.** Zgodnie z aneksem 2 reguły nie stroi się dalej w tym przebiegu.
Kategorie błędnych odrzuceń (cytaty i frazy rzadkie w FWE, bo próbka FWE to 0,32% korpusu):

1. **Teksty prawne, historyczne i literackie oraz cytaty** (12 z 28): preambuła Konstytucji USA, definicja z CFR, sekcja
   kodeksu karnego Indii, słowa Armstronga, Reagan, Kanye West, wiersz Brooke'a, tekst piosenki.
2. **Formułki, szablony i frazy ogólne** (11): szablon Wikipedii o postaciach Marvela, „originally aired on the Fox
   network”, numer Crime Stoppers, „the best way to lose weight…”, definicja słownikowa, wzory matematyczne, ciąg zer w kodzie.
3. **Tytuły, listy nazw i formuły obrzędowe** (5): pełny tytuł Księgi Mormona, tytuły piosenek, lista krajów UE z 2004 r.,
   przysięga małżeńska.

Wątpliwe (17): pojedyncze zdanie z początku artykułu Wikipedii w dokumencie, który nie jest kopią Wikipedii (6), cytaty
prasowe z 1-2 trafieniami (5), tekst literacki użyty jako materiał testu (3), definicje podręcznikowe i ogólne zadanie (3).
W 6 dokumentach trafienie leży poza 20 000 znaków próbki: ocenione po samych 13-gramach.

Koszt reguły z aneksu 2 po stronie przeoczeń: 13 z 34 trafnych odrzuceń drugiego przeglądu i oba trafienia ARC-C w
prawdziwych dokumentach przestają odpadać (kopie testów obecne w sieci są też w FWE). Kolejna zmiana wymaga nowego
aneksu i świeżej próbki; do tego czasu eksport (krok 9) ma `ewal_13gram` bez PASS.

### Aneks 3 do preregistracji, 15.11.2026 (po trzecim przeglądzie)

Zapisany w [`skrypty/preregistracja.json`](skrypty/preregistracja.json), pole `aneks_2026_11_15c`, PO trzecim przeglądzie
(4e0a247). Powód w danych wyżej:

1. **Wykluczenie 13-gramów wspólnych z FWE COFNIĘTE, wraca reguła aneksu 1** (df ≥ 5 i ciągi). Przy aneksie 2 kontrola
   dodatnia przestała łapać prawdziwą kontaminację: ARC-C 0/2 (przy aneksie 1: 2/2), HellaSwag 61/129 (84/129), 13 z 34
   trafnych odrzuceń drugiego przeglądu przestało odpadać. Przeoczona kontaminacja psuje wyniki benchmarków, a fałszywe
   odrzucenia kosztują ok. 0,1% dokumentów: koszt jest asymetryczny.
2. **Dla `ewal_13gram` próg fałszywych odrzuceń ≤10% nie obowiązuje.** Kryterium tego powodu: zero przeoczeń w kontroli
   dodatniej. Stopa fałszywych odrzuceń i utracone tokeny są raportowane. Dekontaminacja zachowawcza, jak w GPT-3 i Llamie.
   To **jawne odstępstwo** od progów aneksu 1, przyjęte po zobaczeniu wyników przeglądów.
3. **PII:** przypadek „login at” bez domeny zostaje wątpliwy; PASS 0/300 zostaje z tym przypisem.

Do odtworzenia pomiaru aneksu 2 (krok
`ewal_fwe`): `HuggingFaceFW/fineweb-edu@87f09149ef4734204d70ed1d046ddc9ca3f2b8f9`, sha256:

| Plik | sha256 |
|---|---|
| `data/CC-MAIN-2014-10/train-00002-of-00014.parquet` | `10d45b5276fd3f0b984bcb8e8079892aa169a11bdb0cccc7b92eed2b7bf1419d` |
| `data/CC-MAIN-2017-04/train-00001-of-00018.parquet` | `820f8562fb2891a02cbac5bf1d4d274b300e72f797a26db307f5dcd4b2321188` |
| `data/CC-MAIN-2017-17/train-00014-of-00022.parquet` | `0f57717de087f63fe908e2e25f936b27db536ad8ddba4d6d89bb52e9bf18885d` |
| `data/CC-MAIN-2018-13/train-00005-of-00016.parquet` | `54b648a4412effe488d90db4621d7d3aec35bd1af8d2bc419fc30800f416a48e` |
| `data/CC-MAIN-2019-39/train-00012-of-00015.parquet` | `ef41ea937469b1b4ab588d7120eb6006f797fa324d49b677d12ab7d8ea2d7d1a` |
| `data/CC-MAIN-2024-26/000_00042.parquet` | `95e8f2d90af289c419c577f98de7c8dc756c01956c6a199571fd8646329929d9` |
| `data/CC-MAIN-2025-13/000_00043.parquet` | `5b31dbdcbfa53c68c82329c3a6b216c2213c2a45f58f995ca1bc80d136591ee9` |
| `data/CC-MAIN-2025-18/000_00023.parquet` | `3f64da6fef57ab38da270f3752011daa87c6c8f2eb797586a438acb675567e6f` |

**Przeliczenie na regule aneksu 1 (15.11.2026, kroki `kontrola`, `ewal_czeste`, `agreguj`, każdy kod 0, 30 s).** `agreguj` w `odtworz.sh` znów czyta `wyniki/ew13`;
kroki aneksu 2 zostają tylko do odtworzenia pomiaru.

| Krok | Wynik |
|---|---|
| `kontrola` + `ewal_czeste` na kontroli | K_hellaswag, K_piqa, K_arc_c, K_winogrande: `ewal_13gram` przed i po wykluczeniach (4/4); pozostałe 10 dostają swoje powody bez zmian |
| `ewal_czeste` na próbce ([`wyniki/ewal_13gram_aneks3.json`](wyniki/ewal_13gram_aneks3.json)) | odpada 1344 z 2821 dokumentów z trafieniem; prawdziwe dokumenty: **PIQA 4/4, ARC-C 2/2**, WinoGrande 0/0, HellaSwag 84/129 (79 trafieniem HellaSwag) |
| `agreguj` ([`wyniki/agreguj.json`](wyniki/agreguj.json)) | **zostaje 993 878 dok. (94,544%), 1 352 267 245 tokenów v6 (91,947%); szacunek do 5 mld v6: 37 shardów (33-43)**, dolna granica |

**`ewal_13gram` w trzech przeglądach (raport, nie kryterium):**

| Przegląd | Reguła | n | Fałszywe odrzucenia [Wilson 95%] | Dokumenty / tokeny v6 z powodem (niezależnie) |
|---|---|---|---|---|
| pierwszy (c14d015) | każde trafienie | 5 | 4 (80,0% [37,6; 96,4]) | 2821 / 15 098 522 (1,03% tokenów) |
| drugi (1e5a152) | aneks 1, **obowiązuje** | 100 | 51 (51,0% [41,4; 60,6]) | 1344 / 7 071 298 (0,48% tokenów; kaskada 1224 dok., 6 620 968 tok.) |
| trzeci (4e0a247) | aneks 2, cofnięty | 100 | 28 (28,0% [20,1; 37,5]) | 750 / 3 579 936 (0,24% tokenów) |

Przy obowiązującej regule fałszywe odrzucenia kosztują ok. 51% z 0,48% tokenów, czyli ok. 0,25% tokenów próbki.

**Werdykt całości: PRZESZŁO z aneksem 3.** 7 powodów przechodzi progi aneksu 1 (drugi przegląd; dedupy z definicją
kopii z aneksu 2, pkt 1, który zostaje). Przeoczenia w zachowanych przechodzą, PII 0/300 (Clopper-Pearson 0,994%) z
przypisem o jednym wątpliwym. `ewal_13gram` przechodzi kryterium kontroli dodatniej (4/4 wstawione, PIQA 4/4, ARC-C 2/2).
**Odstępstwo:** dla `ewal_13gram` nie obowiązuje próg fałszywych odrzuceń z aneksu 1; przy obowiązującej regule stopa
wynosi 51% [41,4; 60,6], próg ≤10% nie jest spełniony, a zmianę kryterium przyjęto po zobaczeniu wyników.

## 9. Eksport do formatu zgłoszeń

| | DCLM-EN |
|---|---|
| Co | NIE ZROBIONE; `key` np. `dclm_baseline_en` |
| Kolumny | `id`←`id` DCLM; `text`←`text` po maskowaniu; `language`=`en`; `text_origin`=`human`; `generator`=null; `derived_from`=null; `license`, `author`, `created`: **do decyzji** (brak licencji i daty per dokument w kopii parquet) |
| Dedup wobec Dynaword | wynik w `stats.json` → `dropped` |
| Pułapki | DCLM premiuje styl czatowy: web pisany przez modele możliwy przy `human` |

## 10. Kontrola końcowa

| | DCLM-EN |
|---|---|
| Co | NIE ZROBIONE |

## 11. Wysyłka (PR na Hugging Face)

### Chwilowo: własne repo do wglądu Arka (decyzja Ani, 15.11.2026)

Instrukcja: [`METODOLOGIA.md` zespołu](https://github.com/slayerlabs/benchmarks-fabryka-ai/blob/main/research/slayer-1b/dane/METODOLOGIA.md), sekcja 4. DCLM-EN: `<login>` = `Lolita67`,
`<key>` = `dclm_baseline_en`, repo `Lolita67/dclm_baseline_en-robocze`. Krok 12 czeka.

| | DCLM-EN |
|---|---|
| Warunek | NIEROZSTRZYGNIĘTY, czeka na Anię |

## 12. Aktualizacja karty danych

| | DCLM-EN |
|---|---|
| Co | wiersz 2026-11-14 już istnieje („w budowie”): zmień link i status |

## Historia odtworzeń DCLM-EN

- 14.11.2026: odbudowa wejść z tego przepisu zgodna z pierwszym przebiegiem (próbka, `idx_wal`, `idx_ivme` bajt w bajt, `ewal` po sumie i rewizjach).
- 14.11.2026: przebieg 216/216 zakończony (`KONIEC 1570s`); kroki 8-12 nie uruchomione.
- 14-15.11.2026: krok 8 (`fwe_url`, `edu`, `agreguj`) zakończony kodem 0;
  ręczna próbka czeka na niezależnego czytelnika; kroki 9-12 nie uruchomione.
- 15.11.2026: ręczna próbka oceniona przez niezależnego agenta: NIE PRZESZŁO (brak 100/100 per powód, brak progu
  w preregistracji, `ewal_13gram` 4/5 fałszywych odrzuceń); sekcja „Ręczny przegląd próbki”.
- 15.11.2026: aneks preregistracji (progi, PII bez zmian, wykluczenie 13-gramów z df ≥ 5 i trywialnych), przeliczenie
  `ewal_czeste` i `agreguj`, druga próbka 900 dok. oceniona przez trzech niezależnych agentów: NIE PRZESZŁO
  (`ewal_13gram` 51% fałszywych odrzuceń); pozostałe 7 powodów i zachowane PASS.
