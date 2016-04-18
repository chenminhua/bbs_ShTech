#coding:utf-8
__author__ = 'chenminhua'

from functools import wraps
import jwt
from bbs import configs
from flask import request, make_response
from bbs import redisClient

def jwt_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        token = request.headers["Authorization"][7:]
        if redisClient.get(token):             #如果已经注销了，就返回400,表示token错误
            return make_response("failure",400)
        username = jwt.decode(token, configs.TOKEN_SECRET)['username']
        return func(*args, username=username, **kwargs)   #token验证通过，将用户信息传入后续函数，并执行

    return wrapper

