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
    grade INTEGER NOT NULL,
    chapter INTEGER NOT NULL,
    japanese TEXT NOT NULL UNIQUE,
    english TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS test_history(
    attempt_id INTEGER PRIMARY KEY AUTOINCREMENT,
    uid TEXT NOT NULL REFERENCES users(uid),
    timestamp VARCHAR(60) NOT NULL,
    grade INTEGER NOT NULL,
    chapter INTEGER NOT NULL,
    score INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS test_content(
    attempt_id INTEGER REFERENCES test_history(attempt_id),
    japanese TEXT NOT NULL,
    english TEXT NOT NULL,
    input TEXT NOT NULL,
    is_correct INTEGER NOT NULL,
    status TEXT NOT NULL,
);