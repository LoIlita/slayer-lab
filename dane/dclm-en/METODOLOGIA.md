# Przepis: budowa zbioru danych do treningu Slayera 1B (przykład: DCLM-baseline EN)

Przepis dla KAŻDEGO zbioru, od rezerwacji do wpisu w karcie danych. Każdy krok: co robisz, komenda,
jak sprawdzić, pułapki, a w ostatniej kolumnie wypełniony przykład DCLM-EN. Reguły kontroli: notatka
wiedzy `budowa-modeli/komplet-kontroli-zbioru` (workspace fabryka-ai). Wymagania wysyłki: repo
[`SlayerLab/dataset-team-submissions`](https://huggingface.co/datasets/SlayerLab/dataset-team-submissions)
(`README.md`, `AGENTS.md`, `LESSONS.md`, skill `.agents/skills/source-rights-review`).

## Zasady stałe

- Ścieżki względne do katalogu głównego repo `slayer-lab`. Zbiór = katalog `dane/<zbiór>/`.
- Katalog roboczy `dane/<zbiór>/robocze/` (w `.gitignore`). **Nigdy `/tmp` ani scratchpad sesji.**
- Każdy krok jest przypadkiem w `dane/<zbiór>/skrypty/odtworz.sh <krok>`; log do `robocze/logi/<krok>.log`.
- Długie kroki: `nohup nice -n 10 bash …/odtworz.sh <krok> > robocze/logi/<krok>.log 2>&1 &`.
- Przed każdym długim krokiem: `pgrep -lx 'Discord|LeagueClient|VTEncoderXPCService'` i
  `memory_pressure | tail -1`. Działa Liga: nie liczysz. Discord wolno (Ania, 14.11.2026), ale wtedy krok
  idzie pod strażnikiem pamięci `bash skrypty/straznik.sh <krok>` (sam startuje krok przez nohup nice): co 30 s wolna pamięć, load, swap i RSS kroku;
  wolna < 25% albo swap > 4 GB: `kill -STOP` pythona kroku do wolnej > 40%; pauza > 15 min albo wolna < 15%:
  `kill -TERM` i zgłoszenie, bez ponawiania. Pauzy w `robocze/logi/straznik.log`.
- Nie edytujesz `odtworz.sh`, gdy jakikolwiek krok go wykonuje: bash czyta skrypt w trakcie i zmiana długości
  pliku przesuwa mu odczyt.
- Wynik sprawdzasz kodem wyjścia i liczbami kontrolnymi, nie wrażeniem. BLOCKED i NOT RUN to nie PASS i
  blokują publikację.
- Wadliwy dokument wyrzucasz w całości, nie łatasz wzorcami.
- Tokeny w naszych wynikach i statystykach (kroki 7-8, karta, raporty) liczysz tokenizerem modelu docelowego
  (v6, słownik 32 768). Kolumna `token_count` w eksporcie (krok 9) to cl100k, bo tego wymaga `check.py` repo
  zgłoszeń (decyzja Ani 14.11.2026).
- Commit ochronny po każdym dniu pracy: wszystko z `dane/<zbiór>/` poza `robocze/`.

## Dwie bramki praw, rozstrzygane osobno

| Bramka | Kryterium | Źródło reguły | DCLM-EN |
|---|---|---|---|
| Można TRENOWAĆ | podstawa treningu: licencja tekstów albo wyjątek TDM (art. 4 dyr. 2019/790) z opisaną ścieżką takedown; opt-out TDM to UWAGA w karcie, nie weto | notatka §3, decyzja Ani 10.11.2026 | TAK (wyjątek TDM, takedown po `url`/`id`) |
| Można ZGŁOSIĆ do `dataset-team-submissions` | licencja per dokument, bez NC/ND, bez opt-outu TDM; sam wyjątek TDM nie wystarcza; licencja kompilacji ≠ licencja tekstów; „unverified = not admitted” | `AGENTS.md`, `LESSONS.md` reguła 5, skill `source-rights-review` | **NIEROZSTRZYGNIĘTY**: CC-BY-4.0 dotyczy kompilacji, teksty z Common Crawl bez licencji per dokument; decyduje Ania |

## Mapa kroków

| Nr | Krok | Produkt | Bramka przejścia |
|---|---|---|---|
| 1 | Rezerwacja | issue w `slayerlabs/benchmarks-fabryka-ai` | issue otwarte, wiersz „w budowie” w `DANE_TRENINGOWE.md` |
| 2 | Karta źródła i bramka praw | `KARTA_ZRODLA.md` | 6 pól wypełnionych, wynik obu bramek praw |
| 3 | Preregistracja | `skrypty/preregistracja.json` | zapisana PRZED pobraniem próbki i liczeniem |
| 4 | Środowisko | `robocze/venv`, `requirements.txt` | `pip freeze` = `requirements.txt` |
| 5 | Pobranie z rewizją i sumą | `robocze/pobrania/`, `wyniki/probka_pliki.json` | sha256 i liczba wierszy każdego pliku zapisane |
| 6 | Indeksy i kontrole | indeksy testów i baz, kontrola dodatnia | każdy wstawiony dokument dostaje właściwy powód |
| 7 | Przebieg | `robocze/wyniki/przebieg/` | wszystkie jednostki, log kończy `KONIEC` |
| 8 | Po przebiegu | `wyniki/agreguj.json`, `wyniki/fwe_url.json` | kaskada, uzysk v6, ręczna próbka |
| 9 | Eksport | `data/<key>/<key>.parquet`, `.stats.json`, `.md` | PII zamaskowane, bramka języka, 12 kolumn |
| 10 | Kontrola końcowa | wynik `pytest` i `src/check.py` | oba kod 0, niezależny agent na tym samym sha256 |
| 11 | Wysyłka | PR na HF do `dataset-team-submissions` | przegląd praw z osobą zatwierdzającą |
| 12 | Aktualizacja karty | PR do `DANE_TRENINGOWE.md` | wiersz z linkiem do zbioru i statusem |

## 1. Rezerwacja

| | Ogólnie | Przykład: DCLM-EN |
|---|---|---|
| Co | issue z celem (testy, liczba tokenów v6), źródłem i osobą; wiersz „w budowie” w sekcji „Dopisane później” `DANE_TRENINGOWE.md` | issue [#197](https://github.com/slayerlabs/benchmarks-fabryka-ai/issues/197); cel ≥5 mld tokenów v6 pod HellaSwag, PIQA, ARC-C, WinoGrande |
| Komenda | `gh issue create -R slayerlabs/benchmarks-fabryka-ai` | — |
| Sprawdzenie | `gh api repos/slayerlabs/benchmarks-fabryka-ai/issues/<nr> --jq .state` = `open` | `open`; wiersz 2026-11-14 „w budowie” istnieje |
| Pułapki | dwie osoby na tym samym źródle; brak celu w tokenach v6 | — |

## 2. Karta źródła i bramka praw

| | Ogólnie | Przykład: DCLM-EN |
|---|---|---|
| Co | `KARTA_ZRODLA.md` z 6 polami notatki §2 przed pobraniem; wynik obu bramek praw; każde twierdzenie z etykietą V (sprawdzone, data, URL, hash) albo I (wywnioskowane); lista „nie sprawdzone” | [`KARTA_ZRODLA.md`](KARTA_ZRODLA.md), 14.11.2026 |
| Prawa | trening i redystrybucja osobno; licencja zbioru ≠ licencja tekstów; opt-out TDM na próbce domen (`robots.txt`, TDMRep); pełny regulamin, nie odznaka | CC-BY-4.0 kompilacji; teksty Common Crawl; karta: „research use only”; opt-out TDM: NIE SPRAWDZONE |
| Sprawdzenie | 6 nagłówków obecnych; bramka „trenować” i „zgłosić” mają wynik albo NIEROZSTRZYGNIĘTY | trenować: TAK; zgłosić: NIEROZSTRZYGNIĘTY |
| Pułapki | kopiowanie statusu praw z innego źródła (reguła 8 skilla); „0 znalezionych w 40” to wynik, nie czyste konto | DCLM jest już w EN 1.07 (`minimal-en-corpus-5b`, 577 998 dok.) |

Karta mapuje się na datasheet `data/<key>/<key>.md` (krok 9). Jedna karta daje datasheet:

| Pole karty (notatka §2) | Sekcja datasheetu | Uwaga |
|---|---|---|
| 1. Identyfikacja | `## Source` | URL, wydawca, rewizja |
| 3. Zawartość | `## Source` | język, dziedzina, plik i pole tekstu |
| 4. Skala i dostęp | `## Source` | dokumenty, format, dostęp |
| 2. Prawa | `## Rights review` | łańcuch praw V/I, decyzja, osoba zatwierdzająca, „not checked” |
| 5. Ryzyka: kopie, testy, OCR, syntetyki | `## Cleaning` | kaskada powodów i uzysk z kroku 8 |
| 6. Nowość | `## Cleaning` | zakresy dedupu i czego nie objęły |
| 5. Ryzyka: PII | `## Personal data` | nasze usunięcie + maskowanie repo (wersja PII) |
| ręczna próbka (krok 8) | `## Sample` | seed, liczności, stopa błędów |

## 3. Preregistracja

| | Ogólnie | Przykład: DCLM-EN |
|---|---|---|
| Co | `skrypty/preregistracja.json` PRZED pobraniem próbki: źródło z rewizją, wybór próbki (seed), tokenizer, kolejność powodów odrzucenia, progi, pomiary (nie filtry), ręczna próbka, kontrole dodatnie | [`skrypty/preregistracja.json`](skrypty/preregistracja.json): seed 20261114, 8 powodów w kaskadzie |
| Sprawdzenie | `git log` pliku starszy niż pierwszy wynik; każda zmiana po wyniku dopisana z powodem i datą | zmiana 15→8 plików FWE dopisana przed wynikiem FWE |
| Pułapki | próg dobrany po zobaczeniu wyniku; brak kolejności powodów (kaskada niejednoznaczna) | — |

## 4. Środowisko

| | Ogólnie | Przykład: DCLM-EN |
|---|---|---|
| Co | venv w `robocze/venv`, wersje przypięte w `requirements.txt` (wynik `pip freeze`) | Python 3.12.2; od 14.11 także `torch==2.15.0`, `transformers==5.23.0` (krok `edu`, 4 wątki CPU) |
| Komenda | `bash dane/<zbiór>/skrypty/odtworz.sh venv` | jw. |
| Sprawdzenie | `robocze/venv/bin/pip freeze` = `requirements.txt` | — |
| Pułapki | wersje niezapisane (stary venv DCLM przepadł w `/tmp` bez listy wersji); doinstalowanie pakietu bez dopisania do `requirements.txt` | — |

## 5. Pobranie z rewizją i sumą

| | Ogólnie | Przykład: DCLM-EN |
|---|---|---|
| Co | tokenizer docelowy, próbka źródła, zbiory testowe, bazy do dedupu; każde z przypiętą rewizją i sha256 | `odtworz.sh tokenizer`, `probka`, `testy`, `baza107`, `walidacja_pobierz` |
| Źródła | — | DCLM `mlfoundations/dclm-baseline-1.0-parquet@817d6752…`; tokenizer v6 sha `0640d3bd…`; EN 1.07 `SlayerLab/slayer-1.07-pretrain@6a337bbf`; walidacje `minimal-en-corpus-5b@bb3aec23`, `minimal-en-corpus-2b-v2@ef0ab069` |
| Sprawdzenie | sha256 i wiersze równe rejestrowi; skrypt przerywa przy złej sumie | `probka`: log `KONIEC 1051235`, 10 plików równe [`wyniki/probka_pliki.json`](wyniki/probka_pliki.json); `tokenizer`: sha, słownik 32 768, token 0 `<\|endoftext\|>`; `baza107`: en_mix/train.bin 3 301 237 628 B, en_fineweb_edu/train.bin 4 471 320 050 B; `testy`: 56 OK, 4 BLOCKED z powodem |
| Pułapki | gałąź `main` zamiast rewizji; kopia „identyczna” nieidentyczna (kopia parquet DCLM ma 100 plików więcej niż `jsonl.zst`); pliki walidacji i miksów zespołu nie wykluczone przed losowaniem | wykluczone 31 plików ([`skrypty/wykluczone.json`](skrypty/wykluczone.json)) |

## 6. Indeksy i kontrole

| | Ogólnie | Przykład: DCLM-EN |
|---|---|---|
| Co | indeksy: 13-gramy testów, historia modeli, walidacja Fabryki, inne miksy zespołu; kontrola dodatnia: znane PII, kawałki testów, kopie baz wstawione do przebiegu | `odtworz.sh ewal`, `idx107`, `idx_wal`, `idx_ivme`, `kontrola` |
| Sprawdzenie | liczby indeksów równe rejestrowi; KAŻDY wstawiony dokument dostaje swój powód, czysty bez powodu | `ewal`: `ogolem 32411348`; `idx107`: 3 278 603 dok., 158 680 048 próbek; `idx_wal` = [`wyniki/indeks_walidacja.json`](wyniki/indeks_walidacja.json) bajt w bajt; `idx_ivme` = [`wyniki/indeks_ivme.json`](wyniki/indeks_ivme.json); kontrola: 14/14 wg [`wyniki/kontrole_dodatnie.json`](wyniki/kontrole_dodatnie.json) |
| Pułapki | **kontrola dodatnia po KAŻDEJ odbudowie indeksów**, nie tylko raz; indeks bez `KONIEC` w logu (koniec = plik wynikowy); kilka kroków liczących naraz z przebiegiem | brak w zakresie: segmenty c01–c10 i gold (niedostępne) |

## 7. Przebieg

| | Ogólnie | Przykład: DCLM-EN |
|---|---|---|
| Co | detektory na każdym dokumencie próbki, wynik per jednostka, zapis atomowy, wznawialny | `odtworz.sh przebieg`, 6 procesów, `nice -n 10` |
| Sprawdzenie | log zaczyna `jednostek N do zrobienia M`, kończy `KONIEC <s>`; N plików wyniku, zero niedokończonych (`.u_*`) | 216/216 `u_*.npz`, `KONIEC 1570s`, 14.11.2026 |
| Wznowienie | uruchom krok ponownie; gotowe jednostki są pomijane, `.u_*.npz` kasujesz | — |
| Pułapki | presja pamięci (Mac 51 GB padł przy 6 procesach i równoległych zadaniach); więcej procesów bez pomiaru RSS jednej jednostki | — |

## 8. Po przebiegu

| | Ogólnie | Przykład: DCLM-EN |
|---|---|---|
| Co | pomiary spoza filtrów (nakładanie z innymi zbiorami, klasyfikator jakości), potem agregacja: dedup wewnątrz, kaskada powodów, uzysk v6 po każdym powodzie, szacunek skali, ręczna próbka | `odtworz.sh fwe_url` (8 plików FWE), `edu` (50 000 dok., cpu float32), `agreguj` |
| Sprawdzenie | kod wyjścia 0; suma kaskady = dokumenty próbki; `niedostepne` w wyniku puste albo opisane; ręczna próbka oceniona przez niezależnego czytelnika | 14-15.11.2026, pod strażnikiem, 0 pauz, swap 0, wolna pamięć ≥91%: **`fwe_url`** kod 0, 2765 s, szczyt RSS 837 MB; 8/8 plików, 4 829 900 wierszy (0,317% z 1 525 223 056 wierszy FWE), 4 748 572 unikalnych url ([`wyniki/fwe_url.json`](wyniki/fwe_url.json)). **`edu`** kod 0, 5414 s, szczyt RSS 7318 MB, cpu float32, **4 wątki** (`EDU_WATKI`, `OMP_NUM_THREADS`, `torch.set_num_threads`; ostrożny start po panice Maca 14.11), `KONIEC 50000`; int_score 0-5: 2608 / 24 007 / 15 931 / 6270 / 1180 / 4; próg ≥2 = 49,52% tokenów, ≥3 = 15,79%. **`agreguj`** kod 0, 30 s (RSS niezmierzony: krótszy niż okres próbki 30 s); 1 051 235 dok., 1 470 704 495 tokenów v6; kaskada 376 + 6738 + 2611 + 29 333 + 2279 + 3679 + 11 741 + 1895 = 58 652 odrzuconych, suma z zachowanymi = dokumenty próbki; **zostaje 992 583 dok. (94,42%), 1 345 901 642 tokenów v6 (91,51%)** (stan przed aneksem 15.11; po aneksie 993 878 dok., 1 352 267 245 tokenów v6, sekcja „Aneks do preregistracji”); `niedostepne` puste; FWE url: 7826 trafień (0,74%); szacunek do 5 mld v6: 38 shardów (34-43) z 27 838, dolna granica ([`wyniki/agreguj.json`](wyniki/agreguj.json)); ręczna próbka 200 wierszy w `robocze/wyniki/probki_reczne.jsonl`, oceniona 15.11.2026: **NIE PRZESZŁO** (sekcja „Ręczny przegląd próbki” niżej) |
| Pułapki | uzysk przeniesiony z innej porcji (mierzysz od nowa, notatka §5); plik ręcznej próbki ma PII odrzuconych, zostaje w `robocze/`; szacunek shardów to dolna granica | — |

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
podają (sprawdzone 15.11.2026), więc obowiązują proponowane przez główną sesję:

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

**Przeliczenie po aneksie (15.11.2026, pod strażnikiem, `nohup nice -n 10`, 0 pauz, swap 0, wolna pamięć 93%).**

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
`ewal_13gram` nie przeszedł, a trzy zastrzeżenia wyżej mogły zmienić werdykt. Rozstrzygnięcia techniczne głównej sesji:

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

## 9. Eksport do formatu zgłoszeń

Robisz w klonie `SlayerLab/dataset-team-submissions`, nie w `slayer-lab`.

| | Ogólnie | Przykład: DCLM-EN |
|---|---|---|
| Co | (1) bierzesz dokumenty bez powodu odrzucenia; (2) skrypt `src/clean_<key>.py` woła `shard.write(key, rows)`, który maskuje PII (`src/pii.py`: Presidio dla EN, NERGAL dla PL, `[PHONE]`, `[PII]`, `[PERSON]` przy `names=True`), stosuje bramkę języka (`src/language_gate.py`, teksty ≥200 znaków), odrzuca teksty Dynaword i blocklisty, liczy `token_count` i pisze `data/<key>/<key>.parquet` oraz `<key>.stats.json`; (3) datasheet `data/<key>/<key>.md` z karty (tabela w kroku 2) | NIE ZROBIONE; `key` np. `dclm_baseline_en` |
| Kolumny | `id`, `text`, `source`, `added`, `created`, `token_count`, `license`, `author`, `language` (`pl`/`en`/`pl+en`), `text_origin` (`human`/`translated`/`synthetic`), `generator`, `derived_from`; `source`, `added`, `token_count` dopisuje `shard.write` | `id`←`id` DCLM; `text`←`text` po maskowaniu; `language`=`en`; `text_origin`=`human`; `generator`=null; `derived_from`=null; `license`, `author`, `created`: **do decyzji** (brak licencji i daty per dokument w kopii parquet) |
| Dedup wobec Dynaword | identyczny klucz tekstu z `dynaword/pin.json` odrzuca `shard.write`; przy nakładaniu hostów near-dup `src/shingle_containment.py`, próg ≥0,9 (LESSONS reguła 13) | wynik w `stats.json` → `dropped` |
| Sprawdzenie | `stats.json`: `dropped`, `lang_gate`, rekord `pii` (`presidio` dla EN) | — |
| Pułapki | `text_origin=synthetic` bez `generator` w formacie `model@rewizja prompt:ścieżka`; tekst złożony tylko z placeholderów PII | DCLM premiuje styl czatowy: web pisany przez modele możliwy przy `human` |

## 10. Kontrola końcowa

| | Ogólnie | Przykład: DCLM-EN |
|---|---|---|
| Co | wpis w `src/sources.py` (pola: `pretty`, `upstream`, `license`, `license_spdx`, `domain`, `added`, `created`, `provenance`, `traceable`, `is_ocr`, `language`, `text_origin`, `legal_note`; opcjonalnie `min_chars`, `dynaword_overlap_reviewed`), wpis `configs` w `README.md`, test kontraktowy `src/test_<key>_contract.py`; komplet kontroli z notatki §1 przez niezależnego agenta na pliku o tym samym sha256 | NIE ZROBIONE |
| Komenda | `.venv/bin/python -m pytest src/test_<key>_contract.py` i `.venv/bin/python src/check.py --source <key>` | — |
| Sprawdzenie | oba kod wyjścia 0; `check.py` sprawdza schemat, unikalność `id`, Dynaword, blocklistę, bramkę języka, `token_count`, ponowny skan PII (200 tekstów), `stats.json` i 5 sekcji datasheetu | — |
| Pułapki | `check.py` nie sprawdza podstawy licencji (tylko niepuste `license`), to robi krok 11; plik LFS-pointer zamiast parquetu | — |

## 11. Wysyłka (PR na Hugging Face)

| | Ogólnie | Przykład: DCLM-EN |
|---|---|---|
| Warunek | bramka „można ZGŁOSIĆ” = TAK; kroki 9-10 zielone | NIEROZSTRZYGNIĘTY, czeka na Anię |
| Co | przegląd praw wg skilla `source-rights-review`: łańcuch praw (każde ogniwo: zapis, URL, data, hash), V/I przy każdym twierdzeniu, decyzja `admitted`/`excluded`/`held_for_review`, co wstrzymane, lista „not checked”, **osoba zatwierdzająca**; próbka treści stron trzecich: seed, ≥40 dok. na warstwę, przedział Wilsona, udział tokenów | — |
| Komenda | `python src/render_sample.py …` (próbka do opisu PR); PR na https://huggingface.co/datasets/SlayerLab/dataset-team-submissions z katalogiem `data/<key>/` | — |
| Opis PR | próbka inline, przegląd praw, wersja PII, stan before/after (`dropped` ze `stats.json`, uzysk v6 z kroku 8) | — |
| Pułapki | kontakt z właścicielami praw, akceptacja regulaminów, zakładanie kont: tylko ludzie; po merge maintainer porównuje stronę licencji z hashem dowodu | — |

## 12. Aktualizacja karty danych

| | Ogólnie | Przykład: DCLM-EN |
|---|---|---|
| Co | PO wysyłce: PR do [`DANE_TRENINGOWE.md`](https://github.com/slayerlabs/benchmarks-fabryka-ai/blob/main/research/slayer-1b/dane/DANE_TRENINGOWE.md), sekcja „Dopisane później”: data, zbiór z linkiem do PR/zbioru na HF, osoba, zgłoszenie, status | wiersz 2026-11-14 już istnieje („w budowie”): zmień link i status |
| Komenda | gałąź w `benchmarks-fabryka-ai`, edycja wiersza, `gh pr create` | — |
| Sprawdzenie | każdy link w wierszu odpowiada 200 (`gh api` / `curl -sIL`) | — |
| Pułapki | wiersz dopisany przed wysyłką (status bez dowodu); nowy wiersz zamiast zmiany istniejącego z rezerwacji | — |

## Rozjazdy: notatka `komplet-kontroli-zbioru` a repo zgłoszeń (do decyzji, nie rozstrzygnięte)

| Temat | Notatka / nasz przebieg | Repo zgłoszeń |
|---|---|---|
| `token_count` | ROZSTRZYGNIĘTE 14.11.2026 (Ania): `token_count` w eksporcie = cl100k; v6 zostaje w naszych wynikach i statystykach | `check.py` wymaga `token_count` = cl100k (`shard.count_tokens`, tiktoken); v6 w kolumnie da czerwony `check.py` |
| PII | dokument z trafieniem usuwany w całości (regex e-mail, telefon, IP) | maskowanie Presidio/NERGAL, `check.py` wymaga rekordu `presidio` |
| Prawa | wyjątek TDM wystarcza do treningu | licencja per dokument; sam TDM nie wystarcza |
| Ręczna próbka | 100 zachowanych + 100 odrzuconych przy KAŻDYM powodzie | ≥40 na warstwę + przedział Wilsona |
| Dedup | historia 1.00–1.08, segmenty, walidacja, gold; MinHash ≥0,8, szkic 13-gramów ≥0,5 | Dynaword: identyczny klucz + containment ≥0,9; reszty nie wymaga |
| Bramka języka | brak w notatce | wymagana, w `stats.json` |
| Kontrola | niezależny agent na całym pliku o tym samym sha256 | `check.py` + lista recenzenta (ludzie) |

## Historia odtworzeń DCLM-EN

- 14.11.2026: wejścia w `/private/tmp` przepadły po restarcie; odbudowa z tego przepisu zgodna z
  przebiegiem sprzed awarii (próbka, `idx_wal`, `idx_ivme` bajt w bajt, `ewal` po sumie i rewizjach).
- 14.11.2026: przebieg 216/216 zakończony (`KONIEC 1570s`); kroki 8-12 nie uruchomione.
- 14-15.11.2026: krok 8 (`fwe_url`, `edu`, `agreguj`) zakończony kodem 0 pod strażnikiem pamięci, bez pauz;
  ręczna próbka czeka na niezależnego czytelnika; kroki 9-12 nie uruchomione.
- 15.11.2026: ręczna próbka oceniona przez niezależnego agenta: NIE PRZESZŁO (brak 100/100 per powód, brak progu
  w preregistracji, `ewal_13gram` 4/5 fałszywych odrzuceń); sekcja „Ręczny przegląd próbki”.
- 15.11.2026: aneks preregistracji (progi, PII bez zmian, wykluczenie 13-gramów z df ≥ 5 i trywialnych), przeliczenie
  `ewal_czeste` i `agreguj`, druga próbka 900 dok. oceniona przez trzech niezależnych agentów: NIE PRZESZŁO
  (`ewal_13gram` 51% fałszywych odrzuceń); pozostałe 7 powodów i zachowane PASS.
