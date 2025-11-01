import tkinter as tk
from tkinter import filedialog, messagebox
import random
from datetime import datetime
import os
import hashlib
import base64
from collections import defaultdict

SOFTWARE_VERSION = "SorteggioApp v1.6.0"
DEFAULT_SAVE_DIR = os.path.join(os.path.expanduser("~"), "SorteggioReports")

ASCII_SIGNATURE = r"""
  ____             _                   _         _    ____  ____  
 / ___|  ___  _ __| |_ ___  __ _  __ _(_) ___   / \  |  _ \|  _ \ 
 \___ \ / _ \| '__| __/ _ \/ _` |/ _` | |/ _ \ / _ \ | |_) | |_) |
  ___) | (_) | |  | ||  __/ (_| | (_| | | (_) / ___ \|  __/|  __/ 
 |____/ \___/|_|   \__\___|\__, |\__, |_|\___/_/   \_\_|   |_|    
                           |___/ |___/                            
                                                                                                                 
   Developed by Francesco Pompilio (Software Engineer)
   GitHub: github.com/francesco2096
"""

class SorteggioApp:
    def __init__(self, master):
        self.master = master
        master.title("SorteggioApp")
        master.geometry("950x800")

        default_font = ("Arial", 18)

        # --- File management buttons ---
        frame_file = tk.Frame(master)
        frame_file.pack(pady=5)

        tk.Label(frame_file, text="Gestione File:", font=default_font).pack(side=tk.LEFT, padx=10)

        tk.Button(frame_file, text="Carica File", font=default_font, command=self.carica_file).pack(side=tk.LEFT, padx=10)
        tk.Button(frame_file, text="Importa Lista da estrazione precedente", font=default_font, command=self.ricostruisci_lista).pack(side=tk.LEFT, padx=10)

        self.count_label = tk.Label(master, text="Nomi caricati: 0", font=default_font)
        self.count_label.pack(pady=5)

        frame_num = tk.Frame(master)
        frame_num.pack(pady=5)
        tk.Label(frame_num, text="Numero di nomi da estrarre:", font=default_font).pack(side=tk.LEFT)
        self.num_entry = tk.Entry(frame_num, width=6, font=default_font)
        self.num_entry.insert(0, "1")
        self.num_entry.pack(side=tk.LEFT, padx=5)

        # --- Esegui sorteggio ---
        frame_sort = tk.Frame(master)
        frame_sort.pack(pady=20)
        self.sort_button = tk.Button(
            frame_sort,
            text="Esegui Sorteggio",
            font=("Arial", 22, "bold"),
            width=20,
            height=2,
            command=self.sorteggia,
            state=tk.DISABLED,
            bg="#2E86C1",
            fg="black",
            activebackground="#1B4F72",
            activeforeground="white"
        )
        self.sort_button.pack()

        # --- Report view buttons ---
        frame_report = tk.Frame(master)
        frame_report.pack(pady=10)
        self.show_report_button = tk.Button(frame_report, text="Mostra lista sorteggiati da Report", font=default_font, command=self.mostra_lista_report)
        self.show_report_button.pack(side=tk.LEFT, padx=10)
        self.show_original_button = tk.Button(frame_report, text="Mostra Lista iniziale da Report", font=default_font, command=self.mostra_lista_partenza_report)
        self.show_original_button.pack(side=tk.LEFT, padx=10)

        # --- Text output ---
        frame_text = tk.Frame(master)
        frame_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(frame_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text = tk.Text(
            frame_text,
            wrap=tk.WORD,
            height=14,
            width=90,
            font=("Courier", 18)
        )
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.result_text.config(state=tk.DISABLED)
        self.result_text.config(yscrollcommand=scrollbar.set)

        scrollbar.config(command=self.result_text.yview)

        # --- Pulsanti inferiori ---
        frame_bottom = tk.Frame(master)
        frame_bottom.pack(side=tk.BOTTOM, fill=tk.X, pady=10, padx=20)

        tk.Button(
            frame_bottom,
            text="Clean",
            font=("Arial", 16),
            command=self.pulisci_output,
            bg="#F7DC6F",
            activebackground="#F4D03F"
        ).pack(side=tk.LEFT)

        tk.Button(
            frame_bottom,
            text="Close",
            font=("Arial", 16),
            command=master.quit,
            bg="#E74C3C",
            fg="black",
            activebackground="#C0392B",
            activeforeground="white"
        ).pack(side=tk.RIGHT)

        # --- Variabili di stato ---
        self.nomi = []
        self.estratti = []
        self.file_path = None
        
    # ---------------- CORE FUNCTIONS ---------------- #
    def carica_file(self):
        self.file_path = filedialog.askopenfilename(title="Seleziona file", filetypes=[("File di testo", "*.txt")])
        if not self.file_path:
            return
        with open(self.file_path, "r", encoding="utf-8") as f:
            righe = [r.strip() for r in f if r.strip()]
        if not righe:
            messagebox.showwarning("Attenzione", "Il file è vuoto o non contiene nomi validi.")
            return

        visti = defaultdict(list)
        for idx, nome in enumerate(righe, start=1):
            visti[nome].append(idx)
        duplicati = {n: l for n, l in visti.items() if len(l) > 1}
        if duplicati:
            modificato = False
            for nome, linee in duplicati.items():
                msg = (
                    f"Trovato nome duplicato:\n\n"
                    f"{nome}\n"
                    f"Presente alle righe: {', '.join(map(str, linee))}\n\n"
                    f"Vuoi rimuovere tutte le copie e mantenerne una sola?"
                )
                risposta = messagebox.askyesno("Duplicato rilevato", msg)
                if risposta:
                    nuova_lista = []
                    visti_nomi = set()
                    for n in righe:
                        if n == nome:
                            if nome not in visti_nomi:
                                nuova_lista.append(n)
                                visti_nomi.add(nome)
                        else:
                            nuova_lista.append(n)
                    righe = nuova_lista
                    modificato = True
                else:
                    messagebox.showwarning("Caricamento annullato", "Caricamento interrotto per duplicati non rimossi.")
                    self.nomi = []
                    self.sort_button.config(state=tk.DISABLED)
                    self.count_label.config(text="Nomi caricati: 0")
                    return
            if modificato:
                with open(self.file_path, "w", encoding="utf-8") as f:
                    f.write("\n".join(righe) + "\n")
                messagebox.showinfo("Aggiornato", "File aggiornato: duplicati rimossi.")
        self.nomi = list(dict.fromkeys(righe))
        self.sort_button.config(state=tk.NORMAL)
        self.count_label.config(text=f"Nomi caricati: {len(self.nomi)}")
        messagebox.showinfo("File valido", f"{len(self.nomi)} nomi caricati correttamente.")

    def sorteggia(self):
        if not self.nomi:
            messagebox.showerror("Errore", "Nessun nome caricato.")
            return
        try:
            n = int(self.num_entry.get())
        except ValueError:
            messagebox.showerror("Errore", "Inserisci un numero valido.")
            return
        if n <= 0:
            messagebox.showerror("Errore", "Il numero deve essere maggiore di 0.")
            return
        if n > len(self.nomi):
            messagebox.showerror("Errore", "Richiesti più nomi di quelli disponibili.")
            return

        self.estratti = random.SystemRandom().sample(self.nomi, n)

        # Visualizza risultati
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        for i, nome in enumerate(self.estratti, start=1):
            self.result_text.insert(tk.END, f"{i}. {nome}\n")
        self.result_text.config(state=tk.DISABLED)

        # Chiede se includere lista originale
        include_original = messagebox.askyesno("Includere lista originale?", "Vuoi includere la lista originale nel report (Base64)?")

        # Salvataggio automatico
        self.salva_report_automatico(include_original)

    def salva_report_automatico(self, include_original):
        if not self.file_path:
            messagebox.showerror("Errore", "Nessun file di origine caricato, impossibile salvare il report.")
            return

        base_dir = os.path.dirname(self.file_path)
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"estrazione_{now}.txt"
        path = os.path.join(base_dir, filename)

        content = f"{SOFTWARE_VERSION}\n"
        content += f"Data estrazione: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        content += f"File origine: {os.path.basename(self.file_path)}\n"
        content += f"Totale nomi nel file: {len(self.nomi)}\n"
        content += f"Nomi estratti ({len(self.estratti)}):\n"
        for i, nome in enumerate(self.estratti, start=1):
            content += f"{i}. {nome}\n"

        if include_original:
            lista_txt = "\n".join(self.nomi)
            lista_b64 = base64.b64encode(lista_txt.encode("utf-8")).decode("utf-8")
            content += "\n<LISTA_BASE64>\n" + lista_b64 + "\n</LISTA_BASE64>\n"

        digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
        content += f"\nSHA256: {digest}\n"

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        messagebox.showinfo("Report salvato", f"Report generato automaticamente in:\n{path}")
        
    # --- Altre funzioni invariate --- #
    def mostra_lista_report(self):
        path = filedialog.askopenfilename(title="Seleziona report per visualizzare la lista estratta", filetypes=[("File di testo", "*.txt")])
        if not path:
            return
        with open(path, "r", encoding="utf-8") as f:
            testo = f.read()
        if "Nomi estratti" not in testo:
            messagebox.showerror("Errore", "Il file selezionato non contiene una sezione di nomi estratti.")
            return
        blocco = testo.split("Nomi estratti", 1)[1]
        blocco = blocco.split("<LISTA_BASE64>")[0] if "<LISTA_BASE64>" in blocco else blocco
        righe = [r for r in blocco.splitlines() if r.strip() and r[0].isdigit() and ". " in r]
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Lista estratti dal report:\n\n")
        for r in righe:
            self.result_text.insert(tk.END, r + "\n")
        self.result_text.config(state=tk.DISABLED)

    def mostra_lista_partenza_report(self):
        path = filedialog.askopenfilename(title="Seleziona report per visualizzare la lista originale", filetypes=[("File di testo", "*.txt")])
        if not path:
            return
        with open(path, "r", encoding="utf-8") as f:
            testo = f.read()
        if "<LISTA_BASE64>" not in testo or "</LISTA_BASE64>" not in testo:
            messagebox.showerror("Errore", "Il file non contiene una sezione LISTA_BASE64.")
            return
        base64_data = testo.split("<LISTA_BASE64>")[1].split("</LISTA_BASE64>")[0].strip()
        try:
            decoded = base64.b64decode(base64_data).decode("utf-8")
            righe = [r.strip() for r in decoded.splitlines() if r.strip()]
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "Lista di partenza dal report:\n\n")
            for i, nome in enumerate(righe, start=1):
                self.result_text.insert(tk.END, f"{i}. {nome}\n")
            self.result_text.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Errore", f"Errore nella decodifica Base64:\n{e}")

    def ricostruisci_lista(self):
        path = filedialog.askopenfilename(title="Seleziona report da cui ricostruire", filetypes=[("File di testo", "*.txt")])
        if not path:
            return
        with open(path, "r", encoding="utf-8") as f:
            testo = f.read()
        if "<LISTA_BASE64>" not in testo or "</LISTA_BASE64>" not in testo:
            messagebox.showerror("Errore", "Il file non contiene una sezione LISTA_BASE64.")
            return
        base64_data = testo.split("<LISTA_BASE64>")[1].split("</LISTA_BASE64>")[0].strip()
        estratti_blocco = ""
        if "Nomi estratti" in testo:
            estratti_blocco = testo.split("Nomi estratti")[1]
            estratti_blocco = estratti_blocco.split("<LISTA_BASE64>")[0] if "<LISTA_BASE64>" in estratti_blocco else estratti_blocco
        estratti_presenti = []
        for riga in estratti_blocco.splitlines():
            if riga.strip() and riga[0].isdigit() and ". " in riga:
                estratti_presenti.append(riga.split(". ", 1)[1].strip())
        try:
            decoded = base64.b64decode(base64_data).decode("utf-8")
            righe = [r.strip() for r in decoded.splitlines() if r.strip()]
            if estratti_presenti:
                rimuovi = messagebox.askyesno("Rimuovere estratti?", f"Trovati {len(estratti_presenti)} nomi già estratti.\nVuoi rimuoverli dalla nuova lista?")
                if rimuovi:
                    righe = [r for r in righe if r not in estratti_presenti]
            self.nomi = list(dict.fromkeys(righe))
            self.count_label.config(text=f"Nomi ricostruiti: {len(self.nomi)}")
            self.sort_button.config(state=tk.NORMAL)
            messagebox.showinfo("Lista ricostruita", f"Ricostruiti {len(self.nomi)} nomi dal file.")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore nella decodifica Base64:\n{e}")

    def pulisci_output(self):
        # Svuota area risultati
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state=tk.DISABLED)
    
        # Reset stato interno
        self.nomi = []
        self.estratti = []
        # self.file_path = None
    
        # UI: aggiorna contatore e disabilita azioni
        self.count_label.config(text="Nomi caricati: 0")
        self.sort_button.config(state=tk.DISABLED)
        
if __name__ == "__main__":
    print(ASCII_SIGNATURE)
    print(f"Versione software: {SOFTWARE_VERSION}")
    root = tk.Tk()
    app = SorteggioApp(root)
    root.mainloop()
