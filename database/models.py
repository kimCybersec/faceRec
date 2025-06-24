import sqlite3

def initDb(dbPath='database/accessControl.db'):
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS AccessLogs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        type TEXT NOT NULL,
        identity TEXT NOT NULL,
        confidence REAL,
        imagePath TEXT)
        ''')
    
    conn.commit()
    conn.close()
    print("[!]Databse initialized.")