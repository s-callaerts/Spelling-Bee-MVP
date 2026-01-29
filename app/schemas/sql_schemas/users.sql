--CREATE DATABASE IF NOT EXISTS spellingbee;
--drop table only for testing, remove on deployment
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS words;
DROP TABLE IF EXISTS test_history;
DROP TABLE IF EXISTS test_content;
DROP TABLE IF EXISTS classroom;
DROP TABLE IF EXISTS classroom_run;
DROP TABLE IF EXISTS classroom_run_teacher;
DROP TABLE IF EXISTS classroom_run_students;


PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users(
    uid TEXT PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    grade INTEGER NOT NULL,
    --isTeacher BOOLEAN NOT NULL,
    isTeacher INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS words(
    word_id INTEGER PRIMARY KEY AUTOINCREMENT,
    grade INTEGER NOT NULL,
    chapter INTEGER NOT NULL,
    japanese TEXT NOT NULL UNIQUE,
    english TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS test_history(
    test_id INTEGER PRIMARY KEY AUTOINCREMENT,
    uid TEXT NOT NULL REFERENCES users(uid),
    started_at VARCHAR(60) NOT NULL,
    last_activity VARCHAR(60) NOT NULL,
    grade INTEGER NOT NULL,
    chapter INTEGER NOT NULL,
    score INTEGER NOT NULL,
    status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS test_content(
    question_id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_id INTEGER REFERENCES test_history(test_id),
    word_id INTEGER REFERENCES words(word_id),
    input TEXT,
    is_correct INTEGER,
    answered INTEGER,
    is_active INTEGER DEFAULT 0
    --answered BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS classroom(
    class_id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_name TEXT NOT NULL,
    teacher_id TEXT NOT NULL REFERENCES users(uid)
);

CREATE TABLE IF NOT EXISTS classroom_run(
    run_id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_id INTEGER NOT NULL REFERENCES classroom(class_id),
    started_at VARCHAR(60) NOT NULL,
    status TEXT NOT NULL
);
CREATE INDEX idx_classroom_run_status ON classroom_run(class_id, status);

CREATE TABLE IF NOT EXISTS classroom_run_teacher(
    cr_id TEXT NOT NULL REFERENCES classroom_run(run_id),
    teacher_id TEXT NOT NUL REFERENCES users(uid),
    PRIMARY KEY (cr_id, teacher_id)
);
CREATE INDEX idx_crt_teacher_run ON classroom_run_teacher(cr_id, teacher_id);

CREATE TABLE IF NOT EXISTS classroom_run_students(
    cr_id TEXT NOT NULL REFERENCES classroom_run(run_id),
    student_id TEXT NOT NULL REFERENCES users(uid),
    PRIMARY KEY (cr_id, student_id)
);
CREATE INDEX idx_crs_student_run ON classroom_run_students(cr_id, student_id);