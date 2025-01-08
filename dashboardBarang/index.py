from helper import validate_input
from helper import load_data
from helper import save_data 

def lihat_barang(database):
    print("\n==== Daftar Barang ====")
    barang_list = database.get("barang", [])

    if not barang_list:
        print("\nTidak ada barang dalam database.\n")
        return

    for idx, barang in enumerate(barang_list, 1):
        print(f"ID Barang: {barang['idBarang']}")
        print(f"Nama Barang: {barang['namaBarang']}")
        print(f"Stok: {barang['stok']}")
        print(f"Harga Jual: {'Rp' + str(barang['hargaJual']) if barang['hargaJual'] else 'Belum Ditentukan'}")
        print(f"Harga Modal: Rp{barang['hargaModal']}")
        print(f"Kategori: {barang['kategori']}")
        print(f"Tanggal Dibuat: {barang['createdAt']}\n")
        print(f"{'-' * 40}")




def tambah_barang(database):
    print("\n==== Tambah Barang Baru ====")
    nama_barang = validate_input("Masukkan nama barang: ",r"^[a-zA-Z0-9!@#$%^&*()_+\-=,.?]+$",str)
    stok =  validate_input("Masukkan stok awal: ", r"^\d+$", int)
    kategori = validate_input("Masukkan kategori barang: ",r"^[a-zA-Z0-9!@#$%^&*()_+\-=,.?]+$",str)
    harga_jual = validate_input("Masukkan harga Jual satuan (tekan Enter jika belum ada): ", r"^\d+$", int, default=0)

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
    lihat_barang(database)

    id_barang = validate_input("Masukkan ID Barang yang ingin diedit: ", r'^[a-zA-Z0-9 ]+$', str)

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

    lihat_barang(database)

    id_barang =validate_input("Masukkan ID Barang yang ingin dihapus: ", r'^[a-zA-Z0-9 ]+$', str)

    # Mencari barang berdasarkan ID Barang
    barang = next((barang for barang in barang_list if barang["idBarang"] == id_barang), None)

    if barang:
        database["barang"].remove(barang)
        print(f"\nBarang {barang['namaBarang']} berhasil dihapus!\n")
    else:
        print(f"\nBarang dengan ID {id_barang} tidak ditemukan.\n")
        
def main():
    database = load_data()

    if not database:
        return

    print("\n=== Sistem Manajemen Barang ===")
    while True:
        print("\n==== Dashboard Barang ====")
        print("1. Lihat Semua Barang")
        print("2. Tambah Barang Baru")
        print("3. Edit Barang")
        print("4. Hapus Barang")
        print("5. Keluar")

        pilihan = validate_input("Pilihan Menu: ",r"^[0-9]+$",str,menu=True,maxMenu=5)

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

