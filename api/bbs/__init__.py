from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.cors import CORS
import redis

app = Flask(__name__)
CORS(app)
app.config['MONGODB_SETTINGS'] = {
    'db': 'bbs_dev',
    'host': 'localhost',
    'port': 27017
}
db = MongoEngine(app)

redisClient = redis.StrictRedis(host='localhost', port=6379, db=0)

from views.user import user_app
from views.topic import topic_app
from views.search import search_app
from views.message import message_app
from views.node import node_app

app.register_blueprint(user_app)
app.register_blueprint(topic_app)
app.register_blueprint(search_app)
app.register_blueprint(message_app)
app.register_blueprint(node_app)