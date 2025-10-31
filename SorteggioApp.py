import tkinter as tk
from tkinter import filedialog, messagebox
import random

class SorteggioApp:
    def __init__(self, master):
        self.master = master
        master.title("Sorteggio Casuale")

        tk.Label(master, text="Carica un file con un nome per riga:").pack(pady=5)

        tk.Button(master, text="Carica File", command=self.carica_file).pack(pady=5)

        frame_num = tk.Frame(master)
        frame_num.pack(pady=5)
        tk.Label(frame_num, text="Numero di nomi da estrarre:").pack(side=tk.LEFT)
        self.num_entry = tk.Entry(frame_num, width=5)
        self.num_entry.insert(0, "1")
        self.num_entry.pack(side=tk.LEFT, padx=5)

        self.sort_button = tk.Button(master, text="Esegui Sorteggio", command=self.sorteggia, state=tk.DISABLED)
        self.sort_button.pack(pady=10)

        self.result_label = tk.Label(master, text="", font=("Arial", 12, "bold"), justify=tk.LEFT)
        self.result_label.pack(pady=10)

        self.nomi = []

    def carica_file(self):
        path = filedialog.askopenfilename(title="Seleziona file", filetypes=[("File di testo", "*.txt")])
        if not path:
            return
        with open(path, "r", encoding="utf-8") as f:
            self.nomi = [r.strip() for r in f if r.strip()]
        if not self.nomi:
            messagebox.showwarning("Attenzione", "Il file è vuoto o non contiene nomi validi.")
            return
        self.sort_button.config(state=tk.NORMAL)
        messagebox.showinfo("Caricato", f"{len(self.nomi)} nomi caricati.")

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
        estratti = random.SystemRandom().sample(self.nomi, n)
        self.result_label.config(text="Nomi estratti:\n" + "\n".join(estratti))

if __name__ == "__main__":
    root = tk.Tk()
    app = SorteggioApp(root)
    root.mainloop()
