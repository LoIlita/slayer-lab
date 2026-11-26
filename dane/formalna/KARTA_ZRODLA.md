# Karta źródła: formalna (biblioteki matematyki formalnej i Stacks Project) dla Slayera 1B

Zapisana 26.11.2026 14:23 CET (mtime 14:23:56), przed klonowaniem repozytoriów (start klonu 14:24:05 CET) i przed
pierwszym liczeniem. Preregistracja: `skrypty/preregistracja.json` (14:23:13 CET). Rezerwacja: https://github.com/slayerlabs/benchmarks-fabryka-ai/issues/357
(część 3 zbioru matematyki). Kandydaci z pomiarami: `dane/matematyka-wspolne/kandydaci_czyste.md` (B1–B6).

Oznaczenia: V = sprawdzone 26.11.2026 (URL, rewizja, plik), I = wywnioskowane.

## 1. Identyfikacja

Jedno źródło „formalna”, dziewięć bibliotek, każda z rewizją zamrożoną 26.11.2026 14:21 CET (V: API GitHub
`repos/<repo>/commits/<prefiks>` rozwiązało prefiksy z kandydatów do pełnych sha):

| biblioteka | repo | rewizja | data commita rewizji (V) | pliki |
|---|---|---|---|---|
| mathlib4 | github.com/leanprover-community/mathlib4 | `e54979a532247ae4eb9d5578a8fd40a1bc332101` | 2026-11-26 | `.lean` |
| afp | github.com/isabelle-prover/mirror-afp-devel | `02fd3c6b5326d1c53704c52c09cabb3fd2a772f5` | 2026-11-25 | `.thy` |
| hol_light | github.com/jrh13/hol-light | `096417cac706ff0818f739bbc19f2ed499e43283` | 2026-11-24 | `.ml` |
| setmm | github.com/metamath/set.mm | `ce7f29d6bb49ca66913cc4adae72bb4df5bcb854` | 2026-11-26 | `set.mm`, `iset.mm` |
| rocq_stdlib | github.com/rocq-prover/stdlib | `9657c7502ceb46ec94131c7500d9e484e1dddf3b` | 2026-11-26 | `.v` |
| mathcomp | github.com/math-comp/math-comp | `656cdbcf752c1624c8afb245886b05dfd16b227c` | 2026-11-26 | `.v` |
| unimath | github.com/UniMath/UniMath | `11e01f098e50285e9ec93fce1f09e57417342eec` | 2026-11-25 | `.v` |
| agda_stdlib | github.com/agda/agda-stdlib | `119d176134c44bcb5aad56bb6ce69bc97851c094` | 2026-11-26 | `.agda`, `.lagda.md` |
| stacks | github.com/stacks/stacks-project | `a04446e57ec1fbc252a871afcec7752fb2807b14` | 2026-07-28 | `.tex` |

Dokument = jeden plik. Wyjątki: set.mm/iset.mm (pliki po 40+ MB) dzielone na sekcje Metamath do 50 000 znaków; pliki
> 1 MB w Stacks dzielone na `\section`, w pozostałych bibliotekach wykluczone (reguły w preregistracji, pole
`dokument`). `url` każdego wiersza to `github.com/<repo>/blob/<rewizja>/<ścieżka>` (dla fragmentów z `#L<od>-L<do>`),
więc każdy wiersz da się odtworzyć i wycofać.

## 2. Prawa

