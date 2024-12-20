import json

users = [
    {"id" : 1, "nama" : " michele", "email" : "michele@gmail.com", "password" : "michele123"},
    {"id" : 2, "nama" : "gabriel", "email" : "gabriel@gmail.com", "password" : "gabrilee"},
]

#menyimpan data ke file JSON
with open("database.json", "w") as file:
    json.dump(users, file)

# Membaca data dari file JSON
with open("database.json", "r") as file:
    loaded_data = json.load(file)

with open("users.json", "w") as file:
    json.dump(users, file, indent=4)

print(loaded_data)