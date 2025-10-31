import tkinter as tk
from tkinter import filedialog, messagebox
import random
from datetime import datetime
import os
from collections import defaultdict

ASCII_SIGNATURE = r"""

 /$$$$$$$$                                                                            
| $$_____/                                                                            
| $$     /$$$$$$  /$$$$$$  /$$$$$$$   /$$$$$$$  /$$$$$$   /$$$$$$$  /$$$$$$$  /$$$$$$ 
| $$$$$ /$$__  $$|____  $$| $$__  $$ /$$_____/ /$$__  $$ /$$_____/ /$$_____/ /$$__  $$
| $$__/| $$  \__/ /$$$$$$$| $$  \ $$| $$      | $$$$$$$$|  $$$$$$ | $$      | $$  \ $$
| $$   | $$      /$$__  $$| $$  | $$| $$      | $$_____/ \____  $$| $$      | $$  | $$
| $$   | $$     |  $$$$$$$| $$  | $$|  $$$$$$$|  $$$$$$$ /$$$$$$$/|  $$$$$$$|  $$$$$$/
|__/   |__/      \_______/|__/  |__/ \_______/ \_______/|_______/  \_______/ \______/ 
                                                                                      
   Developed by Francesco Pompilio (Software Engineer)
   GitHub: github.com/francesco2096
"""

class SorteggioApp:
    def __init__(self, master):
        self.master = master
        master.title("Sorteggio Casuale")
        master.geometry("750x650")

        default_font = ("Arial", 18)

        tk.Label(master, text="Carica un file con un nome per riga:", font=default_font).pack(pady=5)
        tk.Button(master, text="Carica File", font=default_font, command=self.carica_file).pack(pady=5)

        self.count_label = tk.Label(master, text="Nomi caricati: 0", font=default_font)
        self.count_label.pack(pady=5)

        frame_num = tk.Frame(master)
        frame_num.pack(pady=5)
        tk.Label(frame_num, text="Numero di nomi da estrarre:", font=default_font).pack(side=tk.LEFT)
        self.num_entry = tk.Entry(frame_num, width=6, font=default_font)
        self.num_entry.insert(0, "1")
        self.num_entry.pack(side=tk.LEFT, padx=5)

        frame_buttons = tk.Frame(master)
        frame_buttons.pack(pady=10)

        self.sort_button = tk.Button(frame_buttons, text="Esegui Sorteggio", font=default_font, command=self.sorteggia, state=tk.DISABLED)
        self.sort_button.pack(side=tk.LEFT, padx=10)

        self.save_button = tk.Button(frame_buttons, text="Salva Estratti su File", font=default_font, command=self.salva_estrazione, state=tk.DISABLED)
        self.save_button.pack(side=tk.LEFT, padx=10)

        frame_text = tk.Frame(master)
        frame_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(frame_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.result_text = tk.Text(
            frame_text,
            wrap=tk.WORD,
            height=12,
            width=60,
            font=("Courier", 18)
        )
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.result_text.config(state=tk.DISABLED)
        self.result_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.result_text.yview)

        self.nomi = []
        self.estratti = []
        self.file_path = None

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

        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        for i, nome in enumerate(self.estratti, start=1):
            self.result_text.insert(tk.END, f"{i}. {nome}\n")
        self.result_text.config(state=tk.DISABLED)

        self.save_button.config(state=tk.NORMAL)

    def salva_estrazione(self):
        if not self.estratti:
            messagebox.showerror("Errore", "Nessuna estrazione da salvare.")
            return

        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_name = f"estrazione_{now}.txt"
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("File di testo", "*.txt")],
            initialfile=default_name,
            title="Salva estrazione come"
        )
        if not path:
            return

        with open(path, "w", encoding="utf-8") as f:
            f.write(f"Data estrazione: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Totale nomi nel file: {len(self.nomi)}\n")
            f.write(f"Nomi estratti ({len(self.estratti)}):\n")
            for i, nome in enumerate(self.estratti, start=1):
                f.write(f"{i}. {nome}\n")

        messagebox.showinfo("File salvato", f"Estratti salvati in:\n{os.path.abspath(path)}")

if __name__ == "__main__":
    print(ASCII_SIGNATURE)
    root = tk.Tk()
    app = SorteggioApp(root)
    root.mainloop()
