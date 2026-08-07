import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

db = os.path.join(BASE_DIR, "siparis.db")

print("DB =", db)

conn = sqlite3.connect(db)
cur = conn.cursor()

print("\n===== URUNLER TABLOSU =====")
cur.execute("PRAGMA table_info(urunler)")
for satir in cur.fetchall():
    print(satir)

print("\n===== SUBELER TABLOSU =====")
cur.execute("PRAGMA table_info(subeler)")
for satir in cur.fetchall():
    print(satir)

conn.close()
