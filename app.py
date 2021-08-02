import os
import re
from datetime import datetime
import random
from werkzeug.utils import secure_filename
from flask import *
from flask_sqlalchemy import SQLAlchemy

UPLOAD_FOLDER = 'uploads/'

#app = Flask(__name__)
app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.static_folder = 'static'
# app.run(debug=True)
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    uname = db.Column(db.String(30))
    password = db.Column(db.String(500))


class entity_data(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    year = db.Column(db.Integer)
    period = db.Column(db.String(10))
    entity = db.Column(db.String(10))
    no_of_items = db.Column(db.Integer)
    createdBy = db.Column(db.String(50))
    createdDate = db.Column(db.DateTime, default = datetime.now)

@app.route('/login', methods = ['GET', 'POST'])
def login():

    return render_template('login.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        uname = request.form['username']
        id = random.randint(0,10000)
        password = request.form['password']
        repass = request.form['repass']
        email = request.form['email']
        # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
        # account = cursor.fetchone()
        # if account:
        #     msg = 'Account already exists !'
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', uname):
            msg = 'Username must contain only characters and numbers !'
        elif password != repass:
            msg = 'Passswords do not match!'
        elif not uname or not password or not email or not repass:
            msg = 'Please fill out the form!'
        else:
            user = User(id=id, uname = uname, password = password)
            db.session.add(user)
            db.session.commit()
            print("done")
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('signup.html', msg = msg)


# Upload API
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('no file')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('no filename')
            return redirect(request.url)
        else:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print("saved file successfully")
      #send file name as parameter to downlad
            # return redirect('/download/'+ filename)

    return render_template('upload_file.html')

# Download API
@app.route("/downloadfile/<filename>", methods = ['GET'])
def download_file(filename):
    return render_template('download.html',value=filename)

@app.route('/return-files/<filename>')
def return_files_tut(filename):
    file_path = UPLOAD_FOLDER + filename
    return send_file(file_path, as_attachment=True, attachment_filename='')

if __name__ == "__main__":
    context = ('cert.pem', 'key.pem')
    app.run(host='0.0.0.0', debug=True, ssl_context=context)
