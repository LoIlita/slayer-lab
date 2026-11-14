#!/bin/bash
# Odtworzenie przebiegu DCLM-EN od zera, krok po kroku. Opis kroków, wejść i kontroli: dane/dclm-en/METODOLOGIA.md.
# Użycie (z dowolnego katalogu):  bash dane/dclm-en/skrypty/odtworz.sh <krok>
# Kroki: venv | tokenizer | probka | testy | ewal | baza107 | idx107 | walidacja_pobierz | idx_wal | idx_ivme | kontrola | przebieg
#        po przebiegu: fwe_url | edu | agreguj
# Każdy krok jest wznawialny: pobrania pomijają gotowe pliki, przebieg pomija gotowe u_NNNN.npz.
set -euo pipefail

REPO=$(cd "$(dirname "$0")/../../.." && pwd)
[ -f "$REPO/dane/dclm-en/KARTA_ZRODLA.md" ] || { echo "nie znaleziono repo slayer-lab" >&2; exit 2; }
D=$REPO/dane/dclm-en
S=$D/skrypty
RPG=$REPO/dane/korpus-rpg-v2/skrypty
R=$D/robocze
PY=$R/venv/bin/python
NICE="/usr/bin/nice -n 10"
TOK_SHA=0640d3bd3674d7a6e59c540d945a2ad275a12e1bcaeb6007c37a90751f9815dd
mkdir -p "$R/logi" "$R/pobrania" "$R/wyniki"

case "${1:-}" in
venv)
  /Library/Frameworks/Python.framework/Versions/3.12/bin/python3.12 -m venv "$R/venv"
  "$R/venv/bin/pip" install --disable-pip-version-check -r "$D/requirements.txt"
  ;;
tokenizer)  # tokenizer v6 z karty 1.07, sha256 sprawdza skrypt
  $NICE $PY -I "$RPG/pobierz_tokenizer.py" "$R/pobrania/tokenizer_v6" $TOK_SHA
  ;;
probka)  # 10 shardów DCLM (seed 20261114), lokalna kopia z grupami po 5000 wierszy
  $NICE $PY -I "$S/pobierz.py" "$R/pobrania/dclm" "$R/probka_pliki.json" 1000000 "$S/wykluczone.json"
  ;;
testy)  # zbiory ewaluacyjne z testy.json RPG v2
  $NICE $PY -I "$RPG/pobierz_testy.py" "$R/pobrania/ewal" "$R/wyniki" "$RPG/testy.json"
  ;;
ewal)  # indeks 13-gramów i krótkich napisów testów (EW)
  $NICE $PY -I "$RPG/ewal_indeks.py" "$R/pobrania/ewal" "$R/wyniki/status_pobran.json" "$R/wyniki/ewal"
  ;;
baza107)  # angielskie części slayer-1.07-pretrain i technika-i-nauka
  $NICE $PY -I "$RPG/pobierz_107.py" "$R/pobrania"
  ;;
idx107)  # indeks dedupu wobec 1.07 EN (IDX); tokenizer v6 = tokenizer karty 1.07
  $NICE $PY -I "$RPG/bazy_indeks.py" "$R/pobrania" "$R/pobrania/tokenizer_v6/tokenizer.json" "$R/wyniki/idx" 2
  ;;
walidacja_pobierz)  # walidacje minimal-en-corpus z przypiętych rewizji
  "$R/venv/bin/hf" download SlayerLab/minimal-en-corpus-5b validation/shard-00000.parquet --repo-type dataset \
    --revision bb3aec23e3cff66707cecc577650763893834857 --local-dir "$R/pobrania/mincorp/minimal-en-corpus-5b"
  "$R/venv/bin/hf" download SlayerLab/minimal-en-corpus-2b-v2 validation/shard-00000.parquet --repo-type dataset \
    --revision ef0ab06943e40ed4f882b0798b1756e99bbb1410 --local-dir "$R/pobrania/mincorp/minimal-en-corpus-2b-v2"
  shasum -a 256 -c <<EOF
5abe9d6038675e42cfe319ba81046718e0ba30316fbfe92f352402269b063be5  $R/pobrania/mincorp/minimal-en-corpus-5b/validation/shard-00000.parquet
dbdab0a481f04211e8506b7719ee1bc2c30bd5383725721d964f81afbbf598bd  $R/pobrania/mincorp/minimal-en-corpus-2b-v2/validation/shard-00000.parquet
EOF
  ;;
