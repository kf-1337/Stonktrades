from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo

class DeleteUserForm(FlaskForm):
    userid1 = IntegerField('Userid', validators=[DataRequired()])
    username1 = StringField('Username', validators={DataRequired()})
    submit1 = SubmitField('Delete User')


class UserRoleChangeForm(FlaskForm):
    userid2 = IntegerField('Userid', validators=[DataRequired()])
    username2 = StringField('Username', validators={DataRequired()})
    role2 = SelectField('Choose Role', choices=[('Admin', 'Admin'),('User', 'User'),('Guest', 'Guest')])
    submit2 = SubmitField('Change Roll of User')
