from app import application
from app.apis import *

"""
[Driver Module] : It is responsible for stating the server for application for apis serving
"""
if __name__ == "__main__":

    application.run(debug=True, port=8000)
