from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from flask_cors import CORS
from sqlalchemy import create_engine
import os
import sys

from flask_login import LoginManager
from DeltaHubRestApi.Services.System.SystemService import SystemServices

db = SQLAlchemy()
login_manager = LoginManager()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
print(f"Project root: {ROOT_DIR}")
sys.path.append(ROOT_DIR)

print(sys.path)

app = Flask(__name__)

app.config["SECRET_KEY"] = "mysecret"
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:root@localhost/inspectionsdb'

#CORS(app)
"""
cors = CORS(app, resources={
    r"/*": {
        "origins": "*"
    }
})
"""
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login' #login view has LoginManager functions
login_manager.init_app(app)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
print(f"Project root: {ROOT_DIR}")

from .modelsdb import User

#user loader finds
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from .auth import auth as auth_bluepint
app.register_blueprint(auth_bluepint)

from .main import main as main_blueprint
app.register_blueprint(main_blueprint)

"""
def create_app():

    app = Flask(__name__)

    app.config["SECRET_KEY"] = "mysecret"
    app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:root@localhost/inspectionsdb'

    CORS(app)
    cors = CORS(app, resources={
        r"/*": {
            "origins": "*"
        }
    })

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' #login view has LoginManager functions
    login_manager.init_app(app)

    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    print(f"Project root: {ROOT_DIR}")

    from .modelsdb import User

    #user loader finds
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_bluepint
    app.register_blueprint(auth_bluepint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
"""

#Not using it for now.....
def InitDataBase(dataBaseUri):
    engine = create_engine(dataBaseUri)
    with engine.connect() as connection:
        if not (engine.dialect.has_table(connection, "inspections_table") and
                engine.dialect.has_table(connection, "purchase_orders_table") and
                engine.dialect.has_table(connection, "user")):
            print("There are no tables in database, creating them now....")
            db.create_all()
            print("Ready!, tables created! :)")
        else:
            print("There are tables tables in db :)))")
