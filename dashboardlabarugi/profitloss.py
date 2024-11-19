import tkinter as tk
from tkinter import messagebox

#Input from owner and logistics


#Mathematical function 
def calculate_profit():
    jumlah_barang_terjual = int(entry_jbt.get())
    harga_jual_barang = int(entry_hbj.get())
    modal = int(entry_modal.get())

    profit = jumlah_barang_terjual * harga_jual_barang - modal
    return profit
    

def assumption():
    profit = calculate_profit()
    if profit > 0:
            label_hasil.config(text=f"Keuntugan yang didapat: {abs(profit)}")
    elif profit < 0:
            label_hasil.config(text=f"Kerugian  yang didapat: {abs(profit)}")
    elif profit == 0:
            label_hasil.config(text="Tidak mengalami keuntungan ataupun kerugian!")
    else:
        return "Mohon maaf, terjadi kesalahan dalam perhitungan!"


#Window optimization
root = tk.Tk()
root.geometry("300x250")
root.title("Perhitungan laba dan rugi by InvoLite")

#Label
label_jumlah_barang_terjuan = tk.Label(root, text="Jumlah barang terjual:")
label_jumlah_barang_terjuan.pack(pady=5)
entry_jbt = tk.Entry(root)
entry_jbt.pack(pady=5)

label_harga_jual_barang = tk.Label(root, text="Harga jual per barang:")
label_harga_jual_barang.pack(pady=5)
entry_hbj = tk.Entry(root)
entry_hbj.pack(pady=5)

modal = tk.Label(root, text="Modal:")
modal.pack(pady=5)
entry_modal = tk.Entry(root)
entry_modal.pack(pady=5)

calculate_button = tk.Button(root, text="Hitung Profit", command=assumption)
calculate_button.pack(pady=10)

<<<<<<< HEAD
label_hasil = tk.Label(root, text="")
label_hasil.pack(pady=5)

root.mainloop()
=======
#Input from owner and logistics
modal = businessCapital
stock = logisticsStock


#Mathematical function 
def calculate_profit():
    profitLoss = selling_price * total_item - modal
    return profitLoss

#Assumption
def assumption():
    if calculate_profit > 0:
        return "Keuntungan yang didapat sebanyak ", calculate_profit
    elif calculate_profit < 0:
        return "Rugi yang didapat sebanyak ", calculate_profit
    elif calculate_profit == 0:
        return "Tidak mengalami keuntungan maupun kerugian!"
    else:
        return "Mohon maaf, terjadi kesalahan dalam perhitungan!"
    


#Input from accountant
selling_price = int(input("Harga jual per barang: "))
total_item = int(input("Jumlah barang terjual: "))

print('Hello World')
>>>>>>> 18575dcdc244f3d01878e96fe5887c84385d9bdd
