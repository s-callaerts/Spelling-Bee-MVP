from flask import Flask 
import os

def create_app(test_config=None):
    app = Flask(__name__,
                instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path,'spellingbee.sqlite'),
    )

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

    return app