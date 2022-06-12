#app.py
from flask import Flask, render_template, request, jsonify
from wtforms import StringField, TextField, Form
from wtforms.validators import DataRequired, Length
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'cairocoders-ednalan'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
                                                      #password:admin
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:admin@localhost/sampledb'

db = SQLAlchemy(app)

class SearchForm(Form): #create form
    country = StringField('Country',render_kw={"placeholder": "country"})

class Country(db.Model):
    __tablename__='countries'
    id=db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable = False)

    def as_dict(self):
        return {'name': self.name}

@app.route('/')
def index():
    form = SearchForm(request.form)
    return render_template('index.html', form=form)

@app.route('/countries')
def countrydic():

    list_countries = ['Afghanistan', 'Aland Islands', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola', 'Anguilla', 'Antarctica', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan']
    return jsonify(list_countries)

@app.route('/process', methods=['POST'])
def process():
    country = request.form['country']
    if country:
        return jsonify({'country':country})
    return jsonify({'error': 'missing data..'})

if __name__ == '__main__':
    app.run(debug=True)
