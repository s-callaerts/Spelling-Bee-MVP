#from Flask import Flask, request, jsonify, render_template
import sqlite3
import schemas.schema as schema
import models.user as model

#app = Flask(__SpellingBee__)
#DB_name = "users.db"

import os

#DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///local.db")
#appconfig("SQLALCHEMY_DATABASE_URL") = DATABASE_URL

if __name__ == '__main__':
    payload = {'name': '服部太郎',
               'email': 'email@email.co.jp',
               'password': 'ok4yokay!',
               'grade': '6'}
    
    try:
        data = schema.RegistrationSchema.validate(payload)
        print(data)
        model.generate_user(data)
    except ValueError or TypeError:
        raise
