from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField, DecimalField, IntegerField
from flask_wtf.file import FileAllowed, FileRequired, FileField
from wtforms.validators import DataRequired, Email, Regexp, Length


class LoginForm(FlaskForm):
    email = StringField('Email', [DataRequired(), Email()])
    password = PasswordField('Password', [DataRequired()])


class NewCategory(FlaskForm):
    title = StringField('Title', [DataRequired(), Length(2, 50),
                                  Regexp('^[\w ]+$', message="Title must contain only letters & numbers")])
    status = SelectField('Status', choices=[('A', 'Active'), ('P', 'Pending'), ('S', 'Suspend')])


class NewProduct(FlaskForm):
    name = StringField('Name', [DataRequired(), Length(2, 254)])
    description = TextAreaField('Description')
    price = DecimalField('Price', [DataRequired()])
    stock = IntegerField('Stock', [DataRequired()])
    image = FileField('Image', [FileRequired(), FileAllowed(['jpg'], 'Extensions allowed .jpg only.')])
    category_id = IntegerField('Category', [DataRequired()])
    status = SelectField('Status', choices=[('A', 'Active'), ('P', 'Pending'), ('S', 'Suspend')])


class EditProduct(NewProduct):
    image = FileField('Image', [FileAllowed(['jpg'], 'Extensions allowed .jpg only.')])
