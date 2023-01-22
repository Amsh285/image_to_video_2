from flask import Flask, render_template, request, send_file, Response
import requests
import base64
import os

#flask --app main run
#flask --app frontend/main run --port=5000

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/upload_images")
def navigate_upload_images():
    payload = list()
    result = requests.post(url='http://127.0.0.1:5001/save_files', data=payload)
    return render_template("imageupload.html", filenames=result.text)

@app.route("/download_images")
def navigate_download_images():
    payload = list()
    result = requests.post(url='http://127.0.0.1:5001/save_files', data=payload)
    return render_template("imagedownload.html", filenames=result.text)

@app.route("/create_video")
def navigate_create_video():
    payload = list()
    result = requests.post(url='http://127.0.0.1:5001/save_files', data=payload)
    return render_template("videodownload.html", filenames=result.text)

@app.route("/show_video")
def navigate_show_video():
    payload = list()
    result = requests.post(url='http://127.0.0.1:5001/save_video', data=payload)
    
    d1 = '<a target="_blank" href="/show_video/'
    d2 = '">'
    d3 = '</a> \n'
    alllinks = ""
    file_names = result.text.split(" ")
    for fn in file_names:
        if(len(fn)> 2):
            alllinks = alllinks + d1 + fn + d2 + fn + d3
    return render_template("videoshow.html", filenames=alllinks)

@app.route("/save_files", methods=["post"])
def save_images():
    payload = list()

    video_name = request.form.get("videoname")
    payload.append(("videoname", video_name))

    for file in request.files.getlist("imgs"):
        t = file.read()
        payload.append((file.filename, base64.b64encode(t)))

    result = requests.post(url='http://127.0.0.1:5001/save_files', data=payload)
    #return result.text, result.status_code
    return render_template("imageupload.html", filenames=result.text)

@app.route("/load_files", methods=["get"])
def load_files():
    request_file_names = request.args.get("filenames")
    terminator = request.args.get("terminator")

    video_name = request.args.get("videoname")
    

    file_names = request_file_names.split(terminator)
    print("folder:" + video_name)
    payload = {'filenames': file_names, 'videoname': video_name}

    result = requests.get(url="http://127.0.0.1:5001/load_files", data=payload)

    if result.status_code == 200 or result.status_code == 201:
        return Response(result.content, mimetype='application/zip', status=200)
    
    #payload = list()
    #result = requests.post(url='http://127.0.0.1:5001/save_files', data=payload)
    return render_template("imagedownload.html", filenames=result.text)
    #return result.text, result.status_code


@app.route("/request_generate_video", methods=["post"])
def request_generate_video():
    request_file_names = request.form.get("filenames")
    terminator = request.form.get("terminator")
    video_name = request.form.get("videoname")

    file_names = request_file_names.split(terminator)
    payload = {'videoname': video_name, 'filenames': file_names}

    result = requests.post(url="http://127.0.0.1:5002/build_videos_from_repo", data=payload)

    #payload = list()
    #result = requests.post(url='http://127.0.0.1:5001/save_video', data=payload)
    return render_template("videodownload.html", filenames=result.text)
    #return result.text, result.status_code

@app.route("/request_old_video", methods=["post"])
def request_old_video():
    request_file_names = str(request.form.get("videonames"))
    terminator = request.args.get("terminator")
    
    fnx = ""
    file_names = request_file_names.split(terminator)
    for fn in file_names:
        fnx = fnx + ":" + fn + ":"
    payload = {'filenames': file_names}
    result = requests.get(url="http://127.0.0.1:5001/load_video", data=payload)

    if len(file_names) > 0 and (result.status_code == 200 or result.status_code == 201):
        return Response(result.content, mimetype='application/zip', status=200)

    payload = list()
    result = requests.post(url='http://127.0.0.1:5001/save_video', data=payload)
    
    d1 = '<a target="_blank" href="/show_video/'
    d2 = '">'
    d3 = '</a> \n'
    alllinks = ""
    for fn in file_names:
        if(len(fn)> 2):
            alllinks = alllinks + d1 + fn + d2 + fn + d3

    return render_template("videoshow.html", filenames=alllinks)

@app.route("/show_video/<filename>")
def show_old_video(filename):
    return render_template("videoshow2.html", filename=filename)

@app.route('/display/<filename>')
def display_video(filename):
    payload = {'filename': filename}
	
    result = requests.get(url="http://127.0.0.1:5001/show_video", data=payload)
    
    #if result.status_code == 200 or result.status_code == 201:
    return Response(result.content, mimetype="video/mp4")
    #return send_file(os.path.join("./", filename))