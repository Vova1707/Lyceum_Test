from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import PasswordField, SubmitField, IntegerField, FileField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    id_astronaft = IntegerField("id астронавта", validators=[DataRequired()])
    password_astronaft = PasswordField("Пароль астронавта", validators=[DataRequired()])
    id_capitan = IntegerField("id капитана", validators=[DataRequired()])
    password_capitan = PasswordField("Пароль капитана", validators=[DataRequired()])
    submit = SubmitField("Войти", validators=[FileRequired()])


class GalleryForm(FlaskForm):
    file = FileField("Выберите файл")
    submit = SubmitField("Сохранить")
