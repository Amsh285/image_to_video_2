from flask import Flask, render_template, request, send_file
import requests
import base64

#app = Flask(__name__)
#app.run(host='127.0.0.1', port=5001)
#app.run(debug=True, port=8001)

#flask --app main run
#flask --app frontend/main run --port=5000

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('imageupload.html')

@app.route("/upload_images")
def navigate_upload_images():
    return render_template("imageupload.html")

@app.route("/save_images", methods=["post"])
def process_images():
    #print(request.files)

    #requests.post(url='http://127.0.0.1:5001/save_images', data=request.files.to_dict(flat=False))


    #payload = {'ich': 'bin', 'extrem': 'dumm'}
    payload = list()

    for file in request.files.getlist("imgs"):
        t = file.read()
        payload.append((file.filename, base64.b64encode(t)))

    requests.post(url='http://127.0.0.1:5001/save_images', data=payload)

    return "tolo"

