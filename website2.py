from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import database
app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///market.db'
db=SQLAlchemy(app)


# from flask import Flask, render_template
# from flask_sqlalchemy import SQLAlchemy
#
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///market.db'
# db=SQLAlchemy(app)
#
# class Info(db.Model):
#     id=db.Column(db.Integer(),primary_key=True)
#     company=db.Column(db.String(length=30))
#     name=db.Column(db.String(length=30))
#     price= db.Column(db.Integer())
#     discount=db.Column(db.String(length=30))
#     plus_one=db.Column(db.String(length=30))
#     points=db.Column(db.String(length=30))
#     city=db.Column(db.String(length=30))
#     link=db.Column(db.String)
#
#
#     def __repr__(self):
#         return f'Item{self.name}'
# @app.route("/")
# @app.route("/home")
# def home_page():
#     return render_template("home.html")
#
# @app.route("/about")
# def about():
#     return render_template("about.html")
#
# @app.route("/admin")
# def aviv():
#     items= Info.query.all()
#     return render_template("admin.html",items=items)
