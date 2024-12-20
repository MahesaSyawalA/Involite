import json
from tabulate import tabulate

def load_database():
    try:
        with open("database.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Database tidak ditemukan!")
        return None

def save_data(database):
    with open("database.json", "w") as file:
        json.dump(database, file, indent=4)

def dashboard_barang(database):
    while True:
        print("\n==== Dashboard Barang ====")
        print("1. Lihat Semua Barang")
        print("2. Tambah Barang Baru")
        print("3. Edit Barang")
        print("4. Hapus Barang")
        print("5. Keluar")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            lihat_barang(database)
        elif pilihan == "2":
            tambah_barang(database)
            save_data(database)
        elif pilihan == "3":
            edit_barang(database)
            save_data(database)
        elif pilihan == "4":
            hapus_barang(database)
            save_data(database)
        elif pilihan == "5":
            print("\nKeluar dari Dashboard Barang. Sampai jumpa!")
            break
        else:
            print("\nPilihan tidak valid, silakan coba lagi.\n")

def lihat_barang(database):
    print("\n==== Daftar Barang ====")
    barang_list = database.get("barang", [])

    if not barang_list:
        print("\nTidak ada barang dalam database.\n")
        return

    # Membuat tabel dengan data barang
    headers = ["No", "Nama Barang", "Stok", "Harga Jual", "Harga Modal", "Kategori", "Tanggal Dibuat"]
    table = [
        [
            idx,
            barang["namaBarang"],
            barang["stok"],
            f"Rp{barang['hargaJual']}" if barang["hargaJual"] else "Belum Ditentukan",
            f"Rp{barang['hargaModal']}",
            barang["kategori"],
            barang["createdAt"]
        ]
        for idx, barang in enumerate(barang_list, 1)
    ]

    print(tabulate(table, headers=headers, tablefmt="grid"))

def tambah_barang(database):
    print("\n==== Tambah Barang Baru ====")
    nama_barang = input("Masukkan nama barang: ")
    stok = int(input("Masukkan stok awal: "))
    kategori = input("Masukkan kategori barang: ")
    harga_jual = input("Masukkan harga Jual satuan (tekan Enter jika belum ada): ")
    harga_jual = int(harga_jual) if harga_jual.strip() else None

    id_barang = str(len(database.get("barang", [])) + 1)
    new_barang = {
        "idBarang": id_barang,
        "namaBarang": nama_barang,
        "stok": stok,
        "kategori": kategori,
        "hargaJual": harga_jual,
        "hargaModal": 0,  # Harga modal default 0
        "createdAt": "2024-12-16"
    }

    database.setdefault("barang", []).append(new_barang)
    print("\nBarang berhasil ditambahkan!\n")

def edit_barang(database):
    print("\n==== Edit Barang ====")
    barang_list = database.get("barang", [])

    if not barang_list:
        print("\nTidak ada barang dalam database.\n")
        return

    # Menampilkan data barang dengan tabulate
    headers = ["ID Barang", "Nama Barang", "Stok", "Harga Jual", "Kategori", "Tanggal Dibuat"]
    table = [
        [barang["idBarang"], barang["namaBarang"], barang["stok"], 
         f"Rp{barang['hargaJual']}" if barang["hargaJual"] else "Belum Ditentukan", 
         barang["kategori"], barang["createdAt"]]
        for barang in barang_list
    ]
    print(tabulate(table, headers=headers, tablefmt="grid"))

    id_barang = input("Masukkan ID Barang yang ingin diedit: ")

    # Mencari barang berdasarkan ID Barang
    barang = next((barang for barang in barang_list if barang["idBarang"] == id_barang), None)

    if barang:
        print(f"\nMengedit barang: {barang['namaBarang']}")
        barang['namaBarang'] = input(f"Nama Barang [{barang['namaBarang']}]: ") or barang['namaBarang']
        barang['stok'] = int(input(f"Stok [{barang['stok']}]: ") or barang['stok'])
        barang['kategori'] = input(f"Kategori [{barang['kategori']}]: ") or barang['kategori']
        harga_jual = input(f"Harga Jual [{barang['hargaJual'] or 'Belum Ditentukan'}]: ")
        barang['hargaJual'] = int(harga_jual) if harga_jual.strip() else barang['hargaJual']
        print("\nBarang berhasil diperbarui!\n")
    else:
        print(f"\nBarang dengan ID {id_barang} tidak ditemukan.\n")

def hapus_barang(database):
    print("\n==== Hapus Barang ====")
    barang_list = database.get("barang", [])

    if not barang_list:
        print("\nTidak ada barang dalam database.\n")
        return

    # Menampilkan data barang dengan tabulate
    headers = ["ID Barang", "Nama Barang", "Stok", "Harga Jual", "Kategori", "Tanggal Dibuat"]
    table = [
        [barang["idBarang"], barang["namaBarang"], barang["stok"], 
         f"Rp{barang['hargaJual']}" if barang["hargaJual"] else "Belum Ditentukan", 
         barang["kategori"], barang["createdAt"]]
        for barang in barang_list
    ]
    print(tabulate(table, headers=headers, tablefmt="grid"))

    id_barang = input("Masukkan ID Barang yang ingin dihapus: ")

    # Mencari barang berdasarkan ID Barang
    barang = next((barang for barang in barang_list if barang["idBarang"] == id_barang), None)

    if barang:
        database["barang"].remove(barang)
        print(f"\nBarang {barang['namaBarang']} berhasil dihapus!\n")
    else:
        print(f"\nBarang dengan ID {id_barang} tidak ditemukan.\n")
        
def main():
    database = load_database()

    if not database:
        return

    print("\n=== Sistem Manajemen Barang ===")
    dashboard_barang(database)
    save_data(database)

if __name__ == "__main__":
    main()
