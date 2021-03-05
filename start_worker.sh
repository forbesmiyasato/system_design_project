#! /bin/bash

cd /home/ubuntu/system_design_question
source ./env/bin/activate
cd project
gunicorn app:app &
python worker.py &
