import os
import numpy as np
import pandas as pd
import sys
import math
import matplotlib.pyplot as plt
import benford as bf

from curses import meta
from unittest import result
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from benfordParser import benfordParse

ALLOWED_EXTENSIONS = {'txt', 'csv', 'tsv'}
UPLOAD_FOLDER = './upload'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://benfordParser.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_EXTENSIONS'] = ALLOWED_EXTENSIONS
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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
@app.route('/results.html')
def results_page():
    return render_template('results.html')

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
            
            return redirect(url_for('download_file', name=filename))
            return redirect
    return render_template('upload.html')

# @app.rout('/analysis', methods=['GET'])
# def analysis_page():
#     return render_template('analysis.html')


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
   app.run(debug = True, host='0.0.0.0')
