#! ../env/bin/python
# -*- coding: utf-8 -*-
from one_server import create_app
from one_server import mongo
from flask.ext.pymongo import PyMongo
import json
import urllib
from base import test_app

class TestUser:

    def test_init(self):
        assert mongo.db.user.find_one({'nickname': 'asdf'})

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

        rv = test_app.post('users', data=params)
        assert rv.status_code == 200
