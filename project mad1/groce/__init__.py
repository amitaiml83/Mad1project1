from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '7409fad3c2f7ac87fc4a5956a5060475'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite3"
app.static_folder = 'static'
db = SQLAlchemy(app)
app.app_context().push()
db.create_all()
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from groce import routes
