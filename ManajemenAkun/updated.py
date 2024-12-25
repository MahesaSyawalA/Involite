import json

def load_database():
    try:
        with open("database.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Database tidak ditemukan!")
        return None

def save_data(file_path, data):
    """Save JSON data to a file."""
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

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
    username = input("Masukkan username: ")
    password = input("Masukkan password: ")

    for user in database.get("users", []):
        if user["username"] == username and user["password"] == password:
            print(f"\nLogin berhasil! Selamat datang, {user['nama']}!\n")

            new_entry = {
                "namaUser": user['nama']
            }
            database.setdefault("sessions", []).append(new_entry)
            return user

    print("\nLogin gagal! Username atau password salah.\n")
    return None

def validasi_nama_pengguna(prompt):
    while True:
        nama_pengguna = input(prompt).strip()
        if nama_pengguna and any(char.isalpha() for char in nama_pengguna) and nama_pengguna.isalnum() :
            return nama_pengguna
        else:
            print(f"input data tidak boleh kosong dan harus menggandung huruf dan angka. Silahkan coba lagi")

def logout(database):
    sessions = database.get("sessions", [])
    if sessions:
        print("\nLogout dari semua sesi...")
        database["sessions"] = []
        print("Logout berhasil.\n")
    else:
        print("\nTidak ada sesi aktif untuk logout.\n")

def register(database):
    print("==== Register Akun ====")
    nama =  validasi_nama_pengguna("Masukkan nama: ")
    username = validasi_nama_pengguna("Masukkan username: ")
    password = validasi_nama_pengguna("Masukkan password: ")
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
    file_path = "database.json"  
    database = load_database()
    # print(json.dumps(database, indent=4));
    if not database:
        return

    print("=== Selamat Datang di Sistem CLI ===")
    print(check_session(database));
    if check_session(database):
        while True:
            print("\n1. Logout")
            print("2. Keluar")
            pilihan = input("Pilih menu: ")

            if pilihan == "1":
                logout(database)
                print(json.dumps(database, indent=4))
                save_data(file_path, database)
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
                save_data(file_path, database)
                break
        elif pilihan == "2":
            register(database)
            save_data(file_path, database)
        elif pilihan == "3":
            print("\nTerima kasih telah menggunakan sistem. Sampai jumpa!\n")
            break
        else:
            print("\nPilihan tidak valid, silakan coba lagi.\n")

if __name__ == "__main__":
    main()
