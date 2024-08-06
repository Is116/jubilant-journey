from flask import Blueprint, render_template, request, redirect, url_for
from attendance_system.models import get_db_connection

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route('/<int:user_id>/', endpoint='view_attendance')
def view_attendance(user_id):
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM attendance WHERE user_id = ?", (user_id,))
    rows = cur.fetchall()
    return render_template('attendance.html', rows=rows, user_id=user_id)

@attendance_bp.route('/add/<int:user_id>/', methods=['GET', 'POST'], endpoint='add_attendance')
def add_attendance(user_id):
    if request.method == 'POST':
        try:
            date = request.form['date']
            time = request.form['time']

            con = get_db_connection()
            cur = con.cursor()
            cur.execute("INSERT INTO attendance (user_id, date, time) VALUES (?, ?, ?)", (user_id, date, time))
            con.commit()
            msg = "Attendance record successfully added"
        except:
            con.rollback()
            msg = "Error occurred in insert operation"
        finally:
            con.close()
            return redirect(url_for('attendance.view_attendance', user_id=user_id))
    return render_template('add_attendance.html', user_id=user_id)

@attendance_bp.route('/edit/<int:attendance_id>/<int:user_id>/', methods=['GET', 'POST'], endpoint='edit_attendance')
def edit_attendance(attendance_id, user_id):
    if request.method == 'POST':
        try:
            date = request.form['date']
            time = request.form['time']

            con = get_db_connection()
            cur = con.cursor()
            cur.execute("UPDATE attendance SET date = ?, time = ? WHERE id = ?", (date, time, attendance_id))
            con.commit()
            msg = "Attendance record successfully updated"
        except:
            con.rollback()
            msg = "Error occurred in update operation"
        finally:
            con.close()
            return redirect(url_for('attendance.view_attendance', user_id=user_id))
    else:
        con = get_db_connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM attendance WHERE id = ?", (attendance_id,))
        row = cur.fetchone()
        return render_template('edit_attendance.html', row=row, user_id=user_id)

@attendance_bp.route('/delete/<int:attendance_id>/<int:user_id>/', endpoint='delete_attendance')
def delete_attendance(attendance_id, user_id):
    try:
        con = get_db_connection()
        cur = con.cursor()
        cur.execute("DELETE FROM attendance WHERE id = ?", (attendance_id,))
        con.commit()
        msg = "Attendance record successfully deleted"
    except:
        con.rollback()
        msg = "Error occurred in delete operation"
    finally:
        con.close()
        return redirect(url_for('attendance.view_attendance', user_id=user_id, msg=msg))
