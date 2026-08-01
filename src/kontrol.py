import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

db = os.path.join(BASE_DIR, "siparis.db")

print(db)

conn = sqlite3.connect(db)

cur = conn.cursor()

cur.execute("SELECT name FROM sqlite_master WHERE type='table'")

print(cur.fetchall())

conn.close()
