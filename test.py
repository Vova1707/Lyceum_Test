import os
import random

from werkzeug.utils import secure_filename

from data.db_session import create_session
from forms import LoginForm, GalleryForm, RegisterForm, JobsForm, EditJobsForm, DepartmentForm
from flask import Flask, url_for, request, flash, abort
from flask import render_template, redirect
import json
from job_api import jobs_api
from data import db_session
from data.users import User, Jobs, Department
from flask_login import LoginManager, login_required, logout_user, login_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOAD_FOLDER'] = 'C:/Users/konde/PycharmProjects/Test_10/static/k'
app.register_blueprint(jobs_api)

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
            team_leader=current_user.id,
            job=form.job_title.data,
            work_size=form.work_size.data,
            collaborators=form.coloborators.data,
        )
        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
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

@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_jobs(id):
    form = EditJobsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        if current_user.id != 1:
            jobs = db_sess.query(Jobs).filter(Jobs.id == id, Jobs.team_leader == current_user.id).first()
        else:
            jobs = db_sess.query(Jobs).filter(Jobs.id == id).first()
        if jobs:
            form.coloborators.data = jobs.collaborators
            form.work_size.data = jobs.work_size
            form.job_title.data = jobs.job
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if current_user.id != 1:
            jobs = db_sess.query(Jobs).filter(Jobs.id == id, Jobs.team_leader == current_user.id).first()
        else:
            jobs = db_sess.query(Jobs).filter(Jobs.id == id).first()
        if jobs:
            jobs.collaborators = form.coloborators.data
            jobs.work_size = form.work_size.data
            jobs.job = form.job_title.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('jobs_edit.html',
                           title='Редактирование новости',
                           form=form
                           )

@app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                      Jobs.team_leader == current_user.id
                                      ).first()
    if jobs:
        db_sess.delete(jobs)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')

@app.route('/departaments')
def departaments():
    db_sess = db_session.create_session()
    deportaments = db_sess.query(Department).all()
    users = {}
    for deportament in deportaments:
        usera = db_sess.query(User).filter(User.id == deportament.members)
        for user in usera:
            users[deportament.id] = f'{user.name} {user.surname}'
    return render_template('departaments.html', deportaments=deportaments, users=users)


@app.route('/departament/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_departament(id):
    form = DepartmentForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        if current_user.id != 1:
            department = db_sess.query(Department).filter(Department.id == id,
                                                    Department.chief == current_user.id).first()
        else:
            department = db_sess.query(Department).filter(Department.id == id).first()
        if department:
            form.email.data = department.email
            form.members.data = department.members
            form.title.data = department.title
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if current_user.id != 1:
            department = db_sess.query(Department).filter(Department.id == id,
                                                    Department.chief == current_user.id).first()
        else:
            department = db_sess.query(Department).filter(Department.id == id).first()
        if department:
            department.email = form.email.data
            department.members = form.members.data
            department.title = form.title.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('departament_form.html',
                           title='Редактирование новости',
                           form=form
                           )


@app.route('/departament_register', methods=['GET', 'POST'])
def departament_register():
    '''
    Регистрация работы через форму DepartmentForm()
    '''
    form = DepartmentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Department(
            members=form.members.data,
            title=form.title.data,
            chief=current_user.id,
            email=form.email.data,
        )
        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
    return render_template('departament_form.html', title='Регистрация', form=form)



@app.route('/departament_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def departament_delete(id):
    db_sess = db_session.create_session()
    departament = db_sess.query(Jobs).filter(Department.id == id,
                                      Department.chief == current_user.id
                                      ).first()
    if departament:
        db_sess.delete(departament)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('users'))


if __name__ == "__main__":
    db_session.global_init("db/blogs.db")
    app.run(port=8082, host="127.0.0.1")