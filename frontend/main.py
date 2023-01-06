from flask import Flask, render_template, request, send_file

app = Flask(__name__)

#flask --app main run

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/process_images", methods=["post"])
def process_images():
    #print(request.files.getlist("imgs"))
    #print(request.files["imgs"])

    for img in request.files.getlist("imgs"):
        print(img.filename)

    print(request.files.getlist("imgs")[1])
    print(request.files.getlist("imgs")[1].filename)

    return "eine nette meldung"
