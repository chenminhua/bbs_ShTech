from mongoengine import *
import datetime

class Message(Document):
    sender = ReferenceField('UserModel')
    receiver = ReferenceField('UserModel')
    content = StringField()
    sent_at = DateTimeField()
    def save(self):
        self.sent_at = datetime.datetime.now()
        super(Message,self).save()

    def messageConvert(self):
        from bbs.utils import timeGapWithNow
        return {
            "sender_name":self.sender.username,
            "content":self.content,
            "sent_at":timeGapWithNow(self.sent_at)
        }