from os import environ

class Config(object):
    """ Base configuration. """
    SECRET_KEY = environ.get("SECRET_KEY", "my_precious")
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

class ProductionConfig(Config):
    MINIO_SERVER = environ.get("MINIO_SERVER")
    MINIO_ACCESS_KEY = environ.get("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY = environ.get("MINIO_SECRET_KEY")
    MINIO_SECURE = environ.get("MINIO_SECURE", True)

    """ Production specific configuration. """
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL")

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 10,
        "pool_recycle": 60,
        "pool_pre_ping": True,
    }

    DB_NAME = environ.get("DATABASE_URL")
    DB_USER = environ.get("DATABASE_USERNAME")
    DB_PASS = environ.get("DATABASE_PASSWORD")
    DB_HOST = environ.get("DATABASE_HOST")
    DB_PORT = environ.get("DATABASE_PORT")
    DEBUG = False

class DevelopmentConfig(Config):
    """ Development environment specific configuration """
    MINIO_SERVER = "minio.proyecto2024.linti.unlp.edu.ar"
    MINIO_ACCESS_KEY = "1MPYEdD45EDw2smfmRLh"
    MINIO_SECRET_KEY = "ogMilPuE9OunHTvaQxl3qx7uoS5TANPb22xnBBuN"
    MINIO_SECURE = True
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
