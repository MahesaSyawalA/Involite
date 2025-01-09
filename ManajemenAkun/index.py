import json
from helper import load_data,save_data,validate_input,get_sessions



def login(database):
    print("==== Login Menu ====")
    users = database.get('users', [])
    status = False
    selectedUser = []

    while True:
        username = validate_input("Masukkan username: ", r"^[^\s]*$", str)
        for user in users:
            if user['username'] == username:
                status = True
                selectedUser.append(user)
                break  

        if status:
            break
        else:
            print('Username tidak ditemukan')
    print(selectedUser)
    for i in range(3):
        password = validate_input("Masukkan password: ", r"^[^\s]*$", str)
        if selectedUser[0]['password'] == password:
            print('Login Berhasil! Selamat Datang')
            new_entry = {
                "idUsaha":selectedUser[0]['idUsaha'],
                "namaUser": selectedUser[0]['nama'],
                "role":selectedUser[0]['role'],
            }
            database.setdefault("sessions", []).append(new_entry)
            return selectedUser[0]
        print(f'Password Salah!, kesempatan mencoba {2 - i} kali')

    selectedUser.clear()
    print('Anda gagal untuk login')
    return None


def logout(database):
    sessions = database.get("sessions", [])
    if sessions:
        print("\nLogout dari semua sesi...")
        database["sessions"] = []
        save_data(database)

        print("Logout berhasil.\n")
    
    else:
        print("\nTidak ada sesi aktif untuk logout.\n")

def register(database,idUsaha=None):
    print("==== Register Akun ====")
    dataUsaha = database.get('usaha',[]) 
    dataUser = database.get('users',[])
    selectedUsaha = idUsaha
    if not idUsaha:
        show_usaha(database)
        while True :
            inputUsaha = validate_input("Masukan ID usaha anda : ",r"^[a-zA-Z0-9]+$",str)
            ditemukan = False
            for usaha in dataUsaha:
                if inputUsaha == usaha['idUsaha']:
                    selectedUsaha = inputUsaha
                    ditemukan = True
            if ditemukan:
                break
            else:
                print('ID Usaha tidak di temukan masukan ID usaha yang telah di tampilkan ')

    while True:
        inputRole = validate_input("masukan Role yang igin di pilih (owner/logistik/akuntan) :", r"^[a-z]+$",str)
        if inputRole == 'owner':
            break
        elif inputRole == 'logistik':
            break
        elif inputRole == 'akuntan':
            break
        else:
            print('inputan tidak valid coba lagi ')



    nama =  validate_input("Masukkan nama: ",r"^[a-zA-Z0-9\s]+$",str)
    while True:
        username = validate_input("Masukkan username: ",r"^[a-zA-Z][^\s]*$",str)
        used = False
        for user in dataUser:
            if user['username'] == username:
                used = True

        if used == True:
            print('username yang anda masukan sudah digunakan ') 
        else:
            break
    
    while True:
        password = validate_input("Masukkan password: ",r"^(?=.*[a-zA-Z])[^\s]*$",str)
        if password == username :
            print("username dan password tidak boleh sama ")
        else:
            break
    id_user = str(len(database.get("users", [])) + 1)

    new_user = {
        "idUser": id_user,
        "idUsaha":selectedUsaha,
        "nama": nama,
        "username": username,
        "password": password,
        "role":inputRole,
        "createdAt": "2024-12-16"
    }

    database.setdefault("users", []).append(new_user)
    print("\nAkun berhasil didaftarkan! Silakan login.\n")

def show_user(data,idUsaha):
    print('==== Menampilkan Seluruh Data User ====\n')
    users = data.get('users',[])
    for user in users :
        if user['idUsaha'] == idUsaha:

            print(f'ID User : {user['idUser']} ')    
            print(f'Nama User : {user['nama']}')
            print(f'Role User : {user['role']}')
            print(f'Username : {user['username']}')
            print(f'Password : {user['password']}\n')

