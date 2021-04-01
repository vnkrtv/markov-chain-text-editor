FROM snakepacker/python:3.7
MAINTAINER vnkrtv

COPY requirements.txt /mnt/

RUN apt-get update && apt-get install -y python-dev libxml2-dev libxslt1-dev antiword unrtf poppler-utils pstotext tesseract-ocr \
  flac ffmpeg lame libmad0 libsox-fmt-mp3 sox libjpeg-dev swig libpulse-dev zlib1g-dev libpoppler-cpp-dev pkg-config
RUN apt-get install -y python3-venv build-essential python3-dev
RUN python3 -m venv /usr/share/python3/venv \
 && /usr/share/python3/venv/bin/pip install -U pip \
 && /usr/share/python3/venv/bin/pip install -Ur /mnt/requirements.txt

COPY . /usr/share/python3/
COPY deploy/entrypoint /entrypoint

ENTRYPOINT ["/entrypoint"]
