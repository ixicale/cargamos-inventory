"""Flask listener"""

# Flask
from flask import Flask

# Aplicación
from application import setup, db, api
from decouple import config as config_decouple


def create_app(env):
    app = Flask(__name__)
    app.config.from_object(env)

    with app.app_context():
        db.init_app(app)
        db.create_all()
    api.init_app(app)  # loads resources

    return app


env = setup["development"]
if config_decouple("PRODUCTION", default=False):
    env = setup["production"]

app = create_app(env)
app.run(debug=True, host="0.0.0.0")
