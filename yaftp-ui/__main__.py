from flask import Flask, render_template, request, url_for, flash, redirect
import sqlite3
from werkzeug.exceptions import abort
import yaftp

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_yaftp_connection(yaftp_id):
    conn = get_db_connection()
    print(yaftp_id)
    yaftp_connection = conn.execute('SELECT * FROM auth WHERE id = ?', (yaftp_id,)).fetchone()
    conn.close()
    if yaftp_connection is None:
        abort(404)
    return yaftp_connection
    
app = Flask(__name__)
# ALERT: Modify this.
app.config['SECRET_KEY'] = 'fair is foul, and foul is fair'

@app.route('/')
def index():
    conn = get_db_connection()
    auths = conn.execute('SELECT * FROM auth').fetchall()
    conn.close()
    return render_template('index.html', auths = auths)

@app.route('/<int:yaftp_id>', methods=('GET', 'POST'))
def yaftp_connection(yaftp_id):
    if request.method == 'POST':
        flash('POSTED!')
    yaftp_conn = get_yaftp_connection(yaftp_id)
    return render_template(
        'yaftp.html', 
        yaftp_conn=yaftp_conn,
        files=['file1', 'dir1/'],
        local_files=['local1', 'local2']
        )


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        host = request.form['host']
        port = request.form['port']
        username = request.form['username']
        password = request.form['password']
        datadir = request.form['datadir']

        if None in (host, port, username, password, datadir):
            flash('Something is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO auth (username, passwd, datadir, host, port) VALUES (?, ?, ?, ?, ?)',
                         (username, password, datadir, host, port))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')