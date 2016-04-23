# coding:utf-8
import datetime
from flask import Blueprint, request, make_response, jsonify, json
import jwt

from bbs import redisClient
from bbs.models import UserModel, TopicModel
from bbs import configs
from bbs.utils import jwt_required, sendEmail, forgetPass

user_app = Blueprint('user_app', __name__)

##register
@user_app.route('/user', methods=['POST'])
def register():
    form = request.get_json()
    #try:
    u = UserModel(nickname=form['nickname'],username=str(form['username']), password=str(form['password']), email=str(form['email']))
    if u.save():
        print "test"
        token = jwt.encode({'exp': configs.TOKEN_EXPIRATION, 'username': str(form['username'])}, configs.TOKEN_SECRET,
                           algorithm='HS256')
        sendEmail(str(u.email), token)
        return make_response("please activate your account", 200)
    else:
        return make_response('register failure', 400)  #用户名或邮箱不成功
        # except:
        #     return make_response('register failure',400)

##返回用户信息
@user_app.route('/user', methods=['GET'])
@jwt_required
def get_yourself(u):
    return jsonify(user=u.userConvert())

@user_app.route('/user/forgetpass', methods=['POST'])
def forgetpass():
    form = request.get_json()
    try:
        u = UserModel.objects(email=form['email'])[0]
    except:
        return make_response("no that user",400)
    u.changePassword(forgetPass(form['email']))
    return make_response("Please check your email to get your new password")

##signin
@user_app.route('/signin', methods=['POST'])
def signin():
    form = request.get_json()
    try:
        u = UserModel.objects(email=form['email'])[0]
    except:
        return make_response('no this user', 400)  #验证不成功或者邮箱错误
    if not u.is_activated():
        return make_response("please activate first", 200)
    if u.checkPassword(str(form['password'])):
        token = jwt.encode({'exp': configs.TOKEN_EXPIRATION, 'username': u.username}, configs.TOKEN_SECRET,
                           algorithm='HS256')
        return jsonify(token=token)  #登录成功则返回token,否则返回400
    else:
        return make_response('signin failure', 400)  #验证不成功


##logout
@user_app.route('/user', methods=['DELETE'])
def logout():
    try:
        token = request.headers["Authorization"][7:]
    except:
        return make_response("without token", 400)
    try:
        redisClient.setex(token, configs.REDIS_EXPIRATION, token)
    except:
        return make_response("logout failure due to redis", 400)
    return make_response("logout successful", 200)  #客户端注销


##列出user的topics
@user_app.route('/user/<username>/topics', methods=['GET'])
def get_snippets(username):
    try:
        u = UserModel.objects(username=username)[0]
    except:
        return make_response("no that user", 400)
    return jsonify(topics=u.topics)


##like一份topic
@user_app.route('/user/likes/<topic_id>', methods=['PUT'])
@jwt_required
def like(topic_id, u):
    try:
        topic = TopicModel.objects(id=topic_id)[0]
    except:
        return make_response("no that topic", 400)
    if u.is_liked(topic):
        return make_response("you have already liked this topic", 400)
    u.update(push__likes=topic)
    return make_response("liked it successfully", 200)


##取消收藏一份topic
@user_app.route('/user/likes/<topic_id>', methods=['DELETE'])
@jwt_required
def unlike(topic_id, u):
    try:
        topic = TopicModel.objects(id=topic_id)[0]
    except:
        return make_response("no that topic", 400)
    if not u.is_liked(topic):
        return make_response("you haven't liked this topic", 400)
    u.update(pull__likes=topic)
    return "ok"


##获取用户收藏topic
@user_app.route('/user/<username>/likes', methods=['GET'])
def getlikes(username):
    try:
        u = UserModel.objects(username=username)[0]
    except:
        return make_response("no that user", 400)
    topics = [t.topicConvert() for t in u.likes]
    return jsonify(likes=topics)


##follow某个用户
@user_app.route('/user/following/<name>', methods=['PUT'])
@jwt_required
def follow(name, u):
    try:
        other = UserModel.objects(username=name)[0]
    except:
        return make_response("no that user to be followed", 400)
    if u.is_following(other):
        return make_response("you have followed this user", 400)
    u.update(push__followings=other)
    return make_response("follow successful", 200)


##unfollow某个用户
@user_app.route('/user/following/<name>', methods=['DELETE'])
@jwt_required
def unfollow(name, u):
    try:
        other = UserModel.objects(username=name)[0]
    except:
        return make_response("no that user to be unfollowed", 200)
    if not u.is_following(other):
        return make_response("you haven't followed this user", 400)
    u.update(pull__followings=other)
    return make_response("unfollow successful", 200)


##获取某个用户follow的用户
@user_app.route('/user/<name>/following', methods=['GET'])
def get_followings(name):
    u = UserModel.objects(username=name)[0]
    return jsonify(followings=u.followings)


##获取某个用户的follower
@user_app.route('/user/<name>/follower', methods=['GET'])
def get_followers(name):
    u = UserModel.objects(username=name)[0]
    return jsonify(followers=u.followers)


##获取某个用户的信息
@user_app.route('/user/<name>', methods=['GET'])
def get_user(name):
    print name
    u = UserModel.objects(username=name)[0]
    return jsonify(user=u, followingsCount=u.followings_count, followersCount=u.followers_count)


@user_app.route('/user/password', methods=['PUT'])
@jwt_required
def changePass(u):
    form = request.get_json()
    if u.checkPassword(form['oldPass']) and form['newPass'] == form['newPass_confirmed']:
        u.changePassword(form['newPass'])
        return "ok"
    else:
        return make_response("old password wrong", 400)


@user_app.route('/user', methods=['PUT'])
@jwt_required
def changeuserinformation(u):
    form = request.get_json()
    print form
    if form['major'] != u'':
        u.major = str(form['major'])
    if form['hometown'] != u'':
        u.howntown = str(form['hometown'])
    if form['hobby'] != u'':
        u.hobby = str(form['hobby']).split(',')
    if form['description'] != u'':
        u.description = str(form['description'])
    if form['birthday'] != u'':
        print form['birthday']
        u.birthday = datetime.datetime.strptime(str(form['birthday']), "%Y-%m-%d")
    print u.major
    u.save()
    return make_response("change user information successfully!", 200)


@user_app.route('/user/activation/<token>', methods=['GET'])
def activition(token):
    try:
        username = jwt.decode(token, configs.TOKEN_SECRET)['username']
        u = UserModel.objects(username=username)[0]
        u.activation = True
        u.save()
        return make_response("activate successfully", 200)
    except:
        return make_response("no this user", 400)


