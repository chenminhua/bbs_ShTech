from flask import Blueprint, request, make_response, jsonify
from bbs.models import TopicModel
from bbs.models import UserModel
from bbs.utils import jwt_required

topic_app = Blueprint('topic_app', __name__)

## post a topic
@topic_app.route('/topic', methods=['POST'])
@jwt_required
def create(username):
    try:
        user = UserModel.objects(username=username)[0]
        form = request.form.to_dict()
        topic = TopicModel(title=form['title'],content=form['content'])
        topic.author = user
        topic.save()
        return make_response("create successfully",200)
    except:
        return make_response("create failure",400)

## edit a topic
@topic_app.route('/topic/<topic_id>', methods=['PUT'])
@jwt_required
def edit(topic_id,username):
    topic = TopicModel.objects(id=topic_id)[0]
    if topic.isAuthor(username):
        form = request.form.to_dict()
        topic.content = form['content']
        topic.title = form['title']
        topic.save()
        return make_response("edit successfully",200)
    else:
        return make_response("not owner",400)

## delete a topic
@topic_app.route('/topic/<topic_id>', methods=['DELETE'])
@jwt_required
def delete(topic_id,username):
    topic = TopicModel.objects(id=topic_id)[0]
    if topic.isAuthor(username):
        topic.delete()
        return make_response("delete successfully",200)
    else:
        return make_response("delete failure",400)

## get a topic
@topic_app.route('/topic/<topic_id>', methods=['GET'])
def get(topic_id):
    topic = TopicModel.objects(id=topic_id)[0]
    return jsonify(topic=topic)




