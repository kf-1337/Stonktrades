## Getting started

## Install python 3.12.0 from:
https://www.python.org/downloads/release/python-3120/

## Navigate to path:
cd <path_to_app>/stonktrades

## create virtual environment
python -m venv venv

## activate virtual environment
venv/Scripts/activate

## update pip installer if needed
python.exe -m pip install --upgrade pip

## install all modules via the requirements.txt 
pip install -r requirements.txt

## init the DB and the users "admin" and "user"
python init_db.py

## start the app
python stonktrades.py

## login to the users with the password: "password"

## Happy breaking of code :>