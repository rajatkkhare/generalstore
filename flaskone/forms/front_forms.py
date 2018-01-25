from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from flaskone.models import User


class RegisterForm(FlaskForm):
    first_name = StringField('First Name', [DataRequired(), Length(2, 50)])
    last_name = StringField('Last Name', [DataRequired(), Length(2, 50)])
    email = StringField('Email', [DataRequired(), Email(), Length(2, 50)])
    phone = StringField('Phone', [Length(10, 15)])
    address = TextAreaField('Address', [DataRequired(), Length(2, 254)])
    avatar = FileField('Image', [FileRequired(), FileAllowed(['jpg'], 'Extensions allowed .jpg only.')])
    password = PasswordField('Password', [DataRequired(), Length(6, 254),
                                          EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm Password', [DataRequired()])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).count():
            raise ValidationError('Email already in use.')


class LoginForm(FlaskForm):
    email = StringField('Email', [DataRequired(), Email()])
    password = PasswordField('Password', [DataRequired()])
