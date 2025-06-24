import sqlite3
from datetime import datetime

def imgEntry(identity, entryType = 'face', confidence = None, imagePath = None, dbPath = "database/accessControl.db"):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO AccessLogs(timestamp, type, identity, confidence, imagePath)
        VALUES(?, ?, ?, ?, ?)''',(timestamp, entryType, identity, confidence, imagePath))
    
    conn.commit()
    conn.close()
    print(f"[!] Logged {entryType} access for {identity}")