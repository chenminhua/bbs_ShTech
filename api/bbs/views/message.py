from flask import Blueprint, request, make_response, jsonify, json
from bbs.utils import jwt_required
from bbs.models import Message, UserModel

message_app = Blueprint('message_app',__name__)


## send message to a user
@message_app.route('/message/<name>',methods=['POST'])
@jwt_required
def send(name, u):
    form = json.loads(request.data)
    try:
        other = UserModel.objects(username=name)[0]
    except:
        return make_response("no that user", 200)
    message = Message(content=form['content'])
    message.sender = u
    message.receiver = other
    message.save()
    other.update(push__unreadMessages=message)
    return "ok"

## get user's message
@message_app.route('/message/', methods=['GET'])
@jwt_required
def get_message(u):
    sent_messages = Message.objects(sender=u)
    received_messages = Message.objects(receiver=u)
    return jsonify(sent_messages=sent_messages,received_messages=received_messages)

## get user's message with one user
@message_app.route('/message/<name>',methods=['GET'])
@jwt_required
def get_message_with_someone(name,u):
    try:
        other = UserModel.objects(username=name)[0]
    except:
        return make_response("no that user to send message", 400)
    sent_messages = Message.objects(sender=u,receiver=other)
    received_messages = Message.objects(receiver=u,sender=other)
    return jsonify(sent_messages=sent_messages,received_messages=received_messages)

@message_app.route('/message/unread', methods=['GET'])
@jwt_required
def get_unreadmessage(u):
    print u.unreadMessages
    return jsonify(unreadMessages=u.unreadMessages)


@message_app.route('/message/<messageid>', methods=['DELETE'])
@jwt_required
def delete_message(messageid,u):
    message = Message.objects(id=messageid)[0]
    u.update(pull__unreadMessages=message)
    return make_response("delete complete", 200)

