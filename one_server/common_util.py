#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2013 ccheng <ccheng@cchengs-MacBook-Pro.local>
#
# Distributed under terms of the MIT license.

"""

"""

import json
from bson.json_util import dumps

def cursor_to_dict(c):
    """Convert mongodb cursor object to python dict object"""
    return json.loads(dumps(c))

