from datetime import datetime
from helper import load_data,save_data,validate_input



def filter_by_date(data_list, start_date, end_date, date_key):
    """Filter data berdasarkan rentang tanggal"""
    filtered_data = []
    for item in data_list:
        try:
            date = datetime.strptime(item[date_key], "%Y-%m-%d")
            if start_date <= date <= end_date:
                filtered_data.append(item)
        except ValueError:
            print(f"Tanggal tidak valid pada data: {item}")
    return filtered_data

def calculate_profit_loss(start_date, end_date, data):
    """Menghitung laporan laba rugi berdasarkan periode tanggal"""
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    type(end_date)
    type(start_date)


    # Filter data barang masuk dan keluar berdasarkan tanggal
    barang_masuk_filtered = filter_by_date(data['barangMasuk'], start_date, end_date, 'tanggalMasuk')
    barang_keluar_filtered = filter_by_date(data['barangKeluar'], start_date, end_date, 'tanggalKeluar')

    # Total pengeluaran dari barang masuk
    total_pengeluaran = sum(item.get('totalModal', 0) for item in barang_masuk_filtered)

    # Total pemasukan dari barang keluar
    total_pemasukan = sum(item.get('totalPenjualan', 0) for item in barang_keluar_filtered)

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

def create_new_report(data):
    """Membuat laporan laba rugi baru"""
    
    date_pattern = r"^\d{4}-\d{2}-\d{2}$"

    start_date = validate_input(
        prompt="Masukkan tanggal mulai (YYYY-MM-DD): ",
        pattern=date_pattern,
        validate_date=True 
    )

    end_date = validate_input(
        prompt="Masukkan tanggal akhir (YYYY-MM-DD): ",
        pattern=date_pattern,
        validate_date=True
    )

    try:
        report = calculate_profit_loss(start_date, end_date, data)

        print("\n=== LAPORAN LABA RUGI BARU ===")
        print(f"Tanggal Awal : {report['tanggalAwal']}")
        print(f"Tanggal Akhir : {report['tanggalAkhir']}")
        print(f"Total Pemasukan : {report['totalPemasukan']}")
        print(f"Total Pengeluaran : {report['totalPengeluaran']}")
        print(f"Total Laba / Rugi : {report['totalLabaRugi']}")
        print('-' * 40)

        # Simpan laporan ke dalam data
        report["idReport"] = str(len(data["profitLossReport"]) + 1)
        report["createdAt"] = datetime.now().strftime("%Y-%m-%d")
        data["profitLossReport"].append(report)

        # Update file JSON
        save_data(data) 

        print("\nLaporan berhasil disimpan!")

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

def main():
    # Membaca data dari file JSON
    data = load_data()

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

def show_accumulated_reports(data):
    """Menampilkan laporan laba rugi yang sudah diakumulasikan"""
    print("\n=== LAPORAN YANG TELAH DIAKUMULASIKAN ===")
    if not data['profitLossReport']:
        print("Belum ada laporan yang diakumulasikan.")
        return

    for report in data['profitLossReport']:

        print(f'ID Laporan : {report['idReport']}')
        print(f'Tanggal Awal : {report['tanggalAwal']}')
        print(f'Tanggal Akhir : {report['tanggalAkhir']}')
        print(f'Total Pemasukan : {report['totalPemasukan']}')
        print(f'Total Pengeluaran : {report['totalPengeluaran']}')
        print(f'Total Laba / Rugi : {report['totalLabaRugi']}')
        print(f'Created At : {report['createdAt']}')
        print('-'*40)
        
