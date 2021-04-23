"""Flask listener"""

# Flask
from flask import Flask

# Application
from application import setup, db, api, config


def create_app(env = None):
    app = Flask(__name__)
    if env is None:
        app.config.from_object(setup['production'])
    else:
        app.config.from_object(env)

    with app.app_context():
        db.init_app(app)
        db.create_all()

    api.init_app(app)  # loads resources
    return app


env = setup["development"]
if config("PRODUCTION", default=False):
    env = setup["production"]

app = create_app(env)
