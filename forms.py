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


from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, IntegerField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    surname = StringField('Фамилия пользователя', validators=[DataRequired()])
    age = IntegerField("Лет")
    submit = SubmitField('Войти')
    position = StringField('Позиция', validators=[DataRequired()])
    speciality = StringField('Специальность', validators=[DataRequired()])
