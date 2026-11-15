# Dane treningowe Slayera 1B

Stan bazowy według [![Space](https://img.shields.io/badge/HF_Space-SlayerLab%2FSlayer1B-ffcc00?logo=huggingface)](https://huggingface.co/spaces/SlayerLab/Slayer1B) (odczyt 14.11.2026), potem zbiory dopisane później.

## 1. Stan bazowy

| zbiór | rewizja | wersja / segment | licencja | tokeny |
|---|---|---|---|---|
| [![HF](https://img.shields.io/badge/HF-SlayerLab%2Fslayer--pl--8x3b-ffcc00?logo=huggingface)](https://huggingface.co/datasets/SlayerLab/slayer-pl-8x3b/tree/d50df04a6ad46876fa559a87cca5d3e2a96e7098) | `d50df04a` | 1.00–1.06 | różna według źródła | 14,5 mld (do 1.06) |
| [![HF](https://img.shields.io/badge/HF-SlayerLab%2Fslayer--1.07--pretrain-ffcc00?logo=huggingface)](https://huggingface.co/datasets/SlayerLab/slayer-1.07-pretrain/tree/6a337bbfba518d88f14eb54f7d0a9b9f297df0d1) | `6a337bbf` | 1.07; replay w 1.08 (`pl_web`, `en_fineweb_edu`, `en_mix`) | ODC-By, CC BY (DCLM), HPLT CC0 | 8 891 005 707 |
| [![HF](https://img.shields.io/badge/HF-SlayerLab%2Fminimal--en--corpus--5b-ffcc00?logo=huggingface)](https://huggingface.co/datasets/SlayerLab/minimal-en-corpus-5b/tree/bb3aec23e3cff66707cecc577650763893834857) | `bb3aec23` | 1.07, pula EN (FineWeb-Edu, FineMath, open-web-math, DCLM) | — | — |
| [![HF](https://img.shields.io/badge/HF-SlayerLab%2Fslayer--pl--logika--2b-ffcc00?logo=huggingface)](https://huggingface.co/datasets/SlayerLab/slayer-pl-logika-2b/tree/e24c8b71526ca1dc56a280100f88c2f09a79ecdd) | `e24c8b71` | 1.08 | różna według źródła | 1 911 918 958 z EOS |
| [![HF](https://img.shields.io/badge/HF-SlayerLab%2Fenglish--technical--1b-ffcc00?logo=huggingface)](https://huggingface.co/datasets/SlayerLab/english-technical-1b/tree/3b833d36bd3ba9aeecf46f39605c9ac849bb96a3) | `3b833d36` | 1.08 | per wiersz: MIT, Apache-2.0, BSD-3, CC0 | 899 001 323 (train) |
| [![HF](https://img.shields.io/badge/HF-SlayerLab%2Fgollem--corpus--16b--pl-ffcc00?logo=huggingface)](https://huggingface.co/datasets/SlayerLab/gollem-corpus-16b-pl/tree/17f9d37af3c9803178adcc1e056f664ba62a3558) | `17f9d37a` | 1.09: c01, c02, c06 | CC0-1.0 (opakowanie HPLT) | 1 069 547 741 poz. (c01) |
| [![HF](https://img.shields.io/badge/HF-HuggingFaceFW%2Ffinepdfs--edu-ffcc00?logo=huggingface)](https://huggingface.co/datasets/HuggingFaceFW/finepdfs-edu/tree/9cfabe2127faca99b3d5c4dc6d1fcb397399ebde) | `9cfabe21` | 1.09: c03–c06 | ODC-By | — |
| [![HF](https://img.shields.io/badge/HF-HuggingFaceFW%2Ffineweb--edu-ffcc00?logo=huggingface)](https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu) | — | 1.09: c01–c06, EN | ODC-By | 4 278 190 159 poz. (c01) |
| [![HF](https://img.shields.io/badge/HF-SlayerLab%2Fslayer--1.08b--pretrain-ffcc00?logo=huggingface)](https://huggingface.co/datasets/SlayerLab/slayer-1.08b-pretrain) | — | 1.08b (eksperyment, niewydany) | dane niepublikowane | 782 469 318 na ramię |

Karty danych: [![1.08](https://img.shields.io/badge/DATA__CARD-1.08-ffcc00?logo=huggingface)](https://huggingface.co/SlayerLab/Slayer1B-1.08/blob/main/DATA_CARD.md) [![1.09](https://img.shields.io/badge/DATA__CARD-1.09-ffcc00?logo=huggingface)](https://huggingface.co/SlayerLab/Slayer1B-1.09/blob/main/DATA_CARD.md)

## 2. Dopisane później

| data | zbiór | kto | zgłoszenie | status |
|---|---|---|---|---|
| 2026-11-14 | [DCLM-baseline 1.0 EN](https://huggingface.co/datasets/mlfoundations/dclm-baseline-1.0/tree/a3b142c183aebe5af344955ae20836eb34dcf69b) → [`dane/dclm-en/`](dclm-en/KARTA_ZRODLA.md) | Ania | [![#197](https://img.shields.io/badge/GitHub-%23197-181717?logo=github)](https://github.com/slayerlabs/benchmarks-fabryka-ai/issues/197) | w budowie |
| 2026-11-14 | Korpus RPG v2 → [`dane/korpus-rpg-v2/`](korpus-rpg-v2/) | Ania | bez zgłoszenia | w budowie |
| 2026-11-14 | [SlayerLab/hutnictwo-gornictwo-spawalnictwo-preview](https://huggingface.co/datasets/SlayerLab/hutnictwo-gornictwo-spawalnictwo-preview) | SlayerLab | bez zgłoszenia | opublikowany |
| 2026-11-09 | [SlayerLab/polish-dynaword-pretraining-mix](https://huggingface.co/datasets/SlayerLab/polish-dynaword-pretraining-mix) | SlayerLab | bez zgłoszenia | opublikowany |
| 2026-11-08 | [SlayerLab/technika-i-nauka](https://huggingface.co/datasets/SlayerLab/technika-i-nauka) | SlayerLab | bez zgłoszenia | opublikowany |
