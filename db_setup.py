import sqlite3

def init_sqlite_db():
    conn = sqlite3.connect('attendance.db')
    print("Opened database successfully")

    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT
        )
    ''')
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date TEXT,
            time TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    print("Tables created successfully")
    conn.close()

if __name__ == '__main__':
    init_sqlite_db()
