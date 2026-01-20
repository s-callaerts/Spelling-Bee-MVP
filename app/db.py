#import psycopg2-binary
import os
import sqlite3
import json

BASE_DIR = os.getcwd()
WORDS_PATH = os.path.join(BASE_DIR, 'app', 'data', 'words.json')
SQL_SCHEMA_FILES = ["app/schemas/sql_schemas/users.sql"]

def db_setup(db_path):
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    for path in SQL_SCHEMA_FILES:
        with open(path) as f:
            cur.executescript(f.read())

    with open(WORDS_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

        grade = data['grade']
        chapter = data['chapter']
        words = data['words']

        for word in words:
            cur.execute(
                'INSERT INTO words(grade, chapter, japanese, english) VALUES (?, ?, ?, ?)',
                (grade, chapter, word['jap'], word['eng'])
                )
    
    con.commit()
    con.close()

def get_db():
    con = sqlite3.connect('spellingbee.db')
    con.row_factory = sqlite3.Row
    return con

#Register and Login functions
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

#Test functions
def retrieve_words(db_path, grade, chapter):
    try:
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        sql = "SELECT japanese, english FROM words WHERE grade = ? AND chapter = ?"

        cur.execute(sql, (grade, chapter))
        result = cur.fetchall()
        print(result)
        con.close()

        if result:
            test_content = []
            for value in result:
                jap, eng = value
                test_content.append(dict(japanese=jap, english=eng))
            
            print(test_content)
        return test_content
    
    except sqlite3.Error as e:
        print('Problem retrieving data:', e)
        raise

def add_attempt(db_path, values: tuple):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    sql = """INSERT INTO test_history(uid, timestamp, last_activity, grade, chapter, score, status) VALUES (?, ?, ?, ?, ?, ?, ?);"""

    try:
        cur.execute(sql, values)
    except sqlite3.Error as e:
        print("Error adding attempt:", e)
        raise
    
    uid, timestamp, *rest = values

    try:
        sql2 = """SELECT attempt_id FROM test_history WHERE uid = ? AND timestamp = ?;"""
        cur.execute(sql2, (uid, timestamp))
        attempt_id = cur.fetchone()[0]
        con.commit()
        con.close()

        return attempt_id
    except sqlite3.Error as e:
        print("Error retrieving id:", e)
        raise

#keep track of score and status
def update_attempt(db_path, attempt_id, last_activity, score, status):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    sql = """UPDATE test_history
    SET last_activity = ?, score = ?, status = ?
    WHERE attempt_id = ?;"""
        
    try:
        cur.execute(sql, (last_activity, score, status, attempt_id))
        con.commit()
        con.close()
        return True
    
    except sqlite3.Error as e:
        print("Error updating attempt:", e)
        raise

def close_attempt(db_path, values):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    sql = """UPDATE test_history
    SET score = ?, status = ?
    WHERE attempt_id = ?;"""
        
    try:
        cur.execute(sql, values)
        con.commit()
        con.close()
        return True
        
    except sqlite3.Error as e:
        print('error:', e)
        raise

def update_content(db_path, entry):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    sql = """INSERT INTO test_content(attempt_id, japanese, english, input, is_correct)
    VALUES(?,?,?,?,?)"""
        
    try:
        cur.execute(sql, entry)
        con.commit()
        con.close()
        return True
        
    except sqlite3.Error as e:
        print('error:', e)
        raise



