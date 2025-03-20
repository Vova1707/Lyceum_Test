from flask import abort, jsonify
from flask_restful import Resource, reqparse

from data import db_session
from data.users import Jobs


def abort_if_jobs_not_found(job_id):
    session = db_session.create_session()
    jobs = session.query(Jobs).get(job_id)
    if not jobs:
        abort(404, message=f"Jobs {job_id} not found")

class JobsResource(Resource):
    def get(self, job_id):
        abort_if_jobs_not_found(job_id)
        session = db_session.create_session()
        item = session.query(Jobs).get(job_id)
        return jsonify({'Job': [{'id': item.id, 'job': str(item.job), 'work_size': item.work_size}]})

    def delete(self, job_id):
        abort_if_jobs_not_found(job_id)
        session = db_session.create_session()
        jobs = session.query(Jobs).get(job_id)
        session.delete(jobs)
        session.commit()
        return jsonify({'success': 'OK'})


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify({'jobs': [{'id': item.id, 'job': str(item.job), 'work_size': item.work_size} for item in jobs]})

    def post(self):
        session = db_session.create_session()
        user = Jobs(
            job='Работенка',
            work_size=11,
        )
        session.add(user)
        session.commit()
        return jsonify({'id': user.id})


# Парсер POST запроса в JobsListResource
parser = reqparse.RequestParser()
parser.add_argument('job', required=True)
parser.add_argument('work_size', required=True, type=int)