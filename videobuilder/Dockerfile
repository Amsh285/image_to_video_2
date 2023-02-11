# syntax=docker/dockerfile:1
FROM python:3.9-slim-buster@sha256:adb66cf3f0ff529d312460f57ca0a82f99dcb6b24a538b364e04e038acc16239
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5002
WORKDIR /image_to_video
COPY . .
EXPOSE 5002
CMD [ "flask", "run" ]