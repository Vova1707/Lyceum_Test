from flask import Blueprint, jsonify, abort, redirect, request, render_template
from flask_login import login_required, current_user
from forms import LoginForm, GalleryForm, RegisterForm, JobsForm, EditJobsForm, DepartmentForm

from data.db_session import create_session
from data.users import Jobs

jobs_api = Blueprint('jobs_api', __name__, url_prefix='/api/jobs')


@jobs_api.route('<int:id>')
def q_1(id):
    db_sess = create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == id).first()
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


@jobs_api.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
def news_delete(id):
    db_sess = create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == id).first()
    if jobs:
        db_sess.delete(jobs)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@jobs_api.route('add/<int:id>', methods=['GET', 'POST'])
def edit_jobs(id):
    form = EditJobsForm()
    if request.method == "GET":
        db_sess = create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id).first()
        if jobs:
            form.coloborators.data = jobs.collaborators
            form.work_size.data = jobs.work_size
            form.job_title.data = jobs.job
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = create_session()
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

