import os
from flask import Blueprint, request, make_response, send_file
from bbs.models import Image
import shortuuid


image_app = Blueprint("image_app",__name__)

from bbs.models import Image

ALLOWED_EXTENSION = set(['jpg','JPG','png','PNG','jpeg','JPEG','gif','GIF'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSION

@image_app.route('/image', methods=['POST'])
def post():
    print "fuck"
    file = request.files['file']
    if file and allowed_file(file.filename):
        img = Image()
        img.uuid = shortuuid.ShortUUID().random(length=8)
        img.title = file.filename
        img.photo = file
        img.save()
        print img.uuid
    return make_response("upload successfully",200)

@image_app.route('/image/<image_id>', methods=['GET'])
def get(image_id):
    try:
        img = Image.objects(uuid=image_id)[0]
    except:
        return make_response("no that pic", 200)

    return send_file(img.photo, mimetype='image/png')