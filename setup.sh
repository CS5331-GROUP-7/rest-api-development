#!/bin/sh
set -e
apt install python-pip -y
pip install --upgrade pip
pip install -r requirements.txt --user
