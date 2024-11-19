import tkinter as tk
from owner import businessCapital
from logistics import logisticsStock

#Input from owner and logistics
modal = businessCapital
stock = logisticsStock

#Mathematical function 
def calculate_profit():
    jumlah_barang_terjual = int(entry_jbt.get())
    harga_jual_barang = int(entry_hbj.get())
    modal = int(entry_modal.get())

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