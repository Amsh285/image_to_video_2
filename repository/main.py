from flask import Flask, render_template, request, send_file

app = Flask(__name__)

#flask --app repository/main run --port=5001

@app.route("/test", methods=["get"])
def test():
    return "ahoi";

@app.route("/save_images", methods=["post"])
def upload_images():
    #print(request.get_data())
    print("ich bin wirklich dumm!")
    #print(request.get_data(as_text=True))
    print(request.form.to_dict())

    formdata = request.form.to_dict()

    for b in request.form.to_dict():
        print(formdata[b])

    return "hoi"
