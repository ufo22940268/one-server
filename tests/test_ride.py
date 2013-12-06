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


class TestRide:

    def test_list(self):
        params={'lat': 5.0, 'lng': 5.0, 'token': 'aa'}
        rv = test_app.get(make_url_end("rides", params))
        assert rv.status_code != 200

        params={'lat': 5.0, 'lng': 5.0}
        rv = test_app.get(make_url_end("rides", params))
        assert rv.status_code == 200

    def test_add(self):
        for i in range(10):
            params = {
                'title'         : 't',
                'start_off_time': '1922-02-01 21:22',
                'wait_time'     : '1922-02-01 21:22',
                'start_lat'     : float(i),
                'start_lng'     : float(i),
                'dest_lat'      : float(i),
                'dest_lng'      : float(i),
                'price'         : 2,
                'people'        : 2,
                'car_type'      : 1,
                'comment'       : 'asdf',
                'token'         : token,
                }
            rv = test_app.post('rides', data=params)
            assert rv.status_code == 200
        rides_cursor = mongo.db.ride.find()
        assert rides_cursor.count()

        rv = test_app.get(make_url_end('rides', {'lat': 5.0, 'lng': 5.0}))
        js = parse_json(rv.data)
        assert len(js)
        assert js[0]['start_loc'][0] == 5

        rv = test_app.post('rides', data={'a': 0})
        assert rv.status_code != 200
