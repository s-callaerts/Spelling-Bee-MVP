from Flask import Flask, request, jsonify, render_template
import sqlite3
from datetime import datetime
import random
import hashlib

app = Flask(__SpellingBee__)
DB_name = "users.db"

import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///local.db")
appconfig("SQLALCHEMY_DATABASE_URL") = DATABASE_URL
