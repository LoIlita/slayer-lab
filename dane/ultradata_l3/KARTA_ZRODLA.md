# Karta źródła: UltraData-Math L3 (EN, matematyka syntetyczna) dla Slayera 1B

Zapisana 26.11.2026 przed pobraniem zbioru. Zbadane po jednym pliku (`part-0000-of-50`) z każdego z 4 podzbiorów L3,
w `/tmp`, usunięte po pomiarze. Rezerwacja: https://github.com/slayerlabs/benchmarks-fabryka-ai/issues/346

Rola: ~7 mld tokenów v6 dopełnienia zbioru matematyki 20 mld (zamiast FineMath-3+, który odpadł: 19–23% śmieci).
Właścicielka chce zbioru dobrej jakości. Oznaczenia: V = sprawdzone 2026-11-26 w podanym źródle (URL, rewizja, hash,
pomiar), I = wywnioskowane.

## 1. Identyfikacja

- V: https://huggingface.co/datasets/openbmb/UltraData-Math, rewizja `fe10db8efd35597fd7fcff8ff576b5ec4ea5ff87`
  (lastModified 2026-04-15, bez bramki dostępu). Warstwa L3, 4 configi:
  `UltraData-Math-L3-{Conversation,Multi-Style,QA,Textbook-Exercise}-Synthetic`, po 50 plików
  `data/UltraData-Math-L3/<podzbiór>/UltraData-Math-L3-<podzbiór>-part-00NN-of-50.parquet`.
- V: wydawca OpenBMB / ModelBest + Tsinghua; praca „Data Science and Technology Towards AGI Part I: Tiered Data
  Management”, arXiv 2602.09003 (§2.2.4 L3, §3.3 UltraData-Math). Kod generatora:
  https://github.com/UltraData-OpenBMB/UltraData-Math (`UltraData-Math-L3-Generator/`: prompty `qa_synthesis.py`,
  `conversation_synthesis.py`, `multistyle_rewrite.py`, `knowledge_textbook.py`).
- V (karta): L3 = 88 mld tokenów, 81,4 mln dokumentów (tokenizer nie podany; ablacje na MiniCPM3-4B).
- V (karta, Acknowledgements): generatory L3 Qwen2.5-72B-Instruct, Qwen3-32B, GLM-4.5; ziarna („Seed Data”)
  Nemotron-CC-Math-v1, MegaMath, FineMath. Praca (§2.2.4): „multi-model ensemble strategy”, bez przypisania modelu ani
  ziarna do podzbioru.

## 2. Prawa

- V: licencja karty Apache-2.0 (`license: apache-2.0`, sekcja License); praca arXiv: CC BY 4.0 (dotyczy tekstu pracy).
- V: licencje generatorów (karty HF): Qwen3-32B Apache-2.0 (sha `9216db57`); GLM-4.5 MIT (sha `cbb2c7cf`);
  Qwen2.5-72B-Instruct „Qwen License” (sha `495f3936`), §5b: przy trenowaniu na wyjściach modelu udostępnianego
  „prominently display »Built with Qwen« or »Improved using Qwen« in the related product documentation”; §4: limit
  100 mln MAU. Żaden nie wymaga zmiany nazwy modelu. I: obowiązek „Built with Qwen” w dokumentacji Slayera.
- V: polityka „zero modeli zamkniętych”: karta wymienia tylko otwarte modele. ALE V: publiczny skrypt generatora
  (`run_synthesis.py`, README) ma domyślnie `--model gpt-4o` przez API OpenAI. I: to domyślny parametr, nie dowód
  użycia; zbiór nie pozwala tego sprawdzić per wiersz (niżej).
- V (KLUCZOWE): schemat wszystkich 4 podzbiorów to tylko `uid` (UUID) i `content` (tekst). **Brak pola ziarna /
  źródła / URL / generatora / stylu / poziomu.** Wykluczenie wierszy z ziarnem MegaMath ani z danym generatorem
  NIE jest możliwe z metadanych.
