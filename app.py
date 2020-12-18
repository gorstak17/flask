from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///raspored.db'
app.config['SECRET_KEY'] = "adsadasd"


db = SQLAlchemy(app)
class Raspored(db.Model):
   id = db.Column(db.Integer, primary_key = True)
   predmet = db.Column(db.String(40))
   tip = db.Column(db.String(40))
   nastavnik = db.Column(db.String(40))  
   grupe = db.Column(db.String(40))
   dan = db.Column(db.String(40))
   termin = db.Column(db.String(40))
   vreme = db.Column(db.String(40))

db.create_all()

@app.route("/")
def index():
    return redirect("/raspored")

@app.route("/raspored")
def raspored():
    rasporedi = Raspored.query.all()
    nastavnici = set(str(raspored.nastavnik) for raspored in rasporedi)
    ucionice = set(str(raspored.vreme).replace("\\","").replace("n","") for raspored in rasporedi)

    return render_template("raspored.html", rasporedi=rasporedi, nastavnici=nastavnici, ucionice = ucionice)

@app.route("/nastavnik/<ime>")
def nastavnik(ime):
    rasporedi = Raspored.query.filter_by(nastavnik=ime).all()
    return render_template("raspored.html", rasporedi=rasporedi)

@app.route("/ucionica/<ucionica>")
def ucion(ucionica):
    rasporedi = Raspored.query.filter_by(vreme=ucionica+"\\n").all()
    return render_template("raspored.html", rasporedi=rasporedi)


if __name__ == "__main__":
    app.run(debug=True)