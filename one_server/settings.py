class Config(object):
    SECRET_KEY = 'secret key'


class ProdConfig(Config):
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.db'

    DEBUG = True

    CACHE_TYPE = 'simple'

    # This allows us to test the forms from WTForm
    WTF_CSRF_ENABLED = False

    # configuration
    MONGO_HOST = 'localhost'
    MONGO_PORT = 27017
    #MONGO_DBNAME = ""


class DevConfig(Config):
    DEBUG = True

    CACHE_TYPE = 'simple'

    # This allows us to test the forms from WTForm
    WTF_CSRF_ENABLED = False

    # configuration
    MONGO_HOST = 'localhost'
    MONGO_PORT = 27017
    #MONGO_DBNAME = ""
