from flask import Flask, request, send_file
import base64
import os

from glob import glob
from io import BytesIO
from zipfile import ZipFile

app = Flask(__name__)

#flask --app repository/main run --port=5001

@app.route("/test", methods=["get", "post"])
def test():
    return "ahoi";

@app.route("/save_files", methods=["get", "post"])
def upload_files():
    form_data = request.form.to_dict()
    video_name = request.form.get("videoname")
    if video_name is None:
        video_name = ""
    image_folder = os.path.join(app.instance_path, "upload_images", video_name)
    os.makedirs(image_folder, exist_ok=True)

    for b in request.form.to_dict():
        if (b!="videoname"):
            byte_content = base64.b64decode(form_data[b])
            if(len(byte_content) > 0):
                with open(os.path.join(image_folder, b), "wb") as binary_file:
                    binary_file.write(byte_content)

    return list_files(), 201

@app.route("/save_video", methods=["get", "post"])
def save_video():
    video_folder = os.path.join(app.instance_path, "upload_videos")
    os.makedirs(video_folder, exist_ok=True)
    
    if(bool(request.files.get('video', False)) == True and len(request.files) > 0):
        file_data = request.files["video"]   
        file_data.save(os.path.join(video_folder, file_data.filename))

    return list_videos(), 201

@app.route("/load_files", methods={"get", "post"})
def download_files():
    try:
        filenames = request.form.getlist("filenames")
        video_name = request.form.get("videoname")
    
        if video_name is None:
            video_name = request.args.get("videoname")
        if filenames is None or len(filenames) < 1:
            filenames = request.args.getlist("filenames")

        if video_name is None:
            video_name = ""

        print("repo got: "+ video_name+"," +filenames)
    except Exception as e:
         print("Exception: "+ repr(e))

    image_folder = os.path.join(app.instance_path, "upload_images", video_name)

    stream = BytesIO()

    with ZipFile(stream, 'w') as zf:
        for filename in filenames:
            try:
                zf.write(os.path.join(image_folder, filename), filename)
            except FileNotFoundError:
                return f'File: {image_folder} {filename} could not be found', 404
            except IOError:
                return f'File: {filename} could not be processes', 500
            except OSError:
                return f'File: {filename} could not be processes', 500
    stream.seek(0)

    return send_file(stream, as_attachment=True, download_name="archive.zip")

@app.route("/load_video", methods={"get", "post"})
def download_videos():
    filenames = request.form.getlist("filenames")
    image_folder = os.path.join(app.instance_path, "upload_videos")
    stream = BytesIO()
    print(f"folder:{image_folder} {filenames}")
    with ZipFile(stream, 'w') as zf:
        for filename in filenames:
            try:
                zf.write(os.path.join(image_folder, filename), filename)
            except FileNotFoundError:
                return f'File: {filename} could not be found', 404
            except IOError:
                return f'File: {filename} could not be processes', 500
            except OSError:
                return f'File: {filename} could not be processes', 500
    stream.seek(0)

    return send_file(stream, as_attachment=True, download_name="archive.zip")

@app.route("/show_video", methods={"get", "post"})
def show_video():
    filename = request.form.get("filename")
    
    image_folder = os.path.join(app.instance_path, "upload_videos")
    
    #stream = BytesIO()
    #with open(os.path.join(image_folder, filename), "rb") as bif:
    #    content = bif.read()
    #    stream.write(content)
    #    stream.seek(0)

    return send_file(open(os.path.join(image_folder, filename), "rb"), mimetype="video/mp4", download_name=filename)

def list_files():
    image_folder = os.path.join(app.instance_path, "upload_images")
    strTablefirst = "\n" #"<table>\n"
    strTableEntry = "filename " #"<tr><td>filename</td></tr>\n"
    strTablelast = "\n" #"</table>"
    tableEntries = ""
    for filename in os.listdir(image_folder):
        if os.path.isfile(os.path.join(image_folder, filename)):
            tableEntries = tableEntries + strTableEntry.replace("filename", filename)
        else:
            for filename2 in os.listdir(os.path.join(image_folder, filename)):
                tableEntries = tableEntries + strTableEntry.replace("filename", filename + "/" + filename2)
    return strTablefirst + tableEntries + strTablelast

def list_videos():
    image_folder = os.path.join(app.instance_path, "upload_videos")
    strTablefirst = "\n" #"<table>\n"
    strTableEntry = "filename " #"<tr><td>filename</td></tr>\n"
    strTablelast = "\n" #"</table>"
    tableEntries = ""
    for filename in os.listdir(image_folder):
        if os.path.isfile(os.path.join(image_folder, filename)):
            tableEntries = tableEntries + strTableEntry.replace("filename", filename)
    return strTablefirst + tableEntries + strTablelast