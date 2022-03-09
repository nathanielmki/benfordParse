import os
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'txt', 'csv', 'tsv'}
UPLOAD_FOLDER = './upload'
app = Flask(__name__)

app.config['UPLOAD_EXTENSIONS'] = ['.txt', '.csv', '.tsv']
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# what url to navigate to and display html code
# @app.route('/hello')
# def hello_world():
#     return '<h1>Salam, Donya!</h1>'

# @app.route('/about/<username>')
# def about_page(username):
#     return f'<h1>This is the about page of {username}</h1>'

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
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
    return render_template('upload.html')

#@app.route('/')
#def benfordParse():

if __name__ == '__main__':
   app.run(debug = True)
