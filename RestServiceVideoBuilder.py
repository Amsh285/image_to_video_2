import os
import json
from flask import Flask, flash, request, redirect, url_for, jsonify


from video_builder_cv2 import build_video_from_pngs

oneFilename = 'uploads\\8.png'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# GOTO: http://127.0.0.1:5000/rest/data/v1.0/json/en/generate/video/ to generate video
@app.route('/rest/data/v1.0/json/en/generate/video/', methods=['GET', 'POST'])
def generate_video():

    image_folder = 'mandy_pngs'
    video_name = 'video.mp4'     
    
    try:
        build_video_from_pngs(image_folder, video_name)

        return jsonify({'Video generated': True})
    except:
        return jsonify({'Video generated': False})

if __name__ == '__main__':   
    app.run(debug=True)
