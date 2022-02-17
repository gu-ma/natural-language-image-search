# CPU image for the API
ARG BASE_IMAGE=python:3.8
FROM $BASE_IMAGE

RUN pip install -U pip
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
RUN pip install git+https://github.com/openai/CLIP.git
RUN pip install flask flask_restful flask_cors
