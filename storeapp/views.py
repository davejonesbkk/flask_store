
import sqlite3
import os, base64

from flask import render_template, request, session, redirect, url_for, g, flash, abort, send_from_directory

from flask.ext.uploads import UploadSet, configure_uploads, IMAGES, UploadNotAllowed

import flask_bcrypt as bcrypt

from .forms import LoginForm, SignUpForm, AddBookForm

from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename


from storeapp import app

#UPLOAD_FOLDER = os.path.basename('uploads')
UPLOAD_FOLDER = '/Users/david/documents/projects/flask_store/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



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


@app.route('/signup', methods=['GET', 'POST'])
def signup():

	db = get_db()	

	cur = db.cursor()

	form = SignUpForm()
	if request.method == 'POST':
		if form.validate_on_submit():
			username = request.form.get("username")
			email = request.form.get("email")
			password1 = request.form.get("password1")
			password2 = request.form.get("password2")


			if password1 != password2:
				flash('Sorry your passwords must match, please try again')
				return redirect(url_for('signup'))
				


			hashed_pw = bcrypt.generate_password_hash(password1)

			try:
			
				db.execute('insert into users (username, email, password) values (?, ?, ?)',
					[username, email, hashed_pw])

				db.commit()

				flash('Thanks for registering')

				return redirect(url_for('index'))

			except sqlite3.IntegrityError:
				flash('Username already taken')


	return render_template('signup.html', form=form)




@app.route('/login', methods=('GET', 'POST'))
def login():

	form = LoginForm(request.form)
	if request.method == 'POST':
		username = request.form.get("username")
		password = request.form.get("password")
		completion = validate(username, password)
		if completion == False:
			flash('Invalid login, please try again. Are you registered?')
		else:
			flash('Logged in!')
			session['logged_in'] = True
			return redirect(url_for('members'))
	return render_template('login.html', form=form)

def validate(username, password):
	print('Inside validate')
	db = get_db()
	completion = False
	with db:
		cur = db.cursor()
		cur.execute('SELECT * FROM users')
		rows = cur.fetchall()
		for row in rows:
			dbUser = row[1]
			print(username)
			print(dbUser)
			dbPass = row[3]
			print(password)
			print(dbPass)
			if dbUser==username:
				validate_pw = bcrypt.check_password_hash(dbPass, password)
				print(validate_pw)
				if validate_pw == True:
					completion = True
					return completion
			#else:
				#flash('Invalid login!')
	return completion



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
	cur = db.execute('select title, author, category from books order by id desc')
	books = cur.fetchall()


	return render_template('books.html', books=books)

@app.route('/add', methods=['GET','POST'])
def addbook():
	if not session.get('logged_in'):
		abort(401)

	form = AddBookForm(request.form)
	if request.method == 'POST':
		#if form.validate_on_submit():
		title = request.form.get("title")
		author = request.form.get("author")
		category = request.form.get("category")
		imagefile = photos.save(request.files["image"])
		#imagefile = request.form.image.data
		print(imagefile)
		rec = Photo(imagefile=imagefile, user=g.user.id)
		rec.store()
		flash("Photo saved")
		#filename = secure_filename(imagefile.filename)
		#print(filename)
		#imagefile.save(os.path.join(
			#app.config['UPLOAD_FOLDER'], filename))
		db = get_db()	
		db.execute('insert into books (title, author, category, image) values (?, ?, ?)',
				[request.form['title'], request.form['author'], request.form['category'], filename])

		db.commit()
		flash('New book added!')

		return render_template('add.html', form=form)


	
	return render_template('add.html', form=form)

@app.route('/users')
def showusers():
	#if not session.get('logged_in'):
		#abort(401)
	db = get_db()
	cur = db.execute('select username from users order by id desc')
	members = cur.fetchall() 

	return render_template('users.html', members=members)


def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		#check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		#if user does not select file, browser also
		# submit a empty part without filename
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

			return redirect(url_for('send_file', filename=filename))
		

	return render_template('upload.html')


@app.route('/show/<filename>')
def uploaded_file(filename):
	
	return render_template('show.html', filename=filename)

@app.route('/uploads/<filename>')
def send_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)



 


















