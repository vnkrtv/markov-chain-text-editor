# smart-text-editor

[![Build Status](https://travis-ci.com/vnkrtv/smart-text-editor.svg?branch=master)](https://travis-ci.com/vnkrtv/smart-text-editor)

## Description  

Web application for editing text documents with support for intelligent typing based on relevant search in Elasticsearch.

## Installation  

As docker container:
- ```git clone https://github.com/vnkrtv/smart-text-editor.git && cd smart-text-editor```
- ```docker build -t smart-text-editor .``` - build application docker image
- Run application on 80 host port:  
```
docker run --name text-editor\
     -p 0.0.0.0:80:5000 \
     -e SECRET_KEY=<SECRET_KEY> \
     -e ELASTIC_HOST=<ELASTIC_HOST> \
     -e ELASTIC_SHARDS_NUMBER=<ELASTIC_SHARDS_NUMBER> \
     -e ELASTIC_REPLICAS_NUMBER=<ELASTIC_REPLICAS_NUMBER> \
     -d smart-text-editor
```

On windows:
- ```git clone https://github.com/vnkrtv/smart-text-editor.git && cd smart-text-editor```
- ```powershell .\deploy\deploy_on_win.ps1``` - create virtual environment and apply database migrations
- ```.\venv\Scripts\activate``` - activate virtual environment
- Set environment variables   
- ```gunicorn wsgi:app -b 0.0.0.0:80``` - run application on 80 host port
