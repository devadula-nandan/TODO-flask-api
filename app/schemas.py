from marshmallow import Schema, fields

# request schemas


class SignUpRequest(Schema):
    name = fields.Str()
    username = fields.Str()
    password = fields.Str()
    is_admin = fields.Boolean(missing=False, allow_none=True)


class LoginRequest(Schema):
    username = fields.Str()
    password = fields.Str()


class SessionRequest(Schema):
    session_id = fields.Str()


class AddTodoRequest(Schema):
    title = fields.Str()
    text = fields.Str()
    priority = fields.Int()
    deadline = fields.Str()
    session_id = fields.Str()


class ViewTodoRequest(Schema):
    session_id = fields.Str()
    priority = fields.Int(missing=4, allow_none=True)
    active = fields.Boolean(missing=True, allow_none=True)


class DeleteTodoRequest(Schema):
    id = fields.Str()
    session_id = fields.Str()

# response schemas


class BaseResponse(Schema):
    message = fields.Str()


class LoginResponse(Schema):
    message = fields.Str()
    session_id = fields.Str()


class ListResponse(Schema):
    message = fields.Str()
    results = fields.List(fields.Dict())
