#import psycopg2-binary
import os
import sqlite3
from flask import current_app

BASE_DIR = os.getcwd()
WORDS_PATH = os.path.join(BASE_DIR, 'app', 'data', 'words.json')
SQL_SCHEMA_FILES = ["app/schemas/sql_schemas/users.sql"]

def get_db():
    con = sqlite3.connect(current_app.config['DATABASE'])
    return con

def create_classroom(teacher_id):
    #add an entry into the classroom and run tables
    con = get_db()
    cur = con.cursor()
    create_class_sql = """INSERT INTO classroom(class_name, teacher_id) VALUES ?, ?;
                          SELECT class_id FROM classroom WHERE teacher_id = ?;"""
    create_run_sql = "INSERT INTO classroom_run(class_id) VALUES ?;"

def retrieve_classroom(teacher_id):
    #retrieve class_id, cr_id, students from db
    pass

def set_classroom_status(status_input):
    #change the classroom status to input 
    pass

def add_student():
    #add a student into a classroom group
    pass

def remove_student():
    #remove a student from the classroom group
    pass

def get_class_test_score():
    #retrieve scores from classroom students based on search criteria
    pass
