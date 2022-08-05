from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Email, DataRequired, EqualTo, ValidationError, Length
from apps.authentication.models import Users
from apps.authentication.util import check_password_policy

#login
class LoginForm(FlaskForm):
    username = StringField('Username', id='username_login', validators=[DataRequired()])
    password = PasswordField('Password', id='pwd_login', validators=[DataRequired()])


#registration
class CreateAccountForm(FlaskForm):
    firstname = StringField('Firstname', validators=[DataRequired()])
    lastname = StringField('Lastname', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    agreement = BooleanField('I agree to the terms', validators=[DataRequired()])
    submit = SubmitField('Submit')

    #custom validators
    def validate_username(self, username):
        username_len = 4
        if len(username.data) < username_len:
            raise ValidationError(f'Username should be at least {username_len} characters long')

        user = Users.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username already registered')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email already registered')

    def validate_password(self, password):
        if check_password_policy(password.data) is None:
            raise ValidationError('Please use a stronger password')        

#reset password request
class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

#reset password
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Submit')        

    def validate_password(self, password):
        if check_password_policy(password.data) is None:
            raise ValidationError('Please use a stronger password')