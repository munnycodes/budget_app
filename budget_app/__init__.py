from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_datepicker import datepicker


app = Flask(__name__)
Bootstrap(app)
datepicker(app)
app.config['SECRET_KEY'] = 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///budget.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


from budget_app import routes
