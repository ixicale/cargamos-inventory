"""Flask listener"""

# Flask
from flask import Flask

# Aplicación
from application import setup, db, api
from decouple import config as config_decouple


def create_app(env = None):
    app = Flask(__name__)
    if env is None:
        app.config.from_object(setup['production'])
    else:
        app.config.from_object(env)

    with app.app_context():
        db.init_app(app)
        db.create_all()

    return app


env = setup["development"]
if config_decouple("PRODUCTION", default=False):
    env = setup["production"]

if __name__ == "__main__":
    app = create_app(env)
    api.init_app(app)  # loads resources
    app.run(debug=True, host="0.0.0.0")
