import functools

import psycopg2

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password1']
        password2 = request.form['password2']
        address = request.form['address']
        name = request.form['name']
        credit_card_num = request.form['card_number']
        

        conn = psycopg2.connect(database = "railways", user = "postgres", password = "xx", host = "127.0.0.1", port = "5432")
        cur = conn.cursor()

        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not password == password2:
            error = 'Password does not match.'
        else:
            cur.execute("""select * from Booking_agent where username='""" + username + """';""")
            if(cur.fetchone() is not None):
                error = 'User {} is already registered.'.format(username)

        if error is None:
            cur.execute("""INSERT INTO Booking_agent (username, password, name, creditcard_no, address) VALUES ('""" + username + """','""" + password + """','""" + name + """','""" + credit_card_num + """','""" + address + """');""")
            conn.commit()
            conn.close()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = psycopg2.connect(database = "railways", user = "postgres", password = "xx", host = "127.0.0.1", port = "5432")
        cur = conn.cursor()
        error = None
        cur.execute("""select * from Booking_agent where username='""" + username + """';""")
        user = cur.fetchone()
        conn.commit()
        conn.close()

        if user is None:
            error = 'Incorrect username.'
        elif password is None:
            error = 'Password is required.'
        elif not user[1] == password:
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['username'] = user[0]
            session['admin'] = None
            conn = psycopg2.connect(database = "railways", user = "postgres", password = "xx", host = "127.0.0.1", port = "5432")
            cur = conn.cursor()
            cur.execute("""select * from admins where username='""" + username + """';""")
            if cur.fetchone() is not None:
                session['admin'] = True
            conn.commit()
            conn.close()
            return redirect(url_for('user.index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    username = session.get('username')

    if username is None:
        g.user = None
    else:
        conn = psycopg2.connect(database = "railways", user = "postgres", password = "xx", host = "127.0.0.1", port = "5432")
        cur = conn.cursor()
        cur.execute("""select * from Booking_agent where username='""" + username + """';""")
        row = cur.fetchone()
        g.user = {"name": row[2]}

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view