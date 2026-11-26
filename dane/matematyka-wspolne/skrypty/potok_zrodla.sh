#!/bin/bash
# Potok dla źródła z gotową pulą (probka_pliki.json zbudowany skryptem źródła, nie normalizuj.py): przebieg (detektory DCLM-EN),
# ew13, agreguj z bazami Slayera i wcześniej zbudowanych źródeł (finemath4, infiwebmath4). Wynik: dane/<zrodlo>/wyniki/agreguj.json.
# Użycie: bash potok_zrodla.sh <zrodlo> [procesy]
set -euo pipefail
ZB=$1
PROC=${2:-4}
REPO=$(cd "$(dirname "$0")/../../.." && pwd)
D=$REPO/dane
R=$D/$ZB/robocze
PY=$D/matematyka-wspolne/robocze/venv/bin/python
B=$D/matematyka-wspolne/robocze/wyniki/bazy
mkdir -p "$R/wyniki" "$R/logi"
/usr/bin/nice -n 10 "$PY" -I -W ignore "$D/dclm-en/skrypty/przebieg.py" "$D/$ZB/wyniki/probka_pliki.json" \
  "$D/matematyka-wspolne/robocze/wyniki/ewal" "$D/dclm-en/robocze/wyniki/idx" "$D/dclm-en/robocze/pobrania/tokenizer_v6/tokenizer.json" \
  "$R/wyniki/przebieg" "$PROC" walidacja="$D/dclm-en/robocze/wyniki/idx_wal" > "$R/logi/przebieg.log" 2>&1
"$PY" -I "$D/dclm-en/skrypty/ewal_czeste.py" "$R/wyniki/przebieg" "$D/matematyka-wspolne/robocze/wyniki/ewal" "$R/wyniki/ew13" > "$R/logi/ew13.log" 2>&1
/usr/bin/nice -n 10 "$PY" -I "$D/matematyka-wspolne/skrypty/agreguj_mat.py" "$ZB" "$R/wyniki/przebieg" "$R/wyniki/ew13" \
  "$D/$ZB/skrypty/preregistracja.json" "$R/wyniki/agreguj.json" "$R/probka_przegladu.jsonl" "$R/wyniki/wybor.json" \
  walidacja="$D/dclm-en/robocze/wyniki/idx_wal" wlasne="$B:finemath4,$B:infiwebmath4" entech="$B" en8x3b="$B" fwe109="$B" \
  > "$R/logi/agreguj.log" 2>&1
cp "$R/wyniki/agreguj.json" "$D/$ZB/wyniki/agreguj.json"
tail -1 "$R/logi/ew13.log"
"$PY" -c "
import json, sys
a = json.load(open(sys.argv[1]))
print(a['dokumenty'], a['tokeny_v6'])
for k in a['kaskada']:
    print(k['powod'], k['odrzucone_dok'], k['zostaje_tok'], k['zostaje_tok_proc'])" "$D/$ZB/wyniki/agreguj.json"
