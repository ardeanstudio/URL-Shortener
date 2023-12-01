# CREDIT Author: @ArdeanBimaSaputra
# Visit my website https://ardeanstudio.co

import pyshorteners
import sqlite3

# Inisialisasi koneksi database
conn = sqlite3.connect('url_shortener.db')
cursor = conn.cursor()

# Buat tabel jika tidak ada
cursor.execute('''
    CREATE TABLE IF NOT EXISTS urls (
        original_url TEXT,
        short_url TEXT PRIMARY KEY UNIQUE
    )
''')

# Berfungsi untuk memperpendek suatu URL
def shorten_url(original_url):
    
    # Periksa apakah URL sudah ada di database
    cursor.execute('SELECT short_url FROM urls WHERE original_url = ?', (original_url,))
    existing_url = cursor.fetchone()

    if existing_url:
        # Verifikasi: URL sudah ada, mengembalikan URL yang ada
        return existing_url[0]
    else:
        # Verifikasi: URL tidak ada, buat URL baru
        shortener = pyshorteners.Shortener()
        short_url = shortener.tinyurl.short(original_url)

        # Masukkan URL baru ke dalam database
        cursor.execute('INSERT INTO urls (original_url, short_url) VALUES (?, ?)', (original_url, short_url))
        conn.commit()

        return short_url

# Berfungsi untuk membatalkan proses
def unshorten_url(short_url):
    
    # Periksa apakah URL ada di database
    cursor.execute('SELECT original_url FROM urls WHERE short_url = ?', (short_url,))
    original_url = cursor.fetchone()

    if original_url:
        # URL sudah ada, mengembalikan URL asli
        return original_url[0]
    else:
        # URL tidak ada, mengembalikan pesan error
        return "URL not found"

# Masukan url anda disini!
original_url = "https://ardeanstudio.co/cara-blokir-iklan-hp-bebas-iklan-dengan-cara-ini/"
short_url = shorten_url(original_url)

print("URL Asli:", original_url)
print("URL yang di Short:", short_url)

unshortened_url = unshorten_url(short_url)
print("URL yang tidak di proses:", unshortened_url)
