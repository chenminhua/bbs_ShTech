from flask import Blueprint, request, make_response, jsonify, json
from bbs.models import TopicModel, Node
from bbs.models import UserModel
from bbs.utils import jwt_required

topic_app = Blueprint('topic_app', __name__)

## post a topic
@topic_app.route('/topic', methods=['POST'])
@jwt_required
def create(u):
    form = request.get_json()
    try:
        node = Node.objects(name=str(form['node']))[0]
    except:
        return make_response("no that node",400)
    topic = TopicModel(title=str(form['title']),content=str(form['content']))
    topic.node = node
    topic.author = u

    topic.save()
    return make_response("create successfully",200)


## edit a topic
@topic_app.route('/topic/<topic_id>', methods=['PUT'])
@jwt_required
def edit(topic_id,u):
    topic = TopicModel.objects(id=topic_id)[0]
    if topic.isAuthor(u):
        form = request.get_json()
        topic.content = form['content']
        topic.title = form['title']
        topic.save()
        return make_response("edit successfully",200)
    else:
        return make_response("not owner",400)

## delete a topic
@topic_app.route('/topic/<topic_id>', methods=['DELETE'])
@jwt_required
def delete(topic_id,u):
    topic = TopicModel.objects(id=topic_id)[0]
    if topic.isAuthor(u):
        topic.delete()
        return make_response("delete successfully",200)
    else:
        return make_response("delete failure",400)

## get a topic
@topic_app.route('/topic/<topic_id>', methods=['GET'])
def get(topic_id):
    topic = TopicModel.objects(id=topic_id)[0]
    return jsonify(topic=topic)




