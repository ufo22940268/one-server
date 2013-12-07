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

def nearby_cars(lat, lng):
    data = mongo.db.ride.find(
        {"start_loc": {"$near": [lat, lng]}}
    )
    return data
