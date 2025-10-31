@echo off
REM =====================================================
REM Compilazione automatica di sorteggio.py in eseguibile
REM =====================================================

REM Verifica installazione Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Errore: Python non trovato nel PATH.
    pause
    exit /b 1
)

REM Installa PyInstaller se mancante
python -m pip show pyinstaller >nul 2>nul
if %errorlevel% neq 0 (
    echo Installazione di PyInstaller...
    python -m pip install pyinstaller
)

REM Compilazione
echo Compilazione in corso...
python -m PyInstaller --onefile --noconsole SorteggioApp.py

REM Verifica risultato
if exist dist\SorteggioApp.exe (
    echo.
    echo Compilazione completata con successo.
    echo File generato: dist\SorteggioApp.exe
) else (
    echo.
    echo Errore: eseguibile non trovato.
)

pause
