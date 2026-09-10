import sqlite3

connection = sqlite3.connect("ecosync.db")

cursor = connection.cursor()

cursor.execute("SELECT * FROM participants")

data = cursor.fetchall()

for row in data:
    print(row)

connection.close()