def update_user(data, idUsaha):
    dataUser = data.get('users',[])
    selectedUser=[]
    for user in dataUser :
        if user['idUsaha'] == idUsaha:
            selectedUser.append(user)
    
    InputUpdateId = validate_input("Masukan ID yang ingin di Update : ",r'^[1-9][0-9]*$',str)
    for user in selectedUser:
        if user['idUser'] == InputUpdateId:
            print("Data ditemukan. Masukkan data baru atau tekan Enter untuk melewati.")
            user['nama'] =  validate_input("Masukkan nama: ",r"^[a-zA-Z0-9\s]+$",str)
            while True:
                user['role'] = validate_input("masukan Role yang igin di pilih (owner/logistik/akuntan) :", r"^[a-z]+$",str,default=user['role'])
                if user['role'] == 'owner':
                    break
                elif user['role'] == 'logistik':
                    break
                elif user['role'] == 'akuntan':
                    break
                else:
                    print('inputan tidak valid coba lagi ')

            print('username tidak bisa di update lanjut update password')
            while True:
                user['password'] = validate_input("Masukkan password: ",r"^(?=.*[a-zA-Z])[^\s]*$",str, default=user['password'])
                if user['password'] == user['username'] :
                    print("username dan password tidak boleh sama ")
                else:
                    break
            
            print(f'Nama User : {user['nama']}')
            print(f'Role User : {user['role']}')
            print(f'Username : {user['username']}')
            print(f'Password : {user['password']}\n')

def delete_user(data):
    dataUser = data.get('users',[])

    while True:
        inputIdUser = validate_input("Masukan Id yang ingin di hapus : ",r'^[1-9][0-9]*$',str)
        for user in dataUser:
            if user['idUser'] == inputIdUser:
                data['users'].remove(user)
                print('data berhasil dihapus')
                return
        print('id tidak ditemukan pilih id yang sudah di tampilkan')


        
    


def show_usaha(data,idUsaha='all'):
    print('==== Menampilkan Detail Usaha ====\n')
    usaha = data.get('usaha',[])
    if idUsaha == 'all':
        for item in usaha:
            print(f' id Usaha : {item['idUsaha']}')
            print(f' Nama Usaha : {item['namaUsaha']} ')    
            print(f' Contact Info : {item['contactInfo']} ')    
            print(f' Created At : {item['createdAt']} \n')

    for item in usaha:
        if item['idUsaha'] == idUsaha:
            print(f' Nama Usaha : {item['namaUsaha']} ')    
            print(f' Contact Info : {item['contactInfo']} ')    
            print(f' Created At : {item['createdAt']}\n ')    

def main():
    database = load_data()
    user = get_sessions(database)
    idUsaha =''
    roleUser = ''
    if user:
        idUsaha = user[0]['idUsaha'] 
        roleUser = user[0]['role']

    if not database:
        return

    print("=== Selamat Datang di Sistem CLI ===")
    
    if roleUser =='owner':
        while True:
            print("\n1. Tampilkan Semua User")
            print("2. Tambahkan User")
            print("3. Update User")
            print("4. Delete User")
            print("5. Tampilkan Usaha")
            print("6. Logout")
            print("7. Keluar")
            
            pilihan = input("Pilih menu: ")
            print('')
            
            if pilihan =='1':
                show_user(database,idUsaha)
            elif pilihan =='2':
                register(database,idUsaha)
            elif pilihan =='3':
                show_user(database,idUsaha)
                update_user(database,idUsaha)
                save_data(database)
            elif pilihan =='4':
                show_user(database,idUsaha)
                delete_user(database)
                save_data(database)
            elif pilihan =='2':
                show_usaha(database,idUsaha)
            elif pilihan =='5':
                show_usaha(database,idUsaha)
            elif pilihan == "6":
                logout(database)
                print(json.dumps(database, indent=4))
                save_data(database)
                break
            elif pilihan == "7":
                print("\nTerima kasih telah menggunakan sistem. Sampai jumpa!\n")
                return
            else:
                print("\nPilihan tidak valid, silakan coba lagi.\n")
    if user:
        while True:
            print("\n1. Logout")
            print("2. Keluar")
            pilihan = input("Pilih menu: ")
            print('')

            if pilihan == "1":
                logout(database)
                print(json.dumps(database, indent=4))
                save_data(database)
                break
            elif pilihan == "2":
                print("\nTerima kasih telah menggunakan sistem. Sampai jumpa!\n")
                return
            else:
                print("\nPilihan tidak valid, silakan coba lagi.\n")

    while True:
        print("\n1. Login")
        print("2. Register")
        print("3. Keluar")
        pilihan = input("Pilih menu: ")
        print('')
        if pilihan == "1":
            user = login(database)
            if user:
                print(f"\nSelamat datang, {user['nama']}!\n")
                save_data(database)
                break
        elif pilihan == "2":
            register(database)
            save_data(database)
        elif pilihan == "3":
            print("\nTerima kasih telah menggunakan sistem. Sampai jumpa!\n")
            return True
        else:
            print("\nPilihan tidak valid, silakan coba lagi.\n")

