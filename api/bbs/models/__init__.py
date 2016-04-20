#coding:utf-8
__author__ = 'chenminhua'

from mongoengine import *
import datetime
import bcrypt

class UserModel(Document):
    email = EmailField(unique=True,required=True,max_length=128)
    username = StringField(unique=True,required=True,max_length=128)
    password = StringField(required=True)
    created_at = DateTimeField(required=True)
    major = StringField()
    homeTown = StringField(default="china")
    hobby = ListField(StringField())
    description = StringField()
    avatar_url = StringField(required=True)
    likes = ListField(ReferenceField('TopicModel'))
    followings= ListField(ReferenceField('UserModel'))
    birthday = DateTimeField()
    activation = BooleanField(default=False)

    def save(self):
        if not self.avatar_url:
            self.generate_password()
            self.created_at = datetime.datetime.now()
            self.generate_gravatar_url(50)
        #try:
        super(UserModel,self).save()
        return True
        #except:
        #    return False

    def generate_password(self):
        self.password = bcrypt.hashpw(str(self.password),bcrypt.gensalt(14))

    def is_activated(self):
        return self.activation

    def generate_gravatar_url(self,size):
        import hashlib
        root_url = "http://cn.gravatar.com/avatar/"
        self.avatar_url = root_url + hashlib.md5(self.email.lower()).hexdigest() + "?s=" + str(size)

    def checkPassword(self, password):
        return self.password == bcrypt.hashpw(str(password), str(self.password))

    def changePassword(self, password):
        self.password = str(password)
        self.generate_password()
        super(UserModel, self).save()

    @property
    def topics(self):
        return TopicModel.objects(author=self)

    @property
    def topics_count(self):
        return len(self.snippets)

    def is_following(self,user):
        return user in self.followings

    def is_liked(self,topic):
        return topic in self.likes

    @property
    def followers(self):
        return UserModel.objects(followings=self)

    @property
    def followers_count(self):
        return len(UserModel.objects(followings=self))

    @property
    def followings_count(self):
        return len(self.followings)

class TopicModel(Document):
    author = ReferenceField(UserModel)
    title = StringField(required=True)
    content = StringField(required=True)
    created_at = DateTimeField()
    read = IntField()
    replies = IntField()
    node = ReferenceField('Node')
    replies = ListField(StringField())

    def isAuthor(self,u):
        return u == self.author

class Node(Document):
    #节点
    name = StringField(unique=True)
    label = StringField()
    popularity = IntField()

    @property
    def topics(self):
        return TopicModel.objects(node=self)

class Message(Document):
    sender = ReferenceField('UserModel')
    receiver = ReferenceField('UserModel')
    content = StringField()
    sent_at = DateTimeField()
    def save(self):
        self.sent_at = datetime.datetime.now()
        super(Message,self).save()

