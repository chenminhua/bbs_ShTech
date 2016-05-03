from mongoengine import *
import datetime
from reply import Reply


class TopicModel(Document):
    author = ReferenceField('UserModel')
    title = StringField(required=True)
    content = StringField(required=True)
    created_at = DateTimeField()
    lastEdited_at = DateTimeField()
    read = IntField(default=0)
    node = ReferenceField('Node')

    def isAuthor(self,u):
        return u == self.author

    def replies_count(self):
        return len(self.replies)

    def isLiked(self,u):
        return self in u.likes

    def create(self):
        self.created_at = datetime.datetime.now()
        self.updateLastEditedTime()
        self.save()

    def updateLastEditedTime(self):
        self.lastEdited_at = datetime.datetime.now()

    @property
    def replies(self):
        replies = Reply.objects(topic=self)
        replies = [r.replyConvert() for r in replies]
        return replies

    def topicConvert(self):
        from bbs.utils import timeGapWithNow
        return {"id":str(self.id),"title":self.title,"content":self.content,"created_at":timeGapWithNow(self.created_at),
                "node":self.node,"lastEdited_at":timeGapWithNow(self.lastEdited_at),"read":self.read, "replies_count":self.replies_count(),
                "author_avatar_url":self.author.avatar_url,"author_name":self.author.username}

    def getTopicAndReply(self):
        result = self.topicConvert()
        result['replies'] = self.replies
        return result

