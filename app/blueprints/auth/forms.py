from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField 
from wtforms.validators import DataRequired, Email, EqualTo, Length

class SignUpForm(FlaskForm):
    email    = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=10, max=25, message="Password must be between 10 and 25 characters.")])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LogInForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=10, max=25, message="Password must be between 10 and 25 characters.")])
    confirm_new_password = PasswordField("Confirm New Password", validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change Password')