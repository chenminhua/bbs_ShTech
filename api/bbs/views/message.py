from flask import Blueprint, request, make_response, jsonify, json
from bbs.utils import jwt_required
from bbs.models.message import Message
from bbs.models.user import UserModel
from bbs import configs

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
    print request.data
    message = Message(content=form['content'])
    message.sender = u
    message.receiver = other
    message.save()
    other.unreadMessages_count += 1
    other.save()
    return "ok"

## get user's message
@message_app.route('/message', methods=['GET'])
@jwt_required
def get_message(u):
    try:
        page = int(request.args['page'])
    except:
        page = 1
    received_messages = u.messages.order_by('-sent_at').skip((page-1)*configs.TOPICS_IN_EVERYPAGE).limit(configs.TOPICS_IN_EVERYPAGE)
    received_messages = [m.messageConvert() for m in received_messages]
    u.unreadMessages_count = 0
    u.save()
    return jsonify(received_messages=received_messages)

