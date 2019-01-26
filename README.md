#Flask Store

A webstore running on Flask, currently with the following functionality:

- User signup with Flask WTF forms
- User login & logout
- Password hashing & salting
- Image upload

<h3>Installation:</h3>

<b>Clone this repo</b>

```
git clone https://github.com/davejonesbkk/flask_store.git
```

<b>Create a Python 3 virtualenv</b>

```
virtualenv -p python3 env
```

<b>Start the virtualenv</b>

```
source env/bin/activate
```

<b>Install pip requirements (need to have Python pip installed)</b>

```
pip install -r requirements.txt
```

<b>Setup the Flask app & run it</b>

```
export FLASK_APP=run.py

flask run
```
