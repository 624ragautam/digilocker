from flask import Flask,render_template,request,session,redirect,url_for,flash,send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_manager,LoginManager
from flask_login import login_required,current_user
import json
from io import BytesIO
# MY db connection
local_server= True
app = Flask(__name__)
app.secret_key='gautam'
  
guser=""

# this is for getting unique user access
login_manager=LoginManager(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return External_user.query.get(int(user_id))



# app.config['SQLALCHEMY_DATABASE_URL']='mysql://username:password@localhost/databas_table_name'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/documentMS'
db=SQLAlchemy(app)

# here we will create db models that is tables


class User_grants(db.Model):
    uid=db.Column(db.Integer,primary_key=True)
    id=db.Column(db.Integer)
    uname=db.Column(db.String(100))
    fname=db.Column(db.String(100))

class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    email=db.Column(db.String(100))

class External_user(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50))
    email=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(1000))

class File(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    fname=db.Column(db.String(50))
    data=db.Column(db.BLOB(10000000))
    email=db.Column(db.String(50))
    description=db.Column(db.String(50))
    

@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == "POST":
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')
        user=External_user.query.filter_by(email=email).first()
        if user:
            flash("Email Already Exist","warning")
            return render_template('/signup.html')
        encpassword=generate_password_hash(password)

        new_user=db.engine.execute(f"INSERT INTO `external_user` (`username`,`email`,`password`) VALUES ('{username}','{email}','{encpassword}')")

        # this is method 2 to save data in db
        # newuser=User(username=username,email=email,password=encpassword)
        # db.session.add(newuser)
        # db.session.commit()
        flash("Signup Succes Please Login","success")
        return render_template('login.html')

          

    return render_template('signup.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == "POST":
        email=request.form.get('email')
        password=request.form.get('password')
        user=External_user.query.filter_by(email=email).first()

        if user and check_password_hash(user.password,password):
            login_user(user)
            flash("Login Success","primary")
            return redirect(url_for('index'))
        else:
            flash("invalid credentials","danger")
            return render_template('login.html')    

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout SuccessFul","warning")
    return redirect(url_for('login'))

@app.route('/permissions')
@login_required
def permissions():
    query=db.engine.execute(f"SELECT * FROM `user_grants`") 
    return render_template('permissions.html',query=query)

@app.route('/access',methods=['POST','GET'])
@login_required
def access():
    if request.method == "POST":
        key=request.form.get('key')
        x=key.split("$")
        y=x[1]
        user=File.query.filter_by(id=y).first()
        if user:
            upload = File.query.filter_by(id=y).first()
            return send_file(BytesIO(upload.data), attachment_filename=upload.fname, as_attachment=True)
        else:
            flash("invalid credentials","danger")
            return render_template('Acessfile.html')
    return render_template('Acessfile.html')



@app.route('/test')
def test():
    try:
        Test.query.all()
        return 'My database is Connected'
    except:
        return 'My db is not Connected'


app.run(debug=True)    