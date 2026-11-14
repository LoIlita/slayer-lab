# DCLM-baseline EN dla Slayera 1B: metodologia odtworzenia od zera

Jedno miejsce, z którego da się odbudować przebieg dnia 1 bez transkryptów sesji. Co to za źródło, prawa i
ryzyka: [`KARTA_ZRODLA.md`](KARTA_ZRODLA.md). Metoda, progi i kolejność powodów odrzucenia, zapisane przed
wynikiem: [`skrypty/preregistracja.json`](skrypty/preregistracja.json). Ten plik ich nie powtarza, mówi
tylko, JAK je wykonać. Reguły kontroli każdego zbioru: notatka wiedzy `budowa-modeli/komplet-kontroli-zbioru`
(workspace fabryka-ai).

Wszystkie ścieżki są względne do katalogu głównego repo `slayer-lab`. Każdy krok uruchamia
[`skrypty/odtworz.sh`](skrypty/odtworz.sh) `<krok>`; ten plik mówi, co krok robi i jak sprawdzić wynik.

## 0. Wymagania

- macOS albo Linux, Python 3.12 (sprawdzone na 3.12.2), ok. 15 GB wolnego dysku, 18 rdzeni CPU w
  przebiegu z 2026-11-14. Pamięć: patrz sekcja 4.
- Dostęp do Hugging Face z tokenem, który widzi repo `SlayerLab/*` (prywatne). Token czyta sama biblioteka
  `huggingface_hub` z jej zwykłego miejsca; skrypty go nie przyjmują jako argumentu.
- Pakiety: [`requirements.txt`](requirements.txt) (wynik `pip freeze` venv z 2026-11-14, wszystkie wersje
  przypięte). Bezpośrednio używane: `huggingface_hub`, `tokenizers`, `pyarrow`, `numpy`, `requests`, `ftfy`.
  Krok `edu.py` (po przebiegu) potrzebuje dodatkowo `torch` i `transformers`, których ten venv nie ma.
- Kod: skrypty DCLM w `dane/dclm-en/skrypty/` oraz rdzeń i skrypty RPG v2 w `dane/korpus-rpg-v2/skrypty/`
  (commit `c46a7d7`; `wspolne.py` importuje stamtąd `rdzen.py` i `rdzen2.py`).

Katalog roboczy: `dane/dclm-en/robocze/` (w `.gitignore`, nic z niego nie trafia do gita). Nigdy `/tmp`
ani scratchpad sesji: 14.11.2026 restart po awarii skasował `/private/tmp` razem ze wszystkimi wejściami.

```
robocze/
  venv/                       krok venv
  pobrania/tokenizer_v6/      krok tokenizer
  pobrania/dclm/              krok probka (oryginalne parquety + kopie *.rg5000.parquet)
  probka_pliki.json           krok probka (lista plików, sha256, ścieżki lokalne tej maszyny)
  pobrania/ewal/              krok testy
  pobrania/slayer107/, pobrania/technika/   krok baza107
  pobrania/mincorp/           krok walidacja_pobierz
  pobrania/idx/               pobrania kroków idx_wal i idx_ivme (gpt-neox tokenizer, batche ivme)
  wyniki/status_pobran.json   krok testy
  wyniki/ewal/                krok ewal       (EW)
  wyniki/idx/                 krok idx107     (IDX)
  wyniki/idx_wal/, wyniki/idx_ivme/          kroki idx_wal, idx_ivme
  wyniki/kontrola/            krok kontrola
  wyniki/przebieg/            krok przebieg   (u_NNNN.npz + u_NNNN.json, jednostki.json)
  logi/                       log każdego kroku
```

## 1. Kolejność i zależności

```
venv ─┬─ tokenizer ─┬─────────────────────────── idx107 ─┐
      ├─ probka ────┼──────────────────────────────────── ├─ kontrola ─ przebieg
      ├─ testy ─ ewal ─────────────────────────────────── │
      ├─ baza107 ───┘                                     │
      └─ walidacja_pobierz ─ idx_wal ─ idx_ivme ──────────┘
```

Gałęzie są niezależne i mogą iść równolegle (pobrania są ograniczone siecią, nie pamięcią). Kroki liczące
(`ewal`, `idx107`, `idx_wal`, `idx_ivme`) nie powinny iść wszystkie naraz z przebiegiem; patrz sekcja 4.

## 2. Kroki

Uruchomienie: `bash dane/dclm-en/skrypty/odtworz.sh <krok> > dane/dclm-en/robocze/logi/<krok>.log 2>&1`.
Długie kroki puszczaj odłączone (`nohup … &`). Kroki liczące idą przez `nice -n 10`.

