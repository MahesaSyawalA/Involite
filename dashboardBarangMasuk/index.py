import re
import math
import json
from helper import validate_input  
from helper import load_data
from helper import save_data

def generate_id_barang_masuk(data):
    """Generate a new ID Barang Masuk with the format BM001, BM002, etc."""
    if not data["barangMasuk"]:
        return "BM001"

    existing_ids = [int(item["idBarangMasuk"][2:]) for item in data["barangMasuk"] if re.match(r"^BM\d{3}$", item["idBarangMasuk"])]
    new_id_number = max(existing_ids, default=0) + 1
    return f"BM{new_id_number:03d}"

def display_barang_masuk(data):
    """Display the Barang Masuk dashboard."""
    if not data or "barangMasuk" not in data or "barang" not in data:
        print("Data tidak valid atau tidak lengkap.")
        return

    barang_dict = data.get('barang',{})

    print("")
    for entry in data["barangMasuk"]:
        id_barang = entry["idBarang"]
        nama_barang = 'nama barang tidak diketahui'
        for item in barang_dict:
            if item['idBarang'] == id_barang:
                nama_barang = item['namaBarang'] 
        

        paragraph = (
            f"ID Barang Masuk: {entry['idBarangMasuk']}\n"
            f"Nama Barang: {nama_barang}\n"
            f"Jumlah: {entry['jumlah']}\n"
            f"Harga Satuan: {entry['hargaSatuan']}\n"
            f"Total Modal: {entry['totalModal']}\n"
            f"Tanggal Masuk: {entry['tanggalMasuk']}\n"
            f"Deskripsi: {entry['description']}\n"
            f"{'-' * 40}"
        )
        print(paragraph)

def choose_barang(data):
    """Allow user to choose a Barang from the available data."""
    if not data or "barang" not in data:
        print("Data tidak valid atau tidak lengkap.")
        return
    print('')
    for item in data["barang"]:
        print(
            f"ID Barang: {item['idBarang']}\n"
            f"Nama Barang: {item['namaBarang']}\n"
            f"{'-' * 40}"
        )

    while True:
        id_barang = validate_input("Masukkan ID Barang yang dipilih: ",r"^[a-zA-Z0-9]+$")
        for item in data['barang']:
            if item["idBarang"] == id_barang:
                return id_barang
        print("ID Barang tidak valid. Silakan pilih dari daftar.")



def add_barang_masuk(data):
    """Add a new Barang Masuk entry."""
    id_barang_masuk = generate_id_barang_masuk(data)
    id_barang = choose_barang(data)
    jumlah = validate_input("Masukkan Jumlah: ", r"^[1-9][0-9]+$", int)
    harga_satuan = validate_input("Masukkan Harga Satuan: ", r"^\d+$", int)
    total_modal = jumlah * harga_satuan
    tanggal_masuk = validate_input("Masukkan Tanggal Masuk (YYYY-MM-DD): ", r"^\d{4}-\d{2}-\d{2}$",str,validate_date=True)
    description = validate_input("Masukkan Deskripsi: ",r"^.*$",str)

    new_entry = {
        "idBarangMasuk": id_barang_masuk,
        "idBarang": id_barang,
        "jumlah": jumlah,
        "hargaSatuan": harga_satuan,
        "totalModal": total_modal,
        "tanggalMasuk": tanggal_masuk,
        "description": description
    }
    data["barangMasuk"].append(new_entry)

    # Update stok dan harga modal per satuan
    for barang in data["barang"]:
        if barang["idBarang"] == id_barang:
            stok_sebelumnya = barang.get("stok", 0)
            modal_sebelumnya = stok_sebelumnya * barang.get("hargaModal", 0)
            modal_satuan_sebelumnya = barang.get('hargaModal',0)

            stok_baru = stok_sebelumnya + jumlah
            total_modal_baru = modal_sebelumnya + total_modal
            harga_modal_baru = total_modal_baru / stok_baru

            barang["stok"] = stok_baru
            barang["hargaModal"] = math.ceil(harga_modal_baru)

            print(f"Stok barang '{barang['namaBarang']}' berhasil diperbarui.")
            print(f"Stok: {stok_sebelumnya} -> {stok_baru}")
            print(f"Harga Modal/Satuan: {modal_satuan_sebelumnya} -> {math.ceil(harga_modal_baru)}")
            break

    print("Data Barang Masuk berhasil ditambahkan.")

