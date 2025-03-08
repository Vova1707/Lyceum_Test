from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import FileField,  PasswordField, StringField, SubmitField, EmailField, IntegerField
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


class JobsForm(FlaskForm):
    job_title = StringField('Название работы', validators=[DataRequired()])
    work_size = IntegerField('Размер работы', validators=[DataRequired()])
    coloborators = StringField('Колобораторы', validators=[DataRequired()])
    submit = SubmitField("Сохранить")


class EditJobsForm(FlaskForm):
    job_title = StringField('Название работы', validators=[DataRequired()])
    work_size = IntegerField('Размер работы', validators=[DataRequired()])
    coloborators = StringField('Колобораторы', validators=[DataRequired()])
    submit = SubmitField("Сохранить")


class DepartmentForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    members = StringField('Члены экипажа', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    submit = SubmitField("Сохранить")