# Karta źródła: Stack-Edu w wersji Common Pile (`common-pile/stackv2_edu_filtered`), tylko Python, dla Slayera 1B

Zapisana 24.11.2026 przed pobraniem próbki. Rezerwacja: https://github.com/slayerlabs/benchmarks-fabryka-ai/issues/346
Metodologia: https://github.com/slayerlabs/benchmarks-fabryka-ai/blob/main/research/slayer-1b/dane/METODOLOGIA.md

Cel: ramię D microannealu (zwycięzca B/C + 10% kodu): co najmniej 0,25 mld tokenów v6 Pythona po
filtrach. Oznaczenia: **V** = sprawdzone 24.11.2026 (URL, rewizja, hash), **I** = wywnioskowane.

## 1. Identyfikacja

- V: URL https://huggingface.co/datasets/common-pile/stackv2_edu_filtered, rewizja
  `c354dbe88469a1153e97c6a63ac50591849654de` (API `.../api/datasets/common-pile/stackv2_edu_filtered/revision/<rewizja>`,
  `lastModified` 2025-06-06). 97 plików `stack-edu-NNNN.json.gz` (0000–0096), razem 83 037 679 175 B; plus README i
  `.gitattributes`.
- V: wydawca Common Pile (EleutherAI i in.), praca Kandpal i in. 2025, https://arxiv.org/abs/2506.05209; kod
  https://github.com/r-three/common-pile. Klasyfikatory „edu” i metoda z SmolLM2 (Allal i in. 2025,
  https://arxiv.org/abs/2502.02737, §3.4, dod. D).
- V: README pod tą rewizją NIE opisuje tego zbioru: tytuł „Stack V2 Edu”, ale tekst mówi „This is the "raw" version of the
  Stack V2 dataset” i odsyła do wersji filtrowanych, w tym do samego `stackv2_edu_filtered`. Liczby z karty
  (69 588 607 dokumentów, 255 GB) to Stack V2 po filtrze licencji w całości (praca, Tab. 4: 69 588 607 dok., 259,9 GB),
  nie ten podzbiór „edu”. Własnej karty zbioru brak.
- V: pliki są ułożone blokami języków (pierwszy wiersz każdego pliku, 97 odczytów). Python = pliki **0073–0084**
  (12 plików, 11 716 959 758 B skompresowanych); 0084 jest mieszany: 174 868 wierszy Python, potem 753 345 Ruby.
  Pole `metadata.provenance` wskazuje plik upstream (`stack-edu-0055.json.gz:1` w 0073 … `stack-edu-0066.json.gz:175114`
  na końcu Pythona w 0084).
- I: ten zbiór trenował Comma v0.1 (karta README odsyła tu jako „filtered versions used to train Comma v0.1”).

## 2. Prawa

- V: licencja per plik = `metadata.license` (string, kilka licencji rozdzielonych przecinkiem, np. `Apache-2.0,MIT`).
  Obok: `metadata.detected_licenses` (lista z detekcji Stack v2), `metadata.license_type` (zawsze `permissive` w obu
  próbkach), `metadata.gha_license_id` (licencja repo z GH Archive, często `null`/`NOASSERTION`). `license` = złączone
  `detected_licenses`; gdy lista pusta, `license` = `""`.
