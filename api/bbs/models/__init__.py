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

    def save(self):
        if not self.avatar_url:
            self.generate_password()
            self.created_at = datetime.datetime.now()
            self.generate_gravatar_url(50)
        try:
            super(UserModel,self).save()
            return True
        except:
            return False

    def generate_password(self):
        self.password = bcrypt.hashpw(str(self.password),bcrypt.gensalt(14))

    def generate_gravatar_url(self,size):
        import hashlib
        root_url = "http://cn.gravatar.com/avatar/"
        self.avatar_url = root_url + hashlib.md5(self.email.lower()).hexdigest() + "?s=" + str(size)

    def checkPassword(self, password):
        return self.password == bcrypt.hashpw(password, str(self.password))

    @property
    def topics(self):
        return TopicModel.objects(author=self)

    @property
    def topics_count(self):
        return len(self.snippets)

    def is_following(self,user):
        return user in self.followings

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
    node = ReferenceField(NodeModel)

    def isAuthor(self,username):
        return username == self.author.username

class NodeModel(Document):
    name = StringField()
    popularity = IntField()

    @property
    def topics(self):
        return TopicModel.objects(tag=self)

class Message(Document):
    sender = ReferenceField(UserModel)
    content = StringField()