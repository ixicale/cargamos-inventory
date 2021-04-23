"""Flask settings to develop"""
from decouple import config  # to use heroku server


class Config:
    SECRET_KEY = "my-special-key-to-deploy"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    DRIVER = "postgresql+psycopg2"
    USER = "postgres"
    PASS = "postgres"
    HOST = "localhost:5432"
    DATABASE = "cargamos"
    SQLALCHEMY_DATABASE_URI = f"{DRIVER}://{USER}:{PASS}@{HOST}/{DATABASE}"


class DevConfig(Config):
    DEBUG = True


class ProConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = config("DATABASE_URL", default="localhost")


setup = {
    "development": DevConfig,
    "production": ProConfig,
}