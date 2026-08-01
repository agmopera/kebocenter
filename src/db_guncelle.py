import os

print("Çalışma klasörü:", os.getcwd())
print("DB yolu:", os.path.abspath("../siparis.db"))

import sqlite3

DB_NAME = "../siparis.db"

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# Eski tabloyu yedekle
cursor.execute("""
ALTER TABLE subeler
RENAME TO subeler_eski
""")

# Yeni tablo
cursor.execute("""
CREATE TABLE subeler(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    sube_adi TEXT NOT NULL,

    kullanici_adi TEXT UNIQUE,

    sifre TEXT,

    yetkili TEXT,

    telefon TEXT,

    eposta TEXT,

    il TEXT,

    ilce TEXT,

    adres TEXT,

    durum TEXT
)
""")

# Eski verileri yeni sırayla taşı
cursor.execute("""
INSERT INTO subeler
(
    id,
    sube_adi,
    kullanici_adi,
    sifre,
    yetkili,
    telefon,
    eposta,
    il,
    ilce,
    adres,
    durum
)

SELECT
    id,
    sube_adi,
    kullanici_adi,
    sifre,
    yetkili,
    telefon,
    eposta,
    il,
    ilce,
    adres,
    durum

FROM subeler_eski
""")

cursor.execute("DROP TABLE subeler_eski")

conn.commit()
conn.close()

print("Veritabanı başarıyla güncellendi.")
