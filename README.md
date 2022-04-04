# Reversi-Team2

## Requirements
* `pip install mysql-connector-python`
or manually download here: https://dev.mysql.com/downloads/connector/python/
* I'm using python 3.9.10

## Setup environment
1. `virtualenv --python={path to python executable here} env`
  * Note: You may need to install virtualenv via `pip3 install virtualenv` or `brew install virtualenv`
  * Note: to find your python3 path, run `which python3`
2. `source env/bin/activate`
3. `pip install --upgrade pip`
4. `pip install -r requirements.txt`

## Database Info
* Online database was set on a virtual machine IP: 144.202.8.233 PORT: 3306
* username: team2
* password: password123
* database: reversi

## Run the game
In the command line, run: `python3 main.py`
