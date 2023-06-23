import secrets

class Config (object):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = secrets.token_hex(16)
    
class DevConfig (Config):
    DEBUG = True