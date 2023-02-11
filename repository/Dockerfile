# syntax=docker/dockerfile:1
FROM python:3.9-slim-buster@sha256:adb66cf3f0ff529d312460f57ca0a82f99dcb6b24a538b364e04e038acc16239
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN apt-get update

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5001
WORKDIR /image_to_video
COPY . .
EXPOSE 5001
CMD [ "flask", "run" ]