| Krok | Skrypt i wejście | Wyjście | Jak sprawdzić, że się udał |
|---|---|---|---|
| `venv` | `python3.12 -m venv`, `pip install -r requirements.txt` | `robocze/venv` | `robocze/venv/bin/pip freeze` = `requirements.txt` |
| `tokenizer` | `korpus-rpg-v2/skrypty/pobierz_tokenizer.py`; `SlayerLab/slayer-1.07-pretrain` (gałąź main, sprawdzane 14.11 na `6a337bbf`), plik `tokenizer.json` | `pobrania/tokenizer_v6/tokenizer.json` | skrypt sam przerywa, jeśli sha256 ≠ `0640d3bd3674d7a6e59c540d945a2ad275a12e1bcaeb6007c37a90751f9815dd`, słownik ≠ 32 768 albo token 0 ≠ `<\|endoftext\|>` |
| `probka` | `dclm-en/skrypty/pobierz.py`; `mlfoundations/dclm-baseline-1.0-parquet@817d6752765f6a41261085171dd546b104f60626`, seed 20261114, cel 1 000 000 wierszy, bez plików z `wykluczone.json` | `pobrania/dclm/…`, `probka_pliki.json` | ostatnia linia logu `KONIEC 1051235`; 10 plików; `sha256` i `wiersze` każdego pliku równe [`wyniki/probka_pliki.json`](wyniki/probka_pliki.json) (różnią się tylko ścieżki `lokalnie`) |
| `testy` | `korpus-rpg-v2/skrypty/pobierz_testy.py` z `korpus-rpg-v2/skrypty/testy.json` | `pobrania/ewal/<test>/…`, `wyniki/status_pobran.json` | log kończy `KONIEC`; w `status_pobran.json` każdy test ze `status` OK albo BLOCKED z powodem. Rewizje: skrypt bierze bieżącą gałąź main i ZAPISUJE rewizję każdego testu w `status_pobran.json` |
| `ewal` | `korpus-rpg-v2/skrypty/ewal_indeks.py` | `wyniki/ewal/` (EW: `wszystkie_13.npy`, `wszystkie_krotkie.npz`, `<test>__13.npy`, `status_indeks.json`) | log kończy `KONIEC`, linia przed nim: `ogolem 32411348 {'n1': 67858, 'n2': 232281, …, 'n12': 89563}`; 56 testów OK, 4 BLOCKED (X07_proofwriter: repo 404, X08, X09, X10: brak adresu zbioru). Różna suma = inne rewizje testów: porównaj `rewizja` w `status_indeks.json` |
| `baza107` | `korpus-rpg-v2/skrypty/pobierz_107.py`; `SlayerLab/slayer-1.07-pretrain` (main, `6a337bbf` 14.11): `en_mix` i `en_fineweb_edu` (`train.bin`, `docs.idx`, razem ok. 7,8 GB) oraz `SlayerLab/technika-i-nauka` (main, `66cb02d7`) | `pobrania/slayer107/`, `pobrania/technika/` | log kończy `KONIEC`; rozmiary: en_mix/train.bin 3 301 237 628 B, en_fineweb_edu/train.bin 4 471 320 050 B |
| `idx107` | `korpus-rpg-v2/skrypty/bazy_indeks.py`, tokenizer v6 z kroku `tokenizer` (ten sam plik co karta 1.07, sha `0640d3bd`), 2 procesy | `wyniki/idx/` (IDX: `idx_slayer_107_en_{szkic,sig,kl,dok}.npy`, `idx_technika_i_nauka_*`, `liczby_indeks.json`) | `liczby_indeks.json`: slayer_107_en 3 278 603 dokumentów, 158 680 048 próbek szkicu; technika_i_nauka 19 048 / 783 495 |
| `walidacja_pobierz` | `hf download` walidacji `SlayerLab/minimal-en-corpus-5b@bb3aec23e3cff66707cecc577650763893834857` i `SlayerLab/minimal-en-corpus-2b-v2@ef0ab06943e40ed4f882b0798b1756e99bbb1410`, plik `validation/shard-00000.parquet` | `pobrania/mincorp/` | krok sam sprawdza sha256 (`5abe9d60…`, `dbdab0a4…`) |
| `idx_wal` | `dclm-en/skrypty/indeksy.py walidacja`, 4 procesy; poza walidacjami pobiera oś FineWeb-Edu (`HuggingFaceFW/fineweb-edu@87f09149…`, 5000 wierszy) i oś DCLM (`allenai/DataDecide-data-recipes@3baf34ba`, 5000 dokumentów) | `wyniki/idx_wal/` (`idx_walidacja_*.npy`, `walidacja.json`) | `walidacja.json` bajt w bajt równy [`wyniki/indeks_walidacja.json`](wyniki/indeks_walidacja.json) (18 363 dokumentów, 938 948 próbek, 8 089 url). Log nie ma linii `KONIEC`: koniec = istnieje `walidacja.json` |
| `idx_ivme` | `dclm-en/skrypty/indeksy.py ivme`, 4 procesy; `SlayerLab/sub150run-ivme-20b-v3@c9fa17d73a5134b34daa58b668ce7a400681c99d`, 28 batchy `train-dclm` | `wyniki/idx_ivme/` (`idx_ivme_*.npy`, `ivme.json`) | `ivme.json` równy [`wyniki/indeks_ivme.json`](wyniki/indeks_ivme.json) (199 283 dokumentów, 11 391 284 próbek, tokenizer sha `a847369b…`) |
| `kontrola` | `dclm-en/skrypty/kontrola_dodatnia.py` + `przebieg.py` na 1 procesie, te same indeksy co przebieg | `wyniki/kontrola/` i tabela na wyjściu | każdy z 14 wstawionych dokumentów dostaje powód z [`wyniki/kontrole_dodatnie.json`](wyniki/kontrole_dodatnie.json), dokument czysty bez powodu. Przebieg próbki rusza dopiero po tym kroku |
| `przebieg` | `dclm-en/skrypty/przebieg.py`, 6 procesów | `wyniki/przebieg/u_0000…u_0215.{npz,json}`, `jednostki.json` | log zaczyna `jednostek 216 do zrobienia N`, kończy `KONIEC <s>`; 216 plików `u_*.npz` |

