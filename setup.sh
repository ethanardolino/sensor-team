#!/bin/bash

# create a virtual environment for this project
python3 -m venv venv
source venv/bin/activate

# install dependencies in venv
pip install --upgrade pip
pip install -r requirements.txt
