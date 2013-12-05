#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2013 ccheng <ccheng@cchengs-MacBook-Pro.local>
#
# Distributed under terms of the MIT license.

"""

"""

import urllib

def make_url_end(url, params):
    return '%s?%s' % (url, urllib.urlencode(params))
