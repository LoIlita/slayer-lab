#!/bin/bash
# Ponowny eksport JEDNEJ wysłanej części (albo ramienia mikroanneal) z maską zaciemnionych e-maili w tekście stron
# (aneks 2026-11-27 zaciemnione_proza w preregistracji źródła). Pule stron nie są już na dysku, więc wiersze bierze
# eksport/src/reexport_masked.py z poprzedniego eksportu części (pobranego z HF); dalej jak eksport_czesci.sh: shard.write,
# test kontraktowy, check.py tylko z tą częścią w data/ (wyłącznie oczekiwane linie), porównanie z poprzednim eksportem
# (porownaj_eksporty.py prose_obf: te same id i kolejność, tekst = stary po masce, reszta kolumn bez zmian), sha256.
# Użycie: bash remaskuj_czesc.sh <klucz_bazowy> <klucz_czesci> <liczba_czesci|0> <stary.parquet> <stary.stats.json> <datasheet.md> <katalog_wyjscia>
#   klucz_czesci = klucz_bazowy i liczba_czesci 0 dla ramienia (klucz bazowy jest w rejestrze repo zgłoszeń).
set -euo pipefail

BASE=$1
K=$2
N=$3
OLD=$4
OLDS=$5
SHEET=$6
OUT=$7
REPO=$(cd "$(dirname "$0")/../../.." && pwd)
W=$REPO/dane/matematyka-wspolne
RW=$W/robocze
PY=$RW/venv/bin/python
EXPY=${EXPY:-$REPO/dane/pr-zgloszenia/venv/bin/python}
Z=$RW/zgloszenia_maska_$BASE
mkdir -p "$Z" "$OUT"
rsync -a --delete --exclude data --exclude .git "$RW/zgloszenia/" "$Z/"
cp -R "$W/eksport/." "$Z/"
if [ "$N" != 0 ]; then
  $PY "$W/skrypty/rejestr_czesci.py" "$Z" "$BASE" "$N" "$SHEET"
fi
find "$Z/data" -mindepth 1 -maxdepth 1 -type d -exec rm -rf {} +
mkdir -p "$Z/data/$K"
cp "$SHEET" "$Z/data/$K/$K.md"
(cd "$Z" && /usr/bin/nice -n 10 "$EXPY" src/reexport_masked.py "$OLD" "$OLDS" "$K")
(cd "$Z" && MAT_KEY=$K "$EXPY" -m pytest "src/test_${BASE}_contract.py" src/test_mask_prose.py -q)
(cd "$Z" && "$EXPY" src/check.py --source "$K" > "$Z/data/$K/$K.check.txt") || true
if grep -vE "^$K(/.+)?: (PII left after masking: second pass adds|stats\.json pii has no presidio record)" "$Z/data/$K/$K.check.txt"; then
  echo "$K: check.py zgłasza nieoczekiwany błąd (wyżej)" >&2; exit 1
fi
$PY "$W/skrypty/porownaj_eksporty.py" "$OLD" "$Z/data/$K/$K.parquet" prose_obf "$Z/data/$K/$K.porownanie.json" > /dev/null
$PY -c "import json,sys; w=json.load(open(sys.argv[1])); assert w['niezgodne'] == 0 and w['token_count_zmieniony_poza_zmienionym_tekstem'] == 0, w" \
  "$Z/data/$K/$K.porownanie.json"
rm -rf "${OUT:?}/$K"
mv "$Z/data/$K" "$OUT/$K"
(cd "$OUT/$K" && shasum -a 256 "$K.parquet" > "$K.sha256")
echo "$K: $(wc -l < "$OUT/$K/$K.check.txt") linii check.py (oczekiwane), $(cut -c1-12 "$OUT/$K/$K.sha256"), $($PY -c "import json,sys; w=json.load(open(sys.argv[1])); print('wiersze', w['wiersze_stary'], '->', w['wiersze_nowy'], 'zmienione', w['tekst_zmieniony'], 'usuniete', len(w['usuniete']))" "$OUT/$K/$K.porownanie.json")"