| biblioteka | licencja (SPDX) | podstawa |
|---|---|---|
| mathlib4 | Apache-2.0 | V: `LICENSE` (Apache 2.0) na rewizji; I: nagłówki plików „Released under Apache 2.0 license” (sprawdzane przy budowie) |
| afp | per wpis: `bsd` → BSD-3-Clause, `lgpl` → LGPL-2.1-only | V: `metadata/entries/Bernoulli.toml` ma `license = "bsd"`; kandydaci (V): 1 017 × bsd, 26 × lgpl; I: mapowanie SPDX do potwierdzenia tekstem LICENSE po klonie |
| hol_light | BSD-2-Clause | V: `LICENSE` „Redistribution and use… permitted” z dwoma warunkami; V: „Some files in this package are distributed under other licenses; please check individual files or subdirectories” → pliki z inną licencją wykluczone (reguła w preregistracji) |
| setmm | CC0-1.0 | V: `LICENSE` „CC0 1.0 Universal” |
| rocq_stdlib | LGPL-2.1-only | V: `LICENSE` LGPL 2.1; V: nagłówek `theories/Arith/PeanoNat.v` „GNU Lesser General Public License Version 2.1” bez „or later” |
| mathcomp | CECILL-B | V: plik `LICENCE` „CeCILL-B FREE SOFTWARE LICENSE AGREEMENT” (licencja typu BSD, bez copyleft) |
| unimath | LicenseRef-UniMath | V: `LICENSE.md` (18 wierszy): tekst MIT z „UniMath” zamiast „the Software”; I: równoważna MIT |
| agda_stdlib | MIT | V: `LICENCE` (tekst MIT) |
| stacks | GFDL-1.2 | V: `COPYING` „GNU Free Documentation License Version 1.2”; I: wariant only/or-later do ustalenia po klonie |

- Bramka „można TRENOWAĆ”: **TAK** — każda biblioteka ma licencję otwartą bez NC/ND (V, tabela). Takedown: po
  `url`/`path` wiersza.
- Bramka „można ZGŁOSIĆ”: **TAK** dla wierszy z licencją z tabeli; licencja jest per wiersz (AFP per wpis).
  Warunki licencji przy redystrybucji (Apache/BSD/MIT/CeCILL-B: zachowanie nagłówków i informacji o prawach;
  LGPL/GFDL: copyleft dokumentu) — nagłówki plików zostają w tekście (I: spełnia wymóg zachowania nocy prawnych
  dla plików źródłowych; GFDL wymaga dołączenia licencji przy redystrybucji — do datasheet).
- Pochodzenie tekstu: ludzki (V wg kandydatów); I: polityka mathlib4/AFP wobec wkładu generowanego przez LLM nie
  sprawdzona — biblioteki są recenzowane przez opiekunów, każdy dowód sprawdza asystent dowodzenia.

## 3. Zawartość

- Kod formalny (Lean 4, Isabelle/Isar, OCaml HOL Light, Metamath, Rocq/Coq, Agda): definicje, twierdzenia, dowody,
  docstringi i komentarze. Stacks Project: LaTeX geometrii algebraicznej (twierdzenia i dowody w prozie).
- Decyzje wykluczeń (preregistracja, pole `zrodlo.biblioteki.*.wykluczone`):
  - mathlib4 `Mathlib/Tactic`, `Mathlib/Util`, `Mathlib/Lean`: metaprogramowanie Lean (taktyki, parsery, linters),
    nie matematyka; kod ludzki, ale cel części 3 to matematyka. `MathlibTest/` to testy. `Mathlib.lean` itp. to
    listy importów generowane przez `mk_all`. Pliki przeniesione z Lean 3 przez mathport („ported from Lean 3
    source module”) zostają: po porcie były ręcznie poprawiane i recenzowane (I).
  - set.mm/iset.mm: dowody w formacie skompresowanym (`$= ( etykiety ) ABCDEF… $.`) to ciągi liter bez wartości
    językowej; kandydaci (V): 59,9% / 55% bajtów. Zastępujemy je `$= ? $.` (składnia Metamath dla dowodu
    niekompletnego), zostają komentarze, definicje (`$a`), twierdzenia (`$p`) i hipotezy (`$e`).
  - testy i katalogi pomocnicze wszystkich bibliotek, pliki licencji i preambuły LaTeX.

## 4. Skala i dostęp

