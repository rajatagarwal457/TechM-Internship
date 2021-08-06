import os
import io
import xlrd
import xlwt
from xlwt import *
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
    if request.method == 'POST':
        user = User.query.filter_by(uname = request.form['username']).first()
        if request.form['password'] == user.password:
            resp = make_response(redirect('upload'))
            resp.set_cookie("id", str(user.id))
            return resp
    return render_template('login.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    msg = ''
    print(request.method)
    # print("aa"+request.form['username']+" "+ request.form['password'])
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        id = random.randint(0,10000)
        password = request.form['password']
        repass = request.form['re_pass']
        if not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif password != repass:
            msg = 'Passswords do not match!'
        elif not username or not password or not repass:
            msg = 'Please fill out the form!'
        else:
            user = User.query.filter_by(uname = username).all()
            if user:
                msg = 'user already exists!'
                return render_template('register.html', msg=msg)
            user = User(id=id, uname = username, password = password)
            db.session.add(user)
            db.session.commit()
            print("done")
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register.html', msg = msg)


# Upload API
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    msg=""
    if request.method == 'POST':
        if 'file' not in request.files:
            print('no file')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('no filename')
            return redirect(request.url)
        else:
            cb = request.form['createdBy']
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            loc = (f"./uploads/{filename}")
            wb = xlrd.open_workbook(loc)
            sheet = wb.sheet_by_index(0)
            ent = sheet.cell_value(1, 2)
            per = sheet.cell_value(1, 1)
            for i in range(1, sheet.nrows):
                if sheet.cell_value(i, 2) != ent or sheet.cell_value(i, 1) != per:
                    msg = "Period/Entity mismatch!"
                    os.remove(f"./uploads/{filename}")
                    return render_template('upload_file.html', msg = msg)
            for i in range(1, sheet.nrows):
                e = entity_data(year = int(sheet.cell_value(i, 0)), period = sheet.cell_value(i, 1), entity = sheet.cell_value(i, 2), no_of_items = sheet.cell_value(i, 3), createdBy = cb)
                db.session.add(e)
                db.session.commit()
            os.remove(f"./uploads/{filename}")
    return render_template('upload_file.html', msg=msg)

# Download API
@app.route("/download", methods = ['GET', 'POST'])

def download_file():
    if os.path.exists('temp.xls'):
        os.remove('temp.xls')
    if request.method == 'POST':
        if os.path.exists('temp.xls'):
            os.remove('temp.xls')
        en = request.form['entity']
        e = entity_data.query.filter_by(entity = en).all()
        if len(e) == 0:
            return render_template('download.html', msg = "Entity not found!")
        wb = Workbook()
        s = wb.add_sheet('Sheet 1')
        s.write(0, 0, 'Year')
        s.write(0, 1, 'Period')
        s.write(0, 2, 'Entity')
        s.write(0, 3, 'Number of Items')
        c = 1
        for i in e:
            s.write(c, 0, i.year)
            s.write(c, 1, i.period)
            s.write(c, 2, i.entity)
            s.write(c, 3, i.no_of_items)
            c += 1
        wb.save('temp.xls')
        return send_file('temp.xls', as_attachment=True, attachment_filename=en+".xls")
        os.remove('temp.xls')
    return render_template('download.html')

if __name__ == "__main__":
    context = ('cert.pem', 'key.pem')
    app.run(host='0.0.0.0', debug=True, ssl_context=context)
