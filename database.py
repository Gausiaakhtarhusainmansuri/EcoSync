import sqlite3

connection = sqlite3.connect("ecosync.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS participants (
    participant_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    college TEXT NOT NULL,
    e_waste_type TEXT NOT NULL
)
""")

# Create collections table
cursor.execute("""
CREATE TABLE IF NOT EXISTS collections (
    collection_id INTEGER PRIMARY KEY AUTOINCREMENT,
    participant_id INTEGER NOT NULL,
    e_waste_type TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    collection_date TEXT NOT NULL
)
""")

connection.commit()

connection.close()

print("Database created successfully!")