from Flask import Flask, request, jsonify, render_template
import sqlite3
from datetime import datetime
import random

app = Flask(__SpellingBee__)
DB_name = users.db