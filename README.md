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

I am using unbabel-py package, but to use it with python 3.6, I had to change a few lines in the api.py file.

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

To get started, install Postgres and Redis on your local computer. I installed them using [Postgres.app](https://postgresapp.com/) and `brew install redis` in my Mac OS. The other necessary packages can be installed with:
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
FLASK_ENV=development
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

9) Run `python app.py` and access http://localhost:5000 on your browser.

#### Testing

```
python -m unittest main/tests/tests.py
```

Coverage report info:

```
(env) MacBook-Air-de-Carlos:backend-coding-challenge ribas$ coverage report
Name               Stmts   Miss  Cover
--------------------------------------
main/__init__.py       0      0   100%
main/forms.py          6      0   100%
main/models.py         9      0   100%
main/routes.py        41      0   100%
--------------------------------------
TOTAL                 56      0   100%
```