- V: ziarno MegaMath: MegaMath-Web-Pro rafinowany Llama-3.3-70B-Instruct (karta wpisu rejestru, MegaMath §B.2);
  MegaMath-QA częściowo Llama-3.3. Które części MegaMath posłużyły za ziarno — praca i karta nie mówią.
  Próba pomiaru (V): z 1 pliku MegaMath-Web-Pro (`IFM/MegaMath@3cbc6461`, `megamath-web-pro/000_00000.parquet`,
  163 968 dok., 1,1% bajtów Web-Pro) dokumenty L3 z ≥3 trafieniami próbkowanych (1/32) 13-gramów: conv 2 574 / 337 611
  (0,76%), ms 2 984 / 228 911 (1,30%), qa 817 / 542 274 (0,15%), tb 1 742 / 520 101 (0,33%). I: ekstrapolacja ×90
  dla ms dałaby >100%, więc trafienia to w dużej części wspólny tekst stron (Wikipedia, formuły), który jest też w
  surowym webie — pomiar NIE odróżnia ziarna Web-Pro (Llama) od ziarna FineMath/Nemotron o tej samej stronie.
  Wniosek I: L3 na pewno przetwarza strony obecne w Web-Pro; czy jako tekst po Llamie — nieustalone i nieustalalne
  bez pola ziarna.
- V: ziarno Nemotron-CC-Math-v1 (`nvidia/Nemotron-CC-Math-v1@397a2502`, bramka „auto”): licencja „NVIDIA Data
  Agreement for Model Training”: §2.1 tylko „internal training of Company AI Solutions”, §2.2.2 zakaz
  „distribute … or otherwise make available to others”, §2.2.3 zakaz „cause them to become subject to an
  open-source license”; plus klauzula Phi-4 (tekst czyszczony Phi-4, licencja MIT). I: Apache-2.0 na przepisaniach
  ziaren Nemotron jest wątpliwa w łańcuchu praw (czy przepisanie to „portion of the Datasets” — nierozstrzygnięte).
- Bramka „można TRENOWAĆ”: **WARUNKOWO (decyzja właścicielki)**. Za: licencja Apache-2.0, generatory otwarte (wg
  karty), tekst L3 jest wyjściem Qwen/GLM, nie Llamy. Przeciw: (a) polityki „zero tekstu Llamy” nie da się
  zagwarantować filtrem — część wierszy to I przepisania tekstu po Llama-3.3 (Web-Pro), a licencja Llama 3.3 wiąże
  „outputs or results” — czy obejmuje przepisanie przez inny model, nierozstrzygnięte; (b) wiersze z ziarnem
  Nemotron dziedziczą I umowę NVIDIA (trening wewnętrzny dozwolony, więc dla treningu ryzyko niskie). Takedown: po
  `uid` możliwy, po URL strony źródłowej NIE (brak URL).
- Bramka „można ZGŁOSIĆ”: **NIE** — redystrybucja zbioru pochodnego koliduje I z §2.2.2 umowy NVIDIA (ziarna
  Nemotron nieodróżnialne), łańcuch Llamy nierozstrzygnięty, prawa tekstów stron (TDM) jak w karcie FineMath-4+.

## 3. Zawartość i format

- V: angielski; CJK (≥5 znaków) w 2–23 na 20 000 dok. na podzbiór; karta deklaruje EN+ZH dla całego zbioru, w
  zbadanych plikach L3 chińskiego praktycznie brak.
