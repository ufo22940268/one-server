#! ../env/bin/python
# -*- coding: utf-8 -*-
from one_server import create_app, mongo
import one_server
from flask.ext.pymongo import PyMongo
from pymongo import GEO2D

class TestDb:

    def setup(self):
        self.app = create_app('one_server.settings.DevConfig', env='dev')
        self.context = self.app.test_request_context('/')
        self.context.push()
        mongo.db.places.remove()

    def tearDown(self):
        self.context.pop()

    def test_main(self):
        one_server.mongo.db.t.insert({"a": 1})
        assert one_server.mongo.db.t.find().count()

    def test_geo(self):
        db = mongo.db

        db.places.insert({"loc": [2, 5]})
        db.places.insert({"loc": [30, 5]})
        db.places.insert({"loc": [1, 2]})
        db.places.insert({"loc": [4, 4]})
    
        db.places.create_index([("loc", GEO2D)])
        l = list(db.places.find({"loc": {"$near": [1, 3]}}).limit(3))
        assert len(l) == 3
        assert l[0]['loc'] == [1, 2]
