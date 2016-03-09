from flask import render_template, flash, redirect, session, url_for, request, g
from app import app, db
from models import Book, Author
from forms import AuthorForm, BookForm, SearchForm

@app.route('/')
@app.route('/index')
def index():
	authors = Author.query.all()
	return render_template('index.html',
							authors=authors)

@app.route('/add_author', methods=['POST', 'GET'])
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
def delete_author(id):
    author = Author.query.get(id)
    db.session.delete(author)
    db.session.commit()
    flash ('deleted')
	   
    return redirect(url_for('index'))			

@app.route('/edit/book/<id>' , methods=['POST', 'GET'])
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
