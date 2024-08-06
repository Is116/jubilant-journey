from flask import Blueprint, render_template, request, redirect, url_for
from attendance_system.models import get_db_connection
from attendance_system.fingerprint_utils import get_fingerprint
import sqlite3

fingerprint_bp = Blueprint('fingerprint', __name__)

@fingerprint_bp.route('/<int:user_id>', methods=['GET'])
def view_fingerprint(user_id):
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("SELECT fingerprint FROM users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    if row and row['fingerprint']:
        msg = "Fingerprint data is present."
    else:
        msg = "No fingerprint data available."
    return render_template('view_fingerprint.html', fingerprint=row['fingerprint'] if row else None, user_id=user_id, msg=msg)

@fingerprint_bp.route('/add/<int:user_id>', methods=['GET', 'POST'])
def add_fingerprint(user_id):
    con = None
    if request.method == 'POST':
        try:
            fingerprint = get_fingerprint()

            if fingerprint is None:
                msg = "Fingerprint capture failed. Please try again."
                return redirect(url_for('fingerprint.add_fingerprint', user_id=user_id, msg=msg))

            fingerprint_blob = sqlite3.Binary(bytearray(fingerprint))
            print('Storing fingerprint:', fingerprint_blob)

            con = get_db_connection()
            cur = con.cursor()
            cur.execute("UPDATE users SET fingerprint = ? WHERE id = ?", (fingerprint_blob, user_id))
            con.commit()
            msg = "Fingerprint successfully added"
        except Exception as e:
            if con:
                con.rollback()
            msg = "Error occurred in adding fingerprint: " + str(e)
        finally:
            if con:
                con.close()
            return redirect(url_for('fingerprint.view_fingerprint', user_id=user_id, msg=msg))
    return render_template('add_fingerprint.html', user_id=user_id)

@fingerprint_bp.route('/update/<int:user_id>', methods=['GET', 'POST'])
def update_fingerprint(user_id):
    con = None
    if request.method == 'POST':
        try:
            fingerprint = get_fingerprint()

            if fingerprint is None:
                msg = "Fingerprint capture failed. Please try again."
                return redirect(url_for('fingerprint.update_fingerprint', user_id=user_id, msg=msg))

            fingerprint_blob = sqlite3.Binary(bytearray(fingerprint))
            print('Updating fingerprint:', fingerprint_blob)

            con = get_db_connection()
            cur = con.cursor()
            cur.execute("UPDATE users SET fingerprint = ? WHERE id = ?", (fingerprint_blob, user_id))
            con.commit()
            msg = "Fingerprint successfully updated"
        except Exception as e:
            if con:
                con.rollback()
            msg = "Error occurred in updating fingerprint: " + str(e)
        finally:
            if con:
                con.close()
            return redirect(url_for('fingerprint.view_fingerprint', user_id=user_id, msg=msg))
    return render_template('update_fingerprint.html', user_id=user_id)

@fingerprint_bp.route('/delete/<int:user_id>', methods=['POST'])
def delete_fingerprint(user_id):
    con = None
    try:
        con = get_db_connection()
        cur = con.cursor()
        cur.execute("UPDATE users SET fingerprint = NULL WHERE id = ?", (user_id,))
        con.commit()
        msg = "Fingerprint successfully deleted"
    except Exception as e:
        if con:
            con.rollback()
        msg = "Error occurred in deleting fingerprint: " + str(e)
    finally:
        if con:
            con.close()
        return redirect(url_for('fingerprint.view_fingerprint', user_id=user_id, msg=msg))
