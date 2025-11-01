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

## Utilizzo dell’interfaccia principale

Tramite l’interfaccia principale è possibile:

1. **Selezionare il file di input**
   - **1.1** Caricare una lista di nomi da file di testo.  
     > Ogni nome deve trovarsi su una singola riga.
   - **1.2** Importare una lista di nomi da una precedente estrazione, con possibilità di rimuovere le occorrenze già estratte per effettuare un ripescaggio.

2. **Digitare il numero di occorrenze da estrarre**  
   Inserire il valore nel campo dedicato.

3. **Eseguire il sorteggio**  
   Fare clic sul pulsante **"Esegui Sorteggio"** per avviare l’estrazione casuale.

> **N.B. 1:**  
> A ogni sorteggio viene salvato automaticamente un *report di estrazione* nella stessa cartella del file sorgente.  
> Il file avrà nome standard:  
> `estrazione_AAAAMMGG_HHmmss.txt`

4. **Effettuare un ripescaggio (facoltativo)**  
   Tramite il pulsante **"Importa lista da estrazione precedente"** è possibile rieseguire un’estrazione a partire dalla lista codificata nel report precedente.  
   L’utente può scegliere se escludere o meno le occorrenze già estratte.

> **N.B. 2:**  
> Il report generato dopo un ripescaggio conterrà come nuova *lista originale* quella effettivamente utilizzata.  
> Se durante l’importazione sono state rimosse le occorrenze già estratte, queste non compariranno più nel nuovo report.

---

![Interfaccia principale](img/Interfaccia_principale.png)
