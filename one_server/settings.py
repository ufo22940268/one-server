class Config(object):
    SECRET_KEY = 'secret key'


class ProdConfig(Config):
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.db'

    CACHE_TYPE = 'simple'

class DevConfig(Config):
    DEBUG = True

    #SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.db'
    #SQLALCHEMY_ECHO = True

    CACHE_TYPE = 'simple'

    # This allows us to test the forms from WTForm
    WTF_CSRF_ENABLED = False

    # configuration
    MONGO_HOST = 'localhost'
    MONGO_PORT = 27017
    #MONGO_DBNAME = ""
