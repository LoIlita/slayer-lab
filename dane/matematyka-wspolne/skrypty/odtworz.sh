#!/bin/bash
# Odtworzenie zbiorów matematyki do microannealu (#346) krok po kroku. Przepis: research/slayer-1b/dane/METODOLOGIA.md
# w slayerlabs/benchmarks-fabryka-ai; reguły: dane/<zbior>/skrypty/preregistracja.json; wyniki: dane/<zbior>/DZIENNIK.md.
# Użycie: bash dane/matematyka-wspolne/skrypty/odtworz.sh <krok> [zbior]
# Kroki wspólne: venv | ewal_pobierz | ewal
# Kroki zbioru (finemath4 | cranemath | stackedu | infiwebmath4 | finemath3): pula | kontrola | przebieg | ew13 | agreguj | wlasne | eksport
# Część 2 (CZESC=2 dla finemath4 i stackedu; infiwebmath4 i finemath3 mają tylko część 2): agreguj infiwebmath4 wymaga indeksu
# `wlasne finemath4`, agreguj finemath3 indeksów `wlasne finemath4` i `wlasne infiwebmath4`; eksport części: eksport_czesci.sh.
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
  case "$ZB" in finemath4|cranemath|stackedu|infiwebmath4|finemath3) ;; *) echo "nieznany zbiór $ZB" >&2; exit 2 ;; esac
  D=$REPO/dane/$ZB
  R=$D/robocze
  WD=$D/wyniki
  PRE=$D/skrypty/preregistracja.json
  POBR=$R/pobrania
  if [ "${CZESC:-1}" != 1 ]; then  # część N: katalog roboczy i wyniki osobno, pobrania wspólne; pole czesc_N nadpisuje pulę
    R=$D/robocze/cz$CZESC
    WD=$D/wyniki/cz$CZESC
    mkdir -p "$R/wyniki"
    $PY -c "
import json, sys
p = json.load(open(sys.argv[1], encoding='utf-8')); c = p['czesc_' + sys.argv[2]]
p['pula'] = {**p['pula'], 'cel_puli_tok_v6': c['cel_puli_tok_v6'], 'cel_eksportu_tok_v6': c['cel_eksportu_tok_v6'], 'czesc': sys.argv[2]}
p.update({k: v for k, v in c.items() if k == 'kolejnosc_powodow' or k.startswith('aneks_')})  # reguły dodane w tej części
json.dump(p, open(sys.argv[3], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
" "$PRE" "$CZESC" "$R/preregistracja.json"
    PRE=$R/preregistracja.json
  fi
  mkdir -p "$R/logi" "$R/wyniki" "$WD"
  SEED=$($PY -c "import json,sys; print(json.load(open(sys.argv[1]))['seed'])" "$PRE")
fi

case "$KROK" in
venv)
  /Library/Frameworks/Python.framework/Versions/3.12/bin/python3.12 -m venv "$RW/venv"
  "$RW/venv/bin/pip" install --disable-pip-version-check -r "$W/requirements.txt"
  ;;
ewal_pobierz)  # testy RPG v2 z katalogu DCLM-EN (dowiązania) + testy_mat.json (GSM-Plus, GSM1k); status scalony
  echo "$TOK_SHA  $TOK" | shasum -a 256 -c
  mkdir -p "$RW/pobrania/ewal" "$RW/wyniki/mat"
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
  $NICE $PY -I "$W/skrypty/normalizuj.py" "$ZB" "$POBR" "$WD/probka_pliki.json" "$CEL" "$TOK" "$SEED"
  ;;
przebieg)  # detektory DCLM-EN: tokeny v6, domena, PII, mojibake, 13-gramy, MinHash, EN 1.07, walidacja Fabryki
  $NICE $PY -I -W ignore "$DC/skrypty/przebieg.py" "$WD/probka_pliki.json" "$RW/wyniki/ewal" "$DCR/wyniki/idx" \
    "$TOK" "$R/wyniki/przebieg" "${PROC:-6}" walidacja="$DCR/wyniki/idx_wal"
  if [ "$ZB" = cranemath ]; then  # 13-gramy na tekście przed przepisaniem: ta sama pula z text=original_text
    $PY -I -c "
import json, sys
p = json.load(open(sys.argv[1], encoding='utf-8'))
for x in p['pliki']: x['lokalnie'] = x['lokalnie_oryg']
json.dump(p, open(sys.argv[2], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
" "$WD/probka_pliki.json" "$R/wyniki/probka_pliki_oryg.json"
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
  case "$ZB" in  # dedup wobec źródeł zbioru łącznego zbudowanych wcześniej (preregistracja: dedup_finemath4, dedup_infiwebmath4)
    infiwebmath4) ORYG+=(wlasne="$RW/wyniki/bazy:finemath4") ;;
    finemath3) ORYG+=(wlasne="$RW/wyniki/bazy:finemath4,$RW/wyniki/bazy:infiwebmath4") ;;
  esac
  $NICE $PY -I "$W/skrypty/agreguj_mat.py" "$ZB" "$R/wyniki/przebieg" "$R/wyniki/ew13" "$PRE" "$R/wyniki/agreguj.json" \
    "$R/probka_przegladu.jsonl" "$R/wyniki/wybor.json" walidacja="$DCR/wyniki/idx_wal" ${ORYG[@]+"${ORYG[@]}"} \
    entech="$RW/wyniki/bazy" en8x3b="$RW/wyniki/bazy" fwe109="${FWE109:-$RW/wyniki/bazy}"  # FWE109: katalog z idx_fwe109_hu.npy (wstępnie pusty, gdy indeks w budowie)
  cp "$R/wyniki/agreguj.json" "$WD/agreguj.json"
  ;;
