# Dziennik zbioru: FineMath-4+ (EN) dla microannealu Slayera 1B

Przepis: [`METODOLOGIA.md` w repo zespołu](https://github.com/slayerlabs/benchmarks-fabryka-ai/blob/main/research/slayer-1b/dane/METODOLOGIA.md).
Karta źródła: [`KARTA_ZRODLA.md`](KARTA_ZRODLA.md). Reguły: [`skrypty/preregistracja.json`](skrypty/preregistracja.json).
Skrypty wspólne trzech zbiorów #346 (FineMath-4+, CraneMath, Stack-Edu Python): [`../matematyka-wspolne/skrypty/`](../matematyka-wspolne/skrypty/),
każdy krok to `bash dane/matematyka-wspolne/skrypty/odtworz.sh <krok> finemath4`.

## Bramki praw

| bramka | wynik |
|---|---|
| Można TRENOWAĆ | TAK (wyjątek TDM art. 4 dyr. 2019/790; takedown po `url` albo rekordzie WARC) |
| Można ZGŁOSIĆ do `dataset-team-submissions` | NIEROZSTRZYGNIĘTY: ODC-By dotyczy kompilacji, teksty z Common Crawl bez licencji per dokument |

## 1. Rezerwacja

| | |
|---|---|
| Co | issue [#346](https://github.com/slayerlabs/benchmarks-fabryka-ai/issues/346) na tablicy Dataset team (In progress, LoIlita); wiersz „w budowie” w PR [#347](https://github.com/slayerlabs/benchmarks-fabryka-ai/pull/347) |
| Cel | ramię B microannealu (paper mat./med. 1.2): ≥ 0,4 mld tokenów v6 po filtrach |

## 2. Karta źródła

[`KARTA_ZRODLA.md`](KARTA_ZRODLA.md), 24.11.2026, przed pobraniem (commit `6988094`).

## 3. Preregistracja

[`skrypty/preregistracja.json`](skrypty/preregistracja.json), commit `6988094` przed pobraniem puli. Aneks 24.11.2026 (commit
`f159b6e`, przed odczytem agregacji): dedup wobec `english-technical-1b` (1.08) i url FineWeb-Edu 1.09, wymaganie właścicielki
projektu (zero duplikatów z danymi w treningu i z pracą innych).

## 4. Środowisko

`odtworz.sh venv`: Python 3.12, [`../matematyka-wspolne/requirements.txt`](../matematyka-wspolne/requirements.txt) (numpy 2.5.4,
pyarrow 26.0.1, tokenizers 0.23.3, huggingface_hub 2.4.0, zstandard, ftfy 6.3.1). Tokenizer v6 sha256 `0640d3bd…`
z katalogu roboczego DCLM-EN (sprawdzany w kroku `ewal_pobierz`).

## 5. Pobranie

`odtworz.sh pula finemath4`, 24.11.2026: kod 0 części Pythona (`KONIEC 418718 660554470`); 4 pliki z 64 w kolejności
`default_rng(20261124)`, rewizja `e92b25a6`, sha256 każdego pliku w [`wyniki/probka_pliki.json`](wyniki/probka_pliki.json).
Pula: 418 718 dokumentów, 660 554 470 tokenów v6. Bash zakończył się kodem 2 PO wypisaniu `KONIEC`: plik `odtworz.sh` był
edytowany w trakcie przebiegu (bash czyta skrypt przyrostowo); dane i wynik puli pełne, pułapka dopisana poniżej.

## 6. Indeksy i kontrole

- Testy: indeks RPG v2 (60 testów, dowiązania do pobrań DCLM-EN) + T51 GSM-Plus i T52 GSM1k (`odtworz.sh ewal_pobierz`,
  `ewal`): `ogolem 33302686` 13-gramów, `KONIEC`.
- EN 1.07 i walidacja Fabryki: indeksy z katalogu roboczego DCLM-EN (`idx`, `idx_wal`), bez zmian.
- Kontrola dodatnia `odtworz.sh kontrola finemath4`: 14/14 przed aneksem ([`wyniki/kontrola.json`](wyniki/kontrola.json));
  pierwsza wersja kontroli miała parę duplikatów na tym samym tle co dokument czysty, więc `K_dup_a` dostawał
  `dedup_wewnatrz` jako kopia tła; para dostała własny tekst, kontrola powtórzona.

## Pułapki tego przebiegu

- Nie edytuj `odtworz.sh`, gdy którykolwiek krok jest w toku: bash czyta skrypt w trakcie wykonania.
- macOS ma bash 3.2: pusta tablica przy `set -u` daje „unbound variable”; stąd `${ORYG[@]+"${ORYG[@]}"}`.
