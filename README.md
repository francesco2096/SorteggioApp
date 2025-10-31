# Sorteggio Casuale

Applicazione Python con interfaccia grafica per estrarre nomi in modo casuale da un file di testo.
Il sorteggio deve essere equo e non prevedibile.

## Funzionalità

- Carica un file `.txt` contenente un nome per riga
- Specifica quanti nomi estrarre
- Interfaccia grafica semplice e autonoma
- Sorteggio casuale tramite `random.SystemRandom()`
	Basa il funzionamento sulla fonte di entropia del sistema operativo e non su generatori pseudo-casuali.
	Le occorrenze estrattei dipenderanno da eventi fisici e temporali (movimenti del mouse, interrupt hardware, jitter di CPU) non alterabili/prevedibili e riproducibili.

## Dettagli tecnici
- Fonte di entropia reale: 
	su Linux/macOS usa /dev/urandom; 
	su Windows usa CryptGenRandom() o API equivalenti.
- Equità statistica:
	ogni nome ha la stessa probabilità di essere selezionato.
- Sicurezza: 
	il processo non è deterministico, quindi non può essere riprodotto o manipolato tramite un seme noto.

## Requisiti

- Python 3.8 o superiore  
- Librerie standard (`tkinter`, `random`)  
- Per generare un `.exe`: `pyinstaller`

## Utilizzo

Per essere eseguito in modalita' user-friendly e' necessaria la compilazione nell' ambiente di destinazione

1. **Avvia l’applicazione da windows**

	Lanciare script compile.bat, questo generera' un eseguibile nella cartella dist di progetto "SorteggioApp"
	Lanciare con doppio click l' eseguibile creato

2. **Avvia l’applicazione da linux/macOS**

	Lanciare script compile.sh, questo generera' un eseguibile nella cartella dist di progetto "SorteggioApp"
	Lanciare con doppio click l' eseguibile creato

3. **Avvia l’applicazione da cli**
   ```bash
   python3 SorteggioApp.py
