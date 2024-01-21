from flask import Flask, request, render_template
from flask_restful import Api
from application.database import db
from application.model import *
import os
from application.config import LocalDevelopmentConfig

from api.UserAPI import AllUserAPI, UserAPI

app = None



def create_app():
    app = Flask(__name__, template_folder="Templates")
    if os.getenv('ENV', "development") == "production":
      raise Exception("Currently no production config is setup.")
    else:
      print("Staring Local Development")
      app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    app.app_context().push()  
    return app 

app = create_app()

api = Api(app)
api.init_app(app)

app.secret_key="123456789"


from application.controllers import *

api.add_resource(AllUserAPI, '/api/user')
api.add_resource(UserAPI,'/api/user/<int:user_id>')

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8000, debug=True)