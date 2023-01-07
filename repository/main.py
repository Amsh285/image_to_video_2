from flask import Flask, render_template, request, send_file, Response
import base64
import os


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

@app.route("/load_images", methods={"get"})
def download_files():
    form_data = request.form.to_dict()
    print(form_data)

    return 200
