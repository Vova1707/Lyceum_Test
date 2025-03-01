import os
import random

from werkzeug.utils import secure_filename

from forms import LoginForm, GalleryForm
from flask import Flask, url_for
from flask import request, render_template, redirect
import json
from data import db_session
from data.users import User, Jobs


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOAD_FOLDER'] = 'C:/Users/konde/PycharmProjects/Test_10/static/k'

@app.route('/member')
def member():
    with open('templates/crew.json', 'r', encoding='utf-8') as f:
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
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/distribution')
def news():
    with open("fixtures/distribution.json", "rt", encoding="utf8") as f:
        news_list = json.loads(f.read())
    return render_template('distribution.html', news=news_list)

@app.route('/')
def users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return render_template('users.html', users=users)

if __name__ == "__main__":
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    app.run(port=8082, host="127.0.0.1")
