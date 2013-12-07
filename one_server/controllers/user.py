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
from bson import ObjectId
from one_server.model import user_model
from one_server.controllers.base_controller import *

class User(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nickname'    , type=str   , required=True)
        parser.add_argument('status'      , type=str   , required=True)
        parser.add_argument('lat'         , type=float   , required=True)
        parser.add_argument('lng'         , type=float , required=True)
        parser.add_argument('sex'         , type=int , required=True)
        parser.add_argument('age_segment' , type=int , required=True)
        args = parser.parse_args()
        loc = [args['lat'], args['lng']]
        args['loc'] = loc
        del args['lat']
        del args['lng']

        mongo.db.user.insert(args)

class Comment(BaseResource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('commentor_id'    , type=str   , required=True)
        parser.add_argument('comment'    , type=str   , required=True)
        args = parser.parse_args()
        user_id = self.get_user_id()
        mongo.db.user.update({"_id": ObjectId(user_id)},
                {'$set': {'comment': args['comment']}})
        return '', 200

api.add_resource(User, '/users')
api.add_resource(Comment, '/comments')
