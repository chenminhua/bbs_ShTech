# coding:utf-8
import datetime
from flask import Blueprint, request, make_response, jsonify, json
import jwt

from bbs import redisClient
from bbs.models import UserModel
from bbs.models import TopicModel
from bbs import configs
from bbs.utils import jwt_required, sendEmail, forgetPass, sliceList

user_app = Blueprint('user_app', __name__)

##用户注册
@user_app.route('/user', methods=['POST'])
def register():
    form = request.get_json()
    u = UserModel(username=str(form['username']), password=str(form['password']), email=str(form['email']))
    if u.create():
        token = jwt.encode({'exp': configs.TOKEN_EXPIRATION, 'username': str(form['username'])}, configs.TOKEN_SECRET, algorithm='HS256')
        #sendEmail(str(u.email), token)
        return make_response("please activate your account", 200)
    else:
        return make_response('register failure', 400)  #用户名或邮箱不成功

##返回用户信息
@user_app.route('/user', methods=['GET'])
@jwt_required
def get_yourself(u):
    return jsonify(user=u.get_yourself())

##获取某个用户的信息
@user_app.route('/user/<name>', methods=['GET'])
def get_user(name):
    username = request.headers['Username'] if request.headers.has_key('Username') else "";
    u = UserModel.objects(username=name)[0]
    user_rest = u.userConvert()
    if username:
        requser = UserModel.objects(username=username)[0]
        print requser.is_following(u)
        user_rest['is_following'] = requser.is_following(u)
    return jsonify(user=user_rest)
##修改user信息
@user_app.route('/user', methods=['PUT'])
@jwt_required
def changeuserinformation(u):
    form = request.get_json()
    if form.has_key('major') and form['major']:
        u.major = form['major']
    if form.has_key('hometown') and form['hometown']:
        u.hometown = form['hometown']
    if form.has_key('hobby') and form['hobby']:
        u.hobby = form['hobby'].split(',')
    if form.has_key('description') and form['description']:
        u.description = form['description']
    if form.has_key('birthday') and form['birthday']:
        try:
            u.birthday = datetime.datetime.strptime(form['birthday'], "%Y-%m-%d")
        except:
            make_response("the birthday format is invalid",400)
    if form.has_key('avatar_url') and form['avatar_url']:
        u.avatar_url = form['avatar_url']
    u.save()
    return make_response("change user information successfully!", 200)

##修改密码
@user_app.route('/user/forgetpass', methods=['POST'])
def forgetpass():
    form = request.get_json()
    try:
        u = UserModel.objects(email=form['email'])[0]
    except:
        return make_response("no that user",400)
    u.changePassword(forgetPass(form['email']))
    return make_response("Please check your email to get your new password")

##登录
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
        token = jwt.encode({'exp': configs.TOKEN_EXPIRATION, 'username': u.username}, configs.TOKEN_SECRET, algorithm='HS256')
        return make_response(jsonify(token=token),200)  #登录成功则返回token,否则返回400
    else:
        return make_response('signin failure', 400)  #验证不成功

##注销
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



##修改密码
@user_app.route('/user/password', methods=['PUT'])
@jwt_required
def changePass(u):
    form = request.get_json()
    if u.checkPassword(form['oldPass']) and form['newPass'] == form['newPass_confirmed']:
        u.changePassword(form['newPass'])
        return "ok"
    else:
        return make_response("old password wrong", 400)

##激活
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


##列出user的topics
@user_app.route('/user/<username>/topics', methods=['GET'])
def get_snippets(username):
    try:
        page = int(request.args['page'])
    except:
        page = 1
    try:
        u = UserModel.objects(username=username)[0]
    except:
        return make_response("no that user", 400)
    topics = u.topics.order_by('-created_at').skip((page-1)*configs.TOPICS_IN_EVERYPAGE).limit(configs.TOPICS_IN_EVERYPAGE)
    topics = [t.topicConvert() for t in topics]
    return jsonify(topics=topics)


##获取用户收藏topic
@user_app.route('/user/<username>/likes', methods=['GET'])
def getlikes(username):
    try:
        page = int(request.args['page'])
    except:
        page = 1
    try:
        u = UserModel.objects(username=username)[0]
    except:
        return make_response("no that user", 400)
    topics = sliceList(u.likes, configs.TOPICS_IN_EVERYPAGE,page)
    topics = [t.topicConvert() for t in topics]
    return jsonify(likes=topics)

##获取某个用户follow的用户
@user_app.route('/user/<name>/following', methods=['GET'])
def get_followings(name):
    try:
        page = int(request.args['page'])
    except:
        page = 1
    u = UserModel.objects(username=name)[0]
    followings = sliceList(u.followings, configs.USERS_IN_EVERYPAGE,page)
    followings = [u.userConvert() for u in followings]
    return jsonify(followings=followings)

##获取某个用户的follower
@user_app.route('/user/<name>/follower', methods=['GET'])
def get_followers(name):
    try:
        page = int(request.args['page'])
    except:
        page = 1
    u = UserModel.objects(username=name)[0]
    followers = sliceList(u.followers, configs.USERS_IN_EVERYPAGE,page)
    followers = [u.userConvert() for u in followers]
    return jsonify(followers=followers)
