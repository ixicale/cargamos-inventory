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
    SQLALCHEMY_DATABASE_URI = f"postgresql://wsttmnvroiswzi:005b8522d48e28689d73c4e8191858ace466f8d0df0d5a2e6065a21e368a2f55@ec2-23-22-191-232.compute-1.amazonaws.com:5432/dbbsn43ir085l7"


setup = {
    "development": DevConfig,
    "production": ProConfig,
}