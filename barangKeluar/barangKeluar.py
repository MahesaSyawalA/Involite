import datetime

barang = {
    "BARANG A": {
        "Stok" : 10,
        "Harga" : 10000
    }
}
dataInternal = {
    
}

produk = input("Masukan nama barang: ").upper()
if produk in barang:
    if barang[produk]["Stok"] != 0:
        jumlah = int(input("Masukan jumlah barang yang akan dibeli: "))
        if barang[produk]["Stok"] >= jumlah: 
            total = jumlah*barang[produk]["Harga"]
            barang[produk]["Stok"] -= jumlah
            data = {
                "Waktu" : datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Internal" : {
                    "Data barang keluar" : f"{produk} keluar sebanyak {jumlah}",
                
                },
                "External" : {
                    "Produk" : produk,
                    "Harga satuan" : barang[produk]["Harga"],
                    "Jumlah beli" : jumlah,
                    "Total" : total
                }
        }
        else:
            print("Maaf, stok tidak mencukupi")
    else:
        print("Maaf, barang habis")
    print (f'''
Nama Produk: {data["External"]["Produk"]}
Harga satuan: Rp. {data["External"]["Harga satuan"]}
Jumlah beli: {data["External"]["Jumlah beli"]}
Total bayar: Rp. {data["External"]["Total"]}

{data["Waktu"]}
''')
    dataInternal[data["Waktu"]] = data["Internal"]["Data barang keluar"]
else:
    print("Barang tidak ada/salah, coba cek lagi")
