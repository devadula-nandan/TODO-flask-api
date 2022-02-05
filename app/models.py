from sqlalchemy.sql import func
from app import application
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey

"""
[DataBase Access Details]
Below is the configuration mentioned by which the application can make connection with MySQL database
"""
# https://www.db4free.net/
# https://www.db4free.net/phpMyAdmin
db_type = 'mysql'
username = 'nandan_mysql'
password = 'nandan123'
server = 'db4free.net'
port='3306'
database_name = 'nandan_mysql'

application.config['SQLALCHEMY_DATABASE_URI'] = f"{db_type}://{username}:{password}@{server}:{port}/{database_name}"
# application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(application)


class UserMaster(db.Model):
    __tablename__ = 'user_master'

    id = Column(String(100), primary_key=True)
    name = Column(String(200))
    username = Column(String(200), unique=True)
    password = Column(String(200))
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_ts = Column(DateTime, default=func.now())
    updated_ts = Column(DateTime, onupdate=func.now())

    def __init__(self, id, name, username, password, is_admin):
        self.id = id
        self.username = username
        self.name = name
        self.password = password
        self.is_admin = is_admin


class UserSession(db.Model):
    __tablename__ = 'user_session'

    id = Column(String(100), primary_key=True)
    user_id = Column(String(100), ForeignKey("user_master.id"))
    session_id = Column(String(200), unique=True)
    is_active = Column(Boolean, default=True)
    created_ts = Column(DateTime, default=func.now())
    updated_ts = Column(DateTime, onupdate=func.now())

    def __init__(self, id, user_id, session_id):
        self.id = id
        self.user_id = user_id
        self.session_id = session_id


class TodoMaster(db.Model):
    __tablename__ = 'todo_master'

    id = Column(String(100), primary_key=True, index=True)
    user_id = Column(String(100), ForeignKey("user_master.id"))
    title = Column(String(500))
    text = Column(String(500))
    priority = Column(Integer)
    deadline = Column(DateTime)
    is_active = Column(Boolean, default=True)
    created_ts = Column(DateTime, default=func.now())
    updated_ts = Column(DateTime, onupdate=func.now())

    def __init__(self, id, user_id, title, text, priority, deadline):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.text = text
        self.priority = priority
        self.deadline = deadline


db.create_all()
db.session.commit()
