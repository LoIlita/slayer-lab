#!/bin/bash
# Czeka na NER i indeksy baz, potem odpala główny przebieg na 6 procesach (poza NER, więc limit 6 zachowany).
W=/private/tmp/claude-501/-Users-lolita-Documents-GitHub-labaj-agency/c330a372-3808-4b90-8b3a-9629adcb2efb/scratchpad/korpus-rpg-v2-pracownia
R=/private/tmp/claude-501/-Users-lolita-Documents-GitHub-labaj-agency/6bbfbe99-c494-4e16-a463-2cb16f038e2a/scratchpad/rpg-korpus
until grep -q "exit=" "$W/logi/ner.log" 2>/dev/null; do sleep 20; done
until [ -f "$W/wyniki/idx/liczby_indeks.json" ] || ! pgrep -f skrypty/bazy_indeks.py >/dev/null && [ -f "$W/logi/bazy_indeks.log" ] && grep -qE "Traceback|Error" "$W/logi/bazy_indeks.log"; do sleep 30; done
if [ ! -f "$W/wyniki/idx/liczby_indeks.json" ]; then echo "BRAK INDEKSOW"; tail -5 "$W/logi/bazy_indeks.log"; exit 2; fi
until grep -q "KONIEC\|Traceback" "$W/logi/katalog_probka.log" 2>/dev/null; do sleep 20; done
mkdir -p "$W/wyniki/przebieg"
/usr/bin/nice -n 10 "$R/venv/bin/python" -I "$W/skrypty/przebieg.py" "$R/wyniki/korpus_koncowy.parquet" "$W/wyniki/ewal" "$W/wyniki/idx" "$W/wyniki/przebieg" 6 > "$W/logi/przebieg.log" 2>&1
kod=$?
echo "przebieg exit=$kod"
tail -2 "$W/logi/przebieg.log" | cut -c1-200
exit $kod
