# Sorteggio Casuale

Applicazione Python con interfaccia grafica per estrarre nomi in modo casuale da un file di testo.
Il sorteggio deve essere equo e non prevedibile.

## Funzionalità

- Carica un file `.txt` contenente un nome per riga
- Specifica quanti nomi estrarre
- Interfaccia grafica semplice e autonoma
- Rilevamento e eliminazione di nomi duplicati
- Sorteggio casuale tramite `random.SystemRandom()`
	Basa il funzionamento sulla fonte di entropia del sistema operativo e non su generatori pseudo-casuali.
	Le occorrenze estrattei dipenderanno da eventi fisici e temporali (movimenti del mouse, interrupt hardware, jitter di CPU) non alterabili/prevedibili e riproducibili.
- Generazione report di estrazione con graduatoria finale

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

## Primo Avvio

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
   ```

4. **Verificare se un file e' stato manomesso**
	Lanciare da riga comando il seguente comando e confrontare gli hash. Se questi due coincidono il file non è stato alterato.
	Es.
	```bash
	sha256sum estrazione_20251031_184522.txt
	```

## Utilizzo

![Interfaccia principale](img/Interfaccia_principale.png)

	Tramite l'interfaccia principale e' possibile: 
		1) caricare una lista da file, e' omportante che ogni occorrenza sia su una riga
		2) salvare l'estrazione su un file testuale nella posizione desiderata. il file riporterà un nome standard "estrazione_AAAAMMGG_HHmmss.txt"
		3) se necessario rieseguire un nuovo sorteggio, tramite il pulsante "ricostruisci lista da report" sarà possibile estrarre la lista di partenza con possibilità di escludere o no dalla lista le occorrenze già estratte.
			N.B. il report salvato dalla seconda estrazione riporterà come nuova lista originale la lista utilizzata, se sono state rimosse le occorrenze selezionate, queste non saranno più visibili nel nuovo report.
		 
	
