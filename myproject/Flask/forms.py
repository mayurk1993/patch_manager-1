from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, TextField


# from flask_table import Table, Col

class SignUpForm(FlaskForm):
    password = PasswordField('Refresh Token')
    submit = SubmitField('Submit')


class EnvironmentForm(FlaskForm):
    release_version = TextField('Release Version')
    environment = TextField('Environment')
    proceed = SubmitField('Proceed')


class RightScriptForm(FlaskForm):
    rs_name = TextField('Rightscript Name')
    confirm = SubmitField('Confirm')
