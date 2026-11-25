#!/bin/bash
# Eksport pełnej puli części 2 (#346) jako części <klucz>_pNN (krok 9-10 METODOLOGII dla każdej części).
# shard.write i check.py repo zgłoszeń trzymają cały zbiór w pamięci, więc każda część idzie osobno: shard.write, test
# kontraktowy, check.py tylko z tą częścią w data/ (pozostałe przeniesione do katalogu wyjścia), sha256.
# Dedup między częściami nie jest potrzebny w check.py: części to rozłączne kawałki jednej puli po dedupie wewnątrz.
# Użycie: bash eksport_czesci.sh <zbior> <katalog_czesci> <katalog_wyjscia>
#   katalog_czesci: wyjście czesci.py (wybor_pNN.json, czesci.json); wznawialne: gotowe części są pomijane.
# check.py musi kończyć się wyłącznie oczekiwanymi błędami (Presidio wyłączone, datasheet -> Personal data); inny błąd przerywa.
set -euo pipefail

ZB=$1
CZ=$2
OUT=$3
REPO=$(cd "$(dirname "$0")/../../.." && pwd)
W=$REPO/dane/matematyka-wspolne
RW=$W/robocze
PY=$RW/venv/bin/python
EXPY=${EXPY:-$REPO/dane/pr-zgloszenia/venv/bin/python}
case "$ZB" in
  finemath4) KEY=finemath_4plus_en ;;
  stackedu) KEY=stack_edu_python ;;
  infiwebmath4) KEY=infiwebmath_4plus_en ;;
  finemath3) KEY=finemath_3_en ;;
  *) echo "nieznany zbiór $ZB" >&2; exit 2 ;;
esac
D=$REPO/dane/$ZB
Z=$RW/zgloszenia_czesci_$KEY  # osobna kopia na źródło: eksporty różnych źródeł mogą iść równolegle
mkdir -p "$Z" "$OUT"
rsync -a --delete --exclude data --exclude .git "$RW/zgloszenia/" "$Z/"
cp -R "$W/eksport/." "$Z/"
N=$($PY -c "import json,sys; print(len(json.load(open(sys.argv[1]))['czesci']))" "$CZ/czesci.json")
$PY "$W/skrypty/rejestr_czesci.py" "$Z" "$KEY" "$N" "$D/eksport/$KEY.md"
for i in $(seq 1 "$N"); do
  K=${KEY}_p$(printf %02d "$i")
  if [ -f "$OUT/$K/$K.sha256" ]; then echo "$K gotowa"; continue; fi
  find "$Z/data" -mindepth 1 -maxdepth 1 -type d -exec rm -rf {} +
  mkdir -p "$Z/data/$K"
  cp "$Z/arkusze_czesci/$K.md" "$Z/data/$K/$K.md"
  (cd "$Z" && /usr/bin/nice -n 10 "$EXPY" "src/clean_$KEY.py" "$CZ/wybor_p$(printf %02d "$i").json" "${PII_PROC:-8}" "$K")
  (cd "$Z" && MAT_KEY=$K "$EXPY" -m pytest "src/test_${KEY}_contract.py" -q)
  (cd "$Z" && "$EXPY" src/check.py --source "$K" > "$Z/data/$K/$K.check.txt") || true
  if grep -vE "^$K(/.+)?: (PII left after masking: second pass adds|stats\.json pii has no presidio record)" "$Z/data/$K/$K.check.txt"; then  # id FineMath zawiera ':'
    echo "$K: check.py zgłasza nieoczekiwany błąd (wyżej)" >&2; exit 1
  fi
  rm -rf "${OUT:?}/$K"
  mv "$Z/data/$K" "$OUT/$K"
  (cd "$OUT/$K" && shasum -a 256 "$K.parquet" > "$K.sha256")
  echo "$K: $(wc -l < "$OUT/$K/$K.check.txt") linii check.py (oczekiwane), $(cut -c1-12 "$OUT/$K/$K.sha256")"
done
echo KONIEC "$N"
