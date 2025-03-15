from flask import Blueprint, jsonify
from data.db_session import create_session
from data.users import Jobs

test = Blueprint('test', __name__, url_prefix='/api/test')


@test.route('/1/<int:id>')
def get_jobs(id):
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

@test.route('')
def jobs():
    db_sess = create_session()
    jobs = db_sess.query(Jobs).all()
    db_sess.close()
    jobs_list = []
    for job in jobs:
        job_dict = {
            'id': job.id,
            'work_size': job.work_size,
            'collaborators': job.collaborators,
            'team_leader': job.team_leader,
        }
        jobs_list.append(job_dict)
    return jsonify(jobs_list)


@test.route('/2/<int:id>')
def error_two(id):
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
    jobs_list.append('Нет такой работы')
    return jsonify(jobs_list)
