from flask import Flask, render_template, request, url_for, flash, redirect
import sqlite3
from werkzeug.exceptions import abort
import yaftp
import os
from time import sleep

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_yaftp_connection(yaftp_id):
    conn = get_db_connection()
    yaftp_connection = conn.execute('SELECT * FROM auth WHERE id = ?', (yaftp_id,)).fetchone()
    conn.close()
    if yaftp_connection is None:
        abort(404)
    return yaftp_connection

def all_filenames(datadir: str):
    f = []
    for (_, _, filenames) in os.walk(datadir):
        f.extend(filenames)
        break
    return f

def get_folders_and_files(dir_result):
    folders = []
    files = []
    for entry in dir_result:
        if entry.endswith('/'):
            folders.append(entry)
        else:
            files.append(entry)
    return (folders, files)

app = Flask(__name__)
# ALERT: Modify this.
app.config['SECRET_KEY'] = 'fair is foul, and foul is fair'

@app.route('/')
def index():
    conn = get_db_connection()
    auths = conn.execute('SELECT * FROM auth').fetchall()
    conn.close()
    return render_template('index.html', auths = auths)

connections = {}

@app.route('/<int:yaftp_id>', methods=('GET', 'POST'))
def yaftp_connection(yaftp_id):
    yaftp_conn = get_yaftp_connection(yaftp_id)

    username = yaftp_conn['username']
    passwd = yaftp_conn['passwd']
    datadir = yaftp_conn['datadir']
    host = yaftp_conn['host']
    port = yaftp_conn['port']
    local_files = all_filenames(datadir)

    if username not in connections:
        connections[username] = "/"
        
    c = yaftp.YAFTP(
            address=(host, int(port)),
            user=username,
            passwd=passwd
        )

    c.login()
    c.cd(connections[username])

    if request.method == 'POST':
        if "dir" in request.form:
            dir_name = request.form["dir"]
            c.cd(dir_name)
            connections[username] = c.pwd()
            flash(f'cd to {connections[username]}!')
        if "file" in request.form:
            file_name = request.form["file"]
            savepath=os.path.join(datadir, file_name)
            c.get(name=file_name, savepath=savepath)
            flash(f'saved {file_name} in {savepath}')
        if "local_file" in request.form:
            local_file_name = request.form["local_file"]
            filepath = os.path.join(datadir, local_file_name)
            c.send(filepath=filepath, name=local_file_name)
            path = os.path.join(c.pwd(), local_file_name)
            flash(f'sent {local_file_name} to {path}')
        if "delete" in request.form:
            deleted_filename = request.form['delete']
            c.delete(deleted_filename)
            flash(f'deleted {deleted_filename}')

    folders, files = get_folders_and_files(c.dir())
    if connections[username] != "/":
        folders.append("..")

    c.quit()

    t = render_template(
        'yaftp.html', 
        yaftp_conn=yaftp_conn,
        files=files,
        folders=folders,
        local_files=local_files
        )
    return t

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        host = request.form['host']
        port = request.form['port']
        username = request.form['username']
        password = request.form['password']
        datadir = request.form['datadir']

        if not host:
            flash('host is required!')
        if not port:
            flash('port is required!')
        if not username:
            flash('username is required!')
        if not password:
            flash('password is required!')
        if not datadir:
            flash('datadir is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO auth (username, passwd, datadir, host, port) VALUES (?, ?, ?, ?, ?)',
                         (username, password, datadir, host, port))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')