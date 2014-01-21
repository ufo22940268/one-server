#! ../env/bin/python
import os

from flask import Flask
from flask_assets import Environment
from webassets.loaders import PythonLoader as PythonAssetsLoader
from flask.ext.cache import Cache
from flask.ext.pymongo import PyMongo
from pymongo import GEO2D
from bson import ObjectId
from flask.ext.restful import Api

from one_server import assets
from flask.ext.login import LoginManager

# Setup flask cache
cache = Cache()

assets_env = Environment()
api = Api(catch_all_404s=True)
mongo = PyMongo()
login_manager = LoginManager()


def init_db():
    image = 'http://img.bjnews.com.cn/epaper/20130618/C08/022E31DC2098.jpg'
    mongo.db.user.save({'username': 'asdf',
                        'password': 'asdf',
                        'nickname': 'asdf',
                        'sex': '0',
                        'image_url': image,
                        'status': 'asdfasdfasdf',
                        'merchant_coin': 5,
                        'ride_coin ': 10,
                        'age_segment': 80,
                        'rating': 3,
                        '_id': ObjectId('52a468d91d24ead09274284d')})
    #Alternative user for test
    mongo.db.user.save({'username': 'fdsa',
                        'password': 'fdsa',
                        'nickname': 'fdsa',
                        'sex': '0',
                        'image_url': image})
    mongo.db.ride.create_index([('start_loc', GEO2D)])
    mongo.db.ride.create_index([('dest_loc', GEO2D)])
    mongo.db.passenger.create_index([('start_loc', GEO2D)])
    mongo.db.passenger.create_index([('dest_loc', GEO2D)])

def create_app(object_name, env="prod"):
    """
    An flask application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/

    Arguments:
        object_name: the python path of the config object,
                     e.g. one_server.settings.ProdConfig

        env: The name of the current environment, e.g. prod or dev
    """

    app = Flask(__name__)

    app.config.from_object(object_name)
    app.config['ENV'] = env

    #init the cache
    cache.init_app(app)

    # connect to the database
    mongo.init_app(app)

    api.init_app(app)
    login_manager.init_app(app)

    # Import and register the different asset bundles
    assets_env.init_app(app)
    assets_loader = PythonAssetsLoader(assets)
    for name, bundle in assets_loader.load_bundles().iteritems():
        assets_env.register(name, bundle)

    # register our blueprints
    from controllers.main import main
    app.register_blueprint(main)

    import controllers.ride
    import controllers.user

    with app.app_context():
        init_db()

    return app

if __name__ == '__main__':
    # Import the config for the proper environment using the
    # shell var APPNAME_ENV
    env = os.environ.get('APPNAME_ENV', 'prod')
    app = create_app('one_server.settings.%sConfig' % env.capitalize(), env=env)
    app.run()
