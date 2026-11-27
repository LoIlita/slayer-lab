# Dziennik wspólny: zbiór matematyki i kodu EN dla Slayera (`Lolita67/math-code-en`, „Math & Code (English)”)

Dzienniki źródeł: [FineMath-4+](../finemath4/DZIENNIK.md), [Stack-Edu](../stackedu/DZIENNIK.md),
[InfiWebMath-4+](../infiwebmath4/DZIENNIK.md), [arXiv](../arxiv_mat/DZIENNIK.md), [StackExchange](../stackexchange_mat/DZIENNIK.md),
[formalna](../formalna/DZIENNIK.md), [OEIS](../oeis/DZIENNIK.md), [Wikipedia](../wiki_mat/DZIENNIK.md),
[podręczniki](../podreczniki_mat/DZIENNIK.md). Rezerwacje: #346, #357 (slayerlabs/benchmarks-fabryka-ai).

## Stan końcowy (27.11.2026)

Repo HF `Lolita67/math-code-en` (gated manual, anonimowo 401; do 27.11 `Lolita67/matematyka-kod-en-robocze`, stary adres
przekierowuje 307): **11 810 524 dok., 17 018 594 648 tokenów v6** w 26 częściach `data/<klucz>_pNN/` (parquet) i 26 bliźniakach
`tokenized/slayer-v6/<klucz>_pNN.{bin,json}`. Decyzja Ani (26–27.11): zbiór zostaje przy ~17 mld. README na HF po angielsku
(kopia: [`eksport/README_hf_math-code-en.md`](eksport/README_hf_math-code-en.md)).

| źródło | części | dok. | tokeny v6 |
|---|---|---|---|
| FineMath-4+ | 7 | 4 763 307 | 6 950 748 498 |
| Stack-Edu Python | 5 | 3 516 754 | 4 815 014 562 |
| arXiv | 8 | 599 703 | 2 425 618 929 |
| StackExchange | 1 | 1 614 905 | 1 297 166 546 |
| InfiWebMath-4+ | 1 | 1 025 440 | 1 138 599 522 |
| formalna | 1 | 20 390 | 208 104 938 |
| OEIS | 1 | 260 277 | 153 731 738 |
| Wikipedia | 1 | 6 762 | 19 734 493 |
| podręczniki | 1 | 2 986 | 9 875 422 |
| **razem** | 26 | 11 810 524 | 17 018 594 648 |

## Kontrola końcowa (krok 5), 27.11.2026

Agenci recenzujący byli wcześniej masowo blokowani przez dostawcę, więc kontrola jest skryptem i osobnymi wywołaniami modelu
(wynik: [`wyniki/kontrola_koncowa.json`](wyniki/kontrola_koncowa.json)).

| kontrola | wynik |
|---|---|
| Bliźniaki tekst/tokeny | 26/26 części `data/` z `tokenized/slayer-v6/<k>.{bin,json}`; `dokumenty` = wiersze parquetu i `zrodlo_sha256` = sha256 LFS w 26/26; arXiv: sha256 LFS = pliki `.sha256` eksportu 8/8 |
| Licencje w kolumnie `license` (wszystkie wiersze, policzone) | 0 wartości NC/ND/nieznanych we wszystkich 9 źródłach; Stack-Edu 88 identyfikatorów SPDX z listy Blue Oak (m.in. NCSA = licencja Uniwersytetu Illinois, permisywna); arXiv CC-BY-4.0, CC0-1.0, CC-BY-SA-4.0, CC-BY-3.0, CC-PDDC; reszta jak w kartach źródeł |
| Gated, 401 | `gated: manual`; anonimowe pobranie parquetu: 401 |
| README = pliki | liczby dokumentów i tokenów w README policzone z plików `tokenized/slayer-v6/*.json` i metadanych parquetów |
| 50 losowych dok. na źródło (seed 20261127), model „slow”, do 6000 znaków | śmieci (`nie`): FineMath-4+ 3/50, InfiWebMath-4+ 2/50, podręczniki 1/50, Stack-Edu 1/50, pozostałe 0/50; wątpliwe: FineMath-4+ 15, InfiWebMath-4+ 14, podręczniki 8, arXiv 1, Stack-Edu 1, StackExchange 1; PII: 0/50 we wszystkich poza Stack-Edu **1/50** (zaciemniony e-mail `nazwa_at_domena` w nagłówku licencji pliku) |

