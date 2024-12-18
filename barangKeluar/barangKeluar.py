import datetime
import json
from tkinter import Tk, Label, Entry, Button, messagebox, ttk, Canvas, Frame

#Path ke JSON
file_path = "./data_barang.json"
log_file_path = "./data_transaksi.json"

#Fungsi membaca data dari file JSON
def baca_data():
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
#Fungsi untuk menulis data JSON    
def tulis_data(data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

#Fungsi untuk menampilkan data ke dalam tabel
def tampilkan_data():
    for row in tree.get_children():
        tree.delete(row)
    data = baca_data()
    for item in data:
        tree.insert("", "end", values =(item["idbrg"], item["nama"], item["harga_beli"], 
                                        item["harga_jual"],item["stok"],item["tanggal_masuk"]))

#Fungsi search
def search(keyword):
    for row in tree.get_children():
        tree.delete(row)
        
    data = baca_data()
    for item in data:
        if keyword.lower() in item['nama'].lower() or keyword in item['idbrg']:
            tree.insert("", "end", values=(item['idbrg'], item['nama'], item['harga_beli'], item['harga_jual'], item['stok'] ,item['tanggal_masuk']))
    

#Fungsi untuk menambah barang ke tabel catatan pengurangan stok
def tambah_catatan():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Pilih barang!")
        return
    jumlah_keluar = entry_jumlah_keluar.get()
    if not jumlah_keluar.isdigit() or int(jumlah_keluar) <= 0:
        messagebox.showerror("Error", "Masukan jumlah barang yang vaild!")
        return
    
    jumlah_keluar = int(jumlah_keluar)
    barang = tree.item(selected_item,"values")
    stok_sekarang = int(barang[4])
    
    if jumlah_keluar > stok_sekarang:
        messagebox.showerror("Error", "Stok kurang!")
        return

    tree_catatan.insert("", "end", values=(barang[0], barang[1], barang[3], barang[4], jumlah_keluar))
    entry_jumlah_keluar.delete(0, "end")
    
#Fungsi untuk menyimpan log transaksi ke file internal
def simpan_log(log):
    def baca_logs():
        try:
            with open(log_file_path, "r") as file:
                return json.load(file)
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan log: {e}")
    def tulis_log(log):
        with open(log_file_path, "w") as file:
            json.dump(log, file, indent=4)
    data_logs = baca_logs()
    data_logs.extend(log)
    tulis_log(data_logs)
    
#Fungsi untuk menampilkan GUI info transaksi
def info_transaksi(logs):
    info_root = Tk()
    info_root.title("Informasi Transaksi")
    info_root.geometry("400x400")
    
    jumlah_total = sum(log['total_harga'] for log in logs)
    
    canvas = Canvas(info_root)
    scroll_y = ttk.Scrollbar(info_root, orient="vertical", command=canvas.yview)
    frame = Frame(canvas)
    
    for index, log in enumerate(logs):
        Label(frame, text=f"Nama Produk: {log['nama']}").grid(row=index*5, column=0, sticky="w", padx=10, pady=5)
        Label(frame, text=f"Harga Satuan: {log['harga_satuan']}").grid(row=index*5+1, column=0, sticky="w", padx=10, pady=5)
        Label(frame, text=f"Jumlah Beli: {log['jumlah']}").grid(row=index*5+2, column=0, sticky="w", padx=10, pady=5)
        Label(frame, text=f"Total Harga: {log['total_harga']}").grid(row=index*5+3, column=0, sticky="w", padx=10, pady=5)
        Label(frame, text="-"*30).grid(row=index*5+4, column=0, sticky="w", padx=10, pady=5)
    Label(frame, text="="*30).grid(row=len(logs)*5-1, column=0, sticky="w", padx=10, pady=5)
    Label(frame, text=f"Jumlah Total Harga: {jumlah_total}").grid(row=len(logs)*5, column=0, sticky="w", padx=10, pady=5)
    
    canvas.create_window(0,0, anchor="nw", window=frame)
    frame.update_idletasks()
    
    canvas.configure(scrollregion=canvas.bbox("all"), yscrollcommand=scroll_y.set)
    
    canvas.pack(fill="both", expand=True, side="left")
    scroll_y.pack(fill="y", side="right")
    
    info_root.mainloop()
 
 #Fungsi untuk mengkonfirmasi pengurangan stok   
def konfirmasi():
    catatan = tree_catatan.get_children()
    if not catatan:
        messagebox.showerror("Error", "Tidak ada barang yang tercatat untuk keluar")
        return
    
    response = messagebox.askyesno("Konfirmasi Barang Keluar", "Apa Anda yakin ingin mengurangi stok yang tercatat?")
    if response:
        data = baca_data()
        logs = []
        for item in catatan:
            catatan_barang = tree_catatan.item(item, "values")
            id_barang = catatan_barang[0]
            jumlah_keluar = int(catatan_barang[4])
            
            for barang in data:
                if barang["idbrg"] == id_barang:
                    if barang ["stok"] >= jumlah_keluar:
                        barang["stok"] -= jumlah_keluar
                        total_harga = jumlah_keluar * int(catatan_barang[2])
                        time = datetime.datetime.now().strftime("%Y-%m-%d %H: %M: %S")
                        log = {
                            "waktu": time,
                            "idbrg": barang["idbrg"],
                            "nama": barang["nama"],
                            "harga_satuan": int(catatan_barang[2]),
                            "jumlah": jumlah_keluar,
                            "total_harga": total_harga
                        }
                        logs.append(log)
                    else:
                        messagebox.showerror("Error", f"Stok barang {barang['nama']} tidak mencukupi")
                        return
        tulis_data(data)
        tampilkan_data()
        tree_catatan.delete(*tree_catatan.get_children())
        messagebox.showinfo("Berhasil", "Stok barang berhasil diperbarui")
        simpan_log(logs)
        info_transaksi(logs)
        
#Fungsi untuk menghapus item dari catatan
def hapus_catatan():
    selected_item = tree_catatan.selection()
    if not selected_item:
        messagebox.showerror("Error", "Pilih item untuk dihapus dari catatan!")
        return
    tree_catatan.delete(selected_item)
    

        

#GUI Utama
root = Tk()
root.title("Dashboard data keluar")
root.geometry("770x800")

#Tabel data
columns = ("ID Barang", "Nama", "Harga Beli", "Harga Jual", "Stok", "Tanggal Masuk")
tree = ttk.Treeview(root, columns=columns, show="headings", height=15)
scrollbar_tree = ttk.Scrollbar(root, orient="vertical", command=tree.yview)#menambahkan fitur scroll pada tabelnya
tree.configure(yscrollcommand=scrollbar_tree.set)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120)
        
