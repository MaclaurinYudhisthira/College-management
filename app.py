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

# Creating Database
db.create_all()

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/studentSignIn",methods=['GET','POST'])
def studentSignIn():
    if 'user_id' in session:
        flash('Existing login is found','error')
        return redirect(url_for("home"))
    else:
        if request.method=="POST":
            if Students.query.filter_by(email=request.form['email'].lower()).first():
                found_user=Students.query.filter_by(email=request.form['email'].lower()).first()
            else:
                print('Here')
                found_user=Students.query.filter_by(phone_number=request.form['email'].lower()).first()
            if found_user:
                f=Fernet(pass_key)
                Myword=f.decrypt(found_user.password.encode()).decode()
                if request.form['password']==Myword:
                    session.clear()
                    session['user_id']=found_user.student_id
                    flash('You have logged in Successfully','success')
                    return render_template("student/index.html")
            else:
                print("else")
                flash('Account not found','error')
                return redirect(url_for("home"))
        else:
            return render_template("student/login.html")
        pass

@app.route("/signout")
def signout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/load")
def load():
    Myword='123'.encode()
    f=Fernet(pass_key)
    Myword=f.encrypt(Myword).decode()
    Student=Students('Kishan','Dasondhi','kishandasondhi123@gmail.com','+919981392771',Myword)
    db.session.add(Student)
    db.session.commit()
    return "Data is loaded for testing"

if __name__=="__main__":
    app.run(debug=True)
