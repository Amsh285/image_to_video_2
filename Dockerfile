# syntax=docker/dockerfile:1
FROM python:3.9-slim-buster
WORKDIR /video
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
COPY . .
EXPOSE 5000
ENV FLASK_APP=RestServiceVideoBuilder.py
ENTRYPOINT [ "flask"]
CMD [ "run", "--host", "0.0.0.0" ]