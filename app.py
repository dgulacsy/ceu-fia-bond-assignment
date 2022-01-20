import os
from datetime import datetime as dt, timedelta as td
from flask import Flask, request, render_template, redirect, url_for, send_from_directory, current_app
from flask_sqlalchemy import SQLAlchemy
import csv

def empty_to_zero(number):
    if number == "":
        return 0
    return number

##########
# Validations to implement:
# 1. Weights have to be equal to 100%
# empty strings need to be transformed to zero
###########

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ryyohlwbhegroa:0fc7c5e5b5c20fd87c8ac45f49862b3decce41ff9f995cd4fcb6a13845f44d76@ec2-52-214-178-113.eu-west-1.compute.amazonaws.com:5432/d308ve33cr91fu'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["TEMP"] = "temp"

db = SQLAlchemy(app)

class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cet_timestamp = db.Column(db.DateTime())
    team_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    asset1 = db.Column(db.String(100))
    asset2 = db.Column(db.String(100))
    asset3 = db.Column(db.String(100))
    asset4 = db.Column(db.String(100))
    asset5 = db.Column(db.String(100))
    asset6 = db.Column(db.String(100))
    asset7 = db.Column(db.String(100))
    asset8 = db.Column(db.String(100))
    asset9 = db.Column(db.String(100))
    asset10 = db.Column(db.String(100))
    asset11 = db.Column(db.String(100))
    asset12 = db.Column(db.String(100))
    asset13 = db.Column(db.String(100))
    asset14 = db.Column(db.String(100))
    asset15 = db.Column(db.String(100))
    weight1 = db.Column(db.Float())
    weight2 = db.Column(db.Float())
    weight3 = db.Column(db.Float())
    weight4 = db.Column(db.Float())
    weight5 = db.Column(db.Float())
    weight6 = db.Column(db.Float())
    weight7 = db.Column(db.Float())
    weight8 = db.Column(db.Float())
    weight9 = db.Column(db.Float())
    weight10 = db.Column(db.Float())
    weight11 = db.Column(db.Float())
    weight12 = db.Column(db.Float())
    weight13 = db.Column(db.Float())
    weight14 = db.Column(db.Float())
    weight15 = db.Column(db.Float())

    def __init__(self, cet_timestamp, team_name, email, asset1, asset2, asset3, asset4, asset5, asset6, asset7, asset8, asset9, asset10, asset11, asset12, asset13, asset14, asset15, weight1, weight2, weight3, weight4, weight5, weight6, weight7, weight8, weight9, weight10, weight11, weight12, weight13, weight14, weight15):
        self.cet_timestamp = cet_timestamp
        self.team_name = team_name
        self.email = email
        self.asset1 = asset1
        self.asset2 = asset2
        self.asset3 = asset3
        self.asset4 = asset4
        self.asset5 = asset5
        self.asset6 = asset6
        self.asset7 = asset7
        self.asset8 = asset8
        self.asset9 = asset9
        self.asset10 = asset10
        self.asset11 = asset11
        self.asset12 = asset12
        self.asset13 = asset13
        self.asset14 = asset14
        self.asset15 = asset15
        self.weight1 = weight1
        self.weight2 = weight2
        self.weight3 = weight3
        self.weight4 = weight4
        self.weight5 = weight5
        self.weight6 = weight6
        self.weight7 = weight7
        self.weight8 = weight8
        self.weight9 = weight9
        self.weight10 = weight10
        self.weight11 = weight11
        self.weight12 = weight12
        self.weight13 = weight13
        self.weight14 = weight14
        self.weight15 = weight15

@app.route("/")
def main():
    return render_template('main.html')

@app.route("/add_portfolio", methods=['POST'])
def add_portfolio():
    cet_timestamp = dt.now() + td(hours=1)
    team_name = request.form["team_name"]
    email = request.form["email"]
    asset1 = request.form["asset1"]
    asset2 = request.form["asset2"]
    asset3 = request.form["asset3"]
    asset4 = request.form["asset4"]
    asset5 = request.form["asset5"]
    asset6 = request.form["asset6"]
    asset7 = request.form["asset7"]
    asset8 = request.form["asset8"]
    asset9 = request.form["asset9"]
    asset10 = request.form["asset10"]
    asset11 = request.form["asset11"]
    asset12 = request.form["asset12"]
    asset13 = request.form["asset13"]
    asset14 = request.form["asset14"]
    asset15 = request.form["asset15"]
    weight1 = empty_to_zero(request.form["weight1"])
    weight2 = empty_to_zero(request.form["weight2"])
    weight3 = empty_to_zero(request.form["weight3"])
    weight4 = empty_to_zero(request.form["weight4"])
    weight5 = empty_to_zero(request.form["weight5"])
    weight6 = empty_to_zero(request.form["weight6"])
    weight7 = empty_to_zero(request.form["weight7"])
    weight8 = empty_to_zero(request.form["weight8"])
    weight9 = empty_to_zero(request.form["weight9"])
    weight10 = empty_to_zero(request.form["weight10"])
    weight11 = empty_to_zero(request.form["weight11"])
    weight12 = empty_to_zero(request.form["weight12"])
    weight13 = empty_to_zero(request.form["weight13"])
    weight14 = empty_to_zero(request.form["weight14"])
    weight15 = empty_to_zero(request.form["weight15"])
    entry = Portfolio(cet_timestamp, team_name, email, asset1, asset2, asset3, asset4, asset5, asset6, asset7, asset8 , asset9, asset10, asset11, asset12, asset13, asset14, asset15, weight1, weight2, weight3, weight4, weight5, weight6, weight7, weight8, weight9, weight10, weight11, weight12, weight13, weight14, weight15)
    db.session.add(entry)
    db.session.commit()
    return redirect(url_for("success"))

@app.route("/success")
def success():
    return render_template('success.html')

@app.route("/download/<path:filename>'", methods=['GET', 'POST'])
def download(filename):
    print("Initiating data dump...")
    outfile = open('temp/'+filename,'w')
    outcsv = csv.writer(outfile)
    records = db.session.query(Portfolio).all()
    # dump header
    outcsv.writerow([column.name for column in Portfolio.__mapper__.columns])
    # dump data
    [outcsv.writerow([getattr(curr, column.name) for column in Portfolio.__mapper__.columns]) for curr in records]
    outfile.close()
    temp = os.path.join(current_app.root_path, app.config['TEMP'])
    try:
        print("sending file")
        return send_from_directory(temp, filename=filename, as_attachment=True, cache_timeout=0)
    except FileNotFoundError:
        abort(404)

if __name__ == '__main__':
    db.create_all()
    db.session.commit()
    app.run(debug=True)