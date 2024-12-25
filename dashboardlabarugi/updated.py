import json
from datetime import datetime
from tabulate import tabulate

def filter_by_date(data_list, start_date, end_date, date_key):
    """Filter data berdasarkan rentang tanggal"""
    return [
        item for item in data_list
        if start_date <= datetime.strptime(item[date_key], "%Y-%m-%d") <= end_date
    ]

def calculate_profit_loss(start_date, end_date, data):
    """Menghitung laporan laba rugi berdasarkan periode tanggal"""
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    # Filter data barang masuk dan keluar berdasarkan tanggal
    barang_masuk_filtered = filter_by_date(data['barangMasuk'], start_date, end_date, 'tanggalMasuk')
    barang_keluar_filtered = filter_by_date(data['barangKeluar'], start_date, end_date, 'tanggalKeluar')

    # Total pengeluaran dari barang masuk
    total_pengeluaran = sum(item['totalModal'] for item in barang_masuk_filtered)

    # Total pemasukan dari barang keluar
    total_pemasukan = sum(item['totalPenjualan'] for item in barang_keluar_filtered)

    # Menghitung laba/rugi
    total_laba_rugi = total_pemasukan - total_pengeluaran

    # Hasil laporan
    return {
        "tanggalAwal": start_date.strftime("%Y-%m-%d"),
        "tanggalAkhir": end_date.strftime("%Y-%m-%d"),
        "totalPemasukan": total_pemasukan,
        "totalPengeluaran": total_pengeluaran,
        "totalLabaRugi": total_laba_rugi
    }

def show_accumulated_reports(data):
    """Menampilkan laporan laba rugi yang sudah diakumulasikan"""
    print("\n=== LAPORAN YANG TELAH DIAKUMULASIKAN ===")
    if not data['profitLossReport']:
        print("Belum ada laporan yang diakumulasikan.")
        return

    table_data = []
    for report in data['profitLossReport']:
        table_data.append([
            report['idReport'],
            report['tanggalAwal'],
            report['tanggalAkhir'],
            f"Rp{report['totalPemasukan']:,}",
            f"Rp{report['totalPengeluaran']:,}",
            f"Rp{report['totalLabaRugi']:,}",
            report['createdAt']
        ])

    headers = ["ID Laporan", "Tanggal Awal", "Tanggal Akhir", "Total Pemasukan", "Total Pengeluaran", "Total Laba/Rugi", "Dibuat Pada"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

def create_new_report(data):
    """Membuat laporan laba rugi baru"""
    start_date = input("Masukkan tanggal mulai (YYYY-MM-DD): ")
    end_date = input("Masukkan tanggal akhir (YYYY-MM-DD): ")

    try:
        report = calculate_profit_loss(start_date, end_date, data)

        print("\n=== LAPORAN LABA RUGI BARU ===")
        table_data = [[
            report['tanggalAwal'],
            report['tanggalAkhir'],
            f"Rp{report['totalPemasukan']:,}",
            f"Rp{report['totalPengeluaran']:,}",
            f"Rp{report['totalLabaRugi']:,}"
        ]]
        headers = ["Tanggal Awal", "Tanggal Akhir", "Total Pemasukan", "Total Pengeluaran", "Total Laba/Rugi"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))

        # Simpan laporan ke dalam data
        report["idReport"] = str(len(data["profitLossReport"]) + 1)
        report["createdAt"] = datetime.now().strftime("%Y-%m-%d")
        data["profitLossReport"].append(report)

        # Update file JSON
        with open("database.json", "w") as file:
            json.dump(data, file, indent=4)

        print("\nLaporan berhasil disimpan!")

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

def main():
    # Membaca data dari file JSON
    with open("database.json", "r") as file:
        data = json.load(file)

    while True:
        print("\n=== Dashboard Laba Rugi ===")
        print("1. Lihat laporan yang telah diakumulasikan")
        print("2. Buat laporan laba rugi baru")
        print("3. Keluar")

        choice = input("Pilih menu: ")

        if choice == "1":
            show_accumulated_reports(data)
        elif choice == "2":
            create_new_report(data)
        elif choice == "3":
            print("Keluar dari program.")
            break
        else:
            print("Pilihan tidak valid.")


