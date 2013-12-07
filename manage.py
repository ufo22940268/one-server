#!/usr/bin/env python
import os

from flask.ext.script import Manager, Server
from one_server import create_app, mongo
from pymongo import GEO2D

env = os.environ.get('APPNAME_ENV', 'dev')
app = create_app('one_server.settings.%sConfig' % env.capitalize(), env=env)

manager = Manager(app)
manager.add_command("server", Server())

#@manager.command
#def init():
    #app = create_app('one_server.settings.DevConfig', env='dev')
    #context = app.test_request_context('/')
    #init_database()

if __name__ == "__main__":
    manager.run()
