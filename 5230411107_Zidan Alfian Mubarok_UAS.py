#ZIDAN ALFIAN MUBAROK @5230411107
import PySimpleGUI as sg
import sqlite3
import datetime
from datetime import datetime
from streamlit as st

#updated fix hild gui for datasheets
def create_table():
    conn = sqlite3.connect("cuaca.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cuaca (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lokasi TEXT,
            waktu TEXT,
            suhu REAL,
            kondisi TEXT,
            tanggal TEXT  -- Tambahkan kolom yang hilang
        )
    ''')
    conn.commit()
    conn.close()

#2026
def create_user_table():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()


def register_user(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (username, password)
        VALUES (?, ?)
    ''', (username, password))
    conn.commit()
    conn.close()


def verify_login(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    data = cursor.fetchone()
    conn.close()
    return data is not None


def create_login_layout():
    return [
        [sg.Text("🌍WeatherHub App", font=("Helvetica", 16))],
        [sg.Image(filename='44.png', size=(500, 200))],
        [sg.Text("Username:"), sg.InputText(key="login_username")],
        [sg.Text("Password:"), sg.InputText(key="login_password", password_char="*")],
        [sg.Button("Login"), sg.Button("Register"), sg.Button("Delete User Data")]
    ]


def login_window():
    layout = create_login_layout()
    window = sg.Window("Login", layout, resizable=True)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            sg.popup("Selamat tinggal!")
            exit()
        elif event == "Login":
            username = values["login_username"]
            password = values["login_password"]
            if verify_login(username, password):
                window.close()
                return username
            else:
                sg.popup_error("Username atau password salah. Silakan coba lagi.")
        elif event == "Register":
            window.close()
            return register_window()
        elif event == "Delete User Data":
            username = values["login_username"]
            delete_user_data_window(username)


def register_window():
    layout = create_register_layout()
    window = sg.Window("Register", layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            sg.popup("SAMPAI JUMPA DI APP KAMI 🎀")
            exit()
        elif event == "Register":
            username = values["register_username"]
            password = values["register_password"]
            if username and password:
                register_user(username, password)
                sg.popup("Pendaftaran berhasil! Anda sekarang dapat masuk.")
                window.close()
                return login_window()
            else:
                sg.popup_error("Username dan password diperlukan.")


def create_register_layout():
    return [
        [sg.Image(filename='55.png', size=(500, 200))],
        [sg.Text("Username:"), sg.InputText(key="register_username")],
        [sg.Text("Password:"), sg.InputText(key="register_password", password_char="*")],
        [sg.Button("Register")]
    ]


def insert_data(id, location, time, temperature, tanggal):
    condition = determine_condition(temperature)
    
    # Format nilai tanggal sesuai gaya 
    formatted_tanggal = datetime.strptime(tanggal, "%Y-%m-%d %H:%M:%S").strftime("%d-%m-%Y %H:%M:%S")
    
    conn = sqlite3.connect("cuaca.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO cuaca (id, lokasi, waktu, suhu, kondisi, tanggal)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (id, location, time, temperature, condition, formatted_tanggal))
    conn.commit()
    conn.close()


def determine_condition(temperature):
    if temperature < 27:
        return "dingin"
    elif 27 <= temperature <= 31:
        return "normal"
    else:
        return "panas"


def get_all_data():
    conn = sqlite3.connect("cuaca.db")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM cuaca  
    ''')
    data = cursor.fetchall()
    conn.close()
    return data


def delete_data(id):
    conn = sqlite3.connect("cuaca.db")
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM cuaca  
        WHERE id=?
    ''', (id,))
    conn.commit()
    conn.close()


def update_data(id, location, time, temperature):
    condition = determine_condition(temperature)
    conn = sqlite3.connect("cuaca.db")
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE cuaca  
        SET lokasi=?, waktu=?, suhu=?, kondisi=?
        WHERE id=?
    ''', (location, time, temperature, condition, id))
    conn.commit()
    conn.close()


def create_table_layout(data, scroll_text):
    return [
        [sg.Text("ID       :"), sg.InputText(key="id")],
        [sg.Text("Lokasi :"), sg.InputText(key="lokasi")],
        [sg.Text("Waktu  :"), sg.InputText(key="waktu")],
        [sg.Text("Suhu   :"), sg.InputText(key="suhu")],
        [sg.Text("Tanggal:"), sg.CalendarButton("Select Date", target="tanggal", key="calendar_tanggal"),
         sg.InputText(key="tanggal", disabled=True)],
        [sg.Button("Add"), sg.Button("Update"), sg.Button("Delete"), sg.Button("Refresh")],
        [sg.Table(values=data,
                  headings=["ID", "Lokasi", "Waktu", "Suhu", "Kondisi", "Tanggal"],
                  auto_size_columns=False, justification='right', num_rows=10, key="table",
                  text_color='black', background_color='grey',
                  )],
        [sg.Text(scroll_text, key="scroll_text", size=(100, 1))]
    ]


def update_data_popup(id):
    conn = sqlite3.connect("cuaca.db")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cuaca WHERE id=?', (id,))
    data = cursor.fetchone()
    conn.close()

    if not data:
        sg.popup_error(f"Data dengan ID {id} tidak ditemukan.")
        return

    layout = [
        [sg.Text(f"ID: {id}")],
        [sg.Text("Lokasi:"), sg.InputText(default_text=data[1], key="lokasi")],
        [sg.Text("Waktu:"), sg.InputText(default_text=data[2], key="waktu")],
        [sg.Text("Suhu:"), sg.InputText(default_text=str(data[3]), key="suhu")],
        [sg.Button("Update")]
    ]

    window = sg.Window("Update Data", layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break
        elif event == "Update":
            new_location = values["lokasi"]
            new_time = values["waktu"]
            new_temperature = float(values["suhu"])
            update_data(id, new_location, new_time, new_temperature)
            sg.popup("Pembaruan berhasil", f"Data dengan ID {id} telah diperbarui.")
            break

    window.close()


def delete_user_data_window(username):
    layout = [
        [sg.Text(f"Masukkan kata sandi untuk menghapus data pengguna {username}")],
        [sg.Text("Kata Sandi:"), sg.InputText(key="delete_password", password_char="*")],
        [sg.Button("Hapus Data Pengguna")]
    ]

    window = sg.Window("Hapus Data Pengguna", layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break
        elif event == "Hapus Data Pengguna":
            password = values["delete_password"]

            if verify_login(username, password):
                conn = sqlite3.connect("users.db")
                cursor = conn.cursor()
                cursor.execute('''
                    DELETE FROM users  
                    WHERE username=?
                ''', (username,))
                conn.commit()
                conn.close()
                sg.popup("Penghapusan data pengguna berhasil!", f"Data untuk {username} telah dihapus.")
            else:
                sg.popup_error("Kata sandi tidak valid. Silakan coba lagi.")

            break

    window.close()


def main():
    create_table()
    create_user_table()

    username = login_window()

    data = get_all_data()

    scroll_text = "SELAMAT DATANG DI APLIKASI KAMI SEMOGA MENJADI PENGALAMAN TERBAIK. " * 4

    layout = create_table_layout(data, scroll_text)

    window = sg.Window("Sistem Cuaca", layout, resizable=True)

    while True:
        event, values = window.read(timeout=100)

        if event == sg.WIN_CLOSED:
            break
        elif event == "Add":
            if 'tanggal' in values:
                insert_data(
                    int(values["id"]),
                    values["lokasi"],
                    values["waktu"],
                    float(values["suhu"]),
                    values["tanggal"]
                )
            else:
                insert_data(int(values["id"]), values["lokasi"], values["waktu"], float(values["suhu"]))
        elif event == "calendar_tanggal":
            selected_date = sg.popup_get_date("Pilih Tanggal", no_titlebar=True)
            if selected_date:
                formatted_date = selected_date.strftime("%Y-%m")
                window["tanggal"].update(value=formatted_date)
        elif event == "Update":
            input_id = sg.popup_get_text("Masukkan ID untuk diperbarui:")
            if input_id and input_id.isdigit():
                id_to_update = int(input_id)
                update_data_popup(id_to_update)
        elif event == "Delete":
            input_id = sg.popup_get_text("Masukkan ID untuk dihapus:")
            if input_id and input_id.isdigit():
                id_to_delete = int(input_id)
                confirmation = sg.popup_yes_no(f"Apakah Anda yakin ingin menghapus ID {id_to_delete}?", title="Konfirmasi")
                if confirmation == "Yes":
                    delete_data(id_to_delete)
                    sg.popup("Penghapusan berhasil", f"Data dengan ID {id_to_delete} telah dihapus.")
        elif event == "Refresh":
            data = get_all_data()
            window["table"].update(values=data)
            sg.Popup("Semua Data", "\n".join([f"ID: {row[0]}, Lokasi: {row[1]}, Waktu: {row[2]}, Suhu: {row[3]}°C, Kondisi: {row[4]}" for row in data]))

        scroll_text = scroll_text[1:] + scroll_text[0]
        window["scroll_text"].update(scroll_text)

    window.close()


if __name__ == "__main__":
    main()
