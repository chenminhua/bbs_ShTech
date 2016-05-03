#coding:utf-8
from flask import Blueprint, request, make_response, jsonify

import datetime

import re

from bbs import configs

from bbs.models import UserModel, TopicModel, Reply

from bbs.utils import jwt_required, sliceList

reply_app = Blueprint('reply_app',__name__)

@reply_app.route('/reply/<topicid>', methods=['POST'])
@jwt_required
def add_reply(topicid,u):
    try:
        content = request.get_json()['content']
    except:
        make_response("no reply content", 400)
    try:
        topic = TopicModel.objects(id=topicid)[0]
    except:
        return make_response("no such topic", 400)

    #解析content
    pattern = re.compile(r'@\w+')
    usernames = [] + re.findall(pattern, content)
    print usernames
    receivers = set([topic.author])
    for name in usernames:
        try:
            receivers.add(UserModel.objects(username=name[1:])[0])
        except:
            pass  #@了一个没有的人
    reply = Reply()
    reply.sender = u
    reply.topic = topic
    reply.receivers = list(receivers)
    reply.content = content
    reply.save()
    topic.updateLastEditedTime()
    topic.save()
    for receiver in receivers:
        receiver.unreadReplies_count += 1
        receiver.save()

    return make_response("update complete", 200)

@reply_app.route('/reply', methods=['GET'])
@jwt_required
def get_reply(u):
    try:
        page = int(request.args['page'])
    except:
        page = 1
    replies = u.replies.order_by('-created_at').skip((page-1)*configs.TOPICS_IN_EVERYPAGE).limit(configs.TOPICS_IN_EVERYPAGE)
    replies = [r.replyConvert() for r in replies]
    u.unreadReplies_count = 0
    u.save()
    return jsonify(replies=replies)
