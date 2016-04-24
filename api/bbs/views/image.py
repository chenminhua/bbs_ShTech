import os
from flask import Blueprint, request, make_response, send_file, jsonify
from bbs.models import Image
import shortuuid


image_app = Blueprint("image_app",__name__)

from bbs.models import Image

ALLOWED_EXTENSION = set(['jpg','JPG','png','PNG','jpeg','JPEG','gif','GIF'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSION

@image_app.route('/image', methods=['POST'])
def post():
    file = request.files['file']
    if file and allowed_file(file.filename):
        img = Image()
        img.uuid, img.title, img.photo = shortuuid.ShortUUID().random(length=8), file.filename, file
        img.save()
    return jsonify(uuid=img.uuid)

@image_app.route('/image/<image_id>', methods=['GET'])
def get(image_id):
    try:
        img = Image.objects(uuid=image_id)[0]
    except:
        return make_response("no that pic", 200)
    return send_file(img.photo.thumbnail, mimetype='image/png')