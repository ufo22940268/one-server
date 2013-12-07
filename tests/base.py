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

app = create_app('one_server.settings.DevConfig', env='dev')
test_app = app.test_client()
context = app.test_request_context('/')
context.push()

mongo.db.user.remove()
token = str(mongo.db.user.insert({'nickname': 'asdf'}))

def make_url_end(url, params):
    if not params.get('token'):
        params['token'] = token

    return '%s?%s' % (url, urllib.urlencode(params))

def parse_json(raw):
    try:
        return json.loads(raw)
    except:
        raise Exception("%s not valid json string" % raw)

