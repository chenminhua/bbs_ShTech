#coding:utf-8
__author__ = 'chenminhua'
from bbs import create_app as create_app_base
import mongoengine
from flask import json

user = {
    'username': 'cmh',
    'password': '123456',
    'email': 'cmhinseu@163.com'
};

signin_user = {
    'password': '123456',
    'email': 'cmhinseu@163.com'
};

topic = {"title":u"求购捷安特自行车","content":"okok","node":"tzsc"}

node = {"name":"tzsc","label":u"跳蚤市场","category":"whatever"}




class TestBasic:
    @classmethod
    def setup_class(self):
        self.app = create_app_base(
            MONGODB_SETTINGS={'db':'bbs_test'},
            TESTING=True
        ).test_client()

    @classmethod
    def teardown_class(self):
        db = mongoengine.connect('bbs_test')
        db.drop_database('bbs_test')

    def user_register(self, message):
        return self.app.post('/user', data=json.dumps(message), content_type="application/json")
    def user_signin(self, message):
        return self.app.post('/signin', data=json.dumps(message), content_type="application/json")

    def edit_user(self,message,token):
        return self.app.put('/user', data=json.dumps(message),
                             headers={'Authorization': 'Bearer '+token},content_type="application/json")

    def get_user(self,token):
        return self.app.get('/user', headers={'Authorization': 'Bearer '+token})

    def get_user_by_name(self, name):
        return self.app.get('/user/'+name)

    def register_and_signin(self,user):
        self.user_register(user)
        response = self.user_signin(user)
        return json.loads(response.data)['token']

    def create_node(self,node):
        return self.app.post('/node', data=json.dumps(node),content_type="application/json")

    def get_topic_by_id(self, topicid):
        return self.app.get('/topic/'+topicid)

    def get_user_topics(self, name):
        return self.app.get('/user/'+name+'/topics')

    def like_topic(self, token, topicid):
        return self.app.put('/user/likes/'+topicid, headers={'Authorization': 'Bearer '+token})

    def unlike_topic(self, token, topicid):
        return self.app.delete('/user/likes/'+topicid, headers={'Authorization': 'Bearer '+token})

    def get_user_likes(self, username):
        return self.app.get('/user/'+username+'/likes')