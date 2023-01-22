# syntax=docker/dockerfile:1
FROM python:3.9-slim-buster
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN apt-get update

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
WORKDIR /image_to_video
COPY . .
EXPOSE 5000
CMD [ "flask", "run" ]