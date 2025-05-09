#!/bin/bash

# Suche nach dem Python-Bot-Prozess
prozess_id=$(ps aux | grep "python bot.py" | grep -v "grep" | awk '{print $2}')

# ..berpr..fe, ob ein Prozess gefunden wurde
if [ -n "$prozess_id" ]; then
  echo "Killing Prozess mit ID: $prozess_id"
  kill "$prozess_id"
else
  echo "Kein laufender Python-Bot-Prozess gefunden."
fi

# Starte den Python-Bot im Hintergrund
echo "Starte den Python-Bot im Hintergrund..."
nohup python bot.py &
echo "Python-Bot gestartet (siehe nohup.out fuer Details)."