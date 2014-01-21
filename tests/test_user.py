#! ../env/bin/python
# -*- coding: utf-8 -*-
from one_server import mongo
from base import test_app, TestBase, token2, token
import base
from StringIO import StringIO
import pytest

class TestUser(TestBase):

    def test_init(self):
        assert mongo.db.user.find_one({'nickname': 'asdf'})

    def test_add_user(self):
        params = {
            'nickname': 't',
            'status': 'df',
            'lat': 12.2,
            'lng': 12.2,
            #0isformaleand1isforfemale.
            'sex': 0,
            'age_segment': 80,
        }
        params["image"] = StringIO('Foo bar baz'), 'image'
        # rv = test_app.post('users', data=params)
        # assert rv.status_code == 200

        # user = mongo.db.user.find_one({'nickname': 't'})
        # assert user['portrait_url']

    def test_get_user(self):
        data, status_code = self.get('user')
        assert status_code == 200
        assert data['result']
        result = data['result']
        assert result['merchant_coin'] is not None

    def test_get_specific_user(self):
        data, status_code = self.get('specific_user', {"id": token})
        assert status_code == 200
        assert data['result']

    def test_login(self):
        params = {'username': 'asdf', 'password': 'asdf'}
        js, status = self.post('login', params)
        assert status == 200
        assert js['result']['token']

        params = {'username': 'asdfasdfa', 'password': 'asdf'}
        js, status = self.post('login', params)
        assert status == 400

    def test_image(args):
        params = dict()
        params["image"] = StringIO('Foo bar baz'), 'image'
        rv = test_app.post('test', data=params)
        # rv = test_app.post('test', data={
        #     'asdfasdf': 'asdf',
        #     'image': (StringIO('my file contents'), 'hello world.txt'),
        # })
        assert rv.status_code == 200

    def test_validate_code(self):
        params = {'phone': '18668032931'}
        data, code = self.post('validate_code', params)
        assert code == 200

    def test_validate_phone(self):
        params = {'phone': '18668032931', 'code': 'asdf'}
        data, code = self.post('validate_phone', params)
        assert code == 200

        params['code'] = 'kkkk'
        data, code = self.post('validate_phone', params)
        assert code != 200

    def test_submit_password(self):
        params = {'password': 'asdf'}
        data, code = self.post('submit_password', params)
        assert code == 200

class TestComment(TestBase):

    def test_do_comment(self):
        params = {'commentor_id': token2, 'comment': 'good ride experience'}
        js, status = self.post('comments', params)
        assert status == 200

    def test_list_comments(self):
        for _ in range(5):
            params = {'commentor_id': token2, 'comment': 'sb'}
            js, status = self.post('comments', params)
            assert status == 200

        js, status = self.get('comments', params={'user_id': token})
        assert len(js['result'])
        result = js['result']
        first = result[0]
        assert first['commentor_name']
        assert first['time']

class TestComment(TestBase):

    def test_ride_coin(self):
        user = self.get_token_user()
        assert not user.get("ride_coin")

        self.post("donate_ride_coin", {'quantity': '10'})
        user = self.get_token_user()
        user["ride_coin"] == 10

class TestMyRides(TestBase):

    @classmethod
    def setup_class(cls):
        lat = 39.983424 + float(1)/(10**4)
        lng = 116.322987 + float(1)/(10**4)
        params = {
            'title': 't',
            'start_off_time': '1922-02-01 21:22',
            'wait_time': '1',
            'start_lat': lat,
            'start_lng': lng,
            'dest_lat': lat,
            'dest_lng': lng,
            'price': 2,
            'people': 2,
            'comment': 'asdf',
            'debug': 1,
            'token': token,
        }
        
        rv = test_app.post('passengers', data=params)
        assert rv.status_code == 200

        #insert ride info.
        base.insert_ride_item(token)

    def test_list_my_rides(self):
        result, code =  self.get_result('my_passenger_history')
        assert code == 200
        assert len(result) > 0

    def test_comment_my_ride(self):
        result, code =  self.get_result('rides', {'lat': 5.0, 'lng': 5.0})
        first = result[0]
        id = first['_id']
        id2 = result[1]['_id']
        
        result, code =  self.post('ride_comment', {'id': id, 'content': 'great'})
        assert code == 200
        result, code =  self.post('ride_comment', {'id': id, 'content': u'哎呦不错哦'})
        assert code == 200
        result, code =  self.post('ride_comment', {'id': id2, 'content': u'哎呦不错哦'})
        assert code == 200
        
        result, code =  self.get_result('ride_comment', {"user_id": token})
        assert len(result) > 1
        assert result[1].get("time")
                
    def test_list_all_my_rides(self):
        result1, code =  self.get_result('my_all_history')
        result2, code =  self.get_result('my_passenger_history')
        assert result1[0].get('type') is not None
        
class TestCoin(TestBase):

    def test_convert_to_ride_coin(self):
        """
        测试搭车币转换成爱心币的接口
        """
        user_before = self.get_result('user')
        self.post('convert_to_ride_coin', {'coin': 12})
        user_after = self.get_result('user')
        assert user_before != user_after
