from flask import Flask
from apispec import APISpec
from flask_restful import Api
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_cors import CORS

"""
Initialiasing application instance with Flask Framework and applying secret key to the application
"""
application = Flask(__name__) 
CORS(application)
application.config['CORS_HEADERS'] = 'Content-Type'
application.secret_key = 'todo-12345'

"""
Thsi will configure the swagger docs for the application
"""
api = Api(application)  # Flask restful wraps Flask app around it.

application.config.update({
    'APISPEC_SPEC': APISpec(
        title='todo',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/'  # URI to access UI of API Doc
})
docs = FlaskApiSpec(application)

from app.models import *