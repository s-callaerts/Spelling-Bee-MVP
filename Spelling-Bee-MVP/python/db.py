import sqlite3

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    uid INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password VARCHAR(30) NOT NULL,
    grade VARCHAR(15) NOT NULL,
    isTeacher BOOLEAN
    );
''')
conn.commit()

try:
    cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", ("Alice", "alice@example.com"))
    cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", ("John", "john@example.com"))
    conn.commit()
except sqlite3 IntegrityError:
    print("Records already exist, skipping insertion")

cursor.execute("SELECT * FROM users")
records = cursor.fetchall()
print(records)

conn.close()
