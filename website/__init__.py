from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import database
app = Flask(__name__)
db=SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SECRET_KEY'] = "d195291f7c84f47cc96e62c9"
from website import routes
