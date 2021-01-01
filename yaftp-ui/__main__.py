from flask import Flask, render_template
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

@app.route('/')
def index():
    conn = get_db_connection()
    auths = conn.execute('SELECT * FROM auth').fetchall()
    conn.close()
    return render_template('index.html', auths = auths)

@app.route('/<int:yaftp_id>')
def yaftp_connection(yaftp_id):
    yaftp_conn = get_yaftp_connection(yaftp_id)
    return render_template('yaftp.html', yaftp_conn=yaftp_conn, files=['file1', 'dir1/'])
