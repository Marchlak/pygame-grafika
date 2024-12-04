from tkinter import filedialog

def choose_file():
    path = filedialog.askopenfilename(
        title="Wybierz plik",
        filetypes=(("Wszystkie pliki", "*.*"), ("Tekstowe", "*.txt"), ("Obrazy", "*.ppm;*.pbm;*.pgm"))
    )
    return path

