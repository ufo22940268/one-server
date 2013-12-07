#! ../env/bin/python
import os

from flask import Flask
from flask_assets import Environment
from webassets.loaders import PythonLoader as PythonAssetsLoader
from flask.ext.cache import Cache
from flask.ext.pymongo import PyMongo
from flask.ext.restful import reqparse, abort, Api, Resource
from pymongo import GEO2D

from one_server import assets
from flask.ext.login import LoginManager

# Setup flask cache
cache = Cache()

assets_env = Environment()
api = Api(catch_all_404s=True)
mongo = PyMongo()
login_manager = LoginManager()

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
        if not mongo.db.user.find_one({'nickname': 'asdf'}):
            mongo.db.user.insert({"nickname": 'asdf'})
        mongo.db.ride.create_index([("start_loc", GEO2D)])
        mongo.db.ride.create_index([("desc_loc", GEO2D)])

    return app

if __name__ == '__main__':
    # Import the config for the proper environment using the
    # shell var APPNAME_ENV
    env = os.environ.get('APPNAME_ENV', 'prod')
    app = create_app('one_server.settings.%sConfig' % env.capitalize(), env=env)

    app.run()
