import os
import shutil
from flask import Flask, jsonify, request
import requests
import base64
import pika

from video_builder_cv2 import build_video_from_pngs

import io
from zipfile import ZipFile

app = Flask(__name__)
#app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

#flask --app videobuilder\main run --port=5002

#@app.route('/', methods=['GET', 'POST'])
# GOTO: http://localhost:5002/rest/data/v1.0/json/en/generate/video/ to generate video
@app.route('/rest/data/v1.0/json/en/generate/video/', methods=['GET', 'POST'])
def generate_video():

    image_folder = 'mandy_pngs'
    video_name = 'video.mp4'     
    
    try:
        build_video_from_pngs(image_folder, video_name)

        return jsonify({'Video generated': True})
    except:
        return jsonify({'Video generated': False})

@app.route("/build_videos_from_repo", methods={'GET', 'POST'})
def build_videos_from_repo():
    filenames = request.form.getlist("filenames")
    video_name = request.form.get("videoname")
    
    payload = {'videoname': video_name, 'filenames': filenames}
    result = requests.get(url="http://image_to_video.repo:5001/load_files", data=payload)
    #print(result.content)
    zip_stream = io.BytesIO(result.content)
    if(not video_name.endswith(".mp4")):
        video_name = video_name + ".mp4"

    image_folder = os.path.join(app.instance_path, "temp_images")
    if os.path.exists(image_folder):
        shutil.rmtree(image_folder)
        
    os.makedirs(image_folder, exist_ok=True)

    with ZipFile(zip_stream, 'r') as zf:
        image_names = [file_name for file_name in zf.namelist() if file_name.endswith(".png")]
        images = [(zf.open(name).read(), name) for name in image_names]

        for img in images:
            with open(os.path.join(image_folder, img[1]), "wb") as binary_file:
                binary_file.write(img[0])

        build_video_from_pngs(image_folder, video_name)

    with open(video_name, "rb") as file:
        result = requests.post(url='http://image_to_video.repo:5001/save_video', files={"video": file})
        return result.text, result.status_code

    return "internal server error", 500

if __name__ == "__main__":
    app.run()


#if __name__ == '__main__':   
    #app.run()

   # app.run(host="0.0.0.0", port='5002', debug=True)
