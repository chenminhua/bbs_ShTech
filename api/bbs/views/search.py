#coding:utf-8
from flask import Blueprint, request, make_response, jsonify

from bbs.models import UserModel,TopicModel

search_app = Blueprint('search_app',__name__)

##查询snippet
@search_app.route('/search/topic', methods=['GET'])
def search_snippet():
    try:
        q = request.args['q']
        topics = TopicModel.objects(title__contains=q)
        return jsonify(topics=topics)
    except:
        return make_response("error",400)

##查询user
@search_app.route('/search/user', methods=['GET'])
def search_user():
    try:
        q = request.args['q']
        users = UserModel.objects(username__contains=q)
        return jsonify(users=users)
    except:
        return make_response("error",400)