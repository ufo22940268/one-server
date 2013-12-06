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
from flask import request
from bson import ObjectId

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
    try:
        oi = ObjectId(token)
    except:
        return

    c = mongo.db.user.find({'_id': oi})
    return c.count() != 0

