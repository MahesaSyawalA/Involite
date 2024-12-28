import json
from helper import load_data,save_data,validate_input


def check_session(database):
    sessions = database.get("sessions", [])
    if sessions:
        print("\nAnda sudah login sebagai:")
        for session in sessions:
            print(f"- {session['namaUser']}")
        return True
    return False

def login(database):
    print("==== Login Menu ====")
    users = database.get('users',[])
    status = False
    selectedUser = []           
    while True:
        username = validate_input("Masukkan username: ",r"^[^\s]*$",str)
        for user in users:
            if user['username'] == username: 
                status = True
                selectedUser.append(user)
        if status == True:
            break
        else:
            print('Username tidak ditemukan')       

    for i in range(3):
        password = validate_input("Masukkan password: ",r"^[^\s]*$",str)    
        if selectedUser[0]['password'] == password:
            print('Login Berhasil! Selamat Datang')
            new_entry = {
                "namaUser": user['nama']
            }
            database.setdefault("sessions", []).append(new_entry)
            return user
        print(f'Password Salah!, kesempatan mencoba {-i+2} kali')
    return print('Anda gagal untuk login ')


def logout(database):
    sessions = database.get("sessions", [])
    if sessions:
        print("\nLogout dari semua sesi...")
        database["sessions"] = []
        save_data(database)

        print("Logout berhasil.\n")
    
    else:
        print("\nTidak ada sesi aktif untuk logout.\n")

def register(database):
    print("==== Register Akun ====")
    data_user = database.get('users',[])
    nama =  validate_input("Masukkan nama: ",r"^[^\s]+$",str)
    while True:
        username = validate_input("Masukkan username: ",r"^[^\s]+$",str)
        used = False
        for user in data_user:
            if user['username'] == username:
                used = True

        if used == True:
            print('username yang anda masukan sudah digunakan ') 
        else:
            break
    
    while True:
        password = validate_input("Masukkan password: ",r"^[^\s]+$",str)
        if password == username :
            print("username dan password tidak boleh sama ")
        else:
            break
    id_user = str(len(database.get("users", [])) + 1)

    new_user = {
        "idUser": id_user,
        "nama": nama,
        "username": username,
        "password": password,
        "createdAt": "2024-12-16"
    }

    # databaseuser = database.get("users", []).append(new_user)
    database.setdefault("users", []).append(new_user)
    print("\nAkun berhasil didaftarkan! Silakan login.\n")

def main():
    database = load_data()
    # print(json.dumps(database, indent=4));
    if not database:
        return

    print("=== Selamat Datang di Sistem CLI ===")
    if check_session(database):
        while True:
            print("\n1. Logout")
            print("2. Keluar")
            pilihan = input("Pilih menu: ")

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

