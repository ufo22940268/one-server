#! ../env/bin/python
# -*- coding: utf-8 -*-
from one_server import create_app
from one_server import mongo
from flask.ext.pymongo import PyMongo
import json
import urllib
from base import *

def parse_json(raw):
    try:
        return json.loads(raw)
    except:
        raise Exception("%s not valid json string" % raw)

class TestUser:

    @classmethod
    def setup_class(cls):
        cls.app = create_app('one_server.settings.DevConfig', env='dev')
        cls.test_app = cls.app.test_client()
        cls.context = cls.app.test_request_context('/')
        cls.context.push()
        mongo.db.user.remove()

    def test_add_user(self):
        params = {
            'nickname'    : 't',
            'status'      : 'df',
            'lat'         : 12.2,
            'lng'         : 12.2,
            #0 is for male and 1 is for female.
            'sex'         : 0,
            'age_segment' : 80,
        }

        rv = self.test_app.post('users', data=params)
        assert rv.status_code == 200

    @classmethod
    def teardown_class(cls):
        if cls.context:
            cls.context.pop()