- I (kandydaci, V na tych samych rewizjach dla B1–B4, B5 na wcześniejszych sha z prefiksów): mathlib4 ~45 mln
  tokenów v6 (9 351 plików, 104,2 MB), AFP ~135 mln (10 562 `.thy`, 303,4 MB), HOL Light ~44 mln (980 `.ml`,
  87,1 MB), set.mm bez dowodów ~14 mln, B5 razem ~30 mln. Razem ~0,27 mld v6 przed wykluczeniami.
- Dostęp: publiczne repo git, bez bramki; `git clone --filter=blob:none` + checkout rewizji.

### B6: Proof-Pile-2 proofsteps (tylko szacunek, bez budowy)

`EleutherAI/proof-pile-2@901a9273a770e9d4138c5ddd91802f9c5c6cdc4b`, AlgebraicStack:
- V (kandydaci, 26.11): `isa_proofsteps` 258 108 dok., 1 766,8 MB, ~923 mln tokenów v6; `lean_proofsteps` 3 396 dok.,
  ~81 mln. Razem ~1,0 mld przed dedupem.
- I: pary stan dowodu → krok są silnie powtarzalne (te same stany w wielu dokumentach); po dedupie dokładnym i
  MinHash ~0,3–0,5 mld. Treściowo pochodne AFP + dystrybucji Isabelle (BSD/LGPL) i mathlib4 `c779bd5` (Apache-2.0),
  czyli nakładają się z afp i mathlib4 tej puli w innej formie.
- Wyekstrahowane narzędziem (PISA, lean-training-data), bez LLM (V wg pracy Llemma, dod. B.1.2–B.1.3, z kandydatów).
- Bramka ZGŁOSIĆ: NIEROZSTRZYGNIĘTY (licencja pochodna, brak pola licencji per wiersz; I). Budowa = osobna decyzja.

## 5. Ryzyka

- Kopie między bibliotekami i wersjami (np. pliki Isabelle w AFP, fragmenty stdlib w math-comp): `dedup_wewnatrz`.
- Testy: miniF2F/ProofNet nie są w indeksie Fabryki; mathlib4 `Archive/Imo` i wpisy AFP z zadaniami olimpijskimi mogą
  pokrywać się z miniF2F (I). Jeśli model będzie mierzony na miniF2F, potrzebny osobny pomiar przed eksportem.
- PII: e-maile autorów w nagłówkach (`Author: … <adres>`, I częste w AFP i HOL Light) — maskowane przy eksporcie
  (tryb `maskuj_email_usun_telefon_ip`), plik zostaje.
- Dane generowane: tabele liczb w HOL Light (kandydaci: „sporo tabel liczbowych”) i duże pliki — reguła > 1 MB.
- Kod mało „językowy” (taktyki, krótkie lematy): ocenia ręczna próbka (śmieci ≤ 10%).

## 6. Nowość

- I (kandydaci): znikome nakładanie z FineMath-4+/InfiWebMath-4+ (0 trafień `leanprover` w eksporcie FineMath,
  `isa-afp.org` 1 trafienie w InfiWebMath); `metamath.org` 320/266 351 i Stacks 21/266 351 w próbce FineMath-4+
  (strony HTML, nie źródła) — dedup MinHash wobec obu zbiorów w kaskadzie.
- Dowód wpływu: Llemma Tab. 4 (formal-to-formal miniF2F Lean 20,49 → 26,23, Isabelle 17,62 → 22,13 po AlgebraicStack).

## Nie sprawdzone (przed budową)

- Mapowanie `bsd`/`lgpl` AFP na SPDX i licencje AFP wpisów spoza tych dwóch wartości.
- Które pliki HOL Light mają inną licencję.
- Wariant GFDL Stacks (only / or-later) i licencja UniMath jako SPDX.
- Polityka bibliotek wobec kodu z LLM; opt-out TDM (nie dotyczy licencji otwartych, I).
- Pokrycie miniF2F/ProofNet przez mathlib4 Archive i AFP.

Rozstrzygnięcia tej listy po klonie: sekcja „Po klonie i budowie” niżej.

