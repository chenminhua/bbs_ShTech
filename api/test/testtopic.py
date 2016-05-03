#coding:utf-8
from nose.tools import *
from flask import json
from test import TestBasic, user, signin_user,topic, node


class TestTopic(TestBasic):

    def create_topic(self, topic ,token):
        return self.app.post('/topic',data=json.dumps(topic),
                             headers={'Authorization': 'Bearer '+token},content_type="application/json")

class TestTopicPost(TestTopic):
    def test_post_topic(self):
        token = self.register_and_signin(user)
        self.create_node(node)
        topicid = self.create_topic(topic,token).data
        new_topic = json.loads(self.get_topic_by_id(topicid).data)
        eq_(new_topic['topic']['title'],topic['title'])
        eq_(new_topic['topic']['content'],topic['content'])

        u = json.loads(self.get_user(token).data)
        eq_(u['user']['topics_count'], 1)

        topics = json.loads(self.get_user_topics(user['username']).data)['topics']
        eq_(len(topics),1)
        eq_(topics[0]['node']['name'], node['name'])
        eq_(topics[0]['node']['label'], node['label'])
        eq_(topics[0]['author_name'], user['username'])
        eq_(topics[0]['title'], topic['title'])
        eq_(topics[0]['content'], topic['content'])

class TestTopicLike(TestTopic):
    def test_topic_like(self):
        token = self.register_and_signin(user)
        self.create_node(node)
        topicid = self.create_topic(topic,token).data

        self.like_topic(token,topicid)
        u = json.loads(self.get_user(token).data)['user']
        eq_(u["likes_count"], 1)
        like = json.loads(self.get_user_likes(user['username']).data)['likes'][0]
        eq_(like['title'],topic['title'])
        eq_(like['content'],topic['content'])
        eq_(like['author_name'], user['username'])
        eq_(like['author_avatar_url'], u['avatar_url'])

        self.unlike_topic(token,topicid)
        u = json.loads(self.get_user(token).data)['user']
        eq_(u["likes_count"], 0)
        likes = json.loads(self.get_user_likes(user['username']).data)['likes']
        eq_(len(likes), 0)




















