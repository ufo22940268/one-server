#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2013 ccheng <ccheng@cchengs-MacBook-Pro.local>
#
# Distributed under terms of the MIT license.

"""

"""
from flask import Flask
from flask.ext.restful import reqparse, abort, Api, Resource
from flask.ext.restful.types import date
from flask.ext import restful
from flask.ext.login import LoginManager, current_user

from one_server.model.user_model import authenticate
from one_server import api, mongo, login_manager
from bson.json_util import dumps
from bson.dbref import DBRef
import json
from functools import wraps
from one_server.model import ride_model
from bson import ObjectId
from one_server.common_util import distance_on_unit_sphere
from one_server import common_util
from one_server.controllers.base_controller import BaseResource


class Rides(BaseResource):


    method_decorators = [authenticate]

    def __init__(self):
        self.api_parser = reqparse.RequestParser()
        self.api_parser.add_argument('title'          , type=str   , required=True)
        self.api_parser.add_argument('start_off_time' , type=str   , required=True)
        self.api_parser.add_argument('wait_time'      , type=str   , required=True)
        self.api_parser.add_argument('start_lat'      , type=float , required=True)
        self.api_parser.add_argument('start_lng'      , type=float , required=True)
        self.api_parser.add_argument('dest_lat'       , type=float , required=True)
        self.api_parser.add_argument('dest_lng'       , type=float , required=True)
        self.api_parser.add_argument('price'          , type=int   , required=True)
        self.api_parser.add_argument('people'         , type=int   , required=True)
        self.api_parser.add_argument('comment'        , type=str)
        self.api_parser.add_argument('debug'        , type=int)
        self.api_parser.add_argument('car_type'        , type=int)

    def get(self):
        parser = reqparse.RequestParser()
        common_util.setup_pageinfo(parser)
        parser.add_argument('lat'      , type=float , required=True)
        parser.add_argument('lng'      , type=float , required=True)
        args = parser.parse_args()
        data = ride_model.nearby_cars(args['lat'], args['lng'], args)
        # import pdb; pdb.set_trace()
        data = dumps(data)
        data = json.loads(data)

        for x in data:
            x['distance'] = distance_on_unit_sphere(args['lat'], args['lng'], float(x['dest_loc'][0]), float(x['dest_loc'][1]))

            #Mock
            x['rating'] = 3

        return self.result_ok(data, pageinfo=args)

    def post(self):
        args = self.api_parser.parse_args()
        start_loc = [args['start_lat'], args['start_lng']]
        dest_loc = [args['dest_lat'], args['dest_lng']]
        args['start_loc'] = start_loc
        args['dest_loc'] = dest_loc
        if args.get('debug'):
            args['start_addr'] = u'测试_杭州'
            args['dest_addr'] = u'测试_杭州'
        else:
            args['start_addr'] = common_util.readable_address(args['start_lat'], args['start_lng'])
            args['dest_addr'] = common_util.readable_address(args['dest_lat'], args['dest_lng'])

        del args['start_lat']
        del args['start_lng']
        del args['dest_lat']
        del args['dest_lng']
        user_id = current_user.get_id()
        # args['user'] = {'$ref': 'user', '$id': ObjectId(user_id)}
        args['user'] = DBRef('user', ObjectId(user_id))
        mongo.db.ride.insert(args)
        return '', 200

