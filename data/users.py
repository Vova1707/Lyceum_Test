import datetime
import sqlalchemy
from flask_login import UserMixin

from data.db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash



class Category(SqlAlchemyBase):
    __tablename__ = "category"


    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)

class User(SqlAlchemyBase, UserMixin):
    __tablename__ = "users"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String, default="фамилия")
    name = sqlalchemy.Column(sqlalchemy.String, default="имя")
    age = sqlalchemy.Column(sqlalchemy.Integer, default="возраст")
    position = sqlalchemy.Column(sqlalchemy.String, default="должность")
    speciality = sqlalchemy.Column(sqlalchemy.String, default="профессия")
    address = sqlalchemy.Column(sqlalchemy.String, default="адрес")
    modified_date = sqlalchemy.Column(
        sqlalchemy.DateTime, default=datetime.datetime.now
    )

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def __repr__(self):
        return f"<Colonist> {self.id} {self.surname} {self.name}"


class Jobs(SqlAlchemyBase):
    __tablename__ = "jobs"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    team_leader = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id")
    )
    job = sqlalchemy.Column(sqlalchemy.String, default="имя")
    work_size = sqlalchemy.Column(sqlalchemy.Integer, default=datetime.datetime.now)
    collaborators = sqlalchemy.Column(sqlalchemy.String)

    start_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    end_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    is_finished = sqlalchemy.Column(sqlalchemy.Boolean, default=True)

    def __repr__(self):
        return f'<Job> {self.job}'



class Department(SqlAlchemyBase):
    __tablename__ = "departament"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    chief = sqlalchemy.Column(sqlalchemy.Integer)
    members = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(
        sqlalchemy.String, unique=True, nullable=True, default="электронная почта"
    )