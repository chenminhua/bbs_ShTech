#coding:utf-8
from mongoengine import *
from topic import TopicModel
from message import Message
from reply import Reply
import datetime
import bcrypt


class UserModel(Document):
    email = EmailField(unique=True,required=True,max_length=128)
    username = StringField(unique=True,required=True,max_length=20)
    password = StringField(required=True)
    created_at = DateTimeField(required=True)
    major = StringField()
    hometown = StringField(default="china")
    hobby = ListField(StringField())
    description = StringField()
    avatar_url = StringField(required=True)
    likes = ListField(ReferenceField('TopicModel'))
    followings= ListField(ReferenceField('UserModel'))
    birthday = DateTimeField()
    activation = BooleanField(default=True)      #判断用户是否已经激活
    unreadMessages_count = IntField(default=0)
    unreadReplies_count = IntField(default=0)

    def create(self):
        if not self.avatar_url:
            self.generate_password()
            self.created_at = datetime.datetime.now()
            self.generate_gravatar_url(50)
        self.save()
        return True

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
        self.save()

    @property
    def messages(self):
        return Message.objects(receiver=self).order_by('-sent_at')

    @property
    def replies(self):
        return Reply.objects(receivers__contains=self).order_by('-created_at')

    @property
    def topics(self):
        return TopicModel.objects(author=self)

    @property
    def topics_count(self):
        return len(self.topics)

    def is_following(self,user):
        print self.username, user.username
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

    @property
    def likes_count(self):
        return len(self.likes)

    def get_yourself(self):
        result = self.userConvert()
        result['unreadMessages_count'] = self.unreadMessages_count
        result['unreadReplies_count'] = self.unreadReplies_count
        return result

    def userConvert(self):
        from bbs.utils import timeGapWithNow
        result = {
            "username":self.username,"avatar_url":self.avatar_url,"followers_count":self.followers_count,
            "followings_count":self.followings_count,"email":self.email,
            "description":self.description,"hobby":self.hobby,"topics_count":self.topics_count,
            "likes_count":self.likes_count,"created_at":timeGapWithNow(self.created_at),
            "hometown":self.hometown,"major":self.major
        }
        if self.birthday:
            result['birthday'] = self.birthday.strftime("%Y-%m-%d")
        return result