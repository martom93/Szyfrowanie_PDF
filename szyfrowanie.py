import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfReader, PdfWriter
import os

# Globalna lista przechowująca ścieżki do plików
loaded_files = []

def shorten_filename(filename, max_length=32):
    """Skraca nazwę pliku do określonej długości, dodając wielokropek na końcu, jeśli jest zbyt długa."""
    if len(filename) > max_length:
        return filename[:max_length-3] + "..."  # Skróć do max_length-3 i dodaj '...'
    return filename

def encrypt_pdfs(input_pdfs, output_folder, password):
    for input_pdf in input_pdfs:
        file_name = input_pdf.split("/")[-1].split("\\")[-1]
        output_pdf = f"{output_folder}/{file_name}"
        reader = PdfReader(input_pdf)
        writer = PdfWriter()

        for page_num in range(len(reader.pages)):
            writer.add_page(reader.pages[page_num])

        writer.encrypt(password)

        with open(output_pdf, 'wb') as output_file:
            writer.write(output_file)

    print(f"Pliki zostały zaszyfrowane w folderze: {output_folder}")

def select_files():
    # Wybierz pliki PDF
    file_paths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
    for file_path in file_paths:
        if file_path not in loaded_files:
            loaded_files.append(file_path)
            display_files()
    adjust_window_size()

def select_folder_with_pdfs():
    # Wybierz folder z plikami PDF
    folder_path = filedialog.askdirectory()
    if folder_path:
        # Pobierz wszystkie pliki .pdf z wybranego folderu
        pdf_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.pdf')]
        for file_path in pdf_files:
            if file_path not in loaded_files:
                loaded_files.append(file_path)
        display_files()
        adjust_window_size()

def display_files():
    # Czyść istniejące elementy z ramki
    for widget in frame_files.winfo_children():
        widget.destroy()

    # Wyświetl każdy plik na liście wraz z przyciskiem usuwania
    for idx, file_path in enumerate(loaded_files):
        file_name = file_path.split("/")[-1].split("\\")[-1]
        short_name = shorten_filename(file_name)
        lbl_file = tk.Label(frame_files, text=short_name, anchor="w")
        lbl_file.grid(row=idx, column=0, sticky="w", padx=5)

        btn_remove = tk.Button(frame_files, text="Usuń", command=lambda path=file_path: remove_file(path))
        btn_remove.grid(row=idx, column=1, padx=5)

def remove_file(file_path):
    # Usuń plik z listy i zaktualizuj widok
    loaded_files.remove(file_path)
    display_files()
    adjust_window_size()

def adjust_window_size():
    # Dopasuj wysokość okna w zależności od liczby plików
    base_height = 280  # Podstawowa wysokość okna
    file_height = 30   # Dodatkowa wysokość na każdy plik
    new_height = base_height + file_height * len(loaded_files)
    root.geometry(f"{window_width}x{new_height}")

    # Aktualizuj rozmieszczenie przycisków
    update_layout()

