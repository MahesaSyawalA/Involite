import json
from datetime import datetime

# Path ke file JSON
file_path = "./data_barang.json"

# Fungsi untuk membaca data dari file JSON
def baca_data():
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # Jika file tidak ditemukan atau kosong, kembalikan list kosong
        return []

# Fungsi untuk menulis data ke file JSON
def tulis_data(data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

# Fungsi untuk menambahkan barang masuk
def InputBarangMasuk():
    nama = str(input("Masukkan nama barang: "))
    harga_beli_barang = int(input("Masukkan harga beli barang: "))
    harga_jual_barang = int(input("Masukkan harga jual barang: "))
    stok_barang = int(input("Masukkan jumlah stok barang: "))

    # Ambil tanggal saat ini
    nowDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Membuat data barang baru
    dataBarangMasuk = {
        "nama": nama,
        "harga_beli": harga_beli_barang,
        "harga_jual": harga_jual_barang,
        "stok": stok_barang,
        "tanggal_masuk": nowDate
    }

    # Membaca data yang ada dan menambahkan data baru
    data = baca_data()
    data.append(dataBarangMasuk)

    # Menulis data kembali ke file JSON
    tulis_data(data)
    print("Data berhasil ditambahkan!")

# Menampilkan data yang sudah ada
print("Data Barang:")
print(baca_data())

# Menjalankan fungsi berdasarkan input pengguna
action = str(input("Apakah ingin menambahkan data? ya/tidak: ")).lower()
if action == "ya":
    InputBarangMasuk()