tree.grid(row=0, column=0, columnspan=5, padx=10, pady=10)
scrollbar_tree.grid(row=0, column=5, sticky="ns")#menambahkan scroll bar


#Tabel Catatan 
columns_catatan = ("ID Barang", "Nama", "Harga Jual", "Stok", "Jumlah Keluar")
tree_catatan = ttk.Treeview(root, columns=columns_catatan, show="headings", height=10)

scrollbar_tree_catatan = ttk.Scrollbar(root, orient="vertical", command=tree_catatan.yview)
tree_catatan.configure(yscrollcommand=scrollbar_tree_catatan.set)

for col in columns_catatan:
    tree_catatan.heading(col, text=col)
    tree_catatan.column(col, width=120)

tree_catatan.grid(row=3, column=0, columnspan=5, padx=10, pady=10)
scrollbar_tree_catatan.grid(row=3, column=5, sticky="ns")

#Label dan entry untuk jumlah barang keluar
Label(root, text="Jumlah Barang Keluar: ").grid(row=2, column=0, padx= 10, pady=10, sticky="w")
entry_jumlah_keluar = Entry(root, width=30)
entry_jumlah_keluar.grid(row=2, column=1, padx=10, pady=10)

# Entry dan tombol untuk pencarian
Label(root, text="Cari Barang: ").grid(row=1, column=0, padx=10, pady=10, sticky="w")
entry_cari = Entry(root, width=30)
entry_cari.grid(row=1, column=1, padx=10, pady=10)
entry_cari.bind("<KeyRelease>", lambda event: search(entry_cari.get()))

#Tombol untuk menambah catatan
Button(root, text="Tambah ke Catatan", command=tambah_catatan).grid(row=2, column=2, pady=10)

#Tombol untuk menghapus dari catatan
Button(root, text="Hapus barang dari Catatan", command=hapus_catatan).grid(row=2, column=3, pady=10)

#Tombol untuk konfirmasi pengurangan barang
Button(root, text="Konfirmasi Barang Keluar", command=konfirmasi).grid(row=4, column=3, padx=10, pady=10)

#Menampilkan data awal
tampilkan_data()

#Menjalankan GUI
root.mainloop()    
    