def update_layout():
    """Aktualizuje położenie przycisków w zależności od wysokości okna."""
    height = root.winfo_height()
    
    # Ustaw położenie ramki z przyciskami
    frame_buttons.place(x=(window_width // 2) - (frame_buttons.winfo_width() // 2), y=height - 50)  # Przesunięcie wyżej

    # Ustaw położenie adnotacji
    author_label.place(x=0, y=height - 20, width=window_width)  # Przesunięcie wyżej

def reset_gui():
    """Resetuje GUI do początkowego stanu."""
    # Wyczyść listę plików i odśwież wyświetlanie
    loaded_files.clear()
    display_files()

    # Wyczyść pola tekstowe
    entry_output.delete(0, tk.END)
    entry_password.delete(0, tk.END)
    entry_confirm_password.delete(0, tk.END)

    # Resetuj rozmiar okna do początkowego
    root.geometry(f"{window_width}x{window_height}")

    # Przywróć rozmieszczenie elementów do początkowego stanu
    frame_files.grid(row=6, column=0, columnspan=3, pady=10)
    frame_buttons.place(x=(window_width // 2) - (frame_buttons.winfo_width() // 2), y=window_height - 100)  # Przywróć wysokość
    author_label.place(x=0, y=window_height - 60, width=window_width)  # Przywróć wysokość

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        entry_output.delete(0, tk.END)
        entry_output.insert(0, folder_path)

def on_encrypt():
    if not loaded_files:
        messagebox.showwarning("Brak plików", "Musisz dodać pliki do zaszyfrowania.")
        return

    output_folder = entry_output.get()
    password = entry_password.get()
    confirm_password = entry_confirm_password.get()

    if not output_folder or not password or not confirm_password:
        messagebox.showwarning("Brak danych", "Wszystkie pola muszą być wypełnione.")
        return

    if password != confirm_password:
        messagebox.showwarning("Błąd hasła", "Hasła nie są zgodne.")
        return

    try:
        encrypt_pdfs(loaded_files, output_folder, password)
        messagebox.showinfo("Sukces", "Pliki zostały zaszyfrowane.")
        
        # Resetuj GUI do stanu początkowego
        reset_gui()
        
    except Exception as e:
        messagebox.showerror("Błąd", str(e))

def show_author_info():
    author_info = (
        "Autor programu: \n"
        "Marcin Tomaszewski\n"
        "Email: tomaszewsky.marcin@gmail.com\n"
        "GitHub: github.com/martom93\n"
        "\n"
        "Program do szyfrowania plików PDF.\n"
    )
    messagebox.showinfo("Informacje o autorze", author_info)

# Tworzenie głównego okna
root = tk.Tk()
root.title("Szyfrowanie plików PDF")

# Ustawianie rozmiaru okna
window_width = 500
window_height = 230
root.geometry(f"{window_width}x{window_height}")

# Ustaw minimalną wysokość okna
root.minsize(width=window_width, height=230)

# Wyśrodkowanie okna na ekranie
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Etykiety i pola do wprowadzania danych
tk.Label(root, text="Folder wyjściowy:").grid(row=3, column=0, padx=10, pady=10)
entry_output = tk.Entry(root, width=40)
entry_output.grid(row=3, column=1, padx=10, pady=10)
btn_select_folder = tk.Button(root, text="Wybierz folder...", command=select_folder)
btn_select_folder.grid(row=3, column=2, padx=10, pady=10)

tk.Label(root, text="Hasło:").grid(row=4, column=0, padx=10, pady=10)
entry_password = tk.Entry(root, show="*", width=40)
entry_password.grid(row=4, column=1, padx=10, pady=10)

tk.Label(root, text="Potwierdź hasło:").grid(row=5, column=0, padx=10, pady=10)
entry_confirm_password = tk.Entry(root, show="*", width=40)
entry_confirm_password.grid(row=5, column=1, padx=10, pady=10)

# Przycisk do wyboru plików i folderu z PDF w jednej linii
frame_file_buttons = tk.Frame(root)
frame_file_buttons.grid(row=0, column=0, columnspan=3, pady=5)

btn_browse_input = tk.Button(frame_file_buttons, text="Wybierz pliki...", command=select_files, width=16, bg="blue", fg="white")
btn_browse_input.pack(side=tk.LEFT, padx=5)

btn_select_pdfs_folder = tk.Button(frame_file_buttons, text="Wybierz folder z PDF", command=select_folder_with_pdfs, width=22, bg="blue", fg="white")
btn_select_pdfs_folder.pack(side=tk.LEFT, padx=5)

# Ramka na listę plików i przyciski usuwania
frame_files = tk.Frame(root)
frame_files.grid(row=6, column=0, columnspan=3, pady=10)

# Ramka na przyciski szyfrowania i informacji o autorze
frame_buttons = tk.Frame(root)
frame_buttons.place(x=(window_width // 2) - (frame_buttons.winfo_width() // 2), y=window_height - 100)  # Ustaw wyżej

btn_encrypt = tk.Button(frame_buttons, text="Szyfruj PDF", command=on_encrypt)
btn_encrypt.pack(side=tk.LEFT, padx=5)

btn_author_info = tk.Button(frame_buttons, text="Informacje o autorze", command=show_author_info)
btn_author_info.pack(side=tk.LEFT, padx=5)

# Adnotacja z imieniem i nazwiskiem autora na dole okna
author_label = tk.Label(root, text="Wykonawca: Marcin Tomaszewski", font=("Arial", 8), fg="grey")
author_label.grid(row=7, column=0, columnspan=3, pady=10)  # Przesunięcie wyżej

# Dodanie obsługi zdarzenia zmiany rozmiaru okna
root.bind("<Configure>", lambda event: update_layout())

# Uruchomienie głównej pętli aplikacji
root.mainloop()
