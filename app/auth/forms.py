from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=50)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=50)])
    submit = SubmitField('Login')

class SettingsForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=25)])
    old_password = PasswordField('Current Password', validators=[DataRequired(), Length(min=5, max=50)])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=5, max=50)])
    new_conf_password = PasswordField('New Password Confirm', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change Password')