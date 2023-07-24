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


# this is for getting unique user access
login_manager=LoginManager(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



# app.config['SQLALCHEMY_DATABASE_URL']='mysql://username:password@localhost/databas_table_name'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/documentMS'
db=SQLAlchemy(app)

# here we will create db models that is tables
class History(db.Model):
    tid=db.Column(db.Integer,primary_key=True)
    rollno=db.Column(db.String(100))
    action=db.Column(db.String(100))
    timestamp=db.Column(db.String(100))

class User_grants(db.Model):
    uid=db.Column(db.Integer,primary_key=True)
    id=db.Column(db.Integer)
    uname=db.Column(db.String(100))
    fname=db.Column(db.String(100))

class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    email=db.Column(db.String(100))

class User(UserMixin,db.Model):
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

@app.route('/studentdetails')
def studentdetails():
    query=db.engine.execute(f"SELECT * FROM `file`") 
    return render_template('studentdetails.html',query=query)

@app.route('/triggers')
def triggers():
    query=db.engine.execute(f"SELECT * FROM `history`") 
    return render_template('triggers.html',query=query)

@app.route('/search',methods=['POST','GET'])
def search():
    if request.method=="POST":
        fname=request.form.get('fname')
        bio=File.query.filter_by(fname=fname).first()
        return render_template('search.html',bio=bio)
        
    return render_template('search.html')

@app.route("/delete/<string:id>",methods=['POST','GET'])
@login_required
def delete(id):
    db.engine.execute(f"DELETE FROM `file` WHERE `file`.`id`={id}")
    flash("Slot Deleted Successful","danger")
    return redirect('/studentdetails')


@app.route("/edit/<string:id>",methods=['POST','GET'])
@login_required
def edit(id):
   
    posts=File.query.filter_by(id=id).first()
    if request.method=="POST":
        fname=request.form.get('fname')
        description=request.form.get('data')
        data=request.form.get('description')
        query=db.engine.execute(f"UPDATE `file` SET `fname`='{fname}',`description`='{description}',`data`='{data}' WHERE `file`.`id`={id}")
        flash("Slot is Updates","success")
        return redirect('/studentdetails')
    
    return render_template('edit.html',posts=posts)

@app.route('/download/<string:id>')
def download(id):
    upload = File.query.filter_by(id=id).first()
    return send_file(BytesIO(upload.data), attachment_filename=upload.fname, as_attachment=True)


@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == "POST":
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()
        if user:
            flash("Email Already Exist","warning")
            return render_template('/signup.html')
        encpassword=generate_password_hash(password)

        new_user=db.engine.execute(f"INSERT INTO `user` (`username`,`email`,`password`) VALUES ('{username}','{email}','{encpassword}')")

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
        user=User.query.filter_by(email=email).first()

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



@app.route('/addstudent',methods=['POST','GET'])
@login_required
def addstudent():
    email=db.engine.execute(f"select * from user")
    if request.method=="POST":
        fname=request.form.get('fname')
        email=request.form.get('email')
        data=request.form.get('data')
        # data=request.files['data'].read()
        description=request.form.get('description')
        query=db.engine.execute(f"INSERT INTO `file` (`fname`,`email`,`data`,`description`) VALUES ('{fname}','{email}','{data}','{description}')")
        flash("Booking Confirmed","info")


    return render_template('student.html',email=email)

@app.route('/grant',methods=['POST','GET'])
@login_required
def grant():
    user=db.engine.execute(f"select * from external_user")
    file=db.engine.execute(f"select * from file")
    if request.method=="POST":
        uname=request.form.get('uname')
        fname=request.form.get('fname')
        bio=File.query.filter_by(fname=fname).first()
        query=db.engine.execute(f"INSERT INTO `user_grants` (`id`,`email`,`fname`) VALUES ('{bio.id}','{uname}','{fname}')")
        key="#dig$"+str(bio.id)+"$asa"
        return render_template('grant.html',bio=key)
        
    return render_template('grant.html',user=user,file=file)
@app.route('/test')
def test():
    try:
        Test.query.all()
        return 'My database is Connected'
    except:
        return 'My db is not Connected'


app.run(debug=True)    