class RideDetail(BaseResource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id'      , type=str , required=True)
        args = parser.parse_args()
        data = ride_model.nearby_car(args['id'])
        data = common_util.cursor_to_dict(data)

        data['distance'] = distance_on_unit_sphere(data['start_loc'][0],
                                                   data['start_loc'][1],
                                                   data['dest_loc'][0],
                                                   data['dest_loc'][1])
        #Mock
        data['rating'] = 3

        return self.result_ok(data)


class Passengers(BaseResource):

    method_decorators = [authenticate]

    def __init__(self):
        self.api_parser = reqparse.RequestParser()
        self.api_parser.add_argument('title'          , type=unicode   , required=True)
        self.api_parser.add_argument('start_off_time' , type=str   , required=True)
        self.api_parser.add_argument('wait_time'      , type=str   , required=True)
        self.api_parser.add_argument('start_lat'      , type=float , required=True)
        self.api_parser.add_argument('start_lng'      , type=float , required=True)
        self.api_parser.add_argument('dest_lat'       , type=float , required=True)
        self.api_parser.add_argument('dest_lng'       , type=float , required=True)
        self.api_parser.add_argument('price'          , type=int   , required=True)
        self.api_parser.add_argument('people'         , type=int   , required=True)
        self.api_parser.add_argument('comment'        , type=unicode)
        self.api_parser.add_argument('debug'        , type=int)

    def get(self):
        parser = reqparse.RequestParser()
        common_util.setup_pageinfo(parser)
        parser.add_argument('lat'      , type=float , required=True)
        parser.add_argument('lng'      , type=float , required=True)
        args = parser.parse_args()
        data = ride_model.nearby_passengers(args['lat'], args['lng'], args)
        data = dumps(data)
        data = json.loads(data)

        for x in data:
            x['user'] = json.loads(dumps(mongo.db.user.find_one({'_id': ObjectId(x['user_id'])})))
            del x['user']['password']
            distance = distance_on_unit_sphere(args['lat'], args['lng'], float(x['dest_loc'][0]), float(x['dest_loc'][1]))
            x['distance'] = (distance * 100) / 100.0

            #Mock
            x['rating'] = 3
            if not x.get('start_addr'):
                x['start_addr'] = ''

            if not x.get('dest_addr'):
                x['dest_addr'] = ''

        return self.result_ok(data, pageinfo=args)

    def post(self):
        args = self.api_parser.parse_args()
        start_loc = [args['start_lat'], args['start_lng']]
        dest_loc = [args['dest_lat'], args['dest_lng']]
        args['start_loc'] = start_loc
        args['dest_loc'] = dest_loc
        if args.get('debug'):
            args['start_addr'] = u'测试_杭州'
            args['dest_addr'] = u'测试_杭州'
        else:
            args['start_addr'] = common_util.readable_address(args['start_lat'], args['start_lng']) or ''
            args['dest_addr'] = common_util.readable_address(args['dest_lat'], args['dest_lng']) or ''

        del args['start_lat']
        del args['start_lng']
        del args['dest_lat']
        del args['dest_lng']
        args['user_id'] = current_user.get_id()
        mongo.db.passenger.insert(args)
        return '', 200

class PassengerDetail(BaseResource):

    def get(self):
        parser = reqparse.RequestParser()
        common_util.setup_pageinfo(parser)
        parser.add_argument('id'      , type=str , required=True)
        args = parser.parse_args()
        data = ride_model.nearby_passenger(args['id'])
        data = dumps(data)
        data = json.loads(data)

        data['user'] = json.loads(dumps(mongo.db.user.find_one({'_id': ObjectId(data['user_id'])})))
        del data['user']['password']
        distance = distance_on_unit_sphere(data['start_loc'][0],
                                                   data['start_loc'][1],
                                                   data['dest_loc'][0],
                                                   data['dest_loc'][1])

        data['distance'] = (distance * 100) / 100.0

        #Mock
        data['rating'] = 3
        if not data.get('start_addr'):
            data['start_addr'] = ''

        if not data.get('dest_addr'):
            data['dest_addr'] = ''

        return self.result_ok(data, pageinfo=args)


class SearchRides(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('start_lat'      , type=float , required=False)
        parser.add_argument('start_lng'      , type=float , required=False)
        parser.add_argument('dest_lat'      , type=float , required=False)
        parser.add_argument('dest_lng'      , type=float , required=False)
        parser.add_argument('type'      , type=int , required=True)
        args = parser.parse_args()
        data = ride_model.search(args)
        return {'result': data}

api.add_resource(Rides, '/rides')
api.add_resource(RideDetail, '/ride_detail')
api.add_resource(Passengers, '/passengers')
api.add_resource(PassengerDetail, '/passenger_detail')
api.add_resource(SearchRides, '/search_rides')
