from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    id_astronaft = IntegerField('id астронавта', validators=[DataRequired()])
    password_astronaft = PasswordField('Пароль астронавта', validators=[DataRequired()])
    id_capitan = IntegerField('id капитана', validators=[DataRequired()])
    password_capitan = PasswordField('Пароль капитана', validators=[DataRequired()])
    submit = SubmitField('Войти')