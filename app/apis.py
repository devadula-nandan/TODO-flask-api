from lib2to3.pgen2 import token
from app.models import *
from app import *
from flask_restful import Resource
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
from app.schemas import *
from app.services import *


class SignUpAPI(MethodResource, Resource):
    @doc(description='Sign up for a new user account.', tags=['User'])
    @use_kwargs(SignUpRequest, location=('json'))
    @marshal_with(BaseResponse)
    def post(self, **kwargs):
        response = signUp(**kwargs)
        return BaseResponse().dump({'message': response['message']}), response['status_code']


api.add_resource(SignUpAPI, '/signup')
docs.register(SignUpAPI)


class LoginAPI(MethodResource, Resource):
    @doc(description='Login to get back a session ID.', tags=['User'])
    @use_kwargs(LoginRequest, location=('json'))
    @marshal_with(LoginResponse)
    def post(self, **kwargs):
        response = login(**kwargs)
        return LoginResponse().dump({'message': response['message']}), response['status_code'], {'Set-Cookie': 'token=' + response['session_id'] + '; HttpOnly; Path=/' + '; Max-Age=3600' + '; Secure' + '; SameSite=None'}


api.add_resource(LoginAPI, '/login')
docs.register(LoginAPI)


class LogoutAPI(MethodResource, Resource):
    @doc(description='Logout of the session.', tags=['User'])
    @use_kwargs(SessionRequest, location=('cookies'))
    @marshal_with(BaseResponse)
    def delete(self, **kwargs):
        response = logout(**kwargs)
        return BaseResponse().dump({
            'message': response['message'],
        }), response['status_code'], {'Set-Cookie': 'token=; HttpOnly; Path=/' + '; Max-Age=0' + '; Secure' + '; SameSite=Strict'}


api.add_resource(LogoutAPI, '/logout')
docs.register(LogoutAPI)


class AddTodoAPI(MethodResource, Resource):
    @doc(description='add new todo', tags=['Todo'])
    @use_kwargs(AddTodoRequest, location=('json'))
    @marshal_with(AddTodoResponse)
    def post(self, **kwargs):
        response = addTodo(**kwargs)
        return AddTodoResponse().dump({
            'message': response['message'],
            'id': response['id']
        }), response['status_code']


api.add_resource(AddTodoAPI, '/add.todo')
docs.register(AddTodoAPI)


class GetTodoAPI(MethodResource, Resource):
    @doc(description='get all todos', tags=['Todo'])
    @use_kwargs(ViewTodoRequest, location=('json'))
    @marshal_with(ListResponse)
    def post(self, **kwargs):
        response = getTodo(**kwargs)
        return ListResponse().dump({
            'message': response['message'],
            'results': response.get('todos')
        }), response['status_code']


api.add_resource(GetTodoAPI, '/get.todo')
docs.register(GetTodoAPI)


class DeleteTodoAPI(MethodResource, Resource):
    @doc(description='DeleteTodoAPI', tags=['Todo'])
    @use_kwargs(DeleteTodoRequest, location=('json'))
    @marshal_with(BaseResponse)
    def post(self, **kwargs):
        response = deleteTodo(**kwargs)
        return BaseResponse().dump({
            'message': response['message']
        }), response['status_code']


api.add_resource(DeleteTodoAPI, '/delete.todo')
docs.register(DeleteTodoAPI)
