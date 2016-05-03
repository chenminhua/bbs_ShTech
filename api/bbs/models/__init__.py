#coding:utf-8
from mongoengine import *
import datetime

from user import UserModel
from topic import TopicModel
from reply import Reply

class Image(Document):
    uuid = StringField()
    photo = ImageField(thumbnail_size=(50,50,True))
    title = StringField()

class Node(Document):
    #节点
    name = StringField(unique=True)
    label = StringField()
    category = StringField()
    popularity = IntField()

    @property
    def topics(self):
        return TopicModel.objects(node=self)



