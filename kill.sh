#! /bin/bash
#
# kill.sh
# Copyright (C) 2013 garlic <garlic@localhost.localdomain>
#
# Distributed under terms of the MIT license.
#

ps -aux | grep gunicorn | grep 10000 | awk '{print $2}' | xargs -r kill
