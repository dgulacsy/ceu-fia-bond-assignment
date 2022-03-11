import os
from dotenv import load_dotenv
from datetime import datetime as dt, timedelta as td
from flask import Flask, request, render_template, redirect, url_for, send_from_directory, current_app, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
import csv
import pandas as pd

load_dotenv('./venv/.env')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMP'] = 'temp'


db = SQLAlchemy(app)


class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cet_timestamp = db.Column(db.DateTime())
    team_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    asset1 = db.Column(db.String(100))
    weight1 = db.Column(db.Float())
    asset2 = db.Column(db.String(100))
    weight2 = db.Column(db.Float())
    asset3 = db.Column(db.String(100))
    weight3 = db.Column(db.Float())
    asset4 = db.Column(db.String(100))
    weight4 = db.Column(db.Float())
    asset5 = db.Column(db.String(100))
    weight5 = db.Column(db.Float())
    asset6 = db.Column(db.String(100))
    weight6 = db.Column(db.Float())
    asset7 = db.Column(db.String(100))
    weight7 = db.Column(db.Float())
    asset8 = db.Column(db.String(100))
    weight8 = db.Column(db.Float())
    asset9 = db.Column(db.String(100))
    weight9 = db.Column(db.Float())
    asset10 = db.Column(db.String(100))
    weight10 = db.Column(db.Float())
    asset11 = db.Column(db.String(100))
    weight11 = db.Column(db.Float())
    asset12 = db.Column(db.String(100))
    weight12 = db.Column(db.Float())
    asset13 = db.Column(db.String(100))
    weight13 = db.Column(db.Float())
    asset14 = db.Column(db.String(100))
    weight14 = db.Column(db.Float())
    asset15 = db.Column(db.String(100))
    weight15 = db.Column(db.Float())


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/add_portfolio', methods=['POST'])
def add_portfolio():
    columns = [column.name for column in Portfolio.__mapper__.columns]
    [columns.remove(col) for col in ['id', 'cet_timestamp']]
    cet_timestamp = dt.now() + td(hours=1)  # adjust UCT to CET
    values = [request.form[column] if column.startswith(
        'asset') else empty_to_zero(request.form[column]) for column in columns]
    column_value_dict = {col: val for (col, val) in zip(columns, values)}
    column_value_dict.update({'cet_timestamp': cet_timestamp})
    entry = Portfolio(**column_value_dict)
    db.session.add(entry)
    db.session.commit()
    return redirect(url_for('success'))


def empty_to_zero(val):
    return 0 if val == '' else val


@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/current_portfolios')
def current_portfolios():
    subq = (db.session.query(Portfolio.team_name,
                             func.max(Portfolio.cet_timestamp).label('maxdate'))
            .group_by(Portfolio.team_name).subquery())
    q = db.session.query(Portfolio).join(
        subq,
        and_(
            Portfolio.team_name == subq.c.team_name,
            Portfolio.cet_timestamp == subq.c.maxdate)) \
        .order_by(Portfolio.team_name)
    df = pd.read_sql(q.statement, q.session.bind)
    df['cet_timestamp'] = pd.to_datetime(df['cet_timestamp']).round('min')
    df = df.set_index('team_name').drop('id', axis=1).transpose()
    return render_template('current_portfolios.html', tables=[df.to_html(classes='data table')], titles=df.columns.values)


@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    if not os.path.exists('temp'):
        os.makedirs('temp')
    outfile = open('temp/'+filename, 'w')
    outcsv = csv.writer(outfile)
    records = db.session.query(Portfolio).all()
    # dump header
    outcsv.writerow([column.name for column in Portfolio.__mapper__.columns])
    # dump data
    [outcsv.writerow([getattr(curr, column.name)
                     for column in Portfolio.__mapper__.columns]) for curr in records]
    outfile.close()
    temp = os.path.join(current_app.root_path, app.config['TEMP'])
    # abort(404)
    try:
        return send_from_directory(temp, filename=filename, as_attachment=True, cache_timeout=0)
    except FileNotFoundError:
        abort(404)


if __name__ == '__main__':
    db.create_all()
    db.session.commit()
    app.run(debug=True)


# team_name = request.form['team_name']
    # email = request.form['email']
    # asset1 = request.form['asset1']
    # asset2 = request.form['asset2']
    # asset3 = request.form['asset3']
    # asset4 = request.form['asset4']
    # asset5 = request.form['asset5']
    # asset6 = request.form['asset6']
    # asset7 = request.form['asset7']
    # asset8 = request.form['asset8']
    # asset9 = request.form['asset9']
    # asset10 = request.form['asset10']
    # asset11 = request.form['asset11']
    # asset12 = request.form['asset12']
    # asset13 = request.form['asset13']
    # asset14 = request.form['asset14']
    # asset15 = request.form['asset15']

    # weight2 = empty_to_zero(request.form['weight2'])
    # weight3 = empty_to_zero(request.form['weight3'])
    # weight4 = empty_to_zero(request.form['weight4'])
    # weight5 = empty_to_zero(request.form['weight5'])
    # weight6 = empty_to_zero(request.form['weight6'])
    # weight7 = empty_to_zero(request.form['weight7'])
    # weight8 = empty_to_zero(request.form['weight8'])
    # weight9 = empty_to_zero(request.form['weight9'])
    # weight10 = empty_to_zero(request.form['weight10'])
    # weight11 = empty_to_zero(request.form['weight11'])
    # weight12 = empty_to_zero(request.form['weight12'])
    # weight13 = empty_to_zero(request.form['weight13'])
    # weight14 = empty_to_zero(request.form['weight14'])
    # weight15 = empty_to_zero(request.form['weight15'])
