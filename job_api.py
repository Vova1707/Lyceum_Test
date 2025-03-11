from flask import Blueprint, jsonify
from data.db_session import create_session
from data.users import Jobs

jobs_api = Blueprint('jobs_api', __name__, url_prefix='/api/jobs')


@jobs_api.route('')
def get_jobs():
    session = create_session()
    jobs = session.query(Jobs).all()
    session.close()
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