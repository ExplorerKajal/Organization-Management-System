import sqlite3
import os

try:
    print("Checking app.db...")
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables:", tables)
    
    if any('users' in t for t in tables):
        cursor.execute("PRAGMA table_info(users);")
        print("Users table info:", cursor.fetchall())
    else:
        print("users table not found!")
except Exception as e:
    print(f"Error: {e}")
