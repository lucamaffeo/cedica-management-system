from os import environ
from re import DEBUG

class Config(object):
    """ Base configuration. """
    SECRET_KEY = environ.get("SECRET_KEY", "my_precious")
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

class ProductionConfig(Config):
    """ Production specific configuration. """
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL")
    DEBUG = False

class DevelopmentConfig(Config):
    """ Development environment configuration """
    DB_USER = "postgres"
    DB_PASS = "postgres"
    DB_HOST = "localhost"
    DB_PORT = "5432"
    DB_NAME = "grupo10"
    SQLALCHEMY_DATABASE_URI = (
            f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    DEBUG = True

class TestingConfig(Config):
    TESTING = True


config = {
        "development": DevelopmentConfig,
        "testing": TestingConfig,
        "production": ProductionConfig,
        }
