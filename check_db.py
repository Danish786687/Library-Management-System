import os
import sqlite3 #module library.db se connect krnk liy

db_path = os.path.abspath("library.db")   

print("Database path:")
print(db_path)

print()

conn = sqlite3.connect(db_path)

cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")  #to access all tabless of the data

tables = cursor.fetchall()

print("Tables:")

for table in tables:
    print(table[0])

conn.close()