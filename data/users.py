import datetime
import sqlalchemy
from data.db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = "users"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String, default="фамилия")
    name = sqlalchemy.Column(sqlalchemy.String, default="фамилия")
    age = sqlalchemy.Column(sqlalchemy.Integer, default="возраст")
    position = sqlalchemy.Column(sqlalchemy.String, default="должность")
    speciality = sqlalchemy.Column(sqlalchemy.String, default="профессия")
    address = sqlalchemy.Column(sqlalchemy.String, default="адрес")
    email = sqlalchemy.Column(
        sqlalchemy.String, unique=True, nullable=True, default="электронная почта"
    )
    hashed_password = sqlalchemy.Column(
        sqlalchemy.String, unique=True, nullable=True, default="хэшированный пароль"
    )
    modified_date = sqlalchemy.Column(
        sqlalchemy.DateTime, default=datetime.datetime.now
    )

    def __repr__(self):
        return f"<Colonist> {self.id} {self.surname} {self.name}"


class Jobs(SqlAlchemyBase):
    __tablename__ = "jobs"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    team_leader = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id")
    )
    job = sqlalchemy.Column(sqlalchemy.String)
    work_size = sqlalchemy.Column(sqlalchemy.Integer, default=datetime.datetime.now)
    collaborators = sqlalchemy.Column(sqlalchemy.String)

    start_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    end_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    is_finished = sqlalchemy.Column(sqlalchemy.Boolean, default=True)

    def __repr__(self):
        return f'<Job> {self.job}'
