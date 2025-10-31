#!/bin/bash
# ======================================================
# Compilazione automatica di sorteggio.py in eseguibile
# ======================================================

set -e

echo "==> Verifica installazione di Python"
if ! command -v python3 &> /dev/null; then
    echo "Errore: Python3 non trovato nel PATH."
    exit 1
fi

echo "==> Verifica installazione di PyInstaller"
if ! python3 -m pip show pyinstaller &> /dev/null; then
    echo "Installazione di PyInstaller..."
    python3 -m pip install --user pyinstaller
fi

echo "==> Compilazione in corso..."
python3 -m PyInstaller --onefile SorteggioApp.py

echo
if [ -f "dist/SorteggioApp" ]; then
    echo "Compilazione completata con successo."
    echo "File generato: dist/SorteggioApp"
else
    echo "Errore: eseguibile non trovato."
    exit 1
fi
