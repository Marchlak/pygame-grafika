from tkinter import filedialog
import tkinter as tk

def choose_file():
    root = tk.Tk()
    root.withdraw()
    sciezka = filedialog.askopenfilename(
        title="Wybierz plik",
        filetypes=(("Wszystkie pliki", "*.*"), ("Tekstowe", "*.txt"), ("Obrazy", "*.ppm;*.pgm;*.pbm"))
    )
    root.destroy()
    return sciezka

