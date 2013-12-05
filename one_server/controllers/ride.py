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
from one_server import api, mongo
from bson.json_util import dumps
import json

class Rides(Resource):

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
        self.api_parser.add_argument('car_type'       , type=int   , required=True)
        self.api_parser.add_argument('comment'        , type=str)

    def get(self):
        return json.loads(dumps(mongo.db.ride.find()))

    def post(self):
        args = self.api_parser.parse_args()
        mongo.db.ride.insert(args)

api.add_resource(Rides, '/rides')