## 3. Wznowienie po przerwaniu

- Pobrania (`probka`, `testy`, `baza107`, `walidacja_pobierz`) pomijają pliki już pobrane w całości, więc
  wystarczy uruchomić krok ponownie. `pobierz.py` przelicza jednak sha256 i kopię `rg5000` każdego pliku.
- `przebieg.py` zapisuje jednostkę atomowo (`.u_NNNN.npz` → `u_NNNN.npz`) i przy starcie pomija gotowe
  `u_*.npz`. Po przerwaniu uruchom krok ponownie; pliki `.u_*.npz` (z kropką) to niedokończone zapisy do
  skasowania.
- Indeksy (`ewal`, `idx107`, `idx_wal`, `idx_ivme`) liczą od nowa; przerwany krok uruchom ponownie w całości.
- `probka_pliki.json` trzyma ścieżki absolutne tej maszyny (`lokalnie`). Kopia w `wyniki/` jest rejestrem
  (sha256, wiersze); do przebiegu idzie zawsze `robocze/probka_pliki.json` z kroku `probka` na tej maszynie.

## 4. Pamięć i obciążenie

Mac z 51 GB padł 14.11.2026 o 19:09 (kernel panic przy presji pamięci) w trakcie przebiegu na 6 procesach
przy równoległych innych zadaniach. Przed przebiegiem:

- `pgrep -lx 'Discord|LeagueClient|VTEncoderXPCService'` i `memory_pressure | tail -1`; jeśli działają ciężkie
  aplikacje, zapisz to w logu.
- Przebieg zostaje na 6 procesach i `nice -n 10` (każdy proces mapuje te same indeksy przez `mmap`); nie
  zwiększaj liczby procesów bez pomiaru RSS jednej jednostki.
- Nie puszczaj przebiegu równolegle z `idx107`, `ewal` ani drugim przebiegiem.

## 5. Po przebiegu (dzień 1, jeszcze nie uruchamiane)

Argumenty z docstringów skryptów; wynik i progi interpretuje `preregistracja.json`.

1. `fwe_url.py <wyjście> <liczba_plików>`: próbka url FineWeb-Edu (hasze url do nakładania).
2. `edu.py robocze/wyniki/przebieg/jednostki.json <wyjście.npz> <liczba> <urządzenie> [limit_s]`: klasyfikator
   FineWeb-Edu na podpróbce; wymaga Pythona z `torch` i `transformers`.
3. `agreguj.py robocze/wyniki/przebieg robocze/probka_pliki.json <fwe_url_h.npy> <edu.npz> <wyjście.json>
   <probki_reczne.jsonl> walidacja=robocze/wyniki/idx_wal ivme=robocze/wyniki/idx_ivme`: dedup wewnątrz,
   kaskada powodów, uzysk w tokenach v6, ręczna próbka 100/100.

## 6. Historia odtworzeń

- 14.11.2026 wieczorem: pierwsze wejścia (venv, pobrania, EW, IDX, tokenizer) leżały w scratchpadach sesji
  w `/private/tmp` i przepadły po restarcie. Odbudowa tym dokumentem tego samego wieczoru: `probka` (10 plików,
  sha256 i wiersze), `idx_wal` i `idx_ivme` (JSON bajt w bajt) oraz `ewal` (suma 13-gramów i krótkich napisów,
  rewizje testów) zgodne z przebiegiem sprzed awarii. Wersje pakietów starego venv nie były zapisane; od tej
  odbudowy są w `requirements.txt`.
