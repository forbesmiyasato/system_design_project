sudo apt install nginx python3-venv python3-dev awscli

aws config #aws credentials and configurations

create file /etc/nginx/site-enabled/app

sudo service nginx restart

In project director

python3 -m venv env

source env/bin/activate

pip install -r requirements.txt

cd project

gunicorn app:app

access at http://52.27.158.127/80
