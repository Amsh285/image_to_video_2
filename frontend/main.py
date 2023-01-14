from flask import Flask, render_template, request, send_file, Response
import requests
import base64

#flask --app main run
#flask --app frontend/main run --port=5000

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/upload_images")
def navigate_upload_images():
    return render_template("imageupload.html")

@app.route("/download_images")
def navigate_download_images():
    return render_template("imagedownload.html")

@app.route("/create_video")
def navigate_create_video():
    return render_template("videodownload.html")

@app.route("/save_files", methods=["post"])
def save_images():
    payload = list()

    for file in request.files.getlist("imgs"):
        t = file.read()
        payload.append((file.filename, base64.b64encode(t)))

    result = requests.post(url='http://127.0.0.1:5001/save_files', data=payload)
    return result.text, result.status_code

@app.route("/load_files", methods=["get"])
def load_files():
    request_file_names = request.args.get("filenames")
    terminator = request.args.get("terminator")

    file_names = request_file_names.split(terminator)

    payload = {'filenames': file_names}
    result = requests.get(url="http://127.0.0.1:5001/load_files", data=payload)

    if result.status_code == 200:
        return Response(result.content, mimetype='application/zip', status=200)

    return result.text, result.status_code


@app.route("/request_generate_video", methods=["post"])
def request_generate_video():
    request_file_names = request.form.get("filenames")
    terminator = request.form.get("terminator")
    video_name = request.form.get("videoname")

    file_names = request_file_names.split(terminator)
    payload = {'videoname': video_name, 'filenames': file_names}

    result = requests.post(url="http://127.0.0.1:5002/build_videos_from_repo", data=payload)

    return result.text, result.status_code
