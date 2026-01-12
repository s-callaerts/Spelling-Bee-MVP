--CREATE DATABASE IF NOT EXISTS spellingbee;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS words;
--drop table only for testing, remove on deployment

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
    japanese TEXT NOT NULL,
    english TEXT NOT NULL
);