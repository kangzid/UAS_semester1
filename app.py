from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Fungsi untuk menginisialisasi database
def init_db():
    conn = sqlite3.connect('cuaca.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cuaca (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lokasi TEXT NOT NULL,
            waktu TEXT NOT NULL,
            suhu REAL NOT NULL,
            kondisi TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Fungsi untuk menentukan kondisi cuaca berdasarkan suhu
def tentukan_kondisi(suhu):
    if suhu < 27:
        return 'dingin'
    elif 27 <= suhu <= 31:
        return 'normal'
    else:
        return 'panas'

# Fungsi untuk menampilkan semua data cuaca dari database
def get_all_cuaca():
    conn = sqlite3.connect('cuaca.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cuaca')
    data_cuaca = cursor.fetchall()
    conn.close()
    return data_cuaca

# Fungsi untuk menambah data cuaca ke database
def tambah_cuaca(lokasi, waktu, suhu):
    kondisi = tentukan_kondisi(suhu)
    conn = sqlite3.connect('cuaca.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO cuaca (lokasi, waktu, suhu, kondisi)
        VALUES (?, ?, ?, ?)
    ''', (lokasi, waktu, suhu, kondisi))
    conn.commit()
    conn.close()

# Fungsi untuk mengubah data cuaca di database
def ubah_cuaca(id, suhu):
    kondisi = tentukan_kondisi(suhu)
    conn = sqlite3.connect('cuaca.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE cuaca
        SET suhu=?, kondisi=?
        WHERE id=?
    ''', (suhu, kondisi, id))
    conn.commit()
    conn.close()

# Fungsi untuk menghapus data cuaca dari database
def hapus_cuaca(id):
    conn = sqlite3.connect('cuaca.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM cuaca WHERE id=?', (id,))
    conn.commit()
    conn.close()

# Inisialisasi database saat aplikasi dijalankan
init_db()

# Route untuk halaman utama
@app.route('/')
def index():
    data_cuaca = get_all_cuaca()
    return render_template('index.html', data_cuaca=data_cuaca)

# Route untuk menambah data cuaca
@app.route('/tambah', methods=['POST'])
def tambah_data():
    return render_template('tambah.html')

# Route untuk mengubah data cuaca
@app.route('/ubah_data/<int:id>', methods=['POST'])
def ubah_data(id):
    return render_template('ubah.html', id=id)

# Route untuk menghapus data cuaca
@app.route('/hapus/<int:id>')
def hapus_data(id):
    return render_template('hapus.html', id=id)

# Route untuk menangani form penambahan data cuaca
@app.route('/tambah_data', methods=['POST'])
def tambah_data_post():
    lokasi = request.form['lokasi']
    waktu = request.form['waktu']
    suhu = float(request.form['suhu'])
    tambah_cuaca(lokasi, waktu, suhu)
    return redirect(url_for('index'))

# Route untuk menangani form perubahan data cuaca
@app.route('/ubah_data/<int:id>', methods=['POST'])
def ubah_data_post(id):
    suhu = float(request.form['suhu'])
    ubah_cuaca(id, suhu)
    return redirect(url_for('index'))

# Route untuk menangani form penghapusan data cuaca
@app.route('/hapus_data/<int:id>')
def hapus_data_post(id):
    hapus_cuaca(id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