- V (odczyt 15 wierszy na podzbiór + pierwsze linie 20 000 dok.):
  - **Conversation-Synthetic**: dialog, 7 par ról z promptu (Professor A/B, Teacher/Student, Interviewer/Interviewee,
    Student1/2, Layman/Expert…), szablony otwarć („Professor A: Good morning, Professor B.” 720/20 000 jako pierwsza
    linia, „Interviewer: Can you expl…” 963/20 000 jako prefiks 25 znaków). Często przepisane zestawy zadań w
    formie „pytanie → rozwiązanie → »That's correct!«”, ślady źródła („The content suggests…”, odwołania do
    nieistniejących rysunków).
  - **Multi-Style-Synthetic**: tekst ciągły w 7 stylach (wiki, podręcznik, blog, popularnonaukowy, artykuł, notatki,
    wykład); szablonowe tytuły („# Unlocking the Secrets o…”, „# Diving into the World o…”), puste „abstrakty i
    bibliografie”; część to zbiory zadań z rozwiązaniami. V: 2/15 tekstów urwanych.
  - **QA-Synthetic**: zadanie + rozwiązanie krok po kroku („Step 1…”); powtarzalne otwarcia zadań („A rectangular
    garden has…” 302/20 000, „A high school is planning…” 259/20 000).
  - **Textbook-Exercise-Synthetic**: objaśnienie punktu wiedzy + „The exercise:” + „The solution:” (sztywny szablon
    15/15); otwarcia „**Explanation:**”/„The given mathematical knowledge point…”. Wiele ćwiczeń trywialnych
    (sprawdź przemienność mnożenia).
- V format MCQ (regex na 20 000 dok.; luźny wzór „answer/correct option is X”, bez weryfikacji ręcznej każdego):
  conv 293 (1,5%), ms 180 (0,9%), qa 42 (0,2%), tb 2 (0,01%); listy opcji A)/B) w linii: 68 / 53 / 82 / 1.
  V (przykłady): conv „The correct answer is B. 190.”, qa „Choose the correct answer: A) 5 B) 7 …”, ms „Option: 3”
  bez opcji. Do usunięcia filtrem (zespół odrzuca uczenie formatu testu).
- V: `\boxed` w 54 / 496 / 1 310 / 393 na 20 000 (conv/ms/qa/tb).

## 4. Skala i dostęp

Tokeny v6 = tokenizer `dane/dclm-en/robocze/pobrania/tokenizer_v6/tokenizer.json`, współczynnik tok./znak z 20 000
losowych dok. pliku 0, przemnożony przez znaki całego pliku; ×50 = ekstrapolacja I (pliki równej wielkości: V
rozpiętość rozmiarów ≤0,2%).

| podzbiór | pliki | rozmiar (V, API) | wiersze plik 0 (V) | tok. v6 plik 0 (V) | tok. v6/dok. | ×50 wiersze (I) | ×50 tok. v6 (I) |
|---|---|---|---|---|---|---|---|
| Conversation | 50 | 30,80 GB | 337 611 | 387,6 mln | 1 148 | 16,9 mln | 19,4 mld |
| Multi-Style | 50 | 29,46 GB | 228 911 | 372,4 mln | 1 627 | 11,4 mln | 18,6 mld |
| QA | 50 | 29,80 GB | 542 274 | 473,4 mln | 873 | 27,1 mln | 23,7 mld |
| Textbook-Exercise | 50 | 32,48 GB | 520 101 | 508,9 mln | 978 | 26,0 mln | 25,4 mld |
| razem | 200 | 122,5 GB | | | | 81,4 mln | 87,1 mld |

- V: suma wierszy ×50 = 81,4 mln, zgodne z kartą (81,4 mln); 87,1 mld v6 vs 88 mld karty.
- V sha256 plików 0 (zgodne z LFS oid): conv `8c44bbb2…a148`, ms `f5b85476…c262c2`, qa `70323fec…ebac`,
  tb `5ba7567a…f6c7`. V: `uid` unikalne i `content` bez dokładnych duplikatów w każdym pliku 0.
- V: dostęp bez bramki, `resolve/<rewizja>/...`.

## 5. Ryzyka

### Jakość (najważniejsze) — 15 losowych wierszy na podzbiór, każdy rachunek przeliczony (python), V

