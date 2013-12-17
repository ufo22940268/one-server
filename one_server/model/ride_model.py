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
from one_server.common_util import *

def nearby_cars(lat, lng, pageinfo=None):
    data = mongo.db.ride.find(
        {"start_loc": {"$near": [lat, lng]}}
    )
    if pageinfo:
        page(data, pageinfo)

    return data

def search_cars(req_params):
    if req_params.get('start_lat') and req_params.get('start_lng'):
        data = mongo.db.ride.find(
            {"start_loc": {"$near": [req_params['start_lat'], req_params['start_lng']]}}
        )
        return cursor_to_dict(data)

    if req_params.get('dest_lat') and req_params.get('dest_lng'):
        data = mongo.db.ride.find(
            {"dest_loc": {"$near": [req_params['dest_lat'], req_params['dest_lng']]}}
        )
        return cursor_to_dict(data)

def nearby_passengers(lat, lng, pageinfo=None):
    data = mongo.db.passenger.find(
        {"start_loc": {"$near": [lat, lng]}}
    )
    if pageinfo:
        page(data, pageinfo)

    return data
