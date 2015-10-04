# encoding=utf-8

from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, render_template
from config import config


bootstrap = Bootstrap()
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app


def app_log(str):
    try:
        f = open("C:\\yz_log.txt", "a", newline="\n")
        f.write(str)
        f.write("\n")
        f.close()
    except:
        f.close()