idx_wal)
  $NICE $PY -I "$S/indeksy.py" walidacja "$R/pobrania/idx" "$R/wyniki/idx_wal" 4 \
    "$R/pobrania/mincorp/minimal-en-corpus-5b/validation/shard-00000.parquet" \
    "$R/pobrania/mincorp/minimal-en-corpus-2b-v2/validation/shard-00000.parquet"
  ;;
idx_ivme)
  $NICE $PY -I "$S/indeksy.py" ivme "$R/pobrania/idx" "$R/wyniki/idx_ivme" 4
  ;;
kontrola)  # kontrola dodatnia: 14 wstawionych dokumentów przez ten sam przebieg.py i te same indeksy; wynik porównaj z wyniki/kontrole_dodatnie.json
  rm -rf "$R/wyniki/kontrola"
  $PY -I "$S/kontrola_dodatnia.py" "$R/pobrania/ewal" "$R/pobrania/slayer107" "$R/pobrania/tokenizer_v6/tokenizer.json" \
    "$(ls "$R"/pobrania/dclm/filtered/*/*/processed_data/global-shard_01_of_10/local-shard_8_of_10/shard_00000184_processed.rg5000.parquet)" \
    "$R/wyniki/kontrola" "$R/pobrania/mincorp/minimal-en-corpus-5b/validation/shard-00000.parquet" "$R/pobrania/idx/ivme" > /dev/null
  $PY -I -W ignore "$S/przebieg.py" "$R/wyniki/kontrola/probka_kontrola.json" "$R/wyniki/ewal" "$R/wyniki/idx" \
    "$R/pobrania/tokenizer_v6/tokenizer.json" "$R/wyniki/kontrola/przebieg" 1 walidacja="$R/wyniki/idx_wal" ivme="$R/wyniki/idx_ivme"
  $PY -I -c "
import json, sys, numpy as np
k = sys.argv[1]
z = np.load(k + '/przebieg/u_0000.npz'); m = json.load(open(k + '/przebieg/u_0000.json'))
for i, d in enumerate(m['ids']):
    print(d, 'dom', z['dom'][i], 'pii', z['pii'][i], 'ew', m['ew_testy'].get(str(i)), 'moj', z['moj'][i],
          '107', np.round(z['bz_slayer_107_en'][i], 2), 'wal', np.round(z['bz_walidacja'][i], 2), 'ivme', np.round(z['bz_ivme'][i], 2))
" "$R/wyniki/kontrola"
  ;;
przebieg)  # 216 jednostek; PROC=6 (pamięć: patrz METODOLOGIA.md, sekcja Przebieg)
  $NICE $PY -I -W ignore "$S/przebieg.py" "$R/probka_pliki.json" "$R/wyniki/ewal" "$R/wyniki/idx" \
    "$R/pobrania/tokenizer_v6/tokenizer.json" "$R/wyniki/przebieg" 6 walidacja="$R/wyniki/idx_wal" ivme="$R/wyniki/idx_ivme"
  ;;
fwe_url)  # pomiar nakładania url z FineWeb-Edu: 8 plików data/ (preregistracja -> fineweb_edu_url)
  $NICE $PY -I "$S/fwe_url.py" "$R/wyniki/fwe" 8
  ;;
edu)  # klasyfikator FineWeb-Edu na 50 000 dokumentów; cpu = float32 (mps liczy w float16)
  mkdir -p "$R/wyniki/edu"
  $NICE $PY -I "$S/edu.py" "$R/wyniki/przebieg/jednostki.json" "$R/wyniki/edu/edu.npz" 50000 "${EDU_DEV:-cpu}"
  ;;
agreguj)  # kaskada powodów, uzysk v6, szacunek shardów, ręczna próbka 100/100 (probki_reczne.jsonl zostaje w robocze/: ma PII)
  $NICE $PY -I "$S/agreguj.py" "$R/wyniki/przebieg" "$R/probka_pliki.json" "$R/wyniki/fwe/fwe_url_h.npy" "$R/wyniki/edu/edu.npz" \
    "$R/wyniki/agreguj.json" "$R/wyniki/probki_reczne.jsonl" walidacja="$R/wyniki/idx_wal" ivme="$R/wyniki/idx_ivme"
  cp "$R/wyniki/agreguj.json" "$D/wyniki/agreguj.json"
  cp "$R/wyniki/fwe/fwe_url.json" "$D/wyniki/fwe_url.json"
  ;;
*)
  sed -n 2,6p "$0"; exit 2
  ;;
esac
