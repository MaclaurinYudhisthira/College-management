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

class Classes(db.Model):
    class_id = db.Column(db.Integer, primary_key=True)
    class_name=db.Column(db.String(50), nullable=False)
    subject_name=db.Column(db.String(50), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.teacher_id'))
    teacher_name=db.Column(db.String(100))
    def __init__(self,class_name,subject_name,teacher_id=None,teacher_name=None):
        self.class_name=class_name
        self.subject_name=subject_name
        self.teacher_id=teacher_id
        self.teacher_name=teacher_name

# Table for Student and Class association, we will call it enrollments
class Enrollment(db.Model):
    record_id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.class_id'))
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'))
    class_name=db.Column(db.String(50))
    student_name=db.Column(db.String(50))
    def __init__(self,class_id,student_id,class_name=None,student_name=None):
        self.class_id=class_id
        self.student_id=student_id
        self.class_name=class_name
        self.student_name=student_name

# Creating Database
db.create_all()

@app.route("/")
@app.route("/home")
def home():
    if 'user_id' in session and session['role']=='Student':
        return render_template("student/index.html")
    if 'user_id' in session and session['role']=='Teacher':
        return render_template("teacher/index.html")
    if 'user_id' in session and session['role']=='Admin':
        return render_template("admin/index.html")
    return render_template("index.html")

@app.route("/studentSignIn",methods=['GET','POST'])
def studentSignIn():
    if 'user_id' in session and session['role']=='Student':
        return redirect(url_for('home'))
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
                    return redirect(url_for('home'))
            else:   
                flash('Account not found','error')
                return redirect(url_for("home"))
        else:
            return render_template("student/login.html")
        return redirect(url_for('signout'))

@app.route("/teacherSignIn",methods=['GET','POST'])
def teacherSignIn():
    if 'user_id' in session and session['role']=='Teacher':
        return redirect(url_for('home'))
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
                    return redirect(url_for('home'))
            else:
                flash('Account not found','error')
                return redirect(url_for("home"))
        else:
            return render_template("teacher/login.html")
        return redirect(url_for('signout'))

@app.route("/adminSignIn",methods=['GET','POST'])
def adminSignIn():
    if 'user_id' in session and session['role']=='Admin':
        return redirect(url_for('home'))
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
                    return redirect(url_for('home'))
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
        if request.method=="POST":
            Myword=request.form['password'].encode()
            f=Fernet(pass_key)
            Myword=f.encrypt(Myword).decode()
            Admin =Admins(request.form['first_name'].lower().capitalize(),request.form['last_name'].lower().capitalize(),request.form['email'].lower(),request.form['phone_number'].lower(),Myword)
            db.session.add(Admin)
            db.session.commit()
            return redirect(url_for('signout'))
        else:
            return render_template("admin/addadmin.html")
    return redirect(url_for('signout'))

@app.route("/addStudent",methods=['GET','POST'])
def addStudent():
    if 'user_id' in session and session['role']=='Admin':
        if request.method=="GET":
            return render_template("admin/addstudent.html")
        elif request.method=="POST":
            if Students.query.filter_by(email=request.form['email'].lower()).first():
                flash('This Email address is already registerd','error')
                return render_template("admin/addstudent.html")
            elif Students.query.filter_by(phone_number=request.form['phone_number'].lower()).first():
                flash('This phone_number address is already registerd','error')
                return render_template("admin/addstudent.html")
            else:
                Myword=request.form['password'].encode()
                f=Fernet(pass_key)
                Myword=f.encrypt(Myword).decode()
                Student =Students(request.form['first_name'].lower().capitalize(),request.form['last_name'].lower().capitalize(),request.form['email'].lower(),request.form['phone_number'].lower(),Myword)
                db.session.add(Student)
                db.session.commit()
                return redirect(url_for('home'))
    return redirect(url_for('signout'))

@app.route("/addTeacher",methods=['GET','POST'])
def addTeacher():
    if 'user_id' in session and session['role']=='Admin':
        if request.method=="GET":
            return render_template("admin/addteacher.html")
        elif request.method=="POST":
            if Teachers.query.filter_by(email=request.form['email'].lower()).first():
                flash('This Email address is already registerd','error')
                return render_template("admin/addteacher.html")
            elif Teachers.query.filter_by(phone_number=request.form['phone_number'].lower()).first():
                flash('This phone_number address is already registerd','error')
                return render_template("admin/addteacher.html")
            else:
                Myword=request.form['password'].encode()
                f=Fernet(pass_key)
                Myword=f.encrypt(Myword).decode()
                Teacher =Teachers(request.form['first_name'].lower().capitalize(),request.form['last_name'].lower().capitalize(),request.form['email'].lower(),request.form['phone_number'].lower(),Myword)
                db.session.add(Teacher)
                db.session.commit()
                return redirect(url_for('home'))
    return redirect(url_for('signout'))

@app.route("/addClass",methods=['GET','POST'])
def addClass():
    if 'user_id' in session and session['role']=='Admin':
        if request.method=="GET":
            teachers=Teachers.query.all()
            return render_template("admin/addclass.html",teachers=teachers)
        elif request.method=="POST":
            teacher_id=None
            if 'teacher_id' in request.form:
                teacher_id=request.form['teacher_id']
            teacher=Teachers.query.filter_by(teacher_id=teacher_id).first()
            aclass =Classes(request.form['class_name'].lower().capitalize(),request.form['subject_name'].lower().capitalize(),teacher_id,teacher.first_name+' '+teacher.last_name)
            db.session.add(aclass)
            db.session.commit()
            return redirect(url_for('home'))
    return redirect(url_for('signout'))

@app.route("/getStudents",methods=['GET'])
def getStudents():
    if 'user_id' in session and session['role']=='Admin':
        students=Students.query.all()
        return render_template("admin/students.html",students=students)

@app.route("/getTeachers",methods=['GET'])
def getTeachers():
    if 'user_id' in session and session['role']=='Admin':
        teachers=Teachers.query.all()
        return render_template("admin/Teachers.html",teachers=teachers)

@app.route("/getClasses",methods=['GET'])
def getClasses():
    if 'user_id' in session and session['role']=='Admin':
        classes=Classes.query.all()
        return render_template("admin/Classes.html",classes=classes)

@app.route("/getAdmins",methods=['GET'])
def getAdmins():
    if 'user_id' in session and session['role']=='Admin':
        admins=Admins.query.all()
        return render_template("admin/Admins.html",admins=admins)

@app.route("/editTeacher/<id>",methods=['GET','POST'])
def editTeacher(id):
    if 'user_id' in session and session['role']=='Admin':
        if request.method=="POST":
            teacher=Teachers.query.filter_by(teacher_id=id).first()
            teacher.first_name=request.form['first_name']
            teacher.last_name=request.form['last_name']
            teacher.email=request.form['email']
            teacher.phone_number=request.form['phone_number']
            Myword=request.form['password'].encode()
            f=Fernet(pass_key)
            Myword=f.encrypt(Myword).decode()
            teacher.password=Myword
            db.session.commit()
        teacher=Teachers.query.filter_by(teacher_id=id).first()
        f=Fernet(pass_key)
        Myword=f.decrypt(teacher.password.encode()).decode()
        teacher=dict(teacher.__dict__)
        teacher['password']=Myword
        return render_template("admin/editteacher.html",teacher=teacher)

@app.route("/editStudent/<id>",methods=['GET','POST'])
def editStudent(id):
    if 'user_id' in session and session['role']=='Admin':
        if request.method=="POST":
            student=Students.query.filter_by(student_id=id).first()
            student.first_name=request.form['first_name']
            student.last_name=request.form['last_name']
            student.email=request.form['email']
            student.phone_number=request.form['phone_number']
            Myword=request.form['password'].encode()
            f=Fernet(pass_key)
            Myword=f.encrypt(Myword).decode()
            student.password=Myword
            db.session.commit()
        student=Students.query.filter_by(student_id=id).first()
        f=Fernet(pass_key)
        Myword=f.decrypt(student.password.encode()).decode()
        student=dict(student.__dict__)
        student['password']=Myword
        return render_template("admin/editstudent.html",student=student)

@app.route("/editAdmin/<id>",methods=['GET','POST'])
def editAdmin(id):
    if 'user_id' in session and session['role']=='Admin':
        if request.method=="POST":
            admin=Admins.query.filter_by(admin_id=id).first()
            admin.first_name=request.form['first_name']
            admin.last_name=request.form['last_name']
            admin.email=request.form['email']
            admin.phone_number=request.form['phone_number']
            Myword=request.form['password'].encode()
            f=Fernet(pass_key)
            Myword=f.encrypt(Myword).decode()
            admin.password=Myword
            db.session.commit()
        admin=Admins.query.filter_by(admin_id=id).first()
        f=Fernet(pass_key)
        Myword=f.decrypt(admin.password.encode()).decode()
        admin=dict(admin.__dict__)
        admin['password']=Myword
        return render_template("admin/editadmin.html",admin=admin)

@app.route("/editClass/<id>",methods=['GET','POST'])
def editClass(id):
    if 'user_id' in session and session['role']=='Admin':
        if request.method=="POST":
            c=Classes.query.filter_by(class_id=id).first()
            c.class_name=request.form['class_name']
            c.subject_name=request.form['subject_name']
            c.teacher_id=request.form['teacher_id']
            teacher=Teachers.query.filter_by(teacher_id=c.teacher_id).first()
            c.teacher_name=teacher.first_name+' '+teacher.last_name
            db.session.commit()
        c=Classes.query.filter_by(class_id=id).first()
        teachers=Teachers.query.all()
        return render_template("admin/editClass.html",c=c,teachers=teachers)

@app.route("/enrollStudent",methods=['GET','POST'])
def enrollStudent():
    if 'user_id' in session and session['role']=='Admin':
        if request.method=="POST":
            pass
        else:
            for s, e in db.session.query(Students,Enrollment).filter(Students.student_id == Enrollment.student_id).all():
                print(f"{s} {e}")
            return render_template('admin/enrollstudent.html')

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
    Class=Classes('Class','Subject','1','Teacher_Test')
    db.session.add(Student)
    db.session.add(Teacher)
    db.session.add(Class)
    Admin=Admins('Teacher','Test','testadmin@gmail.com','+919900990099',Myword)
    db.session.add(Admin)
    en=Enrollment(1,1,'class','Student Test')
    db.session.add(en)
    db.session.commit()
    return "Data is loaded for testing"

if __name__=="__main__":
    app.run(debug=True)