| podzbiór | błąd istotny | błąd drobny | śmieć/urwane | OK | typowe błędy |
|---|---|---|---|---|---|
| Conversation | **4/15 (27%)** | 4 | 0 | 7 | 1/21 zapisane jako „5/21 ≈ 23,81%”; kąt wpisany 30° → środkowy 30°; zmyślona fizyka (E=mv², prawo Wiena z wykresu prądu); błędny iloczyn w liście ~50 ćwiczeń |
| Multi-Style | **4/15 (27%)** | 6 | 2 urwane, 1 w połowie śmieć | 5 | fałszywe twierdzenie o środkowej trapezu; 63·62·61=231036 (jest 238266), prawdopodobieństwo >1; rh=105 zamiast 105/π; zamienione G/G* w zamianie zmiennych |
| QA | **2/15 (13%)** | 3 | 0 | 10 | zmyślony wynik „numerical solver” (lstsq daje inne współczynniki); sprzeczna treść geometrii (punkty niesymetryczne) i niespójne CD/EF; treści zadań ze sprzecznymi danymi przemilczane |
| Textbook-Exercise | **2/15 (13%)** | 3 | 0 | 10 | „3+6=8” dopasowane do narzuconej odpowiedzi + lista ze sprzecznością; asymptotyka $(1/3)^n$ zamiast $3^n$ |

- I: przy n=15 przedział 95% dla 2/15 to ok. 2–40%, dla 4/15 ok. 8–55% — liczby to sygnał, nie pomiar precyzyjny.
  Proste rachunki są poprawne; błędy rosną z trudnością (kombinatoryka, regresja, geometria analityczna) i z długością
  (listy wielu zadań). Wzorzec wspólny: model dopasowuje rozwiązanie do narzuconej/zmyślonej odpowiedzi, „autokorekty”
  zostawiają błędne kroki pośrednie.
- Porównanie I: CraneMath ~20% błędnych przepisań; QA i Textbook (13%) podobnie lub lepiej, Conversation i
  Multi-Style (27%) gorzej.

### Dekontaminacja

