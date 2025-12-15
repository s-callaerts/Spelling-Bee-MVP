import sqlite3

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
    )
''')
conn.commit()

try:
    cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", ("Alice", "alice@example.com"))
    cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", ("John", "john@example.com"))
    conn.commit()
except sqlite3 IntegrityError:
    print("Records already exist, skipping insertion")

cursor.execute("SELECT + FROM users")
records = cursor.fetchall()
print(records)

conn.close()
