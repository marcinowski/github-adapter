#!/usr/bin/env bash

if [[ -e venv/bin/activate ]]; then
    echo "Virtualenv directory found."
else
    echo "Virtualenv directory not found."
    pip install virtualenv
    echo "Setting up venv"
    virtualenv venv
fi
echo "Activating venv"
source venv/bin/activate
echo "Installing requirements."
pip install -r requirements.txt
echo "Runserver on port 5000"
python src/app.py
