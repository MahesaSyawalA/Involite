import json
from datetime import datetime
import uuid
from tkinter import Tk, Label, Entry, Button, messagebox, ttk

# Path ke file JSON
file_path = "./data_barang.json"

# Fungsi untuk membaca data dari file JSON
def baca_data():
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Fungsi untuk menulis data ke file JSON
def tulis_data(data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

# Fungsi untuk menambahkan barang masuk
def tambah_barang():
    global selected_idbrg  # Menggunakan variabel global untuk ID yang dipilih
    nama = entry_nama.get()
    harga_beli = entry_harga_beli.get()
    harga_jual = entry_harga_jual.get()
    stok = entry_stok.get()

    if not (nama and harga_beli and harga_jual and stok):
        messagebox.showerror("Input Error", "Semua kolom harus diisi!")
        return

    try:
        harga_beli = int(harga_beli)
        harga_jual = int(harga_jual)
        stok = int(stok)
    except ValueError:
        messagebox.showerror("Input Error", "Harga dan stok harus berupa angka!")
        return

    if selected_idbrg:  # Jika sedang dalam mode update (data lama dipilih)
        messagebox.showerror("Error", "Tidak dapat menambah data saat data dipilih untuk update!\nKlik Reset terlebih dahulu.")
        return

    nowDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dataBarang = {
        "idbrg": str(uuid.uuid4()),  # ID baru untuk data baru
        "nama": nama,
        "harga_beli": harga_beli,
        "harga_jual": harga_jual,
        "stok": stok,
        "tanggal_masuk": nowDate
    }

    data = baca_data()
    data.append(dataBarang)
    tulis_data(data)

    messagebox.showinfo("Berhasil", "Data barang berhasil ditambahkan!")
    reset_form()
    tampilkan_data()

# Fungsi untuk menampilkan data ke dalam tabel
def tampilkan_data():
    for row in tree.get_children():
        tree.delete(row)
    data = baca_data()
    for barang in data:
        tree.insert("", "end", values=(barang["idbrg"], barang["nama"], barang["harga_beli"],
                                       barang["harga_jual"], barang["stok"], barang["tanggal_masuk"]))

# Fungsi untuk menghapus data berdasarkan ID
def hapus_barang():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Pilih data yang ingin dihapus!")
        return

    idbrg = tree.item(selected_item, "values")[0]
    data = baca_data()
    data = [barang for barang in data if barang["idbrg"] != idbrg]
    tulis_data(data)

    messagebox.showinfo("Berhasil", "Data barang berhasil dihapus!")
    tampilkan_data()

# Fungsi untuk mengisi form dengan data yang dipilih
def pilih_barang():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Pilih data yang ingin diupdate!")
        return

    barang = tree.item(selected_item, "values")
    entry_nama.delete(0, "end")
    entry_harga_beli.delete(0, "end")
    entry_harga_jual.delete(0, "end")
    entry_stok.delete(0, "end")

    entry_nama.insert(0, barang[1])
    entry_harga_beli.insert(0, barang[2])
    entry_harga_jual.insert(0, barang[3])
    entry_stok.insert(0, barang[4])

    global selected_idbrg
    selected_idbrg = barang[0]  # Simpan ID barang yang dipilih

# Fungsi untuk memperbarui data barang
def update_barang():
    global selected_idbrg  # Menggunakan variabel global untuk ID yang dipilih
    if not selected_idbrg:
        messagebox.showerror("Error", "Pilih data yang ingin diupdate!")
        return

    nama = entry_nama.get()
    harga_beli = entry_harga_beli.get()
    harga_jual = entry_harga_jual.get()
    stok = entry_stok.get()

    if not (nama and harga_beli and harga_jual and stok):
        messagebox.showerror("Input Error", "Semua kolom harus diisi!")
        return

    try:
        harga_beli = int(harga_beli)
        harga_jual = int(harga_jual)
        stok = int(stok)
    except ValueError:
        messagebox.showerror("Input Error", "Harga dan stok harus berupa angka!")
        return

    data = baca_data()
    for barang in data:
        if barang["idbrg"] == selected_idbrg:
            barang["nama"] = nama
            barang["harga_beli"] = harga_beli
            barang["harga_jual"] = harga_jual
            barang["stok"] = stok
            break

    tulis_data(data)
    messagebox.showinfo("Berhasil", "Data barang berhasil diperbarui!")
    reset_form()
    tampilkan_data()

# Fungsi untuk mereset form input
def reset_form():
    entry_nama.delete(0, "end")
    entry_harga_beli.delete(0, "end")
    entry_harga_jual.delete(0, "end")
    entry_stok.delete(0, "end")
    global selected_idbrg
    selected_idbrg = None

# GUI Utama
root = Tk()
root.title("Manajemen Data Barang")
root.geometry("800x600")

selected_idbrg = None  # Variabel untuk menyimpan ID barang yang dipilih

# Form Input
Label(root, text="Nama Barang:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
entry_nama = Entry(root, width=30)
entry_nama.grid(row=0, column=1, padx=10, pady=10)

Label(root, text="Harga Beli:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
entry_harga_beli = Entry(root, width=30)
entry_harga_beli.grid(row=1, column=1, padx=10, pady=10)

Label(root, text="Harga Jual:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
entry_harga_jual = Entry(root, width=30)
entry_harga_jual.grid(row=2, column=1, padx=10, pady=10)

Label(root, text="Stok:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
entry_stok = Entry(root, width=30)
entry_stok.grid(row=3, column=1, padx=10, pady=10)

# Tombol-tombol aksi
Button(root, text="Tambah Barang", command=tambah_barang).grid(row=4, column=0, pady=10)
Button(root, text="Update Barang", command=update_barang).grid(row=4, column=1, pady=10)
Button(root, text="Hapus Barang", command=hapus_barang).grid(row=4, column=2, pady=10)
Button(root, text="Pilih Barang", command=pilih_barang).grid(row=4, column=3, pady=10)

# Tambahkan tombol Reset Data
Button(root, text="Reset Data", command=reset_form).grid(row=4, column=4, pady=10)

# Tabel Data
columns = ("ID Barang", "Nama", "Harga Beli", "Harga Jual", "Stok", "Tanggal Masuk")
tree = ttk.Treeview(root, columns=columns, show="headings", height=15)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120)

tree.grid(row=5, column=0, columnspan=5, padx=10, pady=10)

# Menampilkan data awal
tampilkan_data()

# Menjalankan GUI
root.mainloop()