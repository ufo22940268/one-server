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
from bson.dbref import DBRef
from bson.objectid import ObjectId

def nearby_cars(lat, lng, pageinfo=None):
    data = mongo.db.ride.find(
        {"start_loc": {"$near": [lat, lng]}}
    )
    if pageinfo:
        page(data, pageinfo)

    data = list(data)
    for x in data:
        x['_id'] = str(x['_id'])
        x['user'] = mongo.db.dereference(x['user'])
        del x['user']['password']

    return data

def nearby_car(id):
    data = mongo.db.ride.find_one(
        {"_id": ObjectId(id)}
    )

    data = dict(data)
    data['user'] = mongo.db.dereference(data['user'])
    del data['user']['password']

    return data

def search(req_params):
    coll = mongo.db.ride if req_params['type'] == 0 else mongo.db.passenger
    if req_params.get('start_lat') and req_params.get('start_lng'):
        data = coll.find(
            {"start_loc": {"$near": [req_params['start_lat'], req_params['start_lng']]}}
        )
        return cursor_to_dict(data)

    if req_params.get('dest_lat') and req_params.get('dest_lng'):
        data = coll.find(
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