Wnioski: śmieci w FineMath-4+/InfiWebMath-4+ (6%, 4%) zgodne z przeglądami źródeł (~9–10%, cecha źródła, filtr jakości nie
nałożony). Stack-Edu: forma `_at_` i pokrewne w nagłówkach plików nie były maskowane — naprawione aneksem 27.11 w 5 częściach `data/`
(1 988 plików, 2 258 adresów; [`../stackedu/DZIENNIK.md`](../stackedu/DZIENNIK.md), „Aneks 27.11”); po eksporcie skan: 0 adresów do
maskowania. Formalna matematyka: 0 tych form. Liczby w tabeli wyżej są po aneksie (twin check 26/26 powtórzony po wysyłce
Stack-Edu).

Ramiona `mikroanneal/` (27.11, skan `skan_zaciemnione.py`, pliki z trafieniem `_at_` / `<at>` / `at … dot` / `AT` / `x.y at`):

| ramię | przed | po | zmiana |
|---|---|---|---|
| `stack_edu_python` (180 275 plików) | 7 / 4 / 65 / 6 / 9 | 0 / 0 / 0 / 0 / 0 | przebudowane z `data/stack_edu_python_p01` po aneksie, te same id i kolejność; 91 plików, 109 adresów → `[PII]`; commit HF `872b24af` ([`../stackedu/DZIENNIK.md`](../stackedu/DZIENNIK.md), „Ramię `mikroanneal/stack_edu_python` po aneksie”) |
| `cranemath_en` | 0 / 0 / 0 / 0 / 0 | — | bez zmian |
| `finemath_4plus_en` | 2 / 4 / 28 / 3 / 54 | — | bez zmian, **otwarte**: adresy osób w archiwach list i stopkach stron (reguła `pii_zaciemniony` łapała tylko formy z nawiasami); ramię jest podzbiorem `data/finemath_4plus_en_*`, więc te formy są też w `data/` [wniosek, `data/` FineMath nie skanowane] — do decyzji (maska w eksporcie FineMath-4+ jak w Stack-Edu albo usunięcie dokumentów) |

## Sprzątanie dysku (27.11.2026)

Usunięte (zwolnione ~40 GB):
- `dane/finemath4/robocze/pobrania` (18 GB: lokalne kopie `lok/*.rg5000.parquet` FineMath-4+),
- `dane/infiwebmath4/robocze/pobrania` (16 GB: to samo dla InfiWebMath-4+),
- `dane/dclm-en/robocze/pobrania/dclm` (5,9 GB: pula DCLM-baseline).

Odtworzenie: `HuggingFaceTB/finemath@e92b25a616738fe95dc186b64dfb19f9c8525594` (rewizja w `finemath4/KARTA_ZRODLA.md`,
`finemath4/skrypty/preregistracja.json`, `infiwebmath4/...` tak samo) i `mlfoundations/dclm-baseline-1.0-parquet@817d6752765f6a41261085171dd546b104f60626`
(`dclm-en/KARTA_ZRODLA.md`); krok pobrania i przepisania na grupy po 5 000 wierszy: `odtworz.sh` / `normalizuj.py` (matematyka) i
`dclm-en/skrypty/pobierz.py`. Uwaga: `para_wlasne.py` czyta tekst dokumentu bazy z tych kopii — przy przyszłym źródle z parami
`dedup_finemath4`/`dedup_infiwebmath4` trzeba najpierw odtworzyć `lok/`.

Zostawione: katalogi `przebieg` (`finemath4/robocze/cz2/wyniki/przebieg`, `infiwebmath4/robocze/wyniki/przebieg`: sygnatury do par
i dedupu przyszłych źródeł), `dclm-en/robocze/wyniki/idx` (indeks Slayera 1.07 EN), `dclm-en/robocze/pobrania/{idx,ewal,…}`,
`matematyka-wspolne/robocze/wyniki/bazy`, tokenizer v6.