- V: karta i praca nie opisują dekontaminacji L3 (szukano „decontam”/„contamina” w pracy: tylko w opisie FineMath).
- V (pomiar, pełne pliki 0, 13-gramy słów): GSM8K test (1 319) — **0 trafień** we wszystkich 4 plikach. MATH-500
  (500): trafienia głównie ogólnymi wzorami („frac x h 2 a 2 frac y k 2 b 2 1”, „volume of a cone is given by…”);
  dokumenty zawierające ≥50% 13-gramów zadania MATH-500: conv 0, ms 1 (#110), qa 1 (#224), tb 1 (#474).
  I: ×50 ≈ 50 dok. na podzbiór — niski poziom, ale nasze 13-gramy wobec testów Fabryki obowiązkowe.
- I: ziarna to web (FineMath, MegaMath, Nemotron), nie MATH/GSM8K-train; przecieki dziedziczone z ziaren (FineMath
  dekontaminowany wobec GSM8K/MATH/MMLU/ARC, MegaMath 13-gramami wobec 12 testów, Nemotron — nie sprawdzono).

### Inne

- PII: tekst syntetyczny, przepisany — I: niskie ryzyko; brak skanu.
- Monotonia: sztywne szablony (wyżej) — I: ryzyko uczenia stylu, łagodzone mieszanką z FineMath-4+/InfiWebMath-4+.
- Zmyślone konteksty (nazwy kursów, „problem likely includes…”) — V w próbce ms i tb.

## 6. Nowość i nakładanie z naszymi danymi

- V (karta): ziarna obejmują FineMath → część L3 to przepisania stron, które mamy w FineMath-4+ (cała, w zbiorze 20
  mld). Tekst jest inny (dialog/QA/styl), treść ta sama.
- V (pomiar): 2 000 losowych dok. z pliku 0 każdego podzbioru vs **pełny FineMath-4+** (64/64 pliki
  `dane/finemath4/robocze/pobrania/lok/*.rg5000.parquet`), 13-gramy słów próbkowane 1/4:

  | podzbiór | dok. z ≥1 trafieniem | z ≥5 (≈ ≥20 wspólnych 13-gramów) | ≥25% tekstu w FM-4+ | ≥50% | średni udział tekstu |
  |---|---|---|---|---|---|
  | Conversation | 1 096 (55%) | 443 (22%) | 20 (1,0%) | 6 (0,3%) | 2,4% |
  | Multi-Style | 1 172 (59%) | 510 (26%) | 7 (0,35%) | 1 | 2,0% |
  | QA | 720 (36%) | 141 (7%) | 1 | 0 | 1,1% |
  | Textbook-Exercise | 1 221 (61%) | 404 (20%) | 2 | 0 | 2,4% |

- I: dosłownego kopiowania prawie nie ma (≤1% dok. ma ≥25% tekstu z FM-4+), ale ~20–26% dok. conv/ms/tb dzieli
  z FM-4+ dłuższe fragmenty (treść zadania, definicje) — to przepisania tych samych stron, czyli ta sama wiedza
  w innej formie. QA najmniej związany z FM-4+ (7%), więc najbardziej „nowy”. Część trafień to wspólne formuły i
  definicje, nie ziarno (górna granica). Dedup URL-owy niemożliwy (brak URL); dedup MinHash nie usunie przepisań —
  nakładanie treści trzeba przyjąć jako kontrolowane powtórzenie (podobnie jak CraneMath = przepisany FM-4+).
- I: Slayer 1.07/1.09 nie zawierały UltraData (brak w opisach składu i w rejestrze poza wpisem kandydata).
- Efekt (notatka `wplyw-zbiorow-2-matematyka-syntetyczna`, V tam): MiniCPM-1.2B anneal 10 mld (30% zbioru) L3 vs L1
  MATH500 +5,4, GSM8K +8,7; decay ~100 mld bez spadków ogólnych. Ablacji per podzbiór L3 brak (I: nie wiadomo, który
  podzbiór daje zysk).

## 7. Rekomendacja (~7 mld v6)

- **QA-Synthetic + Textbook-Exercise-Synthetic, po ~3,5 mld v6**: 8 plików QA (I ≈ 3,8 mld) + 7 plików Textbook
  (I ≈ 3,6 mld) ≈ 7,3 mld przed filtrami. Dlaczego: najniższy odsetek błędów istotnych w próbce (13% vs 27%), brak
  urwań, najmniej MCQ (tb ~0%, qa 0,2–0,4%), format zadanie + rozwiązanie najbliższy temu, co dało zysk w ablacjach
  (QA/CoT); dwa różne szablony zmniejszają monotonię. QA najmniej powtarza FineMath-4+ (7% dok. z dłuższym
  wspólnym fragmentem vs 20–26% w pozostałych) — jeśli trzeba ciąć, ciąć Textbook na rzecz QA.
- Odrzucić Conversation (27% błędów, 1,5% MCQ, ślady źródła, szablony ról) i Multi-Style (27% błędów, urwania,
  puste „artykuły”).
- Warunki przed użyciem: (1) decyzja właścicielki o łańcuchu Llamy (MegaMath-Web-Pro) i Nemotron — filtr po polu
  niemożliwy; (2) filtr MCQ (regex jak wyżej) i 13-gramy wobec testów Fabryki; (3) dedup URL-owy niemożliwy (brak
  URL), więc nakładanie z FineMath-4+ zostaje (patrz §6); (4) większa próba jakości przed decyzją (np. 100 wierszy na
  podzbiór z automatycznym przeliczeniem wyniku końcowego) — 13% przy n=15 nie dowodzi „dobrej jakości”.
- I: jeśli wymóg „dobrej jakości” ma być twardy (<10% błędów istotnych), L3 go w próbce NIE spełnia; alternatywa
  bez Llamy: CraneMath (Qwen3-32B, ~20% błędów wg zespołu) — podobny poziom.

## Nie sprawdzone

- Który generator i które ziarno per podzbiór / per wiersz (brak pól; praca nie podaje); czy użyto GPT-4o (domyślny
  model skryptu).
- Czy przepisanie tekstu Llama-3.3 przez Qwen podlega klauzuli nazwy Llama 3.3 (prawnie).
- Pełna treść licencji Nemotron-CC-Math w rewizji z daty powstania L3 (czytano wersję `main` pliku LICENSE).
- Udział ziaren MegaMath-Web-Pro w L3 (pomiar 1 pliku nie odróżnia Web-Pro od surowego webu).
- Odsetek błędów na większej próbie; jakość pozostałych 49 plików na podzbiór.
- Dekontaminacja wobec testów Fabryki poza GSM8K i MATH-500.
- Wpływ szablonów na testy ogólne przy 1B i budżecie ~7 mld (ablacje autorów tylko na całym L3).
