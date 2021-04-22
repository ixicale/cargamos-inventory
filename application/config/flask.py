"""Flask settings to develop"""

class Config:
    SECRET_KEY = 'my-special-key-to-deploy'
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    DRIVER = "postgresql+psycopg2"
    USER = "postgres"
    PASS = "postgres"
    HOST = "localhost:5432"
    DATABASE = "cargamos"
    SQLALCHEMY_DATABASE_URI = f'{DRIVER}://{USER}:{PASS}@{HOST}/{DATABASE}'

    SQLALCHEMY_TRACK_MODIFICATIONS = True