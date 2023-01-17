import os
import shutil
from flask import Flask, jsonify, request
import requests
import base64

from video_builder_cv2 import build_video_from_pngs

import io
from zipfile import ZipFile

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

#flask --app videobuilder\RestServiceVideoBuilder run --port=5002

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

@app.route("/build_videos_from_repo", methods={"post"})
def build_videos_from_repo():
    filenames = request.form.getlist("filenames")
    video_name = request.form.get("videoname")

    payload = {'filenames': filenames}
    result = requests.get(url="http://127.0.0.1:5001/load_files", data=payload)

    zip_stream = io.BytesIO(result.content)

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

    shutil.rmtree(image_folder)
    payload = list()

    with open(video_name, "rb") as file:
        result = requests.post(url='http://127.0.0.1:5001/save_video', files={"video": file})
        return result.text, result.status_code

    return "internal server error", 500


if __name__ == '__main__':   
    app.run()

    #app.run(host="0.0.0.0", port='5000', debug=True)
