import sqlite3
import tkinter as tk
from tkinter import messagebox

def create_table():
    conn = sqlite3.connect('cuaca.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cuaca (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            lokasi TEXT,
            waktu TEXT,
            suhu REAL,
            kondisi TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()

def register():
    username = register_username_entry.get()
    password = register_password_entry.get()

    conn = sqlite3.connect('cuaca.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    conn.close()

    messagebox.showinfo("Info", "Registrasi berhasil. Silakan login.")

def login():
    username = login_username_entry.get()
    password = login_password_entry.get()

    conn = sqlite3.connect('cuaca.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE username = ? AND password = ?', (username, password))
    user_id = cursor.fetchone()

    if user_id:
        login_frame.pack_forget()  # Menyembunyikan form login
        main_menu_frame.pack()  # Menampilkan menu utama
    else:
        messagebox.showerror("Error", "Login Gagal. Periksa kembali username dan password.")

def tambah_cuaca():
    lokasi = lokasi_entry.get()
    waktu = waktu_entry.get()
    suhu = float(suhu_entry.get())

    kondisi = ''
    if suhu < 27:
        kondisi = 'dingin'
    elif 27 <= suhu <= 31:
        kondisi = 'normal'
    else:
        kondisi = 'panas'

    user_id = get_user_id(login_username_entry.get())

    conn = sqlite3.connect('cuaca.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO cuaca (user_id, lokasi, waktu, suhu, kondisi)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, lokasi, waktu, suhu, kondisi))
    conn.commit()
    conn.close()
    messagebox.showinfo("Info", "Data cuaca berhasil ditambahkan.")
    tampilkan_cuaca()

def tampilkan_cuaca():
    user_id = get_user_id(login_username_entry.get())

    conn = sqlite3.connect('cuaca.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cuaca WHERE user_id = ?', (user_id,))
    data_cuaca = cursor.fetchall()
    conn.close()

    if not data_cuaca:
        messagebox.showinfo("Info", "Tidak ada data cuaca.")
    else:
        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)
        for data in data_cuaca:
            result_text.insert(tk.END, f"ID: {data[0]}, Lokasi: {data[2]}, Waktu: {data[3]}, Suhu: {data[4]}, Kondisi: {data[5]}\n")
        result_text.config(state=tk.DISABLED)

def get_user_id(username):
    conn = sqlite3.connect('cuaca.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
    user_id = cursor.fetchone()
    conn.close()

    return user_id[0] if user_id else None

def main():
    create_table()

    root = tk.Tk()
    root.title("Aplikasi Informasi Cuaca")

    # Form Registrasi
    register_frame = tk.Frame(root)
    register_frame.pack(pady=10)

    tk.Label(register_frame, text="Username:").grid(row=0, column=0)
    tk.Label(register_frame, text="Password:").grid(row=1, column=0)

    global register_username_entry, register_password_entry
    register_username_entry = tk.Entry(register_frame)
    register_password_entry = tk.Entry(register_frame, show="*")

    register_username_entry.grid(row=0, column=1)
    register_password_entry.grid(row=1, column=1)

    register_button = tk.Button(register_frame, text="Register", command=register)
    register_button.grid(row=2, column=0, columnspan=2)

    # Form Login
    global login_frame
    login_frame = tk.Frame(root)
    login_frame.pack(pady=10)

    tk.Label(login_frame, text="Username:").grid(row=0, column=0)
    tk.Label(login_frame, text="Password:").grid(row=1, column=0)

    global login_username_entry, login_password_entry
    login_username_entry = tk.Entry(login_frame)
    login_password_entry = tk.Entry(login_frame, show="*")

    login_username_entry.grid(row=0, column=1)
    login_password_entry.grid(row=1, column=1)

    login_button = tk.Button(login_frame, text="Login", command=login)
    login_button.grid(row=2, column=0, columnspan=2)

    # Menu Utama
    global main_menu_frame
    main_menu_frame = tk.Frame(root)

    # Tambah Data Cuaca
    tambah_frame = tk.Frame(main_menu_frame)
    tambah_frame.pack(pady=10)

    tk.Label(tambah_frame, text="Lokasi:").grid(row=0, column=0)
    tk.Label(tambah_frame, text="Waktu (YYYY-MM-DD HH:mm:ss):").grid(row=1, column=0)
    tk.Label(tambah_frame, text="Suhu (Celsius):").grid(row=2, column=0)

    global lokasi_entry, waktu_entry, suhu_entry
    lokasi_entry = tk.Entry(tambah_frame)
    waktu_entry = tk.Entry(tambah_frame)
    suhu_entry = tk.Entry(tambah_frame)

    lokasi_entry.grid(row=0, column=1)
    waktu_entry.grid(row=1, column=1)
    suhu_entry.grid(row=2, column=1)

    tambah_button = tk.Button(tambah_frame, text="Tambah Data Cuaca", command=tambah_cuaca)
    tambah_button.grid(row=3, column=0, columnspan=2)

    # Tampilkan Data Cuaca
    tampilkan_frame = tk.Frame(main_menu_frame)
    tampilkan_frame.pack(pady=10)

    tampilkan_button = tk.Button(tampilkan_frame, text="Tampilkan Data Cuaca", command=tampilkan_cuaca)
    tampilkan_button.pack()

    # Result Text
    global result_text
    result_text = tk.Text(root, height=10, width=50, state=tk.DISABLED)
    result_text.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
