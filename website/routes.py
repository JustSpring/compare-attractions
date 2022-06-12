from website import app
from flask import Flask, render_template, request, redirect, url_for, jsonify,abort
from website.models import data, User
# from flask_sqlalchemy import SQLAlchemy
import database
import os
from pathlib import Path

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
import hashlib
from flask_login import LoginManager



lis_name=[]
connection3 = database.connect3()
cursor3 = connection3.cursor()
cursor3.execute('''SELECT * FROM final_data''')
data3= cursor3.fetchall()
for d in data3:
    if d[2] not in lis_name:
        lis_name.append(d[2])

@app.route("/home")
@app.route('/')
def index():
    return render_template('index.html')

@app.route("/ajaxlivesearch",methods=["POST","GET"])
def ajaxlivesearch():
    connection4 = database.connect4()
    cursor4 = connection4.cursor()
    if request.method == 'POST':
        search_word = request.form['query']
        #print(search_word)
        if search_word == '':
            query = '''SELECT * from id_name ORDER BY id DESC LIMIT 20'''
            cursor4.execute(query)
            employee = cursor4.fetchall()
        else:
            query = """SELECT * from id_name WHERE name LIKE '%{}%'""".format(search_word)
            #print(query)
            cursor4.execute(f"{query}")
            employee = cursor4.fetchall()
            numrows = len(employee)
    return jsonify({'htmlresponse': render_template('response.html', employee=employee, numrows=numrows)})



class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "שם משתמש"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "סיסמא"})

    submit = SubmitField('כניסה')



login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

Login=""
@app.route('/login', methods=['GET', 'POST'])
def login():
    global Login
    form = LoginForm()
    if form.validate_on_submit():
        plaintext = str(form.password).encode('utf-8')
        salt=b'\x1e~m\x83\xae\xc1\xd6\xa1f\xb4\xc1\xd8/\x010\x19 \x96jdt\xf9y\x19J\x8dY*y\x8e\xd3\x8b'
        key= hashlib.pbkdf2_hmac('sha256',plaintext,salt,100000)
        print(key)
        if b')\xde\xf2\xf50+4\xb3\'(9\x82~\x1d\xfbN\xbd\xea\x90\xf6\xb3\x90\xd8\xe0\xca "8$\xf2Ja'==key:
            Login=request.environ.get('REMOTE_ADDR')
            return redirect(url_for('host'))
        #if form.username=="aviv" and hash==

    return render_template('login.html', form=form)


@app.route('/item')
def item():
    connection3 = database.connect3()
    cursor3 = connection3.cursor()
    num=request.args.get("id")
    query = """SELECT * from final_data WHERE id IS {}""".format(num)
    print(query)
    cursor3.execute(f"{query}")
    employee = cursor3.fetchall()
    print(employee)
    for i in employee:
        name=i[2]
    return render_template("item.html", info=employee,name=name)



@app.route("/about", methods=["GET","POST"])
def about():
    if request.method == "POST":
        req= request.form
        print(req)
        email=req["email"]
        message=req["message"]
        print("message from:",email, "that says:",message)

        msg= Message("New Comment", sender='noreply@demo.com', recipients="avivfriedman100@gmail.com")
        msg.body= f'{email} Send you: {message}'
        mail.send(msg)

        return redirect(request.url)
    return render_template("about.html")


@app.route("/host/" , methods=["GET","POST"])
def host():
    global Login
    print(Login)
    if Login!=request.environ.get('REMOTE_ADDR'):
        print("good")
        abort(403)
    print("Started host")
    print(request.remote_addr)
    #print (generate_password_hash("RCAbdc$46", "sha256"))
    # stored_password = "sha256$FrCAGgP7g9scxvDc$fdf8d2877ba747b4530b0f4b7dac1959c5e860d04e78fdcb19a13115dc6fcee4"
    # result= check_password_hash(stored_password, password)
    # if result==False:
    #     return "Wrong Password! Please don't hack my site XD"
    connection = database.connect()
    cursor = connection.cursor()
    cursor.execute('''SELECT * FROM attractions''')
    data= cursor.fetchall()
    connection2 = database.connect2()
    database.create_tables2(connection2)
    cursor2 = connection2.cursor()
    cursor2.execute('''SELECT * FROM data3''')
    data2= cursor2.fetchall()
    lis_link=[]
    for d in data2:
        lis_link.append(d[1])
    # if request.method== "POST":
    #     print("Hello")
    #     val2= request.form.get("action2")
    #     print(val2)
    #     database.delete(connection,str(val2))
    if request.method == 'POST':
        print("hello world")
        if request.form.get("action2"):
            val2= request.form.get("action2")
            print(val2)
            database.delete(connection2,str(val2))
            print("deleted")
        elif request.form.get("new-database"):
            my_file = Path("./id_name.db")
            if my_file.is_file():
                connection4 = database.connect4()
                cursor4 = connection4.cursor()
                cursor4.execute('''DROP table id_name''')
            my_file2 = Path("./final_data.db")
            if my_file2.is_file():
                connection3 = database.connect3()
                cursor3 = connection3.cursor()
                cursor3.execute('''DROP table final_data''')
            database.create_tables3(connection3)
            connection4=database.connect4()
            database.create_tables4(connection4)

            for i in data:
                if i[8] in lis_link:
                    n=database.get_name_and_id_by_link(connection2,i[8])
                    for q in n:
                        id_data=q[0]
                        if q[1]:
                            name_data=q[2]
                        else:
                            name_data=i[2]
                    if int(id_data) != 0:
                        database.add_attraction3(connection3,int(id_data),i[1],name_data,i[3],i[4],i[5],i[6],i[7],i[8])
                else:
                    print("not good!")
            lis_name=[]
            cursor3 = connection3.cursor()
            cursor3.execute('''SELECT * FROM final_data''')
            data3= cursor3.fetchall()
            for d in data3:
                if d[2] not in lis_name:
                    lis_name.append(d[2])
                    database.add_attraction4(connection4,d[0],d[2])
        else:
            text=request.form["text"]
            val= request.form.get("action1")
            print("v",val)
            a=database.get_attraction_by_link(connection,str(val))
            x=0
            for b in a:
                name=b
            name=name[2]
            name=name.strip()
            if request.form["name"]:
                name=request.form["name"]
            if not text:
                text=0
            database.add_attraction2(connection2,int(text),val,name)
        print(" geturl")
        #shutil.copyfile("final_data.db","final_data2.db")
        return redirect(url_for("host"))

    return render_template("host.html",info=data,more_data=lis_link,info2=data2)

