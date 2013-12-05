#!/usr/bin/env python
import os

from flask.ext.script import Manager, Server
from one_server import create_app

env = os.environ.get('APPNAME_ENV', 'dev')
app = create_app('one_server.settings.%sConfig' % env.capitalize(), env=env)

manager = Manager(app)
manager.add_command("server", Server())


if __name__ == "__main__":
    manager.run()
