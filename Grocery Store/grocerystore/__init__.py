from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grocerystore.db'

app.config['SECRET_KEY']='hfouewhfodasdsuw'

db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'customerlogin'
login_manager.needs_refresh_message_category = 'danger'
login_manager.login_message = u"Please login first"

from grocerystore.admin import routes
from grocerystore.products import routes
from grocerystore.carts import carts
from grocerystore.customers import routes

with app.app_context():
    db.create_all()


