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
            package = []
            for value in result:
                jap, eng = value
                package.append(dict(japanese=jap, english=eng))
            
            print(package)
        return package
    
    except sqlite3.Error as e:
        print('Problem retrieving data:', e)
        raise

def record_score(db_path, dictionary):
    try:
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        sql = """INSERT INTO test_history(uid, grade, chapter, english, user_input, correct, total)
    VALUES(?,?,?,?,?,?,?)"""
        
        for entry in dictionary:
            cur.execute(sql, (entry['uid'], 
                              entry['grade'], 
                              entry['chapter'], 
                              entry['english'], 
                              entry['user_input'],
                              entry['correct'],
                              entry['total']))
            
    except sqlite3.Error as e:
        print('error:', e)
        raise

