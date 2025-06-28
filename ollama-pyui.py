#!/usr/bin/env python3

import tkinter as tk
import threading
import ollama

class OllamaUI:
    def __init__(s):
        s.root = tk.Tk()
        s.root.title("Ollama UI")
        s.root.geometry("500x450")  # altezza aumentata

        s.txt = tk.Text(s.root, wrap="word")
        s.txt.pack(expand=True, fill="both")

        f = tk.Frame(s.root, height=40)
        f.pack(fill="x")
        f.pack_propagate(False)

        s.e = tk.Entry(f, font=("Arial", 12))
        s.e.pack(side="left", expand=True, fill="x", padx=4, pady=4)
        s.e.focus_set()  # cursore attivo subito
        s.e.bind("<Return>", lambda e: s.run_thread())  # Invio invia

        tk.Button(f, text="➤", command=s.run_thread).pack(side="right", padx=4)

        s.model = ollama.list()['models'][0]['model']
        s.root.mainloop()

    def run_thread(s):
        threading.Thread(target=s.ask).start()

    def ask(s):
        q = s.e.get()
        s.e.delete(0, tk.END)
        s.txt.insert(tk.END, f"🧑 {q}\n🤖 ")
        s.txt.see(tk.END)

        for chunk in ollama.chat(s.model, messages=[{'role': 'user', 'content': q}], stream=True):
            s.txt.insert(tk.END, chunk['message']['content'])
            s.txt.see(tk.END)
            s.root.update_idletasks()

        s.txt.insert(tk.END, "\n\n")

if __name__ == "__main__":
    OllamaUI()
