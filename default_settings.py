import os

class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # JWT_SECRET_KEY = "jwt secret key 123"
    SECRET_KEY = "this is another secret key 123"

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        value = os.environ.get("DATABASE_URL")

        if not value:
            raise ValueError("DATABASE_URL is not set")

        return value

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    @property
    def SECRET_KEY(self):
        value = os.environ.get("SECRET_KEY")

        if not value:
            raise ValueError("Secret Key is not set")

        return value
class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        value = os.environ.get("DATABASE_URL_TEST")

        if not value:
            raise ValueError("DATABASE_URL_TEST is not set")

        return value

environment = os.environ.get("FLASK_ENV")

if environment == "production":
    app_config = ProductionConfig()
elif environment == "testing":
    app_config = TestingConfig()
else:
    app_config = DevelopmentConfig()