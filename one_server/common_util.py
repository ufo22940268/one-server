#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2013 ccheng <ccheng@cchengs-MacBook-Pro.local>
#
# Distributed under terms of the MIT license.

"""

"""
import math
import json
from bson.json_util import dumps
import requests

def cursor_to_dict(c):
    """Convert mongodb cursor object to python dict object
    If the cursor object contains _id, then convert it to a plain string."""
    r = json.loads(dumps(c))
    
    if type(r) == list:
        for x in r:
            if x.get('_id'):
                x['_id'] = x['_id']['$oid']
                
    else:
        r['_id'] = r['_id']['$oid']

    return r


def distance_on_unit_sphere(lat1, long1, lat2, long2):
    """
    http://www.johndcook.com/python_longitude_latitude.html
    """

    # Convert latitude and longitude to
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0

    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians

    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians

    # Compute spherical distance from spherical coordinates.

    # For two locations in spherical coordinates
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) =
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length

    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) +
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos(cos)

    # Remember to multiply arc by the radius of the earth
    # in your favorite set of units to get length.
    return arc*6373/3600

def readable_address(lat, lng):
    params = {
        'ak': 'w1bKk7oIEvCg4Gmrs0QquUoU',
        'pois': 1,
        'location': "%f,%f" % (lat, lng),
        'output': 'json'
    }
    r = requests.get('http://api.map.baidu.com/geocoder/v2/', params=params)
    return r.json()['result']['addressComponent']['street']

def setup_pageinfo(parser):
    parser.add_argument('page', type=int, default=1)
    parser.add_argument('page_size', type=int, default=10)

def page(cursor, pageinfo):
    if cursor:
        cursor.skip((pageinfo['page'] - 1)*pageinfo['page_size']).limit(pageinfo['page_size'])

    return cursor

def append_pageinfo(rt, pageinfo):
    rt['page'] = pageinfo['page']
    rt['page_size'] = pageinfo['page_size']
