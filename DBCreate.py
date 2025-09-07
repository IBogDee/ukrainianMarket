import sqlite3

conn = sqlite3.connect('market.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        category TEXT NOT NULL
    )
''')

conn.commit()
conn.close()