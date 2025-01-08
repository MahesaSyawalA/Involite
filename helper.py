import re
from datetime import datetime
import json

def load_data():
    """Load JSON data from a file."""
    try:
        with open("database.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("File Database not found.")
        return None
    

def save_data(data):
    """Save JSON data to a file."""
    with open("database.json", "w") as file:
        json.dump(data, file, indent=4)


def validate_input(prompt, pattern, cast_type=str, default=None, validate_date=False, menu=False, maxMenu=0):
    """Validate user input against a regex pattern and additional checks like date validation."""
    while True:
        user_input = input(prompt)
        if not user_input and default is not None:
            return default
        
        if re.match(pattern, user_input):
            if validate_date:
                try:
                    input_date = datetime.strptime(user_input, "%Y-%m-%d").date()
                    today = datetime.today().date()
                    if input_date > today:
                        print("Tanggal tidak boleh lebih dari tanggal hari ini!")
                        continue  
                except ValueError:
                    print("Tanggal tidak valid! Periksa kembali format atau tanggal yang dimasukkan.")
                    continue  

            if menu:
                try:
                    if int(user_input) > maxMenu:
                        print('inputan anda melebihi menu yang ada, silakan input kembali')
                        continue
                except ValueError:
                    print('inputan tidak valid, silakan coba lagi')
                    continue
            return cast_type(user_input)
        
        print("Input tidak valid. Silakan coba lagi.")
