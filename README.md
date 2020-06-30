# Warbler
Warblers are bright and beautiful songbirds, known for their distinctive **TWEETS**!

Warbler is a Twitter clone, built entirely with Python and postgreSQL, with features such as user signup/login, update/delete profile, follow users and like their tweets.

## Setup
Create your Python virtual environment:
```
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
```

Set up the database:
```
(venv) $ createdb warbler
(venv) $ python seed.py
```

Start the server:
```
(venv) $ flask run
```
