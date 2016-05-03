#coding:utf-8
from nose.tools import *
from flask import json
from test import TestBasic, user, signin_user


class TestUser(TestBasic):
    pass

# class TestUserRegister(TestUser):
#     def test_user_register(self):
#         response = self.user_register(user);
#         eq_(200, response.status_code)
#
# class TestUserSignin(TestUser):
#     def test_user_signin(self):
#         self.user_register(user)
#         response = self.user_signin(signin_user)
#         eq_(200,response.status_code)
#
# class TestUserGet(TestUser):
#     def test_get_user(self):
#         self.user_register(user)
#         response = self.user_signin(signin_user)
#         token = json.loads(response.data)['token']
#         response = self.get_user(token)
#         eq_(200, response.status_code)
#         u = json.loads(response.data)
#         eq_(u['user']['username'], user['username'])
#         eq_(u['user']['email'],user['email'])
#
# class TestEditUser(TestUser):
#     def test_edit_user(self):
#         self.user_register(user)
#         response = self.user_signin(signin_user)
#         token = json.loads(response.data)['token']
#
#         self.edit_user({"major":u"信息工程","birthday":"1991-11-24",'hometown':u"地球","hobby":"running,basketball", "avatar_url":"abc", "description":u"此处有签名"},token)
#         response = self.get_user(token)
#         u = json.loads(response.data)
#         eq_(u['user']['major'], u"信息工程")
#         eq_(u['user']['birthday'], "1991-11-24")
#         eq_(u['user']['hometown'], u"地球")
#         eq_(u['user']['description'], u"此处有签名")
#         eq_(u['user']['hobby'], ["running","basketball"])
#         eq_(u['user']['avatar_url'], "abc")
#
# class TestGetUserByName(TestUser):
#     def test_get_uer_by_username(self):
#         self.user_register(user)
#         response = self.user_signin(signin_user)
#         token = json.loads(response.data)['token']
#         self.edit_user({"major":u"信息工程","birthday":"1991-11-24",'hometown':u"地球","hobby":"running,basketball", "avatar_url":"abc", "description":u"此处有签名"},token)
#         response = self.get_user_by_name(user['username'])
#         u = json.loads(response.data)
#         eq_(u['user']['major'], u"信息工程")
#         eq_(u['user']['birthday'], "1991-11-24")
#         eq_(u['user']['hometown'], u"地球")
#         eq_(u['user']['description'], u"此处有签名")
#         eq_(u['user']['hobby'], ["running","basketball"])
#         eq_(u['user']['avatar_url'], "abc")