def update_barang_masuk(data):
    """Update an existing Barang Masuk entry."""
    id_barang_masuk = validate_input("Masukkan ID Barang Masuk yang ingin diupdate: ",r"^[a-zA-Z0-9]+$",str)
    for entry in data["barangMasuk"]:
        if entry["idBarangMasuk"] == id_barang_masuk:
            print("Data ditemukan. Masukkan data baru atau tekan Enter untuk melewati.")
            
            jumlah_lama = entry["jumlah"]
            id_barang = entry["idBarang"]

            entry["idBarang"] = choose_barang(data)
            entry["jumlah"] = validate_input(f"Jumlah ({entry['jumlah']}): ", r"^\d+$", int, default=entry["jumlah"])
            entry["hargaSatuan"] = validate_input(f"Harga Satuan ({entry['hargaSatuan']}): ", r"^\d+$", int, default=entry["hargaSatuan"])
            entry["totalModal"] = entry["jumlah"] * entry["hargaSatuan"]
            entry["tanggalMasuk"] = validate_input(f"Tanggal Masuk ({entry['tanggalMasuk']}): ", r"^\d{4}-\d{2}-\d{2}$", default=entry["tanggalMasuk"])
            entry["description"] = input(f"Deskripsi ({entry['description']}): ") or entry["description"]

            for barang in data["barang"]:
                if barang["idBarang"] == id_barang:
                    stok_sebelumnya = barang.get("stok", 0)
                    modal_sebelumnya = stok_sebelumnya * barang.get("hargaModal", 0)
                    modal_satuan_sebelumnya = barang.get('hargaModal',0)

                    stok_baru = stok_sebelumnya - jumlah_lama + entry["jumlah"]
                    total_modal_baru = modal_sebelumnya - (jumlah_lama * barang.get("hargaModal", 0)) + entry["totalModal"]
                    harga_modal_baru = total_modal_baru / stok_baru

                    barang["stok"] = stok_baru
                    barang["hargaModal"] = harga_modal_baru

                    print(f"Stok barang '{barang['namaBarang']}' berhasil diperbarui.")
                    print(f"Stok: {stok_sebelumnya} -> {stok_baru}")
                    print(f"Harga Modal/Satuan: {modal_satuan_sebelumnya} -> {harga_modal_baru:.2f}")
                    break

            print("Data Barang Masuk berhasil diupdate.")
            return
    print("Data dengan ID tersebut tidak ditemukan.")

def delete_barang_masuk(data):
    id_barang_masuk = input("Masukkan ID Barang Masuk yang ingin dihapus: ")

    # Cari entri barang masuk berdasarkan ID
    for entry in data["barangMasuk"]:
        if entry["idBarangMasuk"] == id_barang_masuk:
            # Kurangi stok barang yang terkait
            id_barang = entry["idBarang"]
            jumlah = entry["jumlah"]
            harga_satuan = entry["hargaSatuan"]

            for barang in data["barang"]:
                if barang["idBarang"] == id_barang:
                    # Kurangi stok barang
                    barang["stok"] -= jumlah

                    if barang["stok"] > 0:
                        total_modal_sekarang = barang["stok"] * barang["hargaModal"]
                        total_modal_baru = total_modal_sekarang - (jumlah * harga_satuan)
                        barang["hargaModal"] = total_modal_baru / barang["stok"]
                    else:
                        barang["hargaModal"] = 0

                    break

            data["barangMasuk"].remove(entry)
            print("Data Barang Masuk berhasil dihapus.")
            return

    print("Data dengan ID tersebut tidak ditemukan.")


def main():
    data = load_data()

    if data:
        while True:
            print("\nDashboard Barang Masuk")
            print("======================")
            print("1. Tampilkan Data Barang Masuk")
            print("2. Tambah Data Barang Masuk")
            print("3. Update Data Barang Masuk")
            print("4. Hapus Data Barang Masuk")
            print("5. Keluar")

            choice = validate_input("Pilih Menu: ",r"^[0-9]+$",str,menu=True,maxMenu=5)

            if choice == "1":
                display_barang_masuk(data)
            elif choice == "2":
                add_barang_masuk(data)
                save_data(data)
            elif choice == "3":
                display_barang_masuk(data)
                update_barang_masuk(data)
                save_data(data)
            elif choice == "4":
                display_barang_masuk(data)
                delete_barang_masuk(data)
                save_data(data)
            elif choice == "5":
                print("Keluar dari program.")
                break
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")
