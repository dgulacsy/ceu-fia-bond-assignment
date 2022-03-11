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
    'DATABASE_URL')
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
            Portfolio.cet_timestamp == subq.c.maxdate))
    q = q.order_by(Portfolio.team_name)
    df = query_result_to_dataframe(q)
    return render_template('current_portfolios.html', tables=[df.to_html(classes='data table')], titles='')


def query_result_to_dataframe(query_result):
    df = pd.read_sql(query_result.statement, query_result.session.bind)
    df['cet_timestamp'] = pd.to_datetime(df['cet_timestamp']).round('min')
    df = df.set_index('team_name').drop('id', axis=1).transpose()
    return df


@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    if not os.path.exists('temp'):
        os.makedirs('temp')
    with open('temp/'+filename, 'w') as outfile:
        outcsv = csv.writer(outfile)
        records = db.session.query(Portfolio).all()
        columns = Portfolio.__mapper__.columns
        outcsv.writerow([column.name for column in columns])  # dump header
        [outcsv.writerow([getattr(record, column.name)
                          for column in columns]) for record in records]  # dump data

    temp_path = os.path.join(current_app.root_path, app.config['TEMP'])
    try:
        return send_from_directory(temp_path, filename=filename, as_attachment=True, cache_timeout=0)
    except FileNotFoundError:
        abort(404)


if __name__ == '__main__':
    db.create_all()
    db.session.commit()
    app.run(debug=True)
