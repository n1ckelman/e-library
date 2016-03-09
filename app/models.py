from app import db
from sqlalchemy import *
from werkzeug import generate_password_hash, check_password_hash

authors_books = db.Table('authors_books', 
    db.Column('book_id', Integer, ForeignKey('books.id')),
    db.Column('author_id', Integer, ForeignKey('authors.id'))
)

class Book(db.Model):
	__tablename__ = 'books'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), index=True, unique=True)
	authors = db.relationship(
		"Author",
		secondary = authors_books,
		backref="books_of_authors",
		passive_deletes=True)

	def __repr__(self):
		return '%s' % (self.title)

class Author(db.Model):
	__tablename__ = 'authors'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), index=True, unique=True)
	books = db.relationship(
		"Book",
		secondary=authors_books,
		backref="authors_books",
		cascade="all, delete-orphan",
		passive_deletes = True,
		single_parent=True)

	def __repr__(self):
		return '%s' % (self.name)

class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key = True)
  email = db.Column(db.String(120), unique=True)
  password = db.Column(db.String(54))
   
  def __init__(self, email, password):
    self.email = email.lower()
    self.password = password

  def is_authenticated(self):
    return True

  def is_active(self):
    return True

  def is_anonymous(self):
    return False

  def get_id(self):
    return unicode(self.id)    