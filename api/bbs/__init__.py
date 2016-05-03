from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.cors import CORS
import redis

redisClient = redis.StrictRedis(host='localhost', port=6379, db=0)

from views.user import user_app
from views.topic import topic_app
from views.search import search_app
from views.message import message_app
from views.node import node_app
from views.image import image_app
from views.reply import reply_app


def create_app(**config_overrides):
    app = Flask(__name__)
    CORS(app)
    app.config['MONGODB_SETTINGS'] = {
        'db': 'bbs_dev',
        'host': 'localhost',
        'port': 27017
    }
    app.config.update(config_overrides)
    db = MongoEngine(app)

    app.register_blueprint(user_app)
    app.register_blueprint(topic_app)
    app.register_blueprint(search_app)
    app.register_blueprint(message_app)
    app.register_blueprint(node_app)
    app.register_blueprint(image_app)
    app.register_blueprint(reply_app)
    return app