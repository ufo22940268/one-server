#! ../env/bin/python
# -*- coding: utf-8 -*-
from one_server import mongo
from base import test_app, TestBase, token2, token
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
