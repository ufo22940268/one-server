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


class BaseResource(Resource):
    def get_user_id(self):
        return current_user.get_id()

    def result_ok(self, data):
        return {'result': data}, 200

    def result_error(self):
        return '', 400
