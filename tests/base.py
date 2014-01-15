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
import one_server
import json
from bson.json_util import dumps

app = create_app('one_server.settings.DevConfig', env='dev')
test_app = app.test_client()
context = app.test_request_context('/')
context.push()

#clear all data.
mongo.db.user.remove()
mongo.db.comment.remove()
mongo.db.ride.remove()
mongo.db.passenger.remove()

one_server.init_db()
token = str(mongo.db.user.find_one({'nickname': 'asdf'})['_id'])

#This user is used to test some function need two users.
token2 = str(mongo.db.user.find_one({'nickname': 'fdsa'})['_id'])

def make_url_end(url, params):
    if not params.get('token'):
        params['token'] = token

    if params:
        return '%s?%s' % (url, urllib.urlencode(params))
    else:
        return url


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

    def get(self, end, params={}):
        rv = test_app.get(make_url_end(end, params))
        return parse_json(rv.data), rv.status_code

    def get_result(self, end, params={}):
        rv = test_app.get(make_url_end(end, params))
        return parse_json(rv.data).get('result'), rv.status_code

    def get_token_user(self):
        data, status_code = self.get('specific_user', {"id": token})
        assert status_code == 200
        return data['result']


def insert_ride_item(uid=token):
    lat = 39.983424 + float(1)/(10**4)
    lng = 116.322987 + float(1)/(10**4)
    params = {
        'title': 't',
        'start_off_time': '1922-02-01 21:22',
        'wait_time': '1922-02-01 21:22',
        'start_lat': lat,
        'start_lng': lng,
        'dest_lat': lat,
        'dest_lng': lng,
        'price': 2,
        'people': 2,
        'car_type': 1,
        'comment': 'asdf',
        'debug': 1,
        'car_type': 1,
        'token': uid,
    }
    
    rv = test_app.post('rides', data=params)
    assert rv.status_code == 200

def insert_passenger_item(uid=token):
        lat = 39.983424 + float(1)/(10**4)
        lng = 116.322987 + float(1)/(10**4)
        params = {
            'title': u'阿斯蒂芬',
            'start_off_time': '1922-02-01 21:22',
            'wait_time': '1',
            'start_lat': lat,
            'start_lng': lng,
            'dest_lat': lat,
            'dest_lng': lng,
            'price': 2,
            'people': 2,
            'comment': u'撒旦法士大夫',
            'debug': 1,
            'token': uid,
        }
        rv = test_app.post('passengers', data=params)
        assert rv.status_code == 200
