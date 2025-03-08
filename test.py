import os
import random

from werkzeug.utils import secure_filename

from data.db_session import create_session
from forms import LoginForm, GalleryForm, RegisterForm, JobsForm
from flask import Flask, url_for, request, flash
from flask import render_template, redirect
import json
from data import db_session
from data.users import User, Jobs
from flask_login import LoginManager, login_required, logout_user, login_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOAD_FOLDER'] = 'C:/Users/konde/PycharmProjects/Test_10/static/k'

# инициализируем LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/jobs_register', methods=['GET', 'POST'])
def jobs():
    '''
    Регистрация работы через форму JobsForm()
    '''
    form = JobsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs(
            team_leader=form.team_leader,
            job=form.job_title,
            work_size=form.work_size,
            collaborators=form.coloborators,
        )
        db_sess.add(job)
        db_sess.commit()
        return redirect('/login')
    return render_template('jobs_form.html', title='Регистрация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    '''
    Регистрация пользователя через форму RegisterForm()
    '''
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            print(form.password.data, form.password_again.data)
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            age=form.age.data,
            surname=form.surname.data,
            position=form.position.data,
            speciality=form.speciality.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/member')
def member():
    '''Подтягивает данные с fixtures/crew.json'''
    with open('fixtures/crew.json', 'r', encoding='utf-8') as f:
        crew_data = json.load(f)
    member = random.choice(crew_data)
    return render_template('member.html', member=member)


@app.route('/gallery', methods=['GET', 'POST'])
def gallery():
    form = GalleryForm()
    if form.validate_on_submit():
        f = form.file.data
        filename = secure_filename(f.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        f.save(filepath)
        return redirect(url_for('gallery'))
    image_files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], f))]
    image_urls = [url_for('static', filename=os.path.join('img/', img)) for img in image_files]
    print(image_urls)
    return render_template('galery.html', title='Галерея', form=form, images=image_urls)


@app.route("/index/<level>")
def index(level):
    return render_template('index.html', level=level)


@app.route("/training/<prof>")
def profession(prof):
    return render_template('training.html', profession=prof)


@app.route("/list_prof/<list>")
def list_prof(list):
    return render_template('list_prof.html', list=list)

@app.route("/table/<sex>/<int:year>")
def table(sex, year):
    return render_template('table.html', sex=sex, year=year)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        session = create_session()
        user = session.query(User).filter(User.email == email).first()
        if user:
            login_user(user)
            flash('Вы успешно вошли!', 'success')
            return redirect(url_for('users'))
        else:
            flash('Неверный email или пароль.', 'danger')
            return render_template('login.html')
    print(request.method)
    return render_template('login.html')


@app.route('/distribution')
def news():
    with open("fixtures/distribution.json", "rt", encoding="utf8") as f:
        news_list = json.loads(f.read())
    return render_template('distribution.html', news=news_list)

@app.route('/')
def users():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    users = {}
    for job in jobs:
        usera = db_sess.query(User).filter(User.id == job.team_leader)
        for user in usera:
            users[job.id] = f'{user.name} {user.surname}'
    return render_template('jobs.html', jobs=jobs, users=users)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('users'))


if __name__ == "__main__":
    db_session.global_init("db/blogs.db")
    app.run(port=8082, host="127.0.0.1")

