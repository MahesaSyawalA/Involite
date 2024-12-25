import json

def load_database():
    try:
        with open("database.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Database tidak ditemukan!")
        return None

def save_data(file_path, data):
    """Save JSON data to a file."""
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

def create_barang_keluar(database):
    """Tambah data barang keluar."""
    print("\n==== Tambah Barang Keluar ====")

    # Tampilkan daftar barang
    show_database(database,'barang')

    # Input data barang keluar
    id_barang = input("Masukkan ID Barang: ")
    barang = next((b for b in database.get("barang", []) if b["idBarang"] == id_barang), None)

    if not barang:
        print("\nID Barang tidak ditemukan. Silakan coba lagi.\n")
        return

    jumlah = int(input("Masukkan jumlah barang keluar: "))
    if jumlah > barang["stok"]:
        print("\nJumlah barang keluar melebihi stok yang tersedia!\n")
        return

    harga_satuan = barang["hargaJual"]
    total_penjualan = jumlah * harga_satuan
    tanggal_keluar = input("Masukkan tanggal keluar (YYYY-MM-DD): ")
    description = input("Masukkan deskripsi: ")

    id_barang_keluar = str(len(database.get("barangKeluar", [])) + 1)
    new_barang_keluar = {
        "idBarangKeluar": id_barang_keluar,
        "idBarang": id_barang,
        "jumlah": jumlah,
        "hargaSatuan": harga_satuan,
        "totalPenjualan": total_penjualan,
        "tanggalKeluar": tanggal_keluar,
        "description": description
    }

    # Tambahkan data barang keluar
    database.setdefault("barangKeluar", []).append(new_barang_keluar)

    # Update stok barang
    barang["stok"] -= jumlah

    print("\nBarang keluar berhasil ditambahkan!\n")

def show_database(database, type='tipe'):
    if type == 'barangKeluar':
        for barang_keluar in database["barangKeluar"]:
            barang = next((b for b in database["barang"] if b["idBarang"] == barang_keluar["idBarang"]), {})
            nama_barang = barang.get("namaBarang", "Tidak Diketahui")
            print(f"""
            ID Barang Keluar: {barang_keluar['idBarangKeluar']}
            Nama Barang: {nama_barang}
            Jumlah: {barang_keluar['jumlah']}
            Harga Satuan: {barang_keluar['hargaSatuan']}
            Total Penjualan: {barang_keluar['totalPenjualan']}
            Tanggal Keluar: {barang_keluar['tanggalKeluar']}
            Deskripsi: {barang_keluar['description']}
            """)
    if type == 'barang':
        barang_list = database.get("barang", [])
        if not barang_list:
            print("\nTidak ada data barang yang tersedia.\n")
            return
        for barang in barang_list:
            print(f"""
        ID Barang: {barang['idBarang']}
        Nama Barang: {barang['namaBarang']}
        Kategori Barang: {barang['kategori']}
        Stok Barang: {barang['stok']}
        Harga Jual: Rp{barang['hargaJual']}
        Tanggal Dibuat: {barang['createdAt']}
        """)

def update_barang_keluar(database):
    """Edit data barang keluar."""
    print("\n==== Edit Barang Keluar ====")

    # Tampilkan daftar barang keluar
    barang_keluar_list = database.get("barangKeluar", [])

    if not barang_keluar_list:
        print("\nTidak ada data barang keluar yang tersedia.\n")
        return

    show_database(database, 'barangKeluar')

    # Pilih data yang akan diedit
    id_barang_keluar = input("Masukkan ID Barang Keluar yang ingin diedit: ")
    barang_keluar = next((bk for bk in barang_keluar_list if bk["idBarangKeluar"] == id_barang_keluar), None)

    if not barang_keluar:
        print("\nID Barang Keluar tidak ditemukan.\n")
        return

    # Tampilkan daftar barang (calling the previous function to show barang)
    show_database(database, type='barang')

    # Edit data barang keluar
    id_barang = input(f"Masukkan ID Barang [{barang_keluar['idBarang']}]: ") or barang_keluar["idBarang"]
    barang = next((b for b in database.get("barang", []) if b["idBarang"] == id_barang), None)

    if not barang:
        print("\nID Barang tidak ditemukan. Silakan coba lagi.\n")
        return

    jumlah_lama = barang_keluar["jumlah"]
    jumlah_baru = int(input(f"Masukkan jumlah barang keluar [{jumlah_lama}]: ") or jumlah_lama)

    if jumlah_baru > barang["stok"] + jumlah_lama:
        print("\nJumlah barang keluar melebihi stok yang tersedia!\n")
        return

    harga_satuan = barang["hargaJual"]
    total_penjualan = jumlah_baru * harga_satuan
    tanggal_keluar = input(f"Masukkan tanggal keluar [{barang_keluar['tanggalKeluar']}]: ") or barang_keluar["tanggalKeluar"]
    description = input(f"Masukkan deskripsi [{barang_keluar['description']}]: ") or barang_keluar["description"]

    # Update data barang keluar
    barang_keluar.update({
        "idBarang": id_barang,
        "jumlah": jumlah_baru,
        "hargaSatuan": harga_satuan,
        "totalPenjualan": total_penjualan,
        "tanggalKeluar": tanggal_keluar,
        "description": description
    })

    # Update stok barang
    barang["stok"] += jumlah_lama - jumlah_baru

    print("\nBarang keluar berhasil diperbarui!\n")

def delete_barang_keluar(database):
    print("==== Hapus Barang Keluar ====")
    show_database(database, 'barangKeluar')
    id_barang_keluar = input("Masukkan ID Barang Keluar yang ingin dihapus: ")

    # Cari barang keluar
    barang_keluar = next((b for b in database["barangKeluar"] if b["idBarangKeluar"] == id_barang_keluar), None)
    if not barang_keluar:
        print("\nBarang keluar dengan ID tersebut tidak ditemukan.\n")
        return

    # Kembalikan stok ke jumlah awal
    barang = next((b for b in database["barang"] if b["idBarang"] == barang_keluar["idBarang"]), None)
    if barang:
        barang["stok"] += barang_keluar["jumlah"]

    # Hapus data barang keluar
    database["barangKeluar"].remove(barang_keluar)
    print("\nBarang keluar berhasil dihapus!\n")

def main():
    file_path = "database.json"
    database = load_database()
    if not database:
        return

    while True:
        print("\n=== Dashboard Barang Keluar ===")
        print("1. Tambah Barang Keluar")
        print("2. Lihat Barang Keluar")
        print("3. Update Barang Keluar")
        print("4. Hapus Barang Keluar")
        print("5. Keluar")
        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            create_barang_keluar(database)
            save_data(file_path, database)
        elif pilihan == "2":
            print("==== Data Barang Keluar ====")
            show_database(database, 'barangKeluar')
        elif pilihan == "3":
            update_barang_keluar(database)
            save_data(file_path, database)
        elif pilihan == "4":
            delete_barang_keluar(database)
            save_data(file_path, database)
        elif pilihan == "5":
            print("\nTerima kasih telah menggunakan sistem. Sampai jumpa!\n")
            break
        else:
            print("\nPilihan tidak valid, silakan coba lagi.\n")

if __name__ == "__main__":
    main()
