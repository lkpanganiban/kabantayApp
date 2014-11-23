from flask import Flask
from config import config
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.bootstrap import Bootstrap
from flask.ext.pagedown import PageDown

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

db = SQLAlchemy()

bootstrap = Bootstrap()

pagedown=PageDown()

def build_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    bootstrap.init_app(app)

    from infraApp.models import db
    db.init_app(app)

    from .infra import infra as infra_blueprint
    app.register_blueprint(infra_blueprint)

    login_manager.init_app(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    pagedown.init_app(app)

    return app
