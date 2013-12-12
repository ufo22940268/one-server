#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2013 ccheng <ccheng@cchengs-MacBook-Pro.local>
#
# Distributed under terms of the MIT license.

"""

"""
from one_server import login_manager, mongo
from functools import wraps
from flask.ext import restful
from flask.ext.login import UserMixin
from flask.ext import login
from flask import request
from bson import ObjectId
from one_server.common_util import cursor_to_dict


def authenticate(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not getattr(func, 'authenticated', True):
            return func(*args, **kwargs)

        token = None
        if request.args.get('token'):
            token = request.args['token']

        if request.form.get('token'):
            token = request.form['token']

        if not token:
            restful.abort(401)

        acct = load_user(token)  # custom account lookup function

        if acct:
            return func(*args, **kwargs)

        restful.abort(401)

    return wrapper


@login_manager.user_loader
def load_user(token):
    #find token in nickname:
    one = mongo.db.user.find_one({'nickname': token})
    if one:
        return login_user(str(one['_id']))
    else:
        try:
            oi = ObjectId(token)
        except:
            return
        one = mongo.db.user.find_one({'_id': oi})
        if one:
            return login_user(token)

def login_user(token):
    um = UserMixin()
    um.id = token
    login.login_user(um)
    return um


def get_comment(user_id):
    user = mongo.db.user.find_one({"_id": ObjectId(user_id)})
    return cursor_to_dict(user).get('comment')
