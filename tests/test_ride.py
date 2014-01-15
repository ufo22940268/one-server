#! ../env/bin/python
# -*- coding: utf-8 -*-
from one_server import create_app
from one_server import mongo
from flask.ext.pymongo import PyMongo
import json
import urllib
from base import *
import pytest


class TestRide(TestBase):

    @classmethod
    def setup_class(cls):
        cls.insert_rides()
        insert_passenger_item()

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
                'car_type': 1,
                'token': token,
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
        assert type(first['car_type']) == int
        assert first['rating']

        assert first.get('start_addr')
        assert first.get('dest_addr')

    def test_ride_detail(self):
        data, state = self.get("rides", {'lat': 5.0, 'lng': 5.0})
        id = data['result'][0]['_id']
        data, state = self.get('ride_detail', {'id': id})
        assert state == 200
        assert data['result']['user']
        assert data['result']['distance'] is not None

    def test_pageination(self):
        params = {'lat': 5.0, 'lng': 5.0, 'page': 1, 'page_size': 2}
        data, status = self.get("rides", params)
        assert len(data['result']) == 2
        assert data['page']
        assert data['page_size']

    @pytest.mark.current
    def test_add(self):
        rides_cursor = mongo.db.ride.find()
        assert rides_cursor.count()

        rv = test_app.get(make_url_end('rides', {'lat': 5.0, 'lng': 5.0}))
        js = parse_json(rv.data)
        assert len(js)

        rv = test_app.post('rides', data={'a': 0})
        assert rv.status_code != 200

    def test_search(self):
        params = {'start_lat': 5.0, 'start_lng': 5.0}
        rv = test_app.get(make_url_end("search_rides", params))
        assert rv.status_code != 200

        params = {
            'start_lat': 5.0,
            'start_lng': 5.0,
            'type': 1
        }
        rv = test_app.get(make_url_end("search_rides", params))
        assert rv.status_code == 200
        assert len(parse_json(rv.data)['result'])

        params = {'dest_lat': 5.0, 'dest_lng': 5.0, 'type': 1}
        rv = test_app.get(make_url_end("search_rides", params))
        assert rv.status_code == 200
        assert len(parse_json(rv.data)['result'])

        params = {'start_lat': 5.0, 'start_lng': 5.0,
                  'dest_lat': 5.0, 'dest_lng': 5.0,
                  'type': 0
        }
        rv = test_app.get(make_url_end("search_rides", params))
        assert rv.status_code == 200
        assert len(parse_json(rv.data)['result'])

        params = {'start_lat': 5.0, 'start_lng': 5.0,
                  'dest_lat': 5.0, 'dest_lng': 5.0,
                  'type': 1
        }
        rv2 = test_app.get(make_url_end("search_rides", params))
        assert rv.data != rv2.data


class TestPassenger(TestBase):

    @classmethod
    def setup_class(cls):
        cls.insert_passengers()

    @classmethod
    def insert_passengers(cls):
        for i in range(10):
            lat = 39.983424 + float(i)/(10**4)
            lng = 116.322987 + float(i)/(10**4)
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
                'token': token,
            }
            rv = test_app.post('passengers', data=params)
            assert rv.status_code == 200

    def test_add(self):
        rides_cursor = mongo.db.ride.find()
        assert rides_cursor.count()

        rv = test_app.get(make_url_end('passengers', {'lat': 5.0, 'lng': 5.0}))
        js = parse_json(rv.data)
        assert len(js)

        rv = test_app.post('passengers', data={'a': 0})
        assert rv.status_code != 200

    def test_passengers(self):
        data, status = self.get('passengers', {'lat': 5.0, 'lng': 5.0})
        assert status == 200
        assert data is not None
        first = data['result'][0]
        assert type(first['_id']) == unicode


    def test_passenger_detail(self):
        data, status = self.get('passengers', {'lat': 5.0, 'lng': 5.0})
        first = data['result'][0]
        id = first['_id']

        data, state = self.get('passenger_detail', {'id': id})
        assert state == 200
        assert data['result']['user']
        assert data['result']['distance'] is not None
        
# class TestRequestRide(TestBase):
    
#     def test_request_take_ride(self):
#         user_token1 = token
#         user_token2 = token2
#         result, status = self.get_result('request_take_ride', params={'token': token})
#         assert status == 200

#         result, status = self.get_result('specific_user', params={'token': token})
#         assert len(result['ride_request_ids']) > 0

