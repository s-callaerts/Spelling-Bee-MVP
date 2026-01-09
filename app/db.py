#import psycopg2-binary
#import os
import sqlite3

SQL_SCHEMA_FILES = ["app/schemas/sql_schemas/users.sql"]

def db_setup():
    """con = psycopg2.connect(
    dbname = "spellingbee",
    user = os.getenv("DB_PASS),
    password = os.getenv("DB_PASS")
    host = os.getenv("DB_HOST")"""
    con = sqlite3.connect('spellingbee.db')
    cur = con.cursor()

    for path in SQL_SCHEMA_FILES:
        with open(path) as f:
            cur.executescript(f.read())
    
    con.commit()
    con.close()

def get_db():
    con = sqlite3.connect('spellingbee.db')
    con.row_factory = sqlite3.Row
    return con

def add_user(values):
    try:
        con = sqlite3.connect("spellingbee.db")
        cur = con.cursor()
        sql = """INSERT INTO users(uid, username, email, password, grade, isTeacher)
        VALUES (?,?,?,?,?,?)"""

        cur.execute(sql, values)
        con.commit()
        con.close()

        print('Succesfully added user to db')
        
        return True
    except sqlite3.Error as e:
        print("Error adding user:", e)
        return False
    finally:
        con.close()
    
def login_user(login_username):
    try:
        con = sqlite3.connect("spellingbee.db")
        cur = con.cursor()
        sql = "SELECT uid, password, isTeacher FROM users WHERE username = ?"

        cur.execute(sql, (login_username,))
        result = cur.fetchone()
        con.close()
        if result:
            uid, stored_password, isTeacher = result
            return (uid, stored_password, isTeacher)
        else:
            return None
    except sqlite3.Error as e:
        print("Error retrieving user:", e)
        raise
