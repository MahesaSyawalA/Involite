import json
from datetime import datetime
from tabulate import tabulate

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
        "idbrg": len(baca_data()) + 1,  # ID unik berdasarkan jumlah data saat ini
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

# Fungsi untuk memperbarui data barang berdasarkan idbrg
def UpdateBarang():
    idbrg = int(input("Masukkan ID Barang yang ingin diperbarui: "))
    data = baca_data()
    barang = next((item for item in data if item["idbrg"] == idbrg), None)
    if barang:
        print(f"Data Barang {idbrg}:")
        print(f"Nama: {barang['nama']}")
        print(f"Harga Beli: {barang['harga_beli']}")
        print(f"Harga Jual: {barang['harga_jual']}")
        print(f"Stok: {barang['stok']}")
        print(f"Tanggal Masuk: {barang['tanggal_masuk']}")
        print("\nMasukkan data baru (biarkan kosong untuk tidak mengubah):")
        nama = input(f"Nama ({barang['nama']}): ") or barang['nama']
        harga_beli_barang = input(f"Harga Beli ({barang['harga_beli']}): ")
        harga_beli_barang = int(harga_beli_barang) if harga_beli_barang else barang['harga_beli']
        harga_jual_barang = input(f"Harga Jual ({barang['harga_jual']}): ")
        harga_jual_barang = int(harga_jual_barang) if harga_jual_barang else barang['harga_jual']
        stok_barang = input(f"Stok ({barang['stok']}): ")
        stok_barang = int(stok_barang) if stok_barang else barang['stok']
        # Update data barang
        barang.update({
            "nama": nama,
            "harga_beli": harga_beli_barang,
            "harga_jual": harga_jual_barang,
            "stok": stok_barang,
            "tanggal_masuk": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        # Menulis data kembali ke file JSON
        tulis_data(data)
        print("Data berhasil diperbarui!")
    else:
        print("ID Barang tidak ditemukan.")

# Fungsi untuk menghapus data barang berdasarkan idbrg
def DeleteBarang():
    idbrg = int(input("Masukkan ID Barang yang ingin dihapus: "))
    data = baca_data()
    barang = next((item for item in data if item["idbrg"] == idbrg), None)
    if barang:
        data.remove(barang)
        # Menulis data kembali ke file JSON
        tulis_data(data)
        print("Data berhasil dihapus!")
    else:
        print("ID Barang tidak ditemukan.")

# Fungsi untuk menampilkan data dalam bentuk tabel
def tampilkan_data():
    data = baca_data()
    if data:
        headers = ["ID Barang", "Nama", "Harga Beli", "Harga Jual", "Stok", "Tanggal Masuk"]
        tabel_data = [
            [d["idbrg"], d["nama"], d["harga_beli"], d["harga_jual"], d["stok"], d["tanggal_masuk"]]
            for d in data
        ]
        print(tabulate(tabel_data, headers=headers, tablefmt="grid"))
    else:
        print("Tidak ada data barang yang tersedia.")

# Menampilkan data yang sudah ada
print("Data Barang:")
tampilkan_data()

# Menjalankan fungsi berdasarkan input pengguna
while True:
    action = input("\nPilih aksi:\n1. Tambah Data\n2. Update Data\n3. Hapus Data\n4. Keluar\nPilihan: ")
    if action == "1":
        InputBarangMasuk()
        print("\nData Barang Terbaru:")
        tampilkan_data()
    elif action == "2":
        UpdateBarang()
        print("\nData Barang Terbaru:")
        tampilkan_data()
    elif action == "3":
        DeleteBarang()
        print("\nData Barang Terbaru:")
        tampilkan_data()
    elif action == "4":
        break
    else:
        print("Pilihan tidak valid.")
