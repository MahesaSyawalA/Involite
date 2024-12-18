import json
from datetime import datetime
import uuid

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
def tambah_barang(nama, harga_beli, harga_jual, stok):
    try:
        harga_beli = int(harga_beli)
        harga_jual = int(harga_jual)
        stok = int(stok)
    except ValueError:
        raise ValueError("Harga dan stok harus berupa angka!")

    nowDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dataBarang = {
        "idbrg": str(uuid.uuid4()),
        "nama": nama,
        "harga_beli": harga_beli,
        "harga_jual": harga_jual,
        "stok": stok,
        "tanggal_masuk": nowDate
    }

    data = baca_data()
    data.append(dataBarang)
    tulis_data(data)

# Fungsi untuk menampilkan data ke terminal
def tampilkan_data():
    data = baca_data()
    for barang in data:
        print(f"ID: {barang['idbrg']} | Nama: {barang['nama']} | Harga Beli: {barang['harga_beli']} | Harga Jual: {barang['harga_jual']} | Stok: {barang['stok']} | Tanggal Masuk: {barang['tanggal_masuk']}")

# Fungsi untuk menampilkan dashboard barang masuk
def dashboard_barang_masuk():
    data = baca_data()
    if not data:
        print("Tidak ada data barang masuk.")
        return

    print("\n=== Dashboard Barang Masuk ===")
    print(f"{'ID':<36} {'Nama':<20} {'Harga Beli':<12} {'Harga Jual':<12} {'Stok':<6} {'Tanggal Masuk':<20}")
    print("-" * 110)
    for barang in data:
        print(f"{barang['idbrg']:<36} {barang['nama']:<20} {barang['harga_beli']:<12} {barang['harga_jual']:<12} {barang['stok']:<6} {barang['tanggal_masuk']:<20}")

# Fungsi untuk menghapus data berdasarkan ID
def hapus_barang(idbrg):
    data = baca_data()
    data_baru = [barang for barang in data if barang["idbrg"] != idbrg]
    if len(data) == len(data_baru):
        raise ValueError("ID barang tidak ditemukan!")
    tulis_data(data_baru)

# Fungsi untuk memperbarui data barang
def update_barang(idbrg, nama=None, harga_beli=None, harga_jual=None, stok=None):
    data = baca_data()
    for barang in data:
        if barang["idbrg"] == idbrg:
            if nama:
                barang["nama"] = nama
            if harga_beli:
                barang["harga_beli"] = int(harga_beli)
            if harga_jual:
                barang["harga_jual"] = int(harga_jual)
            if stok:
                barang["stok"] = int(stok)
            break
    else:
        raise ValueError("ID barang tidak ditemukan!")

    tulis_data(data)

# Contoh Penggunaan
if __name__ == "__main__":
    while True:
        print("\n=== Manajemen Data Barang ===")
        print("1. Tambah Barang")
        print("2. Tampilkan Data")
        print("3. Dashboard Barang Masuk")
        print("4. Hapus Barang")
        print("5. Update Barang")
        print("6. Keluar")

        pilihan = input("Pilih menu: ")
        if pilihan == "1":
            try:
                nama = input("Masukkan Nama Barang: ")
                harga_beli = input("Masukkan Harga Beli: ")
                harga_jual = input("Masukkan Harga Jual: ")
                stok = input("Masukkan Stok: ")
                tambah_barang(nama, harga_beli, harga_jual, stok)
                print("Barang berhasil ditambahkan!")
            except ValueError as e:
                print(f"Error: {e}")
        elif pilihan == "2":
            tampilkan_data()
        elif pilihan == "3":
            dashboard_barang_masuk()
        elif pilihan == "4":
            idbrg = input("Masukkan ID Barang yang ingin dihapus: ")
            try:
                hapus_barang(idbrg)
                print("Barang berhasil dihapus!")
            except ValueError as e:
                print(f"Error: {e}")
        elif pilihan == "5":
            idbrg = input("Masukkan ID Barang yang ingin diupdate: ")
            nama = input("Masukkan Nama Barang Baru (kosongkan jika tidak ingin mengubah): ")
            harga_beli = input("Masukkan Harga Beli Baru (kosongkan jika tidak ingin mengubah): ")
            harga_jual = input("Masukkan Harga Jual Baru (kosongkan jika tidak ingin mengubah): ")
            stok = input("Masukkan Stok Baru (kosongkan jika tidak ingin mengubah): ")
            try:
                update_barang(idbrg, nama, harga_beli, harga_jual, stok)
                print("Barang berhasil diupdate!")
            except ValueError as e:
                print(f"Error: {e}")
        elif pilihan == "6":
            print("Keluar dari program.")
            break
        else:
            print("Pilihan tidak valid, coba lagi.")
