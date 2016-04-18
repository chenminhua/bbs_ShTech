#coding:utf-8
import datetime
from flask import Blueprint, request, make_response, jsonify
import jwt

from bbs import redisClient
from bbs.models import UserModel,TopicModel
from bbs import configs
from bbs.utils import jwt_required

user_app = Blueprint('user_app',__name__)

##register
@user_app.route('/user',methods=['POST'])
def register():
    form = request.form.to_dict()
    try:
        u = UserModel(username=form['username'], password=form['password'],email=form['email'])
        if u.save():
            token = jwt.encode({'exp': configs.TOKEN_EXPIRATION, 'username':form['username']}, configs.TOKEN_SECRET,algorithm='HS256')
            return jsonify(token=token)   #注册成功则返回token，否则返回400
        else:
            return make_response('register failure', 400) #用户名或邮箱不成功
    except:
        return make_response('register failure',400)

##signin
@user_app.route('/signin',methods=['POST'])
def signin():
    form = request.form.to_dict()
    try:
        u = UserModel.objects(email=form['email'])[0]
        if u.checkPassword(str(form['password'])):
            token = jwt.encode({'exp': configs.TOKEN_EXPIRATION, 'username':u.username},configs.TOKEN_SECRET ,algorithm='HS256')
            return jsonify(token=token)    #登录成功则返回token,否则返回400
        else:
            return make_response('signin failure', 400)   #验证不成功
    except:
        return make_response('signin failure',400)  #验证不成功或者邮箱错误

##logout
@user_app.route('/user',methods=['DELETE'])
def logout():
    try:
        token = request.headers["Authorization"][7:]
        redisClient.setex(token, configs.REDIS_EXPIRATION, token)
        return make_response("logout successful",200)    #客户端注销
    except:
        return make_response("logout failure", 400)

##列出user的topics
@user_app.route('/user/<username>/topics',methods=['GET'])
def get_snippets(username):
    try:
        u = UserModel.objects(username=username)[0]
        return jsonify(topics=u.topics)
    except:
        return make_response("failure",400)

##like一份topic
@user_app.route('/user/likes/<topic_id>',methods=['PUT'])
@jwt_required
def like(topic_id, username):
    u = UserModel.objects(username=username)[0]
    topic = TopicModel.objects(id=topic_id)[0]
    u.update(push__likes=topic)
    return "ok"

##取消收藏一份topic
@user_app.route('/user/likes/<topic_id>', methods=['DELETE'])
@jwt_required
def unlike(topic_id, username):
    u = UserModel.objects(username=username)[0]
    topic = TopicModel.objects(id=topic_id)[0]
    u.update(pull__likes=topic)
    return "ok"

##获取用户收藏topic
@user_app.route('/user/<username>/likes', methods=['GET'])
def getlikes(username):
    try:
        u = UserModel.objects(username=username)[0]
        return jsonify(likes=u.likes)
    except:
        return make_response("failure",400)

##follow某个用户
@user_app.route('/user/following/<name>', methods=['PUT'])
@jwt_required
def follow(name, username):
    u = UserModel.objects(username=username)[0]
    other = UserModel.objects(username=name)[0]
    if u.is_following(other):
        return make_response("you have followed this user",400)
    u.update(push__followings=other)
    return make_response("follow successful",200)

##unfollow某个用户
@user_app.route('/user/following/<name>', methods=['DELETE'])
@jwt_required
def unfollow(name, username):
    u = UserModel.objects(username=username)[0]
    other = UserModel.objects(username=name)[0]
    if not u.is_following(other):
        return make_response("you haven't followed this user",400)
    u.update(pull__followings=other)
    return make_response("unfollow successful",200)

##获取某个用户follow的用户
@user_app.route('/user/<name>/following',methods=['GET'])
def get_followings(name):
    u = UserModel.objects(username=name)[0]
    return jsonify(followings=u.followings)

##获取某个用户的follower
@user_app.route('/user/<name>/follower',methods=['GET'])
def get_followers(name):
    u = UserModel.objects(username=name)[0]
    return jsonify(followers=u.followers)

##获取某个用户的信息
@user_app.route('/user/<name>', methods=['GET'])
def get_user(name):
    print name
    u = UserModel.objects(username=name)[0]
    return jsonify(user=u,followingsCount=u.followings_count,followersCount=u.followers_count)

