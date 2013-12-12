#! ../env/bin/python
# -*- coding: utf-8 -*-
from one_server import mongo
from base import test_app, TestBase, token2, token


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

        rv = test_app.post('users', data=params)
        assert rv.status_code == 200

    # def test_login(self):
    #     params = {'username': 'asdf', 'password': 'asdf'}
    #     js, status = self.post('login', params)
    #     assert status == 200



class TestComment(TestBase):

    def test_do_comment(self):
        params = {'commentor_id': token2, 'comment': 'sb'}
        js, status = self.post('comments', params)
        assert status == 200

    def test_list_comments(self):
        for _ in range(5):
            params = {'commentor_id': token2, 'comment': 'sb'}
            js, status = self.post('comments', params)
            assert status == 200

        js, status = self.get('comments', params={'user_id': token})
        assert len(js['result'])
