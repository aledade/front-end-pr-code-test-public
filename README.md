# Installation guide

## Install system dependencies

You will need Python installed, along with developer libraries.

You should also install and configure `git`, `npm`, and `sqlite3`
however you desire on your system.

## Retrieve assets with Bower

    npm install -g bower
    bower install

## Set up a virtual environment

    python3 -m venv venv
    source venv/bin/activate
    pip3 install -r requirements.txt
    
## Initialize the SQLite database

    python manage.py db init
    python manage.py db migrate
    python manage.py build_demo_data

## Run server

    python manage.py runserver
    
Navigate your browser to http://127.0.0.1:5000/