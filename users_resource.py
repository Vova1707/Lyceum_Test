from flask import abort, jsonify
from flask_restful import Resource, reqparse

from data import db_session
from data.users import User


def abort_if_users_not_found(user_id):
    session = db_session.create_session()
    news = session.query(User).get(user_id)
    if not news:
        abort(404, message=f"User {user_id} not found")

class UsersResource(Resource):
    def get(self, user_id):
        abort_if_users_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': [{'id': user.id, 'name': user.name, 'surname': user.surname}]})

    def delete(self, user_id):
        print(3)
        abort_if_users_not_found(user_id)
        session = db_session.create_session()
        news = session.query(User).get(user_id)
        session.delete(news)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'news': [{'id': item.id, 'name': item.name, 'surname': item.surname} for item in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            name=args['name'],
            surname=args['surname'],
            age=args['age'],
        )
        session.add(user)
        session.commit()
        return jsonify({'id': user.id})


# Парсер POST запроса в UsersListResource
parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('surname', required=True)
parser.add_argument('age', required=True, type=int)