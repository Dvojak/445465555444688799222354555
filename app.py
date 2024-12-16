from flask import Flask, render_template, redirect, url_for, request
from wtforms import Form, StringField, SubmitField, IntegerField  # Import IntegerField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_migrate import Migrate  # Import Flask-Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'  # Nastavte si vlastní klíč
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///names.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Inicializace Flask-Migrate

# Definice modelu pro databázi
class Name(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)  # Přidání pole pro věk

# WTForms formulář pro zadání jména
class NameForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])  # Přidání pole pro věk
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        # Uložení jména a věku do databáze
        new_name = Name(name=form.name.data, age=form.age.data)  # Uložení jména a věku
        db.session.add(new_name)
        db.session.commit()
        return redirect(url_for('index'))
    names = Name.query.all()  # Načtení všech jmen z databáze
    return render_template('index.html', form=form, names=names)

@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    # Smazání záznamu z databáze
    name_to_delete = Name.query.get(id)
    if name_to_delete:
        db.session.delete(name_to_delete)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Spuštění aplikace
    app.run(debug=True)
