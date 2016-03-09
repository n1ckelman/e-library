from app import models
from flask.ext.wtf import Form, SelectField, TextField, TextAreaField, SubmitField, validators, ValidationError, PasswordField
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

class SignupForm(Form):
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  password = PasswordField('Password', [validators.Required("Please enter a password.")])
  submit = SubmitField("Create account")
 
  def validate(self):
    if not Form.validate(self):
      return False
     
    user = models.User.query.filter_by(email = self.email.data.lower()).first()
    if user:
      self.email.errors.append("That email is already taken")
      return False
    else:
      return True	

class LoginForm(Form):
    email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
    password = PasswordField('Password', [validators.Required("Please enter a password.")])