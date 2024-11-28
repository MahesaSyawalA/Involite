print(f"ini adalah login")

username_db = "latihan daspro"
password_db = "apaantuh"
jumlah_pengulangan = 0
max_pengulangan = 3
while jumlah_pengulangan < max_pengulangan:
    username = input("masukan username :")
    password = input("masukan password :")
    jumlah_pengulangan += 1
    
    if username == username_db and password == password_db:
        print(f"login berhasil")
        break
    else:
        print(f"login anda  salah dan silahkan tunggu beberapa saat atau rubah password anda")

#riset password dan login menggunakan password baru
password_baru = input("masukan password :")
while jumlah_pengulangan < max_pengulangan:
    username = input("masukan username :")
    password = input("masukan password :")
    jumlah_pengulangan += 1
    
    if username == username_db and password == password_baru:
        print(f"login berhasil")
        break
    else:
        print(f"login anda  salah")