wlasne)  # indeks dedupu z dokumentów wybranych do eksportu tego zbioru, dla źródeł dodanych później
  $NICE $PY -I "$W/skrypty/bazy_mat.py" "wlasne:$ZB:$R/wyniki/wybor.json" "$R/wyniki/przebieg" "$RW/wyniki/bazy" 1
  ;;
kontrola)  # kontrola dodatnia (preregistracja -> kontrole_dodatnie): te same skrypty i indeksy co pula, wynik w wyniki/kontrola.json
  K=$R/wyniki/kontrola
  rm -rf "$K"
  $PY -I "$W/skrypty/kontrola_mat.py" buduj "$ZB" "$RW/pobrania/ewal" "$DCR/pobrania/slayer107" "$TOK" \
    "$DCR/pobrania/mincorp/minimal-en-corpus-5b/validation/shard-00000.parquet" "$K" \
    "$RW/pobrania/entech/data/test.parquet" "$RW/pobrania/en8x3b/shared/en.parquet" "$($PY -c "
from huggingface_hub import HfFileSystem; import pyarrow.parquet as pq
with HfFileSystem().open('datasets/HuggingFaceFW/fineweb-edu@87f09149ef4734204d70ed1d046ddc9ca3f2b8f9/sample/100BT/001_00000.parquet', 'rb') as h:
    print(pq.ParquetFile(h).read_row_group(0, columns=['url']).column(0)[3].as_py())")"
  $PY -I -W ignore "$DC/skrypty/przebieg.py" "$K/probka_kontrola.json" "$RW/wyniki/ewal" "$DCR/wyniki/idx" "$TOK" "$K/przebieg" 1 \
    walidacja="$DCR/wyniki/idx_wal" > /dev/null
  $PY -I "$DC/skrypty/ewal_czeste.py" "$K/przebieg" "$RW/wyniki/ewal" "$K/ew13" > /dev/null
  ORYG=()
  if [ "$ZB" = cranemath ]; then
    $PY -I -W ignore "$DC/skrypty/przebieg.py" "$K/probka_kontrola_oryg.json" "$RW/wyniki/ewal" "$DCR/wyniki/idx" "$TOK" "$K/przebieg_oryg" 1 > /dev/null
    $PY -I "$DC/skrypty/ewal_czeste.py" "$K/przebieg_oryg" "$RW/wyniki/ewal" "$K/ew13_oryg" > /dev/null
    ORYG=(oryg="$K/przebieg_oryg,$K/ew13_oryg")
  fi
  $PY -I "$W/skrypty/agreguj_mat.py" "$ZB" "$K/przebieg" "$K/ew13" "$PRE" "$K/agreguj.json" "$K/probka.jsonl" "$K/wybor.json" \
    walidacja="$DCR/wyniki/idx_wal" ${ORYG[@]+"${ORYG[@]}"} entech="$RW/wyniki/bazy" en8x3b="$RW/wyniki/bazy" fwe109="$RW/wyniki/bazy" > /dev/null
  $PY -I "$W/skrypty/kontrola_mat.py" sprawdz "$ZB" "$K"
  cp "$K/kontrola_wynik.json" "$D/wyniki/kontrola.json"
  ;;
eksport)  # krok 9-10 METODOLOGII: kopia robocza repo zgłoszeń + nakładka eksport/ + karta zbioru, shard.write, test kontraktowy, check.py
  # EXPY: venv z requirements-dev.txt repo zgłoszeń (Presidio, spaCy en_core_web_lg); domyślnie venv dane/pr-zgloszenia
  EXPY=${EXPY:-$REPO/dane/pr-zgloszenia/venv/bin/python}
  Z=$RW/zgloszenia
  [ -f "$Z/src/shard.py" ] || { echo "brak kopii repo zgłoszeń w $Z (hf download SlayerLab/dataset-team-submissions --exclude 'data/**/*.parquet')" >&2; exit 2; }
  case "$ZB" in finemath4) KEY=finemath_4plus_en ;; cranemath) KEY=cranemath_en ;; stackedu) KEY=stack_edu_python ;; esac
  cp -R "$W/eksport/." "$Z/"
  mkdir -p "$Z/data/$KEY"
  cp "$D/eksport/$KEY.md" "$Z/data/$KEY/$KEY.md"
  (cd "$Z" && $NICE "$EXPY" src/clean_$KEY.py "$R/wyniki/wybor.json" "${PII_PROC:-8}")
  (cd "$Z" && "$EXPY" -m pytest "src/test_${KEY}_contract.py" -q && "$EXPY" src/check.py --source "$KEY")
  cp "$Z/data/$KEY/$KEY.stats.json" "$WD/eksport_stats.json"
  shasum -a 256 "$Z/data/$KEY/$KEY.parquet" | tee "$WD/eksport_sha256.txt"
  ;;
*)
  sed -n 2,8p "$0"; exit 2
  ;;
esac
