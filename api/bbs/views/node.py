from flask import request,Blueprint, jsonify, json, make_response
from bbs.models import Node

node_app = Blueprint("node_app",__name__)

@node_app.route('/node', methods=['POST'])
def create():
    form = request.get_json()
    node = Node(name=form['name'],label=form['label'],popularity=1)
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
        node = Node.objects(name=name)[0]
    except:
        return make_response("no this topic", 400)
    return jsonify(topics=node.topics())

@node_app.route('/node', methods=['GET'])
def get_nodes():
    return jsonify(nodes=Node.objects())