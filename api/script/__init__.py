#coding:utf-8
__author__ = 'chenminhua'
import sys
sys.path.append('/Users/chenminhua/workspace/bbs_ShTech/api')
from bbs import create_app as create_app_base
import mongoengine
from flask import json

users = [
    {"username":"cmh1","password":"123456","email":"cmhinseu@163.com"},
    {"username":"cmh2","password":"123456","email":"chenmhgo@gmail.com"},
    {"username":"cmh3","password":"123456","email":"chenmh@shanghaitech.edu.cn"},
]

nodes = [
    {"name":"secondhand","label":u"跳蚤市场","category":u"信息发布"},
    {"name":"xinxi","label":u"信息学院","category":u"信息发布"},
    {"name":"wuzhi","label":u"物质学院","category":u"信息发布"},
    {"name":"shengming","label":u"生命学院","category":u"信息发布"},


    {"name":"nba","label":u"nba","category":u"娱乐活动"},
    {"name":"tvshow","label":u"追剧狂魔","category":u"娱乐活动"},
    {"name":"movie","label":u"看电影","category":u"娱乐活动"},
    {"name":"game","label":"game","category":u"娱乐活动"},
    {"name":"nighttalk","label":u"夜聊时间","category":u"娱乐活动"},
    {"name":"travelling","label":u"走四方","category":u"娱乐活动"},
    {"name":"hangout","label":u"约不约","category":u"娱乐活动"},


    {"name":"ideas","label":u"创意","category":u"分享与探索"},
    {"name":"ideas","label":u"你问我答","category":u"分享与探索"},

    {"name":"food","label":u"美食","category":u"生活"},
    {"name":"love","label":u"爱情","category":u"生活"},
    {"name":"fit","label":u"健身","category":u"生活"},
    {"name":"pet","label":u"宠物","category":u"生活"},


    {"name":"music","label":u"音乐协会","category":u"社团专区"},

    {"name":"programming","label":u"编程之法","category":u"geek"},
    {"name":"hardware","label":u"硬件爱好者","category":u"geek"},
    {"name":"application","label":u"应用小分队","category":u"geek"}

]

topics1 = [
    {"title":u"求购捷安特自行车","content":"okok","node":"secondhand"}
]

replies = [
    {"content":"@cmh2 @cmh3 \n hello \n what is it"}
]


class AutoBuild:
    def __init__(self):
        self.app = create_app_base().test_client()
        db = mongoengine.connect('bbs_dev')
        db.drop_database('bbs_dev')

    def user_register(self,user):
        return self.app.post('/user', data=json.dumps(user), content_type="application/json")

    def user_signin(self, message):
        return self.app.post('/signin', data=json.dumps(message), content_type="application/json")

    def node_create(self,node):
        return self.app.post('/node', data=json.dumps(node),content_type="application/json")

    def create_topic(self,token,topic):
        return self.app.post('/topic',data=json.dumps(topic),
                             headers={'Authorization': 'Bearer '+token},content_type="application/json")

    def create_reply(self, token,topicid,content):
        return self.app.post('/reply/'+topicid,data=json.dumps(content),
                             headers={'Authorization': 'Bearer '+token},content_type="application/json")

ab = AutoBuild()
for user in users:
    ab.user_register(user)   #创建三个用户

for node in nodes:          #创建二十个节点
    ab.node_create(node)

token1 = json.loads(ab.user_signin(users[0]).data)['token']

topicids = []
for topic in topics1:
    topicids.append(ab.create_topic(token1,topic).data)

for reply in replies:
    ab.create_reply(token1, topicids[0], reply)



