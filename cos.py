import sqlite3
conn = sqlite3.connect('library.db')
conn.execute('''
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    isbn TEXT UNIQUE NOT NULL,
    quantity INTEGER NOT NULL,
    room TEXT,
    shelf TEXT,
    section TEXT
)
''')
conn.close()
