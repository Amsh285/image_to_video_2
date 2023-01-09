from flask import Flask, jsonify


from video_builder_cv2 import build_video_from_pngs

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

# GOTO: http://192.168.0.163:5000/rest/data/v1.0/json/en/generate/video/ to generate video
# @app.route('/rest/data/v1.0/json/en/generate/video/', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def generate_video():

    image_folder = 'mandy_pngs'
    video_name = 'video.mp4'     
    
    try:
        build_video_from_pngs(image_folder, video_name)

        return jsonify({'Video generated': True})
    except:
        return jsonify({'Video generated': False})

if __name__ == '__main__':   
    app.run()

    #app.run(host="0.0.0.0", port='5000', debug=True)
