#coding:utf-8
__author__ = 'chenminhua'

from functools import wraps
import jwt
from bbs import configs
from flask import request, make_response
from bbs import redisClient
from bbs.models.user import UserModel

def jwt_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            token = request.headers["Authorization"][7:]
        except:
            return make_response("no valid token",400)
        print token
        # if redisClient.get(token):             #如果已经注销了，就返回400,表示token错误
        #     print "logged out"
        #     return make_response("has been logged out",400)
        username = jwt.decode(token, configs.TOKEN_SECRET)['username']
        print username
        try:
            u = UserModel.objects(username=username)[0]
        except:
            return make_response("no that user",200)
        print u
        if not u.activation:
            return make_response("please activate first", 400)
        return func(*args, u=u, **kwargs)   #token验证通过，将用户信息传入后续函数，并执行

    return wrapper

import os
import smtplib
from email.mime.text import MIMEText
from bbs.configs import SMTP_CONFIG

SMTPserver = SMTP_CONFIG['SMTPserver']
sender = SMTP_CONFIG['sender']
password = SMTP_CONFIG['password']

def send(destination, msg):
    mailserver = smtplib.SMTP(SMTPserver, 25)
    mailserver.login(sender, password)
    mailserver.sendmail(sender, [destination], msg.as_string())
    mailserver.quit()

def sendEmail(destination, token):
    message = 'please click the link below to activate your account! \n'
    url = 'http://localhost:6677/user/activation/'+str(token)
    msg = MIMEText(message+url)
    msg['Subject'] = '上科大BBS注册账号激活'
    msg['From'] = sender
    msg['To'] = str(destination)
    send(destination, msg)

def forgetPass(destination):
    message = 'Your new password is: \n'
    newpassword = ''.join(map(lambda xx:(hex(ord(xx))[2:]),os.urandom(3)))
    msg = MIMEText(message+str(newpassword))
    msg['Subject'] = '上科大BBS账号新密码'
    msg['From'] = sender
    msg['To'] = str(destination)
    send(destination, msg)
    return newpassword

import re
def Istechid(string):
    if re.search(r'(.+)@shanghaitech.edu.cn', string):
        return True
    else:
        return False

import datetime
def timeGapWithNow(time):
	dt = datetime.datetime.now() - time
	if dt.total_seconds() < 60:
		return "%d 秒前" %dt.seconds

	if dt.total_seconds() < 60*60:
		return "%d 分前" % (dt.total_seconds() / 60)

	if dt.total_seconds() < 60*60*24:
		return "%d 小时前" % (dt.total_seconds() / (3600))

	if dt.total_seconds() < 60*60*24*365:
		return "%d 天前" % dt.days

	if dt.total_seconds() >= 60*60*24*365:
		return "%d 年 %d 天前" % (dt.days/365, dt.days%365)


def sliceList(l, per, page):
	start = (page-1)*per
	end = (page)*per
	length = len(l)
	if start >=length:
		return []
	if start <length and end >=length:
		return l[start:length]
	if end <length:
		return l[start:end]

