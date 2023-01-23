# syntax=docker/dockerfile:1
FROM python:3.9-slim-buster
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN apt-get update

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5001
WORKDIR /image_to_video_2
COPY . .
EXPOSE 5001
CMD [ "flask", "run" ]