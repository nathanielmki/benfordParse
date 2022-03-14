import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import csv
import numpy as np
import pandas as pd
import sys
import math
import benford as bf

from curses import meta
from unittest import result
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'txt', 'csv', 'tsv', 'png'}
UPLOAD_FOLDER = './upload'
RESULTS_FOLDER = './results'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://benfordParser.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_EXTENSIONS'] = ALLOWED_EXTENSIONS
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER
db = SQLAlchemy(app)

class Upload(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        filename = db.Column(db.String(50))
        data = db.Column(db.LargeBinary)

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/about')
def about_page():
    return render_template('about.html')

# view results of parsing a file through benfordParser
@app.route('/results.html', methods = ['GET', 'POST'])
def results_page():
    file = request.files['file']
    if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            saved_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(saved_file)
    # create dataframe of uploaded file, 
    # engine is specified to allow python to determine delimiter
    df = pd.read_csv(saved_file, sep=None, engine='python')
    # try:
    #     print(df)
    # except ValueError:
    #     print("Is your file empty?")
    # create dataframe based upon user defined analysis column
    # try:
    # try:
    column_name = request.form['columnOperator']
    # except KeyError:
    #     print("Was a valid column name provided?")    
    analysis_data = df[column_name]
    print(analysis_data)
    # except KeyError:
    #     print("Not a valid column selection, please examine your file and try again")

    # perform Benford test on selected data, with user defined output
    results_name = request.form['resultsOperator']
    save_plot = 'static/results/' + results_name + '_plot.png'
    # try:
    f1d = bf.first_digits(analysis_data, digs=1, save_plot=save_plot)
    print(f1d)

    # except UnboundLocalError:
    #     print("Did you select a valid column to operate on?")
    # saves output csv file to disk
    if results_name !=None:
        save_datafile = 'static/results/' + results_name + '.csv'
        f1d.to_csv(save_datafile, encoding='utf-8', index=True)
    else:
        print(f1d)

    return render_template('results.html', datafile=f1d, plot_path=save_plot, datafile_path=save_datafile)

@app.route('/results/<name>')
def display_csv(name):
    return send_from_directory(app.config["RESULTS_FOLDER"], name)

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # upload = Upload(filename=file.filename, data=file.read())
        # db.session.add(upload)
        # db.session.commit()
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # username = request.form['Username', None]
            # project_name = request.form['Project Name', None]
            # os.path.join([RESULTS_FOLDER, username, project_name])
            return redirect(url_for('download_file', name=filename))
            #return redirect(url_for('interactions.html'))
    return render_template('upload.html', file=file)

# @app.route('/upload/<name>/interactions/benford', methods=['GET', 'POST'])
# def benford(infile = "", outfile=None, analysis_column=""):
#     # create dataframe of uploaded file, 
#     # engine is specified to allow python to determine delimiter
#     df = pd.read_csv(infile, sep=None, engine='python')

#     # create dataframe based upon user defined analysis column
#     analysis_data = df[analysis_column]

#     # perform Benford test on selected data, defined to be the first digits
#     f1d = bf.first_digits(analysis_data, digs=1, save_plot=outfile + '_plot')
#     print(f1d)
    
#     # if outfile name is given, saves output to disk 
#     if outfile !=None:
#         f1d.to_csv(outfile + '.csv', encoding='utf-8', index=False)
#     else:
#         print(f1d)
#     return render_template('benford.html')

# @app.route('/api/v1/upload', methods=['POST'])
# def api_v1_upload():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         # upload = Upload(filename=file.filename, data=file.read())
#         # db.session.add(upload)
#         # db.session.commit()
#         # If the user does not select a file, the browser submits an
#         # empty file without a filename.
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             return redirect(url_for('download_file', name=filename))
#     return render_json()

if __name__ == '__main__':
    #port = int(os.environ.get('PORT', 6080))
    app.run(debug = True, host='0.0.0.0')
