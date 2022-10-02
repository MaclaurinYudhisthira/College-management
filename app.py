# Set-ExecutionPolicy Unrestricted -Scope Process
# env\Scripts\activate
# python app.py
from flask import Flask,render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
import dotenv
import os
from cryptography.fernet import Fernet

# app object
app=Flask(__name__)

# secret key for session
app.secret_key=os.getenv("SECRET_KEY")

# database setup
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db = SQLAlchemy(app)

# loading .env
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

# password encryption key
pass_key=bytes(os.getenv("PASS_KEY"), 'utf-8')

# DB Models
class Students(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    first_name=db.Column(db.String(50), nullable=False)
    last_name=db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120),unique=True, nullable=False)
    password=db.Column(db.String(150), nullable=False)
    phone_number=db.Column(db.String(13),unique=True, nullable=False)
    def __init__(self,first_name,last_name,email,phone_number,password):
        self.first_name=first_name
        self.last_name=last_name
        self.email = email
        self.password = password
        self.phone_number = phone_number

class Teachers(db.Model):
    teacher_id = db.Column(db.Integer, primary_key=True)
    first_name=db.Column(db.String(50), nullable=False)
    last_name=db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120),unique=True, nullable=False)
    password=db.Column(db.String(150), nullable=False)
    phone_number=db.Column(db.String(13),unique=True, nullable=False)
    def __init__(self,first_name,last_name,email,phone_number,password):
        self.first_name=first_name
        self.last_name=last_name
        self.email = email
        self.password = password
        self.phone_number = phone_number

class Admins(db.Model):
    admin_id = db.Column(db.Integer, primary_key=True)
    first_name=db.Column(db.String(50), nullable=False)
    last_name=db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120),unique=True, nullable=False)
    password=db.Column(db.String(150), nullable=False)
    phone_number=db.Column(db.String(13),unique=True, nullable=False)
    def __init__(self,first_name,last_name,email,phone_number,password):
        self.first_name=first_name
        self.last_name=last_name
        self.email = email
        self.password = password
        self.phone_number = phone_number

# Creating Database
db.create_all()

@app.route("/")
@app.route("/home")
def home():
    if 'user_id' in session and session['role']=='Student':
        return render_template("student/index.html")
    if 'user_id' in session and session['role']=='Teacher':
        return render_template("teacher/index.html")
    return render_template("index.html")

@app.route("/studentSignIn",methods=['GET','POST'])
def studentSignIn():
    if 'user_id' in session and session['role']=='Student':
        return render_template("student/index.html")
    else:
        if request.method=="POST":
            if Students.query.filter_by(email=request.form['email'].lower()).first():
                found_user=Students.query.filter_by(email=request.form['email'].lower()).first()
            else:
                found_user=Students.query.filter_by(phone_number=request.form['email'].lower()).first()
            if found_user:
                f=Fernet(pass_key)
                Myword=f.decrypt(found_user.password.encode()).decode()
                if request.form['password']==Myword:
                    session.clear()
                    session['user_id']=found_user.student_id
                    session['role']='Student'
                    flash('You have logged in Successfully','success')
                    return render_template("student/index.html")
            else:   
                flash('Account not found','error')
                return redirect(url_for("home"))
        else:
            return render_template("student/login.html")
        return redirect(url_for('signout'))

@app.route("/teacherSignIn",methods=['GET','POST'])
def teacherSignIn():
    if 'user_id' in session and session['role']=='Teacher':
        return render_template("teacher/index.html")
    else:
        if request.method=="POST":
            if Teachers.query.filter_by(email=request.form['email'].lower()).first():
                found_user=Teachers.query.filter_by(email=request.form['email'].lower()).first()
            else:
                found_user=Teachers.query.filter_by(phone_number=request.form['email'].lower()).first()
            if found_user:
                
                f=Fernet(pass_key)
                Myword=f.decrypt(found_user.password.encode()).decode()
                if request.form['password']==Myword:
                    session.clear()
                    session['user_id']=found_user.teacher_id
                    session['role']='Teacher'
                    flash('You have logged in Successfully','success')
                    return render_template("teacher/index.html")
            else:
                flash('Account not found','error')
                return redirect(url_for("home"))
        else:
            return render_template("teacher/login.html")
        return redirect(url_for('signout'))

@app.route("/adminSignIn",methods=['GET','POST'])
def adminSignIn():
    if 'user_id' in session and session['role']=='Admin':
        return render_template("admin/index.html")
    else:
        if request.method=="POST":
            if Admins.query.filter_by(email=request.form['email'].lower()).first():
                found_user=Admins.query.filter_by(email=request.form['email'].lower()).first()
            elif Admins.query.filter_by(phone_number=request.form['email'].lower()).first():
                found_user=Admins.query.filter_by(phone_number=request.form['email'].lower()).first()
            else:
                return redirect(url_for('signout'))
            if found_user:
                f=Fernet(pass_key)
                Myword=f.decrypt(found_user.password.encode()).decode()
                if request.form['password']==Myword:
                    session.clear()
                    session['user_id']=found_user.admin_id
                    session['role']='Admin'
                    flash('You have logged in Successfully','success')
                    return render_template("admin/index.html")
            else:
                flash('Account not found','error')
                return redirect(url_for("home"))
        elif Admins.query.all() == []:
            return render_template("admin/masterkey.html")
        else:
            return render_template("admin/login.html")
        return redirect(url_for('signout'))

@app.route("/validateMasterKey",methods=['POST'])
def validateMasterKey():
    if 'user_id' in session:
        return redirect(url_for('signout'))
    else:
        if request.method=="POST":
            if 'masterkey' in request.form and request.form['masterkey']==os.getenv("MASTER_KEY"):
                session['ismaster']=True
                return render_template("admin/addadmin.html")
    return redirect(url_for('signout'))

@app.route("/addAdmin",methods=['GET','POST'])
def addAdmin():
    if ('ismaster' in session and session['ismaster'] == True) or ('user_id' in session and session['role']=='Admin'):
        Myword=request.form['password'].encode()
        f=Fernet(pass_key)
        Myword=f.encrypt(Myword).decode()
        Admin =Admins(request.form['first_name'].lower().capitalize(),request.form['last_name'].lower().capitalize(),request.form['email'].lower(),request.form['phone_number'].lower(),Myword)
        db.session.add(Admin)
        db.session.commit()
        return render_template("admin/index.html")
    return redirect(url_for('signout'))

@app.route("/signout")
def signout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/load")
def load():
    Myword='123'.encode()
    f=Fernet(pass_key)
    Myword=f.encrypt(Myword).decode()
    Student=Students('Student','Test','teststudent@gmail.com','+919900990099',Myword)
    Teacher=Teachers('Teacher','Test','testteacher@gmail.com','+919900990099',Myword)
    
    db.session.add(Student)
    db.session.add(Teacher)
    # Admin=Admins('Teacher','Test','testteacher@gmail.com','+919900990099',Myword)
    # db.session.add(Admin)
    db.session.commit()
    return "Data is loaded for testing"

if __name__=="__main__":
    app.run(debug=True)
