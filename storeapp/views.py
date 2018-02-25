
import sqlite3
import os

from flask import render_template, request, session, redirect, url_for, g, flash, abort
from flask.ext.bcrypt import Bcrypt 

from .forms import LoginForm, SignUpForm

from storeapp import app 

app.config.update(dict(
	DATABASE=os.path.join(app.root_path, 'store.db'),
	SECRET_KEY='vqE/O0iNhARuC1e6c9AM9mg0C2DLUGkHfrZDwN3/qgHJFdYP14TRmIuZngPrrwKVd1KcD+KfyEkh/yxxkPyi5nhlyk8OF32wC6HM',
	USERNAME='admin',
	PASSWORD='default'
))
app.config.from_envvar('STOREAPP_SETTINGS', silent=True)

def connect_db():
	#connects to the db
	rv = sqlite3.connect(app.config['DATABASE'])
	rv.row_factory = sqlite3.Row 
	return rv 

def init_db():
	db = get_db()
	with app.open_resource('schema.sql', mode='r') as f:
		db.cursor().executescript(f.read())
	db.commit()

@app.cli.command('initdb')
def initdb_command():
	#inits the db
	init_db()
	print('Initialized the database')


def get_db():
	#Opens a new DB connection if there is none for the app
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db=connect_db()
	return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
	#closes the db at end of request
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()




@app.route('/')
def index():
	db = get_db()
	cur = db.execute('select title, author from books order by id desc')
	books = cur.fetchall()

	return render_template('index.html', books=books)

@app.route('/signup-form')
def signup_form():

	return render_template('signup.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = SignUpForm()
	username = request.form.get("username")
	email = request.form.get("email")
	password1 = request.form.get("password1")
	password2 = request.form.get("password2")

	if password1 != password2:
		return redirect(url_for('signup'))

	pw_hash = Bcrypt.generate_password_hash(password1).decode('utf-8')


	db = get_db()
	db.execute('insert into users (username, email, pw_hash) values (?, ?)', 
		request.form['username'], request.form['email'], request.form['password1'])

	return redirect(url_for('signup_form'))




@app.route('/login', methods=('GET', 'POST'))
def login():
	form = LoginForm()
	if request.method == 'POST':
		if form.validate_on_submit():
			session['logged_in'] = True
			flash('You were logged in')
			return redirect(url_for('members'))
	return render_template('login.html', form=form)

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('index'))

@app.route('/members')
def members():

	if not session.get('logged_in'):
		abort(401)

	return render_template('members.html')

@app.route('/books')
def books():

	db = get_db()
	cur = db.execute('select title, author, category from entries order by id desc')
	entries = cur.fetchall()


	return render_template('books.html', entries=entries)

@app.route('/add', methods=['POST'])
def addbook():
	if not session.get('logged_in'):
		abort(401)
	db = get_db()	
	db.execute('insert into books (title, author, category) values (?, ?, ?)',
				[request.form['title'], request.form['author'], request.form['category']])

	db.commit()
	flash('New book added!')
	return redirect(url_for('books'))



"""
@app.route('/add', methods=['GET', 'POST'])
def addbook():
	if not session.get('logged_in'):
		flash('You need to be logged in to access this page')
		return redirect(url_for('login'))

	form = AddBookForm()x`
	if request.method == 'POST':
		if form.validate_on_submit():
			return redirect(url_for('books'))

	
	return render_template('add.html', form=form)

"""








