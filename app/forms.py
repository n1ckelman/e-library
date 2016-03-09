from flask.ext.wtf import Form
from wtforms import TextField, SelectField
from wtforms.validators import Required
from config import SEARCH_CHOICES

class BookForm(Form):
	title = TextField('title', validators = [Required()])
	authors = TextField('authors')

class AuthorForm(Form):
	name = TextField('name', validators = [Required()])	

class SearchForm(Form):
	search = TextField('search')
	target = SelectField('target', choices = [('authors', 'authors'), ('books', 'books')], validators=[Required()])