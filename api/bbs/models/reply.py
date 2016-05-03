from mongoengine import *
import datetime
class Reply(Document):
    topic = ReferenceField('TopicModel')
    content = StringField()
    sender = ReferenceField('UserModel')
    receivers = ListField(ReferenceField('UserModel'))
    created_at = DateTimeField(required=True)

    def save(self):
        self.created_at = datetime.datetime.now()
        super(Reply,self).save()

    def replyConvert(self):
        from bbs.utils import timeGapWithNow
        return { "content":self.content,"sender_name":self.sender.username,"sender_avatar":self.sender.avatar_url,
                 "created_at": timeGapWithNow(self.created_at),"topic_title":self.topic.title,"topic_id":str(self.topic.id)
        }
