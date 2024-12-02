import json

# Membuat dummy database
data = {
    "users": [
        {"id": 1, "name": "Alice", "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "email": "bob@example.com"}
    ]
}

dataBarangMasuk = [
    {
        "idbrg" :"1",
        "nama": "Beras",
        "harga_beli": 12000,
        "harga_jual": 15000,
        "stok": 50,
        "tanggal_masuk": "2024-11-01"
    },
    {
        "idbrg" :"2",
        "nama": "Minyak Goreng",
        "harga_beli": 14000,
        "harga_jual": 17000,
        "stok": 30,
        "tanggal_masuk": "2024-11-05"
    },
    {
        "idbrg" :"3",
        "nama": "Gula Pasir",
        "harga_beli": 13000,
        "harga_jual": 16500,
        "stok": 40,
        "tanggal_masuk": "2024-11-10"
    },
    {
        "idbrg" :"4",
        "nama": "Kopi Bubuk",
        "harga_beli": 25000,
        "harga_jual": 30000,
        "stok": 20,
        "tanggal_masuk": "2024-11-15"
    },
    {
        "idbrg" :"5",
        "nama": "Teh Celup",
        "harga_beli": 8000,
        "harga_jual": 10000,
        "stok": 60,
        "tanggal_masuk": "2024-11-20"
    }
]



# Menyimpan data ke file JSON
with open("database.json", "w") as file:
    json.dump(data, file)

# Membaca data dari file JSON
with open("database.json", "r") as file:
    loaded_data = json.load(file)

with open("data_barang.json", "w") as file:
    json.dump(dataBarangMasuk, file, indent=4)

print(loaded_data)