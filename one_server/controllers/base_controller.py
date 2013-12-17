#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2013 ccheng <ccheng@cchengs-MacBook-Pro.local>
#
# Distributed under terms of the MIT license.

"""

"""
from flask.ext.restful import Resource
from flask.ext.login import current_user
from bson import ObjectId
from one_server import common_util

class BaseResource(Resource):

    def get_user_id(self):
        return current_user.get_id()

    def get_user_object_id(self):
        return ObjectId(self.get_user_id())

    def result_ok(self, data='', pageinfo=None):
        rt = {'result': data}
        if pageinfo:
            common_util.append_pageinfo(rt, pageinfo)
        return rt, 200

    def result_error(self):
        return '', 400
