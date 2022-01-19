import os
from datetime import datetime as dt, timedelta as td
from flask import Flask, request, render_template, redirect, url_for, send_from_directory, current_app
from flask_sqlalchemy import SQLAlchemy
import csv

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ryyohlwbhegroa:0fc7c5e5b5c20fd87c8ac45f49862b3decce41ff9f995cd4fcb6a13845f44d76@ec2-52-214-178-113.eu-west-1.compute.amazonaws.com:5432/d308ve33cr91fu'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["TEMP"] = "temp"
# app.secret_key = 'secret'

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
    weight1 = db.Column(db.Float())
    weight2 = db.Column(db.Float())
    weight3 = db.Column(db.Float())
    weight4 = db.Column(db.Float())
    weight5 = db.Column(db.Float())
    weight6 = db.Column(db.Float())
    weight7 = db.Column(db.Float())

    def __init__(self, cet_timestamp, team_name, email, asset1, asset2, asset3, asset4, asset5, asset6, asset7, weight1, weight2, weight3, weight4, weight5, weight6, weight7):
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
        self.weight1 = weight1
        self.weight2 = weight2
        self.weight3 = weight3
        self.weight4 = weight4
        self.weight5 = weight5
        self.weight6 = weight6
        self.weight7 = weight7

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
    weight1 = request.form["weight1"]
    weight2 = request.form["weight2"]
    weight3 = request.form["weight3"]
    weight4 = request.form["weight4"]
    weight5 = request.form["weight5"]
    weight6 = request.form["weight6"]
    weight7 = request.form["weight7"]
    entry = Portfolio(cet_timestamp, team_name, email, asset1, asset2, asset3, asset4, asset5, asset6, asset7, weight1, weight2, weight3, weight4, weight5, weight6, weight7)
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