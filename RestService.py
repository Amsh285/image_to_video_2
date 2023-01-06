import os
import json
from flask import Flask, flash, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import numpy as np
from keras.models import load_model
import imageio
import requests

UPLOAD_FOLDER = '../uploads/'
maxrecord = 0
allrecords = []
oneFilename = 'uploads\\8.png'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/rest/data/v1.0/json/en/upload/image/png/', methods=['GET', 'POST'])
def upload_file():
    filename = ""
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = oneFilename #secure_filename(file.filename)
            file.save(filename)
            #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #return redirect(url_for('download_file', name=filename))
            id = maxrecord
            #create_record(id, 'uploads\\' + filename)
            return jsonify({'id': id})         
    else:
        return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
@app.route('/rest/data/v1.0/json/en/identify_number/image/', methods=['GET'])
def identify():
    id = request.args.get('id')
    path = query_records(id)
    if path == 'error':
        return jsonify({'error': 'data not found'})
   
    #TODO: insert Code here to actually test the value
    # LOAD IMAGE
    image = imageio.v2.imread(oneFilename)   
    # Scale images to the [0, 1] range
    x_test = image.astype("float32") / 255
    # Make sure images have shape (28, 28, 1)
    x_test = np.expand_dims(x_test, -1)
    prediction = model.predict(np.expand_dims(x_test,0))
    
    predicted_number = int(np.argmax(prediction))
    #print('\n\t===> Predicted Number:', predicted_number, '<===')
    #print('\n\t     Is this correct? Check your Input Image!')
    confidence = []
    for i in range(10):
        confidence.append(str(i)+'-->'+str(np.round(prediction[0][i]*100))+'%')
    
    return jsonify({'identified_number': predicted_number, 'confidence': confidence})
    

def query_records(name):
    path = allrecords[int(name)]
    if path and len(path) > 3:
        return path
    return 'error'

def create_record(name, filename):
    global maxrecord

    # record = json.loads({name: filename})

    # with open('data.txt', 'r') as f:
    #     data = f.read()
    # if not data:
    #     records = [record]
    # else:
    #     records = json.loads(data)
    # updated = False
    # # for r in records:
    # #     if r[name] != filename:
    # #         r[name] = filename
    # #         updated = True
    # if not updated:
    #     records.append(record)
    #     allrecords.append(record)
    #     maxrecord = int(maxrecord) + 1

    # with open('data.txt', 'w') as f:
    #     f.write(json.dumps(records, indent=2))

# def get_records():
#     with open('data.txt', 'r') as f:
#         data = f.read()
#     if data:

#         return json.loads(data)
#     else:
#         return {}


if __name__ == '__main__':   
    allrecords = {0: 'uploads\\8.png'} #get_records()
    # for r in allrecords:
    #     for ar in r:
    #         if int(ar) > maxrecord:
    #             maxrecord = int(ar) + 1

    #TODO: insert global Code here load model once, etc
    # LOAD MODEL
    model = load_model('PREDICTOR.h5')

    app.run(debug=True)
