import sqlite3

def create_database():
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            name TEXT,
            face_embedding BLOB
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()
