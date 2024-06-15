import sqlite3

#TODO: Connect to db
def connect_to_db():
    conn = sqlite3.connect('users.db')
    return conn

#TODO: Create user function
def create_tables():
    conn = connect_to_db()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS keys
                 (username TEXT UNIQUE, public_key INTEGER, n INTEGER)''')
    conn.commit()
    conn.close()

def add_user(username, password):
    conn = connect_to_db()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
    except sqlite3.IntegrityError:
        print("Username already exists.")
    conn.close()

def get_user(username, password):
    conn = connect_to_db()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    return user

def add_keys(username, public_key, n):
    conn = connect_to_db()
    c = conn.cursor()
    c.execute("INSERT INTO keys (username, public_key, n) VALUES (?, ?, ?)", (username, public_key, n))
    conn.commit()
    conn.close()

def get_keys(username):
    conn = connect_to_db()
    c = conn.cursor()
    c.execute("SELECT * FROM keys WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()
    return user

def delete_keys(username):
    conn = connect_to_db()
    c = conn.cursor()
    c.execute("DELETE FROM keys WHERE username=?", (username,))
    conn.commit()
    conn.close()

create_tables()
