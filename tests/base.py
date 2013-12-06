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
    if not params.get('token'):
        params['token'] = 'hongbosb'

    return '%s?%s' % (url, urllib.urlencode(params))
