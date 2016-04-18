from flask import Flask
from flask.ext.mongoengine import MongoEngine
import redis

app = Flask(__name__)
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

app.register_blueprint(user_app)
app.register_blueprint(topic_app)
app.register_blueprint(search_app)