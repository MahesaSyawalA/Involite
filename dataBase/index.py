import json

# Membuat dummy database dengan tambahan 'role' di 'users'
data = {
    "users": [
        {"idUser": "1", "nama": "Alice", "username": "alice123", "password": "password123", "role": "admin", "createdAt": "2024-11-01"},
        {"idUser": "2", "nama": "Bob", "username": "bob456", "password": "password456", "role": "user", "createdAt": "2024-11-02"}
    ],
    "barang": [
        {"idBarang": "1", "namaBarang": "Beras", "stok": 100, "kategori": "Sembako", "hargaModal": 15000, "hargaJual": 18000, "createdAt": "2024-11-01"},
        {"idBarang": "2", "namaBarang": "Minyak Goreng", "stok": 50, "kategori": "Sembako", "hargaModal": 17000, "hargaJual": 20400, "createdAt": "2024-11-01"}
    ],
    "barangMasuk": [
        {"idBarangMasuk": "1", "idBarang": "1", "jumlah": 50, "hargaSatuan": 12000, "totalModal": 600000, "tanggalMasuk": "2024-11-01", "description": "Stok awal"},
        {"idBarangMasuk": "2", "idBarang": "2", "jumlah": 30, "hargaSatuan": 14000, "totalModal": 420000, "tanggalMasuk": "2024-11-02", "description": "Pembelian baru"}
    ],
    "barangKeluar": [
        {"idBarangKeluar": "1", "idBarang": "1", "jumlah": 10, "hargaSatuan": 15000, "totalPenjualan": 150000, "tanggalKeluar": "2024-11-03", "description": "Penjualan ke pelanggan"},
        {"idBarangKeluar": "2", "idBarang": "2", "jumlah": 5, "hargaSatuan": 17000, "totalPenjualan": 85000, "tanggalKeluar": "2024-11-04", "description": "Penjualan ke pelanggan"}
    ],
    "profitLossReport": [
        {"idReport": "1", "tanggalAwal": "2024-11-01", "tanggalAkhir": "2024-11-30", "totalPemasukan": 235000, "totalPengeluaran": 1020000, "totalLabaRugi": -785000, "createdAt": "2024-12-01"}
    ],
    "sessions": [
        {"namaUser": "zahra"}
    ]
}

# Menyimpan data ke file JSON
with open("database.json", "w") as file:
    json.dump(data, file, indent=4)

# Membaca data dari file JSON
with open("database.json", "r") as file:
    loaded_data = json.load(file)

print("Data berhasil dimodifikasi, disimpan, dan dimuat:")
print(json.dumps(loaded_data, indent=4))

def rundb():
    with open("database.json", "w") as file:
        json.dump(data, file, indent=4)
