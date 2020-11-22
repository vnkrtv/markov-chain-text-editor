# markov-chain-text-editor

[![Build Status](https://travis-ci.com/vnkrtv/markov-chain-text-editor.svg?branch=master)](https://travis-ci.com/vnkrtv/markov-chain-text-editor)

## Description  

Web application for editing text documents with support for intelligent typing based on Markov chains.

## Installation  

As docker container:
- ```git clone https://github.com/vnkrtv/markov-chain-text-editor.git```
- ```cd markov-chain-text-editor```
- ```docker build -t markov-chain-text-editor .``` - build application docker image
- ```docker run --name text-editor -p 0.0.0.0:80:5000 -d markov-chain-text-editor``` - run application on 80 host port  

On windows:
- ```git clone https://github.com/vnkrtv/markov-chain-text-editor.git```
- ```cd markov-chain-text-editor```
- ```powershell .\deploy\deploy_on_win.ps1``` - create virtual environment and apply database migrations
- ```.\venv\Scripts\activate``` - activate virtual environment
- ```gunicorn wsgi:app -b 0.0.0.0:80``` - run application on 80 host port
