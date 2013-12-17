#! ../env/bin/python
# -*- coding: utf-8 -*-
from one_server import create_app
from one_server import mongo
from flask.ext.pymongo import PyMongo
import json
import urllib
from base import *


class TestRide(TestBase):

    @classmethod
    def setup_class(cls):
        cls.insert_rides()

    @classmethod
    def insert_rides(cls):
        for i in range(10):
            lat = 39.983424 + float(i)/(10**4)
            lng = 116.322987 + float(i)/(10**4)
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
                'token': token,
                'car_type': u'自驾车'
                }
            rv = test_app.post('rides', data=params)
            assert rv.status_code == 200

    def test_list_ride(self):
        params = {'lat': 5.0, 'lng': 5.0}
        data, status = self.get("rides", params)
        assert status == 200
        first = data['result'][0]
        assert first['user']
        assert first['user']['sex']
        assert first['user']['image_url']
        assert not first['user'].get('password')
        assert first['distance'] is not None
        assert first['car_type'] == u'自驾车'
        assert first['rating']

        assert first.get('start_addr')
        assert first.get('dest_addr')

    def test_pageination(self):
        params = {'lat': 5.0, 'lng': 5.0, 'page': 1, 'page_size': 2}
        data, status = self.get("rides", params)
        assert len(data['result']) == 2
        assert data['page']
        assert data['page_size']


    def test_add(self):
        rides_cursor = mongo.db.ride.find()
        assert rides_cursor.count()
        assert rides_cursor[0]['user_id']

        rv = test_app.get(make_url_end('rides', {'lat': 5.0, 'lng': 5.0}))
        js = parse_json(rv.data)
        assert len(js)

        rv = test_app.post('rides', data={'a': 0})
        assert rv.status_code != 200

    def test_search(self):
        params = {'start_lat': 5.0, 'start_lng': 5.0}
        rv = test_app.get(make_url_end("search_rides", params))
        assert rv.status_code == 200
        assert len(parse_json(rv.data)['result'])

        params = {'dest_lat': 5.0, 'dest_lng': 5.0}
        rv = test_app.get(make_url_end("search_rides", params))
        assert rv.status_code == 200
        assert len(parse_json(rv.data)['result'])

        params = {'start_lat': 5.0, 'start_lng': 5.0,
                'dest_lat': 5.0, 'dest_lng': 5.0}
        rv = test_app.get(make_url_end("search_rides", params))
        assert rv.status_code == 200
        assert len(parse_json(rv.data)['result'])
