#!/bin/bash
# Odtworzenie zbiorów matematyki do microannealu (#346) krok po kroku. Przepis: research/slayer-1b/dane/METODOLOGIA.md
# w slayerlabs/benchmarks-fabryka-ai; reguły: dane/<zbior>/skrypty/preregistracja.json; wyniki: dane/<zbior>/DZIENNIK.md.
# Użycie: bash dane/matematyka-wspolne/skrypty/odtworz.sh <krok> [zbior]
# Kroki wspólne: venv | ewal_pobierz | ewal
# Kroki zbioru (finemath4 | cranemath | stackedu): pula | przebieg | ew13 | agreguj
# Indeksy EN 1.07 i walidacji Fabryki oraz tokenizer v6 pochodzą z katalogu roboczego DCLM-EN (dane/dclm-en/skrypty/odtworz.sh:
# tokenizer, baza107, idx107, walidacja_pobierz, idx_wal); detektory to przebieg.py i ewal_czeste.py DCLM-EN bez zmian.
# Każdy krok jest wznawialny: pula pomija pliki z probka_pliki.json, przebieg pomija gotowe u_NNNN.npz.
set -euo pipefail

REPO=$(cd "$(dirname "$0")/../../.." && pwd)
W=$REPO/dane/matematyka-wspolne
[ -f "$W/skrypty/agreguj_mat.py" ] || { echo "nie znaleziono repo slayer-lab" >&2; exit 2; }
RW=$W/robocze
DC=$REPO/dane/dclm-en
DCR=$DC/robocze
RPG=$REPO/dane/korpus-rpg-v2/skrypty
PY=$RW/venv/bin/python
NICE="/usr/bin/nice -n 10"
TOK=$DCR/pobrania/tokenizer_v6/tokenizer.json
TOK_SHA=0640d3bd3674d7a6e59c540d945a2ad275a12e1bcaeb6007c37a90751f9815dd
mkdir -p "$RW/logi" "$RW/pobrania" "$RW/wyniki"

KROK=${1:-}
ZB=${2:-}
if [ -n "$ZB" ]; then
  case "$ZB" in finemath4|cranemath|stackedu) ;; *) echo "nieznany zbiór $ZB" >&2; exit 2 ;; esac
  D=$REPO/dane/$ZB
  R=$D/robocze
  PRE=$D/skrypty/preregistracja.json
  mkdir -p "$R/logi" "$R/wyniki" "$D/wyniki"
  SEED=$($PY -c "import json,sys; print(json.load(open(sys.argv[1]))['seed'])" "$PRE")
fi

case "$KROK" in
venv)
  /Library/Frameworks/Python.framework/Versions/3.12/bin/python3.12 -m venv "$RW/venv"
  "$RW/venv/bin/pip" install --disable-pip-version-check -r "$W/requirements.txt"
  ;;
ewal_pobierz)  # testy RPG v2 z katalogu DCLM-EN (dowiązania) + testy_mat.json (GSM-Plus, GSM1k); status scalony
  echo "$TOK_SHA  $TOK" | shasum -a 256 -c
  mkdir -p "$RW/pobrania/ewal"
  for t in "$DCR"/pobrania/ewal/*/; do ln -sfn "$t" "$RW/pobrania/ewal/$(basename "$t")"; done
  $NICE $PY -I "$RPG/pobierz_testy.py" "$RW/pobrania/ewal" "$RW/wyniki/mat" "$W/skrypty/testy_mat.json"
  $PY -I -c "
import json, sys
a = json.load(open(sys.argv[1], encoding='utf-8')); b = json.load(open(sys.argv[2], encoding='utf-8'))
assert not set(a) & set(b); a.update(b)
json.dump(a, open(sys.argv[3], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print({k: v.get('status') for k, v in b.items()}, len(a))
" "$DCR/wyniki/status_pobran.json" "$RW/wyniki/mat/status_pobran.json" "$RW/wyniki/status_pobran.json"
  ;;
ewal)  # indeks 13-gramów i krótkich napisów: 60 testów RPG v2 + 2 testy matematyki
  $NICE $PY -I "$RPG/ewal_indeks.py" "$RW/pobrania/ewal" "$RW/wyniki/status_pobran.json" "$RW/wyniki/ewal"
  ;;
pula)  # pobranie i normalizacja plików źródła do celu puli (preregistracja -> pula)
  CEL=$($PY -c "import json,sys; print(json.load(open(sys.argv[1]))['pula']['cel_puli_tok_v6'])" "$PRE")
  $NICE $PY -I "$W/skrypty/normalizuj.py" "$ZB" "$R/pobrania" "$D/wyniki/probka_pliki.json" "$CEL" "$TOK" "$SEED"
  ;;
przebieg)  # detektory DCLM-EN: tokeny v6, domena, PII, mojibake, 13-gramy, MinHash, EN 1.07, walidacja Fabryki
  $NICE $PY -I -W ignore "$DC/skrypty/przebieg.py" "$D/wyniki/probka_pliki.json" "$RW/wyniki/ewal" "$DCR/wyniki/idx" \
    "$TOK" "$R/wyniki/przebieg" "${PROC:-6}" walidacja="$DCR/wyniki/idx_wal"
  if [ "$ZB" = cranemath ]; then  # 13-gramy na tekście przed przepisaniem: ta sama pula z text=original_text
    $PY -I -c "
import json, sys
p = json.load(open(sys.argv[1], encoding='utf-8'))
for x in p['pliki']: x['lokalnie'] = x['lokalnie_oryg']
json.dump(p, open(sys.argv[2], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
" "$D/wyniki/probka_pliki.json" "$R/wyniki/probka_pliki_oryg.json"
    $NICE $PY -I -W ignore "$DC/skrypty/przebieg.py" "$R/wyniki/probka_pliki_oryg.json" "$RW/wyniki/ewal" "$DCR/wyniki/idx" \
      "$TOK" "$R/wyniki/przebieg_oryg" "${PROC:-6}"
  fi
  ;;
ew13)  # trafiające 13-gramy testów, df w puli (ewal_czeste.py DCLM-EN bez listy wykluczeń)
  $NICE $PY -I "$DC/skrypty/ewal_czeste.py" "$R/wyniki/przebieg" "$RW/wyniki/ewal" "$R/wyniki/ew13"
  if [ "$ZB" = cranemath ]; then
    $NICE $PY -I "$DC/skrypty/ewal_czeste.py" "$R/wyniki/przebieg_oryg" "$RW/wyniki/ewal" "$R/wyniki/ew13_oryg"
  fi
  ;;
agreguj)  # kaskada powodów, uzysk, wybór do eksportu, ręczna próbka (probka_przegladu.jsonl zostaje w robocze/: ma PII)
  ORYG=()
  [ "$ZB" = cranemath ] && ORYG=(oryg="$R/wyniki/przebieg_oryg,$R/wyniki/ew13_oryg")
  $NICE $PY -I "$W/skrypty/agreguj_mat.py" "$ZB" "$R/wyniki/przebieg" "$R/wyniki/ew13" "$PRE" "$R/wyniki/agreguj.json" \
    "$R/probka_przegladu.jsonl" "$R/wyniki/wybor.json" walidacja="$DCR/wyniki/idx_wal" "${ORYG[@]}"
  cp "$R/wyniki/agreguj.json" "$D/wyniki/agreguj.json"
  ;;
*)
  sed -n 2,8p "$0"; exit 2
  ;;
esac
