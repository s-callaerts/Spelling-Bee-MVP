from flask import Flask 
import os
from .db import db_setup, retrieve_words
#import psycopg2

def create_app(test_config=None):
    app = Flask(__name__,
                instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path,'spellingbee.sqlite'),
    )

    """con = psycopg2.connect(
    DB_NAME = "os.getenv(DB_NAME)",
    DB_USER = os.getenv("DB_USER),
    DB_PASS = os.getenv("DB_PASS")
    DB_HOST = os.getenv("DB_HOST")"""

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .routes import auth, main
    app.register_blueprint(auth.authorization_bp)
    app.register_blueprint(main.main_bp)

    db_setup(app.config['DATABASE'])
    retrieve_words(app.config['DATABASE'], 3, 1)

    return app