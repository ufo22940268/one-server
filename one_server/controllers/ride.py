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
from flask.ext.login import LoginManager

from one_server.model.user_model import authenticate
from one_server import api, mongo, login_manager
from bson.json_util import dumps
import json
from functools import wraps

class Rides(Resource):
    
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

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('lat'      , type=float , required=True)
        parser.add_argument('lng'      , type=float , required=True)
        args = parser.parse_args()
        return json.loads(dumps(mongo.db.ride.find(
            {"start_loc": {"$near": [args['lat'], args['lng']]}}
        )))

    def post(self):
        args = self.api_parser.parse_args()
        start_loc = [args['start_lat'], args['start_lng']]
        dest_loc = [args['dest_lat'], args['dest_lng']]
        args['start_loc'] = start_loc
        args['dest_loc'] = dest_loc
        del args['start_lat']
        del args['start_lng']
        del args['dest_lat']
        del args['dest_lng']
        mongo.db.ride.insert(args)

api.add_resource(Rides, '/rides')
