from flask import Blueprint, request, make_response, jsonify

from bbs.models import UserModel, TopicModel, Reply

from bbs.utils import jwt_required

reply_app = Blueprint('reply_app',__name__)

@reply_app.route('/reply/<topicid>/<username>', methods=['POST'])
@jwt_required
def add_reply(topicid,username,u):

    form = request.get_json()
    try:
        receiver = UserModel.objects(username=str(username))[0]
    except:
        return make_response("no such user", 400)
    try:
        topic = TopicModel.objects(id=topicid)[0]
    except:
        return make_response("no such topic", 400)
    reply = Reply()
    reply.sender = u
    reply.topic = topic
    reply.receiver = receiver
    reply.content = form['content']
    reply.save()
    topic.save()

    if u != receiver:
        receiver.update(push__unreadReplies=reply)

    return make_response("update complete", 200)

@reply_app.route('/reply/unread', methods=['GET'])
@jwt_required
def get_reply(u):
    return jsonify(unreadReplies=u.unreadReplies)

@reply_app.route('/reply/replyid/<replyid>', methods=['DELETE'])
@jwt_required
def delete_reply(replyid,u):
    reply = Reply.objects(id=replyid)[0]
    u.update(pull__unreadReplies=reply)
    return make_response("delete complete", 200)

@reply_app.route('/reply/topicid/<topicid>', methods=['DELETE'])
@jwt_required
def delete_reply_topicid(topicid,u):
    for t in u.unreadReplies:
        if str(t.topic.id) == topicid:
            u.update(pull__unreadReplies=t)
    return make_response("delete complete", 200)


