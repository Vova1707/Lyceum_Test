from forms import LoginForm
from flask import Flask
from flask import request, render_template, redirect
import json


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route("/<level>")
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
    with open("data/distribution.json", "rt", encoding="utf8") as f:
        news_list = json.loads(f.read())
    return render_template('distribution.html', news=news_list)


if __name__ == "__main__":
    app.run(port=8081, host="127.0.0.1")
