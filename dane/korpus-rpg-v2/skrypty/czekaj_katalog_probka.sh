#!/bin/bash
# Po indeksach baz (2 zwolnione procesy) liczy próbkę detektora katalogów.
W=/private/tmp/claude-501/-Users-lolita-Documents-GitHub-labaj-agency/c330a372-3808-4b90-8b3a-9629adcb2efb/scratchpad/korpus-rpg-v2-pracownia
R=/private/tmp/claude-501/-Users-lolita-Documents-GitHub-labaj-agency/6bbfbe99-c494-4e16-a463-2cb16f038e2a/scratchpad/rpg-korpus
until [ -f "$W/wyniki/idx/liczby_indeks.json" ]; do
  if ! pgrep -f skrypty/bazy_indeks.py >/dev/null; then echo "bazy_indeks nie działa, brak wyniku"; tail -3 "$W/logi/bazy_indeks.log"; exit 3; fi
  sleep 20
done
mkdir -p "$W/wyniki/katalog"
/usr/bin/nice -n 10 "$R/venv/bin/python" -I "$W/skrypty/katalog.py" "$R/wyniki/korpus_koncowy.parquet" "$W/wyniki/katalog" 2 sample > "$W/logi/katalog_probka.log" 2>&1
kod=$?
echo "katalog_probka exit=$kod"
tail -2 "$W/logi/katalog_probka.log" | cut -c1-200
exit $kod
