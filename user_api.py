import requests
from flask import Blueprint, jsonify, abort, redirect, request, render_template, flash, url_for
from flask_login import login_required, current_user, login_user
from forms import LoginForm, GalleryForm, RegisterForm, JobsForm, EditJobsForm, DepartmentForm
from data.users import User, Jobs, Department

from data.db_session import create_session
from data.users import Jobs

user_api = Blueprint('user_api', __name__, url_prefix='/api/users/')


@user_api.route('')
def all_user():
    db_sess = create_session()
    users = db_sess.query(User).all()
    db_sess.close()
    users_list = []
    for user in users:
        if user:
            job_dict = {
                'id': user.id,
                'name': user.name,
            }
            users_list.append(job_dict)
    return jsonify(users_list)


@user_api.route('<int:id>')
def q_1_user(id):
    db_sess = create_session()
    job = db_sess.query(User).filter(User.id == id).first()
    db_sess.close()
    jobs_list = []
    if job:
        job_dict = {
            'id': job.id,
            'work_size': job.work_size,
            'collaborators': job.collaborators,
            'team_leader': job.team_leader,
        }
        jobs_list.append(job_dict)
    return jsonify(jobs_list)


@user_api.route('delete/<int:id>', methods=['GET', 'POST'])
def newsa_delete_user(id):

    db_sess = create_session()
    user = db_sess.query(User).filter(User.id == id).first()
    if user:
        db_sess.delete(User)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@user_api.route('add', methods=['GET', 'POST'])
def add_user():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            print(form.password.data, form.password_again.data)
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = create_session()
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

@user_api.route('edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
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


@user_api.route('show')
def show():
    server_address = 'http://geocode-maps.yandex.ru/1.x/?'
    api_key = '8013b162-6b42-4997-9691-77b7074026e0'
    geocode = 'Австралия'
    geocoder_request = f'{server_address}apikey={api_key}&geocode={geocode}&format=json'
    response = requests.get(geocoder_request)
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    main_coords = map(float, toponym_coodrinates.split())
    params = {
        "ll": ",".join(map(str, main_coords)),
        "spn": ",".join(['0.18', '0.18']),
        "apikey": "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13",
    }
    map_file = 'map.png'
    get_response(map_file, params)
    with open(map_file, "wb") as file:
        file.write(response.content)
    return render_template('show.html', photo=map_file)


def get_response(map_file, params):
    api_server = "https://static-maps.yandex.ru/v1"
    response = requests.get(api_server, params=params)

    if not response:
        print('Ошибка выполнения запроса:')
        print('Http статус:', response.status_code, '(', response.reason, ')')
    with open(map_file, 'wb') as file:
        file.write(response.content)