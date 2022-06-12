import database
from website import db
class User(db.Model):
   id= db.Column(db.Integer(),primary_key=True)
   username= db.Column(db.String(length=30),nullable=False,unique=True)
   email_address= db.Column(db.String(length=50),nullable=False,unique=True)
   password_hash = db.Column(db.String(length=60),nullable=False)
   budget= db.Column(db.Integer(),nullable=False,default=1000)
connection = database.connect()
cursor = connection.cursor()
cursor.execute('''SELECT * FROM attractions''')
data= cursor.fetchall()

