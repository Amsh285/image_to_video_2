from flask import Flask, request, send_file
import base64
import os

from glob import glob
from io import BytesIO
from zipfile import ZipFile

app = Flask(__name__)

#flask --app repository/main run --port=5001

@app.route("/test", methods=["get"])
def test():
    return "ahoi";

@app.route("/save_files", methods=["post"])
def upload_files():
    form_data = request.form.to_dict()

    image_folder = os.path.join(app.instance_path, "upload_images")
    os.makedirs(image_folder, exist_ok=True)

    for b in request.form.to_dict():
        byte_content = base64.b64decode(form_data[b])

        with open(os.path.join(image_folder, b), "wb") as binary_file:
            binary_file.write(byte_content)

    return {'message': 'File(s) saved successful.'}, 201


@app.route("/load_files", methods={"get"})
def download_files():
    filenames = request.form.getlist("filenames")
    image_folder = os.path.join(app.instance_path, "upload_images")
    stream = BytesIO()

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
