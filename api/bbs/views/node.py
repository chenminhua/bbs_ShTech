#coding:utf-8
from flask import request,Blueprint, jsonify, json, make_response
from bbs.models import Node
from bbs import configs

node_app = Blueprint("node_app",__name__)

@node_app.route('/node', methods=['POST'])
def create():
    form = request.get_json()
    node = Node(name=form['name'],label=form['label'],category=form['category'],popularity=1)
    node.save()
    return jsonify({"status":"ok"})

@node_app.route('/node/<name>', methods=['DELETE'])
def delete(name):
    node = Node.objects(name=name)
    node.delete()
    return make_response("ok",200)


#return the node's newest topic
@node_app.route('/node/<name>', methods=['GET'])
def get_nodes_topic(name):
    try:
        page = int(request.args['page'])
    except:
        page = 1
    try:
        node = Node.objects(name=name)[0]
    except:
        return make_response("no this topic", 400)
    topics = node.topics.order_by('-lastEdited_at').skip((page-1)*configs.TOPICS_IN_EVERYPAGE).limit(configs.TOPICS_IN_EVERYPAGE)
    topics = [t.topicConvert() for t in topics]
    return jsonify(topics=topics)

#返回全部node
@node_app.route('/node', methods=['GET'])
def get_nodes():
    categories = []
    for node in Node.objects:
        if node["category"] not in categories:
            categories.append(node["category"])
    return jsonify(nodes=Node.objects().order_by('-popularity'),categories=categories)