## Po klonie i budowie (dopisane 26.11.2026 od 14:46 CET)

Przebieg (godziny CET, logi w `robocze/logi/`): preregistracja 14:23:13, karta 14:23:56, klon 14:24:05–14:27:32
(`klon.log`, wszystkie 9 `rev-parse HEAD` = rewizja), aneks_2026_11_26 (licencje) 14:29, budowa 1 14:29:03–14:30:24
(`buduj.log`), aneks_2026_11_26b (commity z LLM) ok. 14:36, budowa 2 14:37:18–14:41:10 (`buduj2.log`), checkout
nowych rewizji 14:43:05, aneks_2026_11_26c (rewizje sprzed AI, decyzja integratora) ok. 14:43, budowa 3 (pula
końcowa) 14:43:41–14:45:30 (`buduj3.log`), kontrola kontraktu 14:46 (`wyniki/kontrakt.json`: PASS). Treść karty i
preregistracji sprzed klonu zmieniona po 14:24 tylko w godzinach zapisu (poprawka na rzeczywiste mtime) i przez
dopisane aneksy oraz tę sekcję; mtime plików jest więc późniejszy niż pule, kolejność potwierdzają godziny w treści
i logi.

### Licencje po klonie (aneks_2026_11_26)

- V AFP: `thys/LICENSE` = BSD 3 klauzule (BSD-3-Clause), `thys/LICENSE.LGPL` = LGPL 2.1 bez „or later”. Oznaczenie
  `License: LGPL` w pliku ma pierwszeństwo przed wpisem (57 plików LGPL we wpisach `bsd`, 2 z literówką `LPGL`).
  Toml: 1 017 × `bsd`, 26 × `lgpl`, wszystkie 1 043 wpisy w `thys/` mają toml.
- V HOL Light: `GL/COPYING`, `Quaternions/COPYING` = BSD-2 (inni właściciele praw) → BSD-2-Clause; `eval_compile/LICENSE`
  = MIT (tylko pliki `.hl`, poza regułą `*.ml`). Wykluczone nagłówkiem: `100/transcendence.ml` (public domain / CC0 —
  licencja otwarta, wykluczona regułą konserwatywnie), `Jordan/float.ml` (GPL). 94 pliki `.hl` nie wchodzą.
- V Stacks: `introduction.tex` „GFDL Version 1.2 or any later version; with no Invariant Sections…” →
  `GFDL-1.2-no-invariants-or-later`. GFDL przy redystrybucji wymaga dołączenia tekstu licencji (datasheet).
- V UniMath: `LICENSE.md` = tekst MIT z nazwą „UniMath” → `LicenseRef-UniMath` (I: równoważna MIT).
- V mathlib4: na rewizji 9bed6a56 brak nagłówka „Apache 2.0” w części plików-stubów (na rewizji listopadowej 112 plików
  `deprecated_module` z samym importem); takie pliki odpadną w `min_tresc`.

### Tekst z modeli (aneksy 2026_11_26b i 2026_11_26c)

- V: na rewizjach z 14:23 historia git ujawnia wkład modeli zamkniętych: mathlib4 709 commitów (od 2025-04; jeden z
  2023-10), m.in. masowe refaktory „Generated by Claude Opus, reviewed” (3 855, 1 310, 845 plików), „Prepared with
  Claude Code”, Codex, Aristotle (Harmonic), Gemini, GPT-4.1 (literówki); HOL Light 40 commitów (od 2026-01):
  katalog `Autoformalization/` („formalized entirely autonomously by AI systems”), `ANT/`, `Sieve/`, `Baker/`,
  przebudowa `Library/` („majority … developed by Claude Code”), `Co-Authored-By: Claude Opus 5.5`; UniMath 1 commit
  (7a4b03cc, 49 plików, `Co-authored-by: Claude Opus 5.5`); set.mm 22 (dowody GPT-f/OpenAI 2020, skracanie dowodów
  modelem 2025, mathbox OpenAI, cytaty odpowiedzi Claude). AFP, Rocq stdlib, math-comp, agda-stdlib, Stacks: 0.
