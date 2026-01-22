--CREATE DATABASE IF NOT EXISTS spellingbee;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS words;
DROP TABLE IF EXISTS test_history;
DROP TABLE IF EXISTS test_content;
--drop table only for testing, remove on deployment

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
    input TEXT NOT NULL,
    is_correct INTEGER NOT NULL,
    answered INTEGER NOT NULL
    --answered BOOLEAN NOT NULL
);