from sqlalchemy.sql import func
from app import application
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash

"""
[DataBase Access Details]
Below is the configuration mentioned by which the application can make connection with MySQL database
"""

db_type = 'mysql'
username = 'aytxh93xtpt15lcs'
password = 'o12cyt24u4s65jmq'
server = 'exbodcemtop76rnz.cbetxkdyhwsb.us-east-1.rds.amazonaws.com'
port='3306'
database_name = 'iavsynbh0loui7go'

application.config['SQLALCHEMY_DATABASE_URI'] = f"{db_type}://{username}:{password}@{server}:{port}/{database_name}"
# application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(application)


class UserMaster(db.Model):
    __tablename__ = 'user_master'

    id = Column(String(100), primary_key=True)
    name = Column(String(200))
    username = Column(String(200), unique=True)
    password_hash = Column(String(200))
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_ts = Column(DateTime, default=func.now())
    updated_ts = Column(DateTime, onupdate=func.now())

    def __init__(self, id, name, username, is_admin):
        self.id = id
        self.username = username
        self.name = name
        self.is_admin = is_admin
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


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
    deadline = Column(DateTime, default=None)
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
