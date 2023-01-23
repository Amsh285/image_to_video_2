import cv2
import os

import os
import shutil
import requests
import pika

import io
from zipfile import ZipFile


def build_video_from_pngs(image_folder: str, video_name: str = "output.mp4"):

    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape
    
    #print("Video saved to:", os.getcwd())

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(video_name, fourcc, 5, frameSize=(width,height))
    
    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))
    
    cv2.destroyAllWindows()
    video.release()
    
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

    payload = str(body).split(';')
    filenames = payload[1].split(' ')
    video_name =str(payload[0]).replace("b'","")
    filenames[-1] = filenames[-2]
    payload = {'videoname': video_name, 'filenames': filenames}
    print(payload)
    result = requests.get(url="http://image_to_video.repo:5001/load_files", data=payload)

    zip_stream = io.BytesIO(result.content)
    if(not video_name.endswith(".mp4")):
        video_name = video_name + ".mp4"

    image_folder = os.path.join("./", "temp_images")
    if os.path.exists(image_folder):
        shutil.rmtree(image_folder)
        
    os.makedirs(image_folder, exist_ok=True)

    with ZipFile(zip_stream, 'r') as zf:
        image_names = [file_name for file_name in zf.namelist() if file_name.endswith(".png")]
        images = [(zf.open(name).read(), name) for name in image_names]

        for img in images:
            with open(os.path.join(image_folder, img[1]), "wb") as binary_file:
                binary_file.write(img[0])

        build_video_from_pngs(image_folder, video_name)

        with open(video_name, "rb") as file:
            requests.post(url='http://image_to_video.repo:5001/save_video', files={"video": file})
    return


def main():
    print(' executing queue code')
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'image_queue', port = 5672, credentials=pika.PlainCredentials("guest", "guest")))
    
        channel = connection.channel()

        channel.queue_declare(queue='VideoComposer')
        channel.basic_consume(queue='VideoComposer',
                      auto_ack=True,
                      on_message_callback=callback)


        print(' [*] Waiting for messages. To exit press CTRL+C')

        channel.start_consuming()
    except Exception as e:
        print("Ex occ:"  + repr(e))

if __name__ == "__main__":
    main()