- Wykrywanie: wzorzec PCRE na pełnej wiadomości commita (`git log -P --grep`), zapisany w `aneks_2026_11_26b.wzorzec`
  i `skrypty/buduj_pule.py` (`AI_WZORZEC`): nazwy i znaczniki narzędzi (`Claude Code/Opus/Sonnet/Fable/Haiku`,
  `noreply@anthropic.com`, ChatGPT, GPT-n, GPT-f, LLM, Copilot, Gemini, AlphaProof, DeepSeek, OpenAI, Anthropic,
  autoformaliz*, language model, AI-generated/assisted, „generated by AI”, „AI system”, Codex, Kimina, Goedel-Prover,
  Aristotle, aristotle-harmonic, Gauss AI, Math Inc). Plik zmieniony przez taki commit (diff wobec 1. rodzica) →
  wykluczony w całości; set.mm: fragment z „Contributed by OpenAI” albo „asking Claude” → wykluczony (2 fragmenty,
  40 573 tok.), adnotacje „(Proof shortened by OpenAI, …)” zostają (dowody usunięte).
- Decyzja integratora (aneks_2026_11_26c): mathlib4 i HOL Light na rewizjach sprzed pierwszego ujawnionego commita z AI:
  mathlib4 `9bed6a56adef68a259c58f72d5dc46ba3a68c176` (2025-03-31T22:40:31Z, #21800), HOL Light
  `b9a430b8fee43cc94babc8e3970cdd2740a994dc` (2025-12-11T20:28:06Z). Na nich reguła wyklucza: mathlib4 1 plik
  (`Mathlib/Data/List/Basic.lean`, commit z 2023-10, 22 507 tok.), HOL Light 0. UniMath: 49 plików, 578 161 tok.
- Pula odrzucona (rewizje z 14:23 + reguła per plik; usunięta z `robocze/`, liczby w
  `wyniki/budowa_odrzucona_rewizje_listopad.json`): 16 917 wierszy, 180 297 515 tok. v6; mathlib4 1 498 wierszy /
  4 038 490 tok. (6 866 plików wykluczonych, 38,7 mln tok.), HOL Light 467 / 6 370 279 (506 plików, 34,7 mln tok.).
  Przed regułą AI (budowa 1): 24 326 wierszy, 239 112 139 tok.

### Pula końcowa (budowa 3, `wyniki/probka_pliki.json`, `wyniki/budowa.json`)

| biblioteka | rewizja | wiersze | pliki źródłowe | bajty źródeł | tokeny v6 | licencje wierszy (wiersze / tokeny) |
|---|---|---|---|---|---|---|
| mathlib4 | 9bed6a56 | 5 892 | 5 892 | 70 174 698 | 30 775 066 | Apache-2.0 |
| afp | 02fd3c6b | 10 557 | 10 557 | 296 880 226 | 129 985 322 | BSD-3-Clause 10 238 / 125 816 763; LGPL-2.1-only 319 / 4 168 559 |
| hol_light | b9a430b8 | 541 | 541 | 25 538 239 | 12 555 462 | BSD-2-Clause |
| setmm | ce7f29d6 | 621 | 2 | 64 170 648 | 11 155 284 | CC0-1.0 |
| rocq_stdlib | 9657c750 | 583 | 583 | 6 390 575 | 2 605 422 | LGPL-2.1-only |
| mathcomp | 656cdbcf | 149 | 149 | 5 948 466 | 2 776 193 | CECILL-B |
| unimath | 11e01f09 | 1 659 | 1 659 | 26 591 510 | 10 183 276 | LicenseRef-UniMath |
| agda_stdlib | 119d1761 | 1 190 | 1 190 | 5 208 665 | 2 156 221 | MIT |
| stacks | a04446e5 | 193 | 115 | 27 650 410 | 11 027 028 | GFDL-1.2-no-invariants-or-later |
| **razem** | | **21 385** | | | **213 219 274** | |

- Wykluczone (poza AI): mathlib4 `Mathlib/{Tactic,Util,Lean}` 336, `MathlibTest` 268, inne poza katalogami 23; AFP
  5 plików > 1 MB; HOL Light 9 > 1 MB, 2 licencja, 2 nie-UTF-8 (`Proofrecording/diffs/*`); Rocq poza `theories/` 321;
  UniMath poza `UniMath/` 6; agda poza `src/` 80; Stacks 4 (fdl, preamble, chapters, book).
- Pliki > 1 MB (`wyniki/duze_pliki.json`): AFP wykluczone `IsaGeoCoq/Tarski_Neutral.thy` (1,55 MB),
  `Broadcast_Psi/Semantics.thy` (1,51), `Bicategory/BicategoryOfSpans.thy` (1,11) — teorie ludzkie, nie dane;
  `Crypto_Standards/*_Test_Vectors.thy` (1,30 i 1,02) — dane testowe. HOL Light wykluczone `Multivariate/`
  topology, metric, measure, paths, integration, cauchy, complex_database (1,0–1,7 MB), `Jordan/jordan_curve_theorem.ml`,
  `Divstep/hull_light.ml` — poza complex_database to teorie pisane ręcznie; reguła z preregistracji („I: tabele i dane
  generowane”) okazała się dla nich błędna, koszt I ok. 6–7 mln tok. v6 (≈ 12,3 MB / ~2 B/tok.); bez aneksu, do
  decyzji (podział na granicach `let … = prove` do 50 tys. znaków). Stacks `algebra.tex` → 44 fragmenty,
  `more-algebra.tex` → 36.
- Długość dokumentów: maks. 528 357 tok. (AFP), 518 942 (HOL Light), mediana 786 (agda) – 30 648 (Stacks).
- `created` = data ostatniego commita zmieniającego plik (dla set.mm: data rewizji).
- Kontrola kontraktu (`skrypty/sprawdz_kontrakt.py` → `wyniki/kontrakt.json`): PASS — kolumny text/url/id/license/
  created/repo/path typu string (+ `biblioteka`, `tokeny_v6`), grupy po 5 000 wierszy, 21 385 unikalnych id, sha256 i
  rozmiar parquetów, tokeny v6 przeliczone od nowa = `probka_pliki.json` (213 219 274), url z rewizją, w set.mm brak
  dowodów innych niż `$= ? $.`.

### B6 (bez budowy)

Szacunek bez zmian (§4): ~1,0 mld tok. v6 surowo, ~0,3–0,5 mld po dedupie (I). Dodatkowo I: `lean_proofsteps`
pochodzi z mathlib4 `c779bd5` (2023), sprzed ujawnionych commitów AI; `isa_proofsteps` z AFP + Isabelle (0 ujawnionych
commitów AI w lustrze AFP).

## Nie sprawdzone (po budowie)

- Użycie LLM nieujawnione w wiadomości commita — niewykrywalne tą metodą; lustro AFP ma zwięzłe wiadomości (0 trafień),
  więc brak trafień nie dowodzi braku AI (AFP = 61% tokenów puli). Także Rocq stdlib, math-comp, agda-stdlib, Stacks,
  UniMath poza 1 commitem i set.mm poza wykrytymi miejscami.
- Pliki przemianowane po commicie z AI (reguła nie śledzi zmian nazw).
- Polityka bibliotek wobec wkładu z LLM (regulaminy AFP, mathlib, UniMath).
- Pokrycie miniF2F/ProofNet przez mathlib4 `Archive/Imo` i AFP; detektory i agregacja nie uruchamiane (integrator).
- Mapowanie `LicenseRef-UniMath` na listę licencji akceptowanych przez `check.py`.
- PII: liczba e-maili w nagłówkach (maskowanie po stronie integratora) nie liczona.
- Wycięte pliki HOL Light > 1 MB (koszt tokenów I, nie zmierzony).
