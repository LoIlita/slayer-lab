# Metodologia: zbiór danych do treningu Slayera 1B

Jeden przepis dla każdego zbioru, od rezerwacji do wpisu w [`KARTA_DANYCH_TRENINGOWYCH.md`](KARTA_DANYCH_TRENINGOWYCH.md). Wypełniony przykład każdego kroku: [`dclm-en/METODOLOGIA.md`](dclm-en/METODOLOGIA.md). Wymagania wysyłki: [![HF](https://img.shields.io/badge/HF-SlayerLab%2Fdataset--team--submissions-ffcc00?logo=huggingface)](https://huggingface.co/datasets/SlayerLab/dataset-team-submissions) (`README.md`, `AGENTS.md`, `LESSONS.md`, skill `source-rights-review`).

## 1. Zasady stałe

- Zbiór = katalog `dane/<zbiór>/`. Pliki robocze w `dane/<zbiór>/robocze/` (w `.gitignore`), nigdy w `/tmp`.
- Każdy krok to przypadek w `dane/<zbiór>/skrypty/odtworz.sh <krok>`, log w `robocze/logi/<krok>.log`. Wzór skryptu: [`dclm-en/skrypty/odtworz.sh`](dclm-en/skrypty/odtworz.sh).
- Długi krok: `nohup nice -n 10 bash dane/<zbiór>/skrypty/odtworz.sh <krok> > robocze/logi/<krok>.log 2>&1 &`, przy obciążonej maszynie pod strażnikiem pamięci ([`dclm-en/skrypty/straznik.sh`](dclm-en/skrypty/straznik.sh)).
- Nie edytujesz `odtworz.sh`, gdy krok go wykonuje.
- Wynik = kod wyjścia i liczby kontrolne. BLOCKED i NOT RUN to nie PASS i blokują publikację.
- Wadliwy dokument wyrzucasz w całości, nie łatasz.
- Tokeny w wynikach liczysz tokenizerem v6 (słownik 32 768). Wyjątek: `token_count` w eksporcie to cl100k, bo tego wymaga `check.py`.
- Po każdym dniu pracy commit wszystkiego z `dane/<zbiór>/` poza `robocze/`.

## 2. Dwie bramki praw

| bramka | przechodzi, gdy | źródło reguły |
|---|---|---|
| można TRENOWAĆ | licencja tekstów albo wyjątek TDM (art. 4 dyr. 2019/790) z opisaną ścieżką takedown; opt-out TDM to uwaga, nie weto | notatka `komplet-kontroli-zbioru` §3 |
| można ZGŁOSIĆ | licencja per dokument, bez NC/ND i opt-outu TDM; licencja kompilacji ≠ licencja tekstów; niesprawdzone = nieprzyjęte | `AGENTS.md`, `LESSONS.md` reguła 5 |

## 3. Kroki

| nr | krok | co robisz | gotowe, gdy |
|---|---|---|---|
| 1 | Rezerwacja | issue w [![GitHub](https://img.shields.io/badge/GitHub-benchmarks--fabryka--ai-181717?logo=github)](https://github.com/slayerlabs/benchmarks-fabryka-ai/issues) z celem (testy, tokeny v6), źródłem i osobą: `gh issue create -R slayerlabs/benchmarks-fabryka-ai`; wiersz „w budowie” w karcie danych | issue `open`, wiersz jest |
| 2 | Karta źródła | `KARTA_ZRODLA.md` PRZED pobraniem: identyfikacja, prawa, zawartość, skala, ryzyka, nowość; każde twierdzenie V (sprawdzone: data, URL, hash) albo I (wywnioskowane); lista „nie sprawdzone” | 6 pól, obie bramki praw z wynikiem albo NIEROZSTRZYGNIĘTY |
| 3 | Preregistracja | `skrypty/preregistracja.json` PRZED próbką: rewizja źródła, seed, tokenizer, kolejność powodów odrzucenia, progi, kontrole dodatnie, ręczna próbka | commit starszy niż pierwszy wynik; każda późniejsza zmiana jako aneks z datą i powodem |
| 4 | Środowisko | venv w `robocze/venv`, wersje w `requirements.txt`: `odtworz.sh venv` | `pip freeze` = `requirements.txt` |
| 5 | Pobranie | tokenizer, próbka, testy, bazy do dedupu, każde z rewizją i sha256 | sumy i liczby wierszy zgodne z rejestrem; zła suma przerywa skrypt |
| 6 | Indeksy i kontrole | indeksy 13-gramów testów, poprzednich danych modelu, walidacji; kontrola dodatnia: wstawiasz znane PII, kawałki testów, kopie | każdy wstawiony dokument dostaje swój powód; kontrola po KAŻDEJ odbudowie indeksów |
| 7 | Przebieg | detektory na każdym dokumencie, wynik per jednostka, wznawialny | log kończy `KONIEC`, zero niedokończonych jednostek |
| 8 | Po przebiegu | pomiary (nakładanie, jakość), dedup, kaskada powodów, uzysk v6, szacunek skali, ręczna próbka oceniona przez niezależnego czytelnika | kod 0; suma kaskady = dokumenty próbki; próbka PRZESZŁO wg progów z kroku 3 |
| 9 | Eksport | w klonie `dataset-team-submissions`: `src/clean_<key>.py` z `shard.write(key, rows)` (maskuje PII, bramka języka, dedup Dynaword) i datasheet `data/<key>/<key>.md` z karty | `data/<key>/<key>.parquet`, `.stats.json`, `.md`; 12 kolumn |
| 10 | Kontrola końcowa | wpis w `src/sources.py`, `configs` w `README.md`, test kontraktowy; `pytest src/test_<key>_contract.py` i `python src/check.py --source <key>` | oba kod 0; niezależny agent na pliku o tym samym sha256 |
| 11 | Wysyłka | chwilowo: własne repo do wglądu Arka (sekcja 4); docelowo PR do `dataset-team-submissions` z przeglądem praw i osobą zatwierdzającą | Arek ma link i dostęp |
| 12 | Karta danych | PO wysyłce: w wierszu z kroku 1 link do zbioru i status | każdy link w wierszu odpowiada 200 |

## 4. Wysyłka do wglądu Arka (chwilowo, od 15.11.2026)

Każdy wgrywa na SWOIM koncie Hugging Face. Pliki widzi tylko właściciel i Arek (`Maggio33`); publicznie widać nazwę repo i README. `<login>` to Twój login HF, `<key>` z kroku 9.

| nr | co robisz | komenda |
|---|---|---|
| 0 | raz na maszynie | `pip install -U huggingface_hub` i `hf auth login` (token z zapisem) |
| 1 | repo z bramką PRZED plikami i dostęp dla Arka | `python -c "from huggingface_hub import HfApi as A; a=A(); r='<login>/<key>-robocze'; a.create_repo(r, repo_type='dataset'); a.update_repo_settings(r, gated='manual', repo_type='dataset'); a.grant_access(r, 'Maggio33', repo_type='dataset')"` |
| 2 | sprawdź bramkę | okno incognito: strona repo nie pokazuje listy plików |
| 3 | wgraj | `hf upload <login>/<key>-robocze data/<key> data/<key> --repo-type dataset` |
| 4 | README | jedno zdanie „Zbiór roboczy do recenzji, nie do użytku.”; opis zbioru w `data/<key>/OPIS.md`, za bramką |
| 5 | wyślij Arkowi link | `https://huggingface.co/datasets/<login>/<key>-robocze` |

Arek pobiera po `hf auth login`: `hf download <login>/<key>-robocze --repo-type dataset`. Kolejna osoba: `grant_access` z jej loginem; odebranie: `reject_access_request`. Krok 12 czeka do zwykłej wysyłki.

## 5. Pułapki

- Gałąź `main` zamiast rewizji; „identyczna kopia” zbioru, która nie jest identyczna.
- Próg dobrany po zobaczeniu wyniku bez aneksu.
- Uzysk przeniesiony z innej porcji danych: mierzysz od nowa.
- Plik ręcznej próbki zawiera PII odrzuconych: zostaje w `robocze/`.
- Kilka ciężkich kroków naraz: Mac 51 GB padł przy 6 procesach.
- Status praw skopiowany z innego źródła.
