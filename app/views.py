from flask import render_template, flash, redirect, session, url_for, request, g
from app import app, db, login_manager
from flask.ext.login import login_user, logout_user, current_user, login_required
from models import Book, Author, User
from forms import AuthorForm, BookForm, SearchForm, SignupForm, LoginForm

@login_manager.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.before_request
def before_request():
	g.user = current_user  

@app.route('/')
@app.route('/index')
@login_required
def index():
	authors = Author.query.all()
	return render_template('index.html', authors=authors)

@app.route('/add_author', methods=['POST', 'GET'])
@login_required
def add_author():
	form = AuthorForm()
	if request.method == 'POST':
		author = Author(name=form.name.data)
		db.session.add(author)
		db.session.commit()
		flash('New author was successfully added!')
	return render_template('add.html', 
							elem = 'author', 
							form=form)

@app.route('/add_book/<author_name>', methods=['POST', 'GET'])
@login_required
def add_book(author_name):
	form = BookForm()
	form.authors.data = author_name
	if request.method == 'POST':
		author = Author.query.filter_by(name=form.authors.data).first()
		if (author):
			book = Book(title=form.title.data)
			book.authors.append(author)
			db.session.add(book)
			db.session.commit()
			flash('New book was successfully added!')
		else:
			return render_template('add.html', elem = 'book', form=form,
									error = "Author with name " + form.authors.data + 
									" was not found. ")
	return render_template('add.html', 
							elem = 'book', 
							form=form)

@app.route('/edit/author/<id>' , methods=['POST', 'GET'])
@login_required
def edit_author(id):
	form = AuthorForm()
	author = Author.query.get(id)
	form.name.data = author.name
	if request.method == 'POST':		
		author.name = request.form['name']
		db.session.commit()
		flash('Author was successfully edited!')
	return render_template('edit.html', form=form, elem='author', 
							name=author.name)

@app.route('/delete/author/<id>' , methods=['POST', 'GET'])
@login_required
def delete_author(id):
	author = Author.query.get(id)
	db.session.delete(author)
	db.session.commit()
	flash ('deleted')
	   
	return redirect(url_for('index'))			

@app.route('/edit/book/<id>' , methods=['POST', 'GET'])
@login_required
def edit_book(id):
	form = BookForm()
	book = Book.query.get(id)
	if request.method == 'POST':		
		book.title = request.form['title']
		book.authors[0] = Author.query.filter_by(name=form.authors.data).first()
		db.session.commit()
		flash('Book was successfully edited!')
	return render_template('edit.html', form=form, elem='book', 
							name=book.title)

@app.route('/delete/book/<id>' , methods=['POST', 'GET'])
@login_required
def delete_book(id):
	book = Book.query.get(id)
	db.session.delete(book)
	db.session.commit()
	flash ('deleted')
	   
	return redirect(url_for('index'))	    									

@app.route('/search', methods=['GET', "POST"])
def search():
		form = SearchForm()
		if request.method=='POST':
			if form.target.data == 'authors':
				results = Author.query.filter(Author.name.ilike('%' + form.search.data + '%')).all()
			else:
				results = Book.query.filter(Book.title.ilike('%' + form.search.data + '%')).all()
			return render_template('search.html', results=results, form=form)
		return render_template('search.html', form=form)	
	

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = SignupForm()
   
  if request.method == 'POST':
	if form.validate() == False:
	  return render_template('signup.html', form=form)
	else:   
	  newuser = User(form.email.data, form.password.data)
	  db.session.add(newuser)
	  db.session.commit()

	  session['email'] = newuser.email
	  flash('Registration complete. Please, login in system')
	  return redirect('/login')
  return render_template('signup.html', form=form)
   
@app.route('/login', methods=['GET', 'POST'])
def login():
#	if g.user is not None and g.user.is_authenticated():
#	  return redirect(url_for('index'))
	form = LoginForm()
	if request.method == 'POST':
		user = User.query.filter_by(email = form.email.data).first()
		if form.validate_on_submit():
			if (form.password.data == user.password):
				login_user(user)
				flash('Logged in successfully.')
			else:
				flash("Incorrect credintials. Try again")	
				return render_template('login.html', form=form)

		return index()
	return render_template('login.html', form=form)	      

@app.route("/logout")
@login_required
def logout():
	logout_user()
	flash('Logged out')
	return redirect('/login')	

@login_manager.unauthorized_handler
def unauthorized():
    return login()