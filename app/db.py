#import psycopg2-binary
import os
import sqlite3
import json

BASE_DIR = os.getcwd()
WORDS_PATH = os.path.join(BASE_DIR, 'app', 'data', 'words.json')
SQL_SCHEMA_FILES = ["app/schemas/sql_schemas/users.sql"]
db_path = os.getenv('DATABASE', 'spellingbee.db')

def db_setup():
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
    con = sqlite3.connect(db_path)
    return con

#Register and Login functions
def add_user(values):
    try:
        con = get_db()
        cur = con.cursor()
        sql = """INSERT INTO users(uid, username, email, password, grade, isTeacher)
        VALUES (?,?,?,?,?,?)"""

        cur.execute(sql, values)
        con.commit()

        print('Succesfully added user to db')
        
        return True
    except sqlite3.Error as e:
        print("Error adding user:", e)
        return False
    finally:
        con.close()
    
def login_user(login_username):
    try:
        con = get_db()
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
def retrieve_words(grade, chapter):
    """Get test content from db"""
    try:
        con = get_db()
        cur = con.cursor()
        sql = "SELECT word_id FROM words WHERE grade = ? AND chapter = ?"

        cur.execute(sql, (grade, chapter))
        result = cur.fetchall()
        print(result)
        con.close()

        if result:
            print(result)
            return result
    
    except sqlite3.Error as e:
        print('Problem retrieving data:', e)
        raise

def add_attempt(values: tuple):
    #Add the test_attempt instance to db
    con = get_db()
    cur = con.cursor()
    sql = """INSERT INTO test_history(uid, started_at, last_activity, grade, chapter, score, status) VALUES (?, ?, ?, ?, ?, ?, ?);"""

    try:
        cur.execute(sql, values)
    except sqlite3.Error as e:
        print("Error adding attempt:", e)
        raise
    
    uid, timestamp, *rest = values

    try:
    #return test_id to store in session for rehydrating
        sql2 = """SELECT test_id FROM test_history WHERE uid = ? AND timestamp = ?;"""
        cur.execute(sql2, (uid, timestamp))
        attempt_id = cur.fetchone()[0]
        con.commit()
        con.close()

        return attempt_id
    except sqlite3.Error as e:
        print("Error retrieving id:", e)
        raise

def update_test(test_id, last_activity, score):
    #keep track of score and status
    con = get_db()
    cur = con.cursor()
    sql = """UPDATE test_history
    SET last_activity = ?, score = ?
    WHERE test_id = ?;"""
        
    try:
        cur.execute(sql, (last_activity, score, test_id))
        con.commit()
        con.close()
        return True
    
    except sqlite3.Error as e:
        print("Error updating attempt:", e)
        raise

def update_content(entry):
    """update test content with input and is_correct, set answered to true(1) to prevent it from being included in rehydration"""
    # should be used in tandem with update_test
    con = get_db()
    cur = con.cursor()
    sql = """UPDATE test_content SET input = ?, is_correct = ?, answered = ? WHERE test_id = ? AND question_id = ?"""
        
    try:
        cur.execute(sql, entry)
        con.commit()
        con.close()
        return True
        
    except sqlite3.Error as e:
        print('error:', e)
        raise

def revive_attempt(test_id):
    con = get_db()
    cur = con.cursor()

    def get_question(test_id):
        sql = """SELECT test_content.question_id, words.japanese, words.english FROM test_content 
        JOIN words ON test_content.word_id = words.word_id 
        WHERE test_content.test_id = :test_id AND test_content.answered = 0;"""

        try:
            cur.execute(sql, {'test_id': test_id})
            result = cur.fetchall()
            return result
        except sqlite3.Error as e:
            print('Error retrieving questions:', e)
            raise
    
    def get_attempt_values(test_id):
        sql = """SELECT uid, started_at, last_activity, grade, chapter, score, status 
        FROM test_history WHERE test_id = ?;"""

        try:
            cur.execute(sql, (test_id,))
            result = cur.fetchone()
            return result
        except sqlite3.Error as e:
            print('Error retrieving attempt values:', e)
            raise
    
    con.close()
    questions = get_question(test_id)
    attempt_values = get_attempt_values(test_id)
    return (questions, attempt_values)
    

def close_attempt(values):
    con = get_db()
    cur = con.cursor()
    sql = """UPDATE test_history
    SET last_activity = ?, score = ?, status = ?
    WHERE test_id = ?;"""
        
    try:
        cur.execute(sql, values)
        con.commit()
        con.close()
        return True
        
    except sqlite3.Error as e:
        print('error:', e)
        raise
