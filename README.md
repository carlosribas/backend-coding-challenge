# Unbabel Backend Challenge

## Challenge

1) Build a basic web app with a simple input field that takes an English (EN) input translates it to Spanish (ES).
2) When a new translation is requested it should add to a list below the input field (showing one of three status: requested, pending or translated) - (note: always request human translation)
3) The list should be dynamically ordered by the size of the translated messages

#### Requirements
* Use Flask web framework
* Use PostgreSQL
* Create a scalable application. 
* Only use Unbabel's Translation API on sandbox mode
* Have tests

#### Notes
* Page load time shouldnt exceed 1 second

#### Resources
* Unbabel's API: http://developers.unbabel.com/

## About my code

I changed some lines from the api.py file to work with python 3.6. I am still working on this challenge, but this version already works. Features missing: 

- Scalable application
- More mock tests 
- Dynamic updates?

#### Instalation

1) Clone my repository:
```
git clone https://github.com/carlosribas/backend-coding-challenge.git
```

2) Create the virtualenv (I'm using python 3.6):
```
cd backend-coding-challenge
virtualenv --python=python3.6  env
source env/bin/activate
```

3) Install packages:

To get started, install Postgres and Redis on your local computer. I installed using [Postgres.app](https://postgresapp.com/) and `brew install redis` in my Mac OS. The other necessary packages can be installed with:
```
pip install -r requirements.txt
``` 

4) Once you have Postgres installed and running, create a database to use as local development database and a database to use for testing:
``` 
$ psql
# create database db_name;
CREATE DATABASE
# create database db_testing_name;
CREATE DATABASE
# \q
``` 

5) Create a .env file with:
```
SECRET_KEY="your-secret-key"
APP_SETTINGS="config.DevelopmentConfig"
DATABASE_URL="postgresql://localhost/db_name"
DATABASE_TESTING="postgresql://localhost/db_testing_name"
USERNAME="your-unbabel-username"
API_KEY="your-unbabel-key"
REDIS_URL="redis://localhost:6379"
``` 
 
6) Create table:
```
python manage.py db migrate
python manage.py db upgrade
``` 

7) Open a new terminal to run redis:
```
redis-server
``` 

8) In another terminal window, start a worker process to listen for queued tasks:
```
cd backend-coding-challenge
source env/bin/activate
python worker.py
``` 

9) Access http://localhost:5000 on your browser.

#### Testing

```
python -m unittest tests/tests.py
```