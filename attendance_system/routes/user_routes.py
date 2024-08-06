from flask import Blueprint, render_template, request, redirect, url_for
from attendance_system.models import get_db_connection

user_bp = Blueprint('user', __name__)

@user_bp.route('/register/', methods=['GET', 'POST'], endpoint='register')
def register():
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']

            con = get_db_connection()
            cur = con.cursor()
            cur.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
            con.commit()
            msg = "User successfully added"
        except:
            con.rollback()
            msg = "Error occurred in insert operation"
        finally:
            con.close()
            return redirect(url_for('user.list_users', msg=msg))
    return render_template('add_user.html')

@user_bp.route('/', endpoint='list_users')
def list_users():
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    msg = request.args.get('msg')  # Retrieve the success message
    return render_template('all_users.html', rows=rows, msg=msg)

@user_bp.route('/delete/<int:user_id>/', endpoint='delete_user')
def delete_user(user_id):
    try:
        con = get_db_connection()
        cur = con.cursor()
        cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
        con.commit()
        msg = "User successfully deleted"
    except:
        con.rollback()
        msg = "Error occurred in delete operation"
    finally:
        con.close()
        return redirect(url_for('user.list_users', msg=msg))

@user_bp.route('/edit/<int:user_id>/', methods=['GET', 'POST'], endpoint='edit_user')
def edit_user(user_id):
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']

            con = get_db_connection()
            cur = con.cursor()
            cur.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", (name, email, user_id))
            con.commit()
            msg = "User successfully updated"
        except:
            con.rollback()
            msg = "Error occurred in update operation"
        finally:
            con.close()
            return redirect(url_for('user.list_users', msg=msg))
    else:
        con = get_db_connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cur.fetchone()
        return render_template('edit_user.html', row=row)
