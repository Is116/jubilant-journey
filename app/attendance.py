import sqlite3
from datetime import datetime

def mark_attendance(employee_id):
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO attendance (employee_id, timestamp)
        VALUES (?, ?)
    """, (employee_id, datetime.now()))
    conn.commit()
    conn.close()
