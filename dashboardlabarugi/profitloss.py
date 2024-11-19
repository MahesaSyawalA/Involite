import tkinter as tk
from owner import businessCapital
from logistics import logisticsStock

#Window optimization
root = tk.Tk()
root.geometry("300x250")
root.title("Perhitungan laba dan rugi by InvoLite")

#Label
label_modal = tk.Label(root, text="Harga Jual per barang:  ")
label_modal.pack(pady=5)
entry_modal = tk.Entry(root)
entry_modal.pack(pady=5)


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

