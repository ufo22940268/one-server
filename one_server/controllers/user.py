#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2013 ccheng <ccheng@cchengs-MacBook-Pro.local>
#
# Distributed under terms of the MIT license.

"""

"""
from flask.ext.restful import reqparse, Resource
from one_server import api, mongo
from bson import ObjectId
from one_server.model import user_model
from one_server import common_util
from one_server.controllers.base_controller import BaseResource
import werkzeug.datastructures
import arrow
from one_server.model.user_model import authenticate
from bson.dbref import DBRef

class User(Resource):
    
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nickname', type=str, required=True)
        parser.add_argument('status', type=str, required=True)
        parser.add_argument('lat', type=float, required=True)
        parser.add_argument('lng', type=float, required=True)
        parser.add_argument('sex', type=int, required=True)
        parser.add_argument('age_segment', type=int, required=True)
        parser.add_argument('image',
                            type=werkzeug.datastructures.FileStorage,
                            location='files')
        args = parser.parse_args()
        filename = str(arrow.utcnow().timestamp)
        args['image'].save('one_server/static/public/files/%s' % filename)
        image_url = '/static/public/files/%s' % filename
        args['portrait_url'] = image_url
        del args['image']
        loc = [args['lat'], args['lng']]
        args['loc'] = loc
        del args['lat']
        del args['lng']

        mongo.db.user.insert(args)

class SingleUser(BaseResource):
    
    method_decorators = [authenticate]

    def get(self):
        uid = self.get_user_id()
        user = mongo.db.user.find_one({'_id': ObjectId(uid)})
        user = common_util.cursor_to_dict(user)
        if user.get('password'):
            del user['password']
        return self.result_ok(user)

class SpecificUser(BaseResource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str, required=True)
        args = parser.parse_args()
        
        uid = args['id']
        user = mongo.db.user.find_one({'_id': ObjectId(uid)})
        user = common_util.cursor_to_dict(user)
        del user['password']
        return self.result_ok(user)

class Comment(BaseResource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('commentor_id', type=str, required=True)
        parser.add_argument('comment', type=str, required=True)
        args = parser.parse_args()
        user_id = self.get_user_id()
        commentor_id = args['commentor_id']
        comment_dict = {'comment': args['comment']}
        comment_dict['commentor'] = DBRef('user', ObjectId(commentor_id))
        comment_dict['time'] = arrow.utcnow().format('YYYY-MM-DD HH:mm')
        mongo.db.user.update(
            {"_id": ObjectId(user_id)},
            {'$push': {'comment': comment_dict}})
        return '', 200

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=str, required=True)
        args = parser.parse_args()
        return {'result': user_model.get_comment(args['user_id'])}

class Login(BaseResource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()
        user = mongo.db.user.find_one({'username': args['username']})
        if user:
            return self.result_ok({'token': str(user['_id'])})
        else:
            return self.result_error()


class Test(BaseResource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('image',
                            type=werkzeug.datastructures.FileStorage,
                            location='files')


class ValidatePhone(BaseResource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('phone', type=str, required=True)
        parser.add_argument('code', type=str, required=True)
        args = parser.parse_args()

        if args['code'] == 'asdf':
            return self.result_ok('')
        else:
            return self.result_error()

class ValidateCode(BaseResource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('phone', type=str, required=True)
        args = parser.parse_args()
        return self.result_ok({'code': 'asdf'})


class SubmitPassword(BaseResource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('password', type=str, required=True)
        password = parser.parse_args()['password']
        mongo.db.user.update({'_id': self.get_user_object_id()},
                             {'$set': {'password': password}})
        return self.result_ok()

class DonateRideCoin(BaseResource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('quantity', type=int, required=True)
        quantity = parser.parse_args()['quantity']
        mongo.db.user.update({'_id': self.get_user_object_id()},
                             {'$inc': {'ride_coin': quantity}})
        return self.result_ok()


api.add_resource(User, '/users')
api.add_resource(SingleUser, '/user')
api.add_resource(SpecificUser, '/specific_user')
api.add_resource(Comment, '/comments')
api.add_resource(Login, '/login')
api.add_resource(Test, '/test')
api.add_resource(ValidatePhone, '/validate_phone')
api.add_resource(ValidateCode, '/validate_code')
api.add_resource(SubmitPassword, '/submit_password')
api.add_resource(DonateRideCoin, '/donate_ride_coin')
