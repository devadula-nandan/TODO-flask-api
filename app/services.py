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
        return {'message': 'Username already exists.', 'status_code': 400}
    user = UserMaster(
        id=generateId(),
        name=kwargs['name'],
        username=kwargs['username'],
        is_admin=kwargs['is_admin']
    )
    user.set_password(kwargs.pop('password'))
    saveData(user)
    return {
        'message': f'new {"admin" if kwargs["is_admin"] else "user"} account created.',
        'status_code': 201,
    }


def login(**kwargs):
    if not len(kwargs.values()) or None in kwargs.values():
        return {'message': 'Incomplete information provided', 'status_code': 400}
    pw = kwargs.pop('password')
    user = getUser(**kwargs)
    if not user:
        return {'message': 'User not found.', 'status_code': 404}
    if not user.check_password(pw):
        return {'message': 'Incorrect password.', 'status_code': 401}
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
    session_id = kwargs.get('token')
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
    session = getUserSession(kwargs.pop("token"))
    if not session:
        return {'message': 'Unauthorized', 'status_code': 401}
    if kwargs.get("priority") in [0, 1, 2, 3]:
        if kwargs["deadline"] not in ["", None]:
            kwargs["deadline"] = datetime.strptime(
                f'{kwargs["deadline"]}', '%Y-%m-%dT%H:%M')
        id = generateId()
        newTodo = TodoMaster(
            id=id,
            user_id=session.user_id,
            **kwargs
        )
        saveData(newTodo)
        return {'message': 'New todo added.', 'id': id, 'status_code': 200}
    else:
        return {'message': 'enter a valid priority', 'status_code': 401}


def getTodo(**kwargs):
    if None in list(kwargs.values()):
        return {'message': 'Incomplete information provided.', 'status_code': 400}
    session_id = kwargs.get('token')
    session = getUserSession(session_id)
    if not session:
        return {'message': 'Not logged in.', 'status_code': 403}
    if kwargs.get('priority') in [-1, 0, 1, 2, 3]:
        print(kwargs.get('priority'))
        todo_rows = TodoMaster.query.filter_by(
            user_id=session.user_id, is_active=1 if kwargs.get('active') else 0, priority=kwargs.get('priority') if kwargs.get('active') else 0).order_by(TodoMaster.created_ts.desc())
    else:
        todo_rows = TodoMaster.query.filter_by(
            user_id=session.user_id, is_active=1 if kwargs.get('active') else 0,).where(TodoMaster.priority.in_([0, 1, 2, 3]))
    todos_list = []
    for todo_row in todo_rows:
        todos_list.append(todo_row)
    todos = getTodosList(todos_list)
    return {'message': f'user has {len(todos)} {"active" if kwargs.get("priority") != -1  else "completed"} todo(s)', 'todos': todos, 'status_code': 200}


def deleteTodo(**kwargs):
    if None in list(kwargs.values()):
        return {'message': 'Incomplete information provided.', 'status_code': 400}
    id, session_id = kwargs['id'], kwargs.get('token')
    session = getUserSession(session_id)
    if not session:
        return {'message': 'Not logged in.', 'status_code': 403}
    todo = TodoMaster.query.filter_by(id=id).first()
    todo.is_active = 0
    todo.priority = 0
    saveData(todo)
    return {'message': f'todo deleted',  'status_code': 200}

def verifySession(**kwargs):
    session_id = kwargs.get('token')
    print(session_id)
    if not session_id:
        return {'message': False, 'status_code': 400}
    session = getUserSession(session_id)
    if session:
        user = getUser(id=session.user_id)
        return {'message': user.username, 'status_code': 200}
    else:
        return {'message': False, 'status_code': 403}

def updateTodo(**kwargs):
    if None in list(kwargs.values()):
        return {'message': 'Incomplete information provided.', 'status_code': 400}
    id, session_id = kwargs['id'], kwargs.get('token')
    session = getUserSession(session_id)
    if not session:
        return {'message': 'Not logged in.', 'status_code': 403}
    todo = TodoMaster.query.filter_by(id=id).first()
    if not todo:
        return {'message': 'Todo not found.', 'status_code': 404}
    if kwargs.get('priority') in [0, 1, 2, 3]:
        todo.priority = kwargs.get('priority')
    if kwargs.get('deadline') not in ["", None]:
        todo.deadline = datetime.strptime(
            f'{kwargs.get("deadline")}', '%Y-%m-%dT%H:%M')
    todo.title = kwargs.get('title')
    todo.text = kwargs.get('text')
    saveData(todo)
    return {'message': 'Todo updated', 'status_code': 200}

def checkTodo(**kwargs):
    if None in list(kwargs.values()):
        return {'message': 'Incomplete information provided.', 'status_code': 400}
    id, session_id = kwargs['id'], kwargs.get('token')
    session = getUserSession(session_id)
    if not session:
        return {'message': 'Not logged in.', 'status_code': 403}
    todo = TodoMaster.query.filter_by(id=id).first()
    if not todo:
        return {'message': 'Todo not found.', 'status_code': 404}
    todo.priority = -1
    saveData(todo)
    return {'message': 'Todo checked', 'status_code': 200}

def uncheckTodo(**kwargs):
    if None in list(kwargs.values()):
        return {'message': 'Incomplete information provided.', 'status_code': 400}
    id, session_id = kwargs['id'], kwargs.get('token')
    session = getUserSession(session_id)
    if not session:
        return {'message': 'Not logged in.', 'status_code': 403}
    todo = TodoMaster.query.filter_by(id=id).first()
    if not todo:
        return {'message': 'Todo not found.', 'status_code': 404}
    todo.priority = 0
    saveData(todo)
    return {'message': 'Todo unchecked', 'status_code': 200}