- V (próbka: cały Python z pliku 0084, 174 868 wierszy): 873 wiersze (0,50%) mają `license` = `""` i puste
  `detected_licenses`; licencję daje wtedy tylko `gha_license_id` (539 BSD-3-Clause, 266 MIT, 56 Apache-2.0, 8
  BSD-2-Clause, 3 BSD-3-Clause-Clear, 1 Unlicense). Wszystkie pozostałe identyfikatory z próbki (MIT 115 911, Apache-2.0
  37 305, BSD-3-Clause 14 674, BSD-2-Clause 5 798, Unlicense 2 027, CC0-1.0 1 256, Python-2.0 707, ISC 635, …, ZPL-2.1,
  BSL-1.0, Artistic-2.0, NCSA, AFL-3.0, PSF-2.0, LPPL-1.3c, MS-PL) są na liście Blue Oak Council
  (https://blueoakcouncil.org/list.json, wersja 16, 225 licencji; porównanie po identyfikatorze SPDX).
- V: w pliku 0000 (Markdown) wiersz z pustą `license` miał `gha_license_id` = `CC-BY-4.0`, którego NIE ma na liście
  Blue Oak (Common Pile uznaje CC BY za otwartą, praca §2). W Pythonie z 0084 takiego przypadku nie było.
- V (praca, „The Stack V2”): licencje to detekcja twórców Stack v2 na poziomie repozytorium; przy kilku licencjach
  wszystkie muszą być „openly licensed”. Karta: „license laundering and inaccurate metadata can cause us to erroneously
  assign the incorrect license”; zgłoszenia przez dyskusje repo.
- I: licencja jest licencją repo, nie konkretnego pliku; plik skopiowany z innego projektu (vendoring, wklejki ze
  StackOverflow na CC BY-SA) może mieć inne prawa. `is_vendor` = true tylko w 28 wierszach Pythona 0084.
- V: repo HF nie ma pola `license` w karcie (`cardData.license` = null); licencji kompilacji brak.
- Opt-out TDM: NIE SPRAWDZONE. Licencje permisywne pozwalają na trening z samego brzmienia; Stack v2 miał własny
  proces opt-out („Am I in the Stack”) — czy ta kopia uwzględnia późniejsze opt-outy: nie sprawdzone.

**Bramka „można TRENOWAĆ”: TAK.** Podstawa: licencja per plik z listy Blue Oak (V dla 99,5% Pythona próbki), dla
reszty licencja repo z `gha_license_id` (V, wszystkie z listy Blue Oak). Zapasowo wyjątek TDM art. 4 dyr. 2019/790;
ścieżka takedown: usunięcie po `id` (= `blob_id`, V: zgodne w 100% próbki) albo `repo_name` w kolejnej wersji.
Warunek: odrzucić wiersze z pustą `license` I `gha_license_id` spoza Blue Oak / null.

**Bramka „można ZGŁOSIĆ”: TAK, warunkowo** — dla wierszy z niepustą `license` z listy Blue Oak (licencja per dokument,
bez NC/ND). Wiersze z pustą `license` (0,5%): odrzucamy ze zgłoszenia (licencja tylko na poziomie repo z GHA). Opt-out
TDM per repo nie sprawdzony; przy licencjach MIT/BSD/Apache opt-out nie zmienia uprawnienia licencyjnego (I).
Wymogi atrybucji (MIT, BSD, Apache: zachowanie notki) spełniamy, zachowując `metadata.url`, `repo_name`, `license` w
wierszu zgłoszenia.

## 3. Zawartość

- V: pola wiersza: `added`, `created`, `id`, `int_score`, `metadata` (obiekt JSON, nie string), `score`, `source`
  (= `stackv2`), `text`. Pole tekstu: **`text`** (cały plik źródłowy).
- V: `metadata` ma: `blob_id, branch_name, committer_date, content_id, detected_licenses, directory_id, extension,
  filename, fork_events_count, gha_created_at, gha_event_created_at, gha_language, gha_license_id, github_id,
  is_generated, is_vendor, language, length_bytes, license, license_type, path, provenance, repo_name, revision_date,
  revision_id, snapshot_id, src_encoding, star_events_count, url, visit_date`.
- V: adres źródłowy jest gotowy w `metadata.url` =
  `https://raw.githubusercontent.com/{repo_name}/{revision_id}{path}` (`path` zaczyna się od `/`); zgodność wzoru w
  100% z 174 868 wierszy. Strona repo: `https://github.com/{repo_name}/blob/{revision_id}{path}` (I, ten sam wzór).
- V: filtr języka: `metadata.language == "Python"`.
- V (praca §4.1): heurystyki kodu RedPajama V1, potem klasyfikatory „edu” SmolLM2 per język z progiem NIŻSZYM niż w
  SmolLM2. V (próbka): `int_score` w Pythonie 0084: 2 → 79 347, 3 → 83 842, 4 → 11 203, 5 → 476 (45% wierszy poniżej
  progu SmolLM2 = 3). Klasyfikator trenowany na etykietach Llama3-70B-Instruct (SmolLM2, dod. D.1) — tekst nie jest
  generowany, model tylko oceniał.
- V: plik 0084 to Python ze `stack-edu-0066` upstream; w pozostałych 11 plikach Pythona proporcji nie liczono.

## 4. Skala i dostęp

- V: jeden plik (0084): 987 435 422 B gz, sha256 `5e2ad7d634976f90694a2f644922a6fc92b54d624958440eea532a7ae2bda3b8`
  (= LFS oid), 4 127 136 525 B po rozpakowaniu, **928 213 wierszy** (174 868 Python + 753 345 Ruby). Python: 838 342 673
  B tekstu (śr. 4,8 kB / plik).
- V: tokenizer v6 (`SlayerLab/Slayer1B-1.07@a090b54e`, `tokenizer.json` sha256 `0640d3bd…815dd`, słownik 32 768),
  co 50. wiersz Pythona 0084: 17 389 101 B → 5 509 952 tokenów (z EOT), **3,16 B/token**. Plik 0084 = ok. 0,27 mld
  tokenów v6 samego Pythona.
- I: pliki 0073–0083 są w całości Pythonem i mają ten sam stopień kompresji co 0084 (~4,2:1) → ok. 11 × 4,1 GB + 0,84 GB
  ≈ 46 GB tekstu ≈ **14–15 mld tokenów v6** Pythona. Dla porównania SmolLM2 (Tab. 7, V): Stack-Edu Python 21,8 mld
  tokenów (tokenizer StarCoder, próg 3, bez filtra licencji).
- I: cel 0,25 mld tokenów to ok. 1,7% Pythona; sam `int_score ≥ 3` z jednego pliku (54% wierszy) daje ~0,15 mld, więc
  wystarczą 2 pliki z progiem 3 albo 1 plik bez progu. Zapas na dedup i filtry jest duży.
- V: dostęp z HF bez bramki (`resolve/<rewizja>/stack-edu-NNNN.json.gz`), ok. 2 min na plik.

## 5. Ryzyka

- PII — V: Common Pile NIE zredagował PII w kodzie: Stack V2 nie ma kolumny PII w Tab. 3 pracy; redakcja
  `<EMAIL_ADDRESS>` dotyczyła tekstu z HTML (§4.1). W Pythonie 0084: 0 wystąpień `<EMAIL_ADDRESS>`, 8 216 plików (4,7%)
  z adresem e-mail (regex), np. `__email__ = "..."`, nagłówki `# (C) … <adres>`, listy autorów. Plan: maskowanie
  adresów (zamiana na znacznik), nie usuwanie plików; adresy w rodzaju `admin@example.com` też łapie regex.
- Sekrety — V (regex, Python 0084): przypisania `api_key/secret_key/password/token = "…"` 1 401 plików (0,8%, dużo
  fałszywych: hasła testowe, wartości przykładowe); klucze Google `AIza…` 51, AWS `AKIA…` 17, `-----BEGIN … PRIVATE
  KEY-----` 14, tokeny Slack 9; GitHub `gh*_` i OpenAI `sk-` 0. Plan: odrzucić pliki z kluczami o rozpoznawalnym
  formacie (AWS, Google, prywatne klucze, Slack) i maskować przypisania sekretów.
- Kod generowany — V: `is_generated` = true w 2 wierszach; nagłówki typu „auto-generated / generated by / do not
  edit / protoc / Django” w pierwszych 2 kB: 3 111 plików (1,8%; obejmuje migracje Django i pliki PyQt). Plan:
  odrzucić po nagłówku. Kod pisany przez LLM (lata 2023+) — nie da się odróżnić; I: `revision_date` pozwala ograniczyć,
  daty nie analizowane.
- Kontaminacja — V (heurystyka, Python 0084): sygnatury lub fragmenty promptów HumanEval w 47 plikach (dużo fałszywych:
  `factorize(`, `strlen(`, `longest(strings` w zwykłym kodzie); zdania MBPP dosłownie: 0; frazę „Write a function to”
  ma 19 plików. Common Pile nie opisuje dekontaminacji wobec testów kodu (I: brak w §4.1). Plan: 13-gramy wobec HumanEval,
  MBPP i reszty ~60 testów (GSM8K, MATH, MMLU, MathQA, GSM-Plus, GSM1k); repozytoria z rozwiązaniami HumanEval/MBPP
  usuwamy po `repo_name`.
- Kopie — I: Stack v2 deduplikowany na poziomie plików przez BigCode; forków i kopii wewnątrz zbioru Common Pile nie
  opisuje. Dedup wewnątrz zbioru i wobec EN 1.07 i walidacji Fabryki obowiązkowy.
- Licencje — V/I: patrz §2 (licencja repo ≠ pliku, ryzyko „license laundering” z karty).
- OCR: nie dotyczy.

## 6. Nowość

- V (z kontekstu zespołu): kodu Slayer prawie nie widział. Skład 1.09: FineWeb-Edu EN, GoLLeM web, FinePDFs-Edu PL,
  FineWeb-2 PL; 1.07 `en_mix` (`SlayerLab/slayer-1.07-pretrain@6a337bbf`, z `SlayerLab/minimal-en-corpus-5b`): FineMath,
  open-web-math, FineWeb-Edu, DCLM — bez kodu z GitHuba.
- I: 1.08b (niewydany) miał self-oss-instruct i OpenCodeReasoning — syntetyczne zadania kodowe, nie pliki z repo; te same
  funkcje mogą się powtarzać jako ziarna (self-oss-instruct powstał z The Stack), stąd dedup wobec nich, jeśli 1.08b
  wejdzie do historii.
- I: przyrost pokrycia duży (nowa dziedzina: kod Pythona z repozytoriów). Dowód efektu z publikacji (cudze wyniki):
  SmolLM2-1.7B, annealing 200 mld tokenów kodu, HumanEval 20,7 → 25,6 wobec niefiltrowanego StarCoder2Data (arXiv
  2502.02737 Tab. 2); testów ogólnych nie mierzono. „To Code, or Not To Code?” (2408.10914): cooldown z 20% kodu
  +3,6% wzgl. rozumowanie przy 470M. DeepSeekMath (2402.03300): kod i matematyka razem w jednym etapie przy 1,3B
  obniżyły GSM8K 20,5 → 17,6 — ramię D mierzyć wobec B/C. Common Pile nie publikuje ablacji per źródło.

## Nie sprawdzone

- Proporcje licencji, PII, sekretów, kodu generowanego i `int_score` w plikach 0073–0083 (liczone tylko na 0084).
- Liczba wierszy i bajtów Pythona w całości (14–15 mld tokenów v6 to ekstrapolacja z jednego pliku).
- Szczegóły detekcji licencji Stack v2 (karta `bigcode/the-stack-v2` za bramką, nie odczytana) i próg klasyfikatora
  „edu” użyty przez Common Pile (praca: tylko „lower threshold”).
- Opt-out TDM i opt-outy „Am I in the Stack” po dacie zrzutu Software Heritage.
- Czy licencja repo odpowiada licencji każdego pliku (vendoring, kopie z innych projektów).
- Dekontaminacja wobec testów kodu u Common Pile/SmolLM2; dokładne 13-gramy (zrobione tylko heurystyki tekstowe).
- Nakładanie z danymi 1.08b (self-oss-instruct, OpenCodeReasoning) i z walidacją Fabryki.
- Daty plików (`revision_date`) jako filtr kodu pisanego przez LLM.
