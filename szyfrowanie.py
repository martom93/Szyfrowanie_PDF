import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfReader, PdfWriter

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

    print(f"Pliki zosta³y zaszyfrowane w folderze: {output_folder}")

def select_files():
    file_paths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
    if file_paths:
        entry_input.delete(0, tk.END)
        entry_input.insert(0, ";".join(file_paths))

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        entry_output.delete(0, tk.END)
        entry_output.insert(0, folder_path)

def on_encrypt():
    input_pdfs = entry_input.get().split(";")
    output_folder = entry_output.get()
    password = entry_password.get()
    confirm_password = entry_confirm_password.get()

    if not input_pdfs or not output_folder or not password or not confirm_password:
        messagebox.showwarning("Brak danych", "Wszystkie pola musz¹ byæ wype³nione.")
        return

    if password != confirm_password:
        messagebox.showwarning("B³¹d has³a", "Has³a nie s¹ zgodne.")
        return

    try:
        encrypt_pdfs(input_pdfs, output_folder, password)
        messagebox.showinfo("Sukces", "Pliki zosta³y zaszyfrowane.")
        
        # Czyœæ pola po pomyœlnym szyfrowaniu
        entry_input.delete(0, tk.END)
        entry_output.delete(0, tk.END)
        entry_password.delete(0, tk.END)
        entry_confirm_password.delete(0, tk.END)
        
    except Exception as e:
        messagebox.showerror("B³¹d", str(e))

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

# Tworzenie g³ównego okna
root = tk.Tk()
root.title("Szyfrowanie plików PDF")

# Ustawianie ikony okna (tylko dla formatów .ico)
#icon_path = "hype.ico"
#root.iconbitmap(icon_path)

# Ustawianie rozmiaru okna
window_width = 500
window_height = 250
root.geometry(f"{window_width}x{window_height}")

# Wyœrodkowanie okna na ekranie
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Zablokowanie zmiany rozmiaru okna
root.resizable(False, False)

# Etykiety i pola do wprowadzania danych
tk.Label(root, text="Pliki wejœciowe:").grid(row=0, column=0, padx=10, pady=10)
entry_input = tk.Entry(root, width=40)
entry_input.grid(row=0, column=1, padx=10, pady=10)
btn_browse_input = tk.Button(root, text="Wybierz pliki...", command=select_files)
btn_browse_input.grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="Folder wyjœciowy:").grid(row=1, column=0, padx=10, pady=10)
entry_output = tk.Entry(root, width=40)
entry_output.grid(row=1, column=1, padx=10, pady=10)
btn_select_folder = tk.Button(root, text="Wybierz folder...", command=select_folder)
btn_select_folder.grid(row=1, column=2, padx=10, pady=10)

tk.Label(root, text="Has³o:").grid(row=2, column=0, padx=10, pady=10)
entry_password = tk.Entry(root, show="*", width=40)
entry_password.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root, text="PotwierdŸ has³o:").grid(row=3, column=0, padx=10, pady=10)
entry_confirm_password = tk.Entry(root, show="*", width=40)
entry_confirm_password.grid(row=3, column=1, padx=10, pady=10)

# Przycisk do uruchomienia szyfrowania i przycisk do informacji o autorze
frame_buttons = tk.Frame(root)
frame_buttons.grid(row=4, column=0, columnspan=3, pady=20)

btn_encrypt = tk.Button(frame_buttons, text="Szyfruj PDF", command=on_encrypt)
btn_encrypt.pack(side=tk.LEFT, padx=10)

btn_author_info = tk.Button(frame_buttons, text="Informacje o autorze", command=show_author_info)
btn_author_info.pack(side=tk.RIGHT, padx=10)

# Uruchomienie g³ównej pêtli aplikacji
root.mainloop()