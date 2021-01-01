import sqlite3

connection = sqlite3.connect('database.db')

with open("schema.sql") as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO auth (username, passwd, datadir, host, port) VALUES (?, ?, ?, ?, ?)",
            ("OFEY", "404", "/home/ofey/Downloads", "127.0.0.1", "2121"))

cur.execute("INSERT INTO auth (username, passwd, datadir, host, port) VALUES (?, ?, ?, ?, ?)",
            ("ANONYMOUS", "", "/home/ofey/Downloads", "127.0.0.1", "2121"))
connection.commit()

connection.close()