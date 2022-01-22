from app.models import TodoMaster, UserMaster, UserSession
from app import db
import uuid
from datetime import datetime

"""
[Services Module] Implement various helper functions here as a part of api
                    implementation using MVC Template
"""

# utility functions


def saveData(data=None):
    if data:
        db.session.add(data)
    db.session.commit()


def generateId():
    return str(uuid.uuid4().int)[:8]


def getUser(**kwargs):
    return UserMaster.query.filter_by(**kwargs).first()


def getUserSession(session_id):
    return UserSession.query.filter_by(session_id=session_id, is_active=True).first()


def getTodosList(todos):
    todoList = []
    for todo in todos:
        _todo = {
            'id': todo.id,
            'user_id': todo.user_id,
            'title': todo.title,
            'text': todo.text,
            'priority': todo.priority,
            'deadline': todo.deadline,
        }
        todoList.append(_todo)
    return todoList


# api controllers


def signUp(**kwargs):
    if not len(kwargs.values()) or None in kwargs.values():
        return {'message': 'Incomplete information provided', 'status_code': 400}
    user = getUser(username=kwargs['username'])
    if user:
        return {'message': 'Username already exists.', "status_code": 400}
    user = UserMaster(
        id=generateId(),
        **kwargs
    )
    saveData(user)
    return {
        'message': f'new {"admin" if kwargs["is_admin"] else "user"} account created.',
        'status_code': 201,
    }


def login(**kwargs):
    if not len(kwargs.values()) or None in kwargs.values():
        return {'message': 'Incomplete information provided', 'status_code': 400}
    user = getUser(**kwargs)
    if not user:
        return {
            'message': 'Invalid information provided',
            'status_code': 401
        }
    session_id = str(uuid.uuid4())
    user_session = UserSession(
        id=generateId(),
        user_id=user.id,
        session_id=session_id,
    )
    saveData(user_session)
    return {
        'message': 'Logged in successfully',
        'session_id': session_id,
        'status_code': 200,
    }


def logout(**kwargs):
    session_id = kwargs.get('session_id')
    if not session_id:
        return {'message': 'No session ID', 'status_code': 400}
    session = getUserSession(session_id)
    if session:
        UserSession.query.filter_by(
            session_id=session_id, is_active=True).delete()
        saveData()
        return {'message': 'Logged out successfully', 'status_code': 200}
    else:
        return {'message': 'Session does not exist.', 'status_code': 403}


def addTodo(**kwargs):
    if not len(kwargs.values()) or None in kwargs.values():
        return {'message': 'Incomplete information provided', 'status_code': 400}
    session = getUserSession(kwargs.pop("session_id"))
    if not session:
        return {'message': 'Unauthorized', 'status_code': 401}
    if kwargs.get("priority") in [0, 1, 2, 3]:
        kwargs["deadline"] = datetime.strptime(
            f'{kwargs["deadline"]}', '%Y-%m-%dT%H:%M')
        newTodo = TodoMaster(
            id=generateId(),
            user_id=session.user_id,
            **kwargs
        )
        saveData(newTodo)
        return {'message': 'New todo added.', 'status_code': 201}
    else:
        return {'message': 'enter a valid priority', 'status_code': 401}


def getTodo(**kwargs):
    if None in list(kwargs.values()):
        return {'message': 'Incomplete information provided.', 'status_code': 400}
    session_id = kwargs.get('session_id')
    session = getUserSession(session_id)
    if not session:
        return {'message': 'Not logged in.', 'status_code': 403}
    if kwargs.get('priority') in [0, 1, 2, 3]:
        print(kwargs.get('priority'))
        todo_rows = TodoMaster.query.filter_by(
            user_id=session.user_id, is_active=1 if kwargs.get('active') else 0, priority=kwargs.get('priority') if kwargs.get('active') else 0)
    else:
        todo_rows = TodoMaster.query.filter_by(
            user_id=session.user_id, is_active=1 if kwargs.get('active') else 0)
    todos_list = []
    for todo_row in todo_rows:
        todos_list.append(todo_row)
    todos = getTodosList(todos_list)
    return {'message': f'user has {len(todos)} {"active" if kwargs.get("active") else "completed"} todo(s)', 'todos': todos, 'status_code': 200}


def deleteTodo(**kwargs):
    if None in list(kwargs.values()):
        return {'message': 'Incomplete information provided.', 'status_code': 400}
    id, session_id = kwargs['id'], kwargs.get('session_id')
    session = getUserSession(session_id)
    if not session:
        return {'message': 'Not logged in.', 'status_code': 403}
    todo = TodoMaster.query.filter_by(id=id).first()
    todo.is_active = 0
    todo.priority = 0
    saveData(todo)
    return {'message': f'todo deleted',  'status_code': 200}
