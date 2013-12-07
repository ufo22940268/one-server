#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2013 ccheng <ccheng@cchengs-MacBook-Pro.local>
#
# Distributed under terms of the MIT license.

"""

"""

import urllib
from one_server import create_app, mongo
import json
from flask.ext.login import LoginManager, current_user
from bson.json_util import dumps

app = create_app('one_server.settings.DevConfig', env='dev')
test_app = app.test_client()
context = app.test_request_context('/')
context.push()

#clear all data.
mongo.db.user.remove()
mongo.db.comment.remove()

token = str(mongo.db.user.insert({'nickname': 'asdf'}))

#This user is used to test some function need two users.
token2 = str(mongo.db.user.insert({'nickname': 'fdsa'}))

def make_url_end(url, params):
    if not params.get('token'):
        params['token'] = token

    return '%s?%s' % (url, urllib.urlencode(params))

def parse_json(raw):
    try:
        return json.loads(raw)
    except:
        raise Exception("%s not valid json string" % raw)

def to_dict(c):
    """Convert mongodb cursor object to python dict object"""
    return json.loads(dumps(c))

class TestBase(object):

    def post(self, end, params):
        rv = test_app.post(end, data=params)
        return parse_json(rv.data), rv.status_code
        
    def get_user_id(self):
        return current_user.get_id()
