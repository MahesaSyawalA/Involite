#registrasi akun 

email = input("masukan email :")
password_email = input("masukan password :")
no_telepon = int(input("masukan nomor telepon :"))
alamat = input("masukan alamat :")
print(f'{email}\n {password_email}\n {no_telepon}\n {alamat}')

#login berdasarkan registrasi akun
username_db = email
password_db = password_email
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
        print(f"login anda  salah")


