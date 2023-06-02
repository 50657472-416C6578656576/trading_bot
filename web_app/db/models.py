from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_wtf.csrf import CSRFProtect
app = Flask(__name__,  template_folder='../templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
csrf = CSRFProtect(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer,
               primary_key = True)
    username = db.Column(db.String(20),
                         unique = True, 
                         nullable = False)
    email = db.Column(db.String(120), 
                      unique = True, 
                      nullable = False,)
    password = db.Column(db.String(60), 
                         nullable = False)