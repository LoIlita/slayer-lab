#!/bin/bash
# Strażnik pamięci: uruchamia krok odtworz.sh i pilnuje pamięci do jego końca.
# Użycie: bash robocze/straznik.sh <krok>   (z katalogu dane/dclm-en)
# Pauza (STOP) przy wolnej < 25% albo swap > 4096 MB; wznowienie (CONT) przy wolnej > 40%.
# Przerwanie (TERM) przy pauzie > 15 min albo wolnej < 15%.
set -u
K=$1
D=/Users/lolita/Documents/GitHub/slayer-lab/dane/dclm-en
L=$D/robocze/logi
cd "$D" || exit 2
wolna() { memory_pressure | tail -1 | grep -oE '[0-9]+' | tail -1; }
swapmb() { sysctl vm.swapusage | sed -E 's/.*used = ([0-9.]+)M.*/\1/' | cut -d. -f1; }
load() { sysctl -n vm.loadavg | tr -d '{}' | xargs; }
potomki() { local p; for p in $(pgrep -P "$1"); do echo "$p"; potomki "$p"; done; }
pytony() { for p in $(potomki "$1"); do ps -o comm= -p "$p" 2>/dev/null | grep -qi python && echo "$p"; done; }
rss_mb() { local s=0 r; for p in $(potomki "$1"); do r=$(ps -o rss= -p "$p" 2>/dev/null | xargs); s=$((s + ${r:-0})); done; echo $((s / 1024)); }
log() { echo "$(date '+%F %T') [$K] $*" >> "$L/straznik.log"; }

echo "$(date '+%F %T') START wolna=$(wolna)% load=$(load) swap=$(swapmb)MB" > "$L/straznik_$K.log"
nohup nice -n 10 bash skrypty/odtworz.sh "$K" > "$L/$K.log" 2>&1 &
P=$!
t0=$(date +%s); szczyt=0; i=0; pauzy=0
while kill -0 "$P" 2>/dev/null; do
  sleep 30
  kill -0 "$P" 2>/dev/null || break
  f=$(wolna); s=$(swapmb); r=$(rss_mb "$P"); [ "$r" -gt "$szczyt" ] && szczyt=$r
  i=$((i + 1))
  [ $((i % 4)) -eq 0 ] && echo "$(date '+%F %T') wolna=${f}% load=$(load) swap=${s}MB rss_kroku=${r}MB" >> "$L/straznik_$K.log"
  if [ "$f" -lt 15 ]; then
    log "TERM: wolna=${f}% < 15% swap=${s}MB load=$(load)"; kill -TERM $(pytony "$P") "$P" 2>/dev/null; break
  fi
  if [ "$f" -lt 25 ] || [ "$s" -gt 4096 ]; then
    PY=$(pytony "$P"); ps0=$(date +%s); pauzy=$((pauzy + 1))
    log "PAUZA (STOP pid $PY): wolna=${f}% swap=${s}MB load=$(load) rss_kroku=${r}MB"
    kill -STOP $PY 2>/dev/null
    while :; do
      sleep 30
      f=$(wolna); s=$(swapmb)
      if [ "$f" -lt 15 ] || [ $(( $(date +%s) - ps0 )) -gt 900 ]; then
        log "TERM po pauzie $(( $(date +%s) - ps0 ))s: wolna=${f}% swap=${s}MB load=$(load)"
        kill -TERM $PY "$P" 2>/dev/null; kill -CONT $PY 2>/dev/null; break 2
      fi
      if [ "$f" -gt 40 ]; then
        log "WZNOWIENIE (CONT) po $(( $(date +%s) - ps0 ))s: wolna=${f}% swap=${s}MB load=$(load)"
        kill -CONT $PY 2>/dev/null; break
      fi
    done
  fi
done
wait "$P"; kod=$?
echo "$(date '+%F %T') KONIEC kod=$kod czas=$(( $(date +%s) - t0 ))s szczyt_rss=${szczyt}MB pauzy=$pauzy wolna=$(wolna)% swap=$(swapmb)MB" >> "$L/straznik_$K.log"
tail -1 "$L/straznik_$K.log"
exit $kod
