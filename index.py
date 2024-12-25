import json
from dashboardBarang.index import main as DashboardBarang
from dashboardBarangMasuk.index import main as DashboardBarangMasuk
from barangKeluar.index import main as DashboardBarangKeluar
from dashboardlabarugi.index import main as DashboardLabaRugi
from ManajemenAkun.index import main as ManagementAkun
from ManajemenAkun.index import logout as Logout
# from dataBase.index import rundb  

def load_database():
    try:
        with open("database.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Database tidak ditemukan!")
        return None

if __name__ == "__main__":
    database = load_database()

    if database is None:
        print("Database kosong atau tidak ditemukan. Menjalankan `rundb` untuk inisialisasi...")
        # rundb()
    else:
        print("Database berhasil dimuat!")

    print('Selamat Datang di Aplikasi Involite')

    while True:
        session = database.get('sessions', [])  # Selalu perbarui `session` dari database terbaru
        if session:
            while session:
                print('\n1. Logout')
                print('2. Dashboard Barang')
                print('3. Dashboard Barang Masuk')
                print('4. Dashboard Barang Keluar')
                print('5. Dashboard Laba Rugi')
                opsi = input('Pilih Menu yang ingin Anda gunakan: ')
                
                if opsi == '1':
                    print('Logout...')
                    Logout(database)
                    database = load_database()  # Perbarui `database` setelah logout
                    break  # Keluar dari loop `while session` untuk mengecek ulang sesi
                elif opsi == '2':
                    DashboardBarang()
                elif opsi == '3':
                    DashboardBarangMasuk()
                elif opsi == '4':
                    DashboardBarangKeluar()
                elif opsi == '5':
                    DashboardLabaRugi()
                else:
                    print('Masukkan opsi yang tepat.')
        else:
            print('\nTidak ada sesi aktif. Silakan login atau register terlebih dahulu.')
            ManagementAkun()
            database = load_database()  # Perbarui `database` setelah login atau register
