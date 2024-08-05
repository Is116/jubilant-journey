from flask import render_template, jsonify
from app import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/attendance', methods=['GET'])
def attendance():
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM attendance")
    records = cursor.fetchall()
    conn.close()
    return jsonify(records)

