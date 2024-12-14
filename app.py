from flask import Flask, render_template ,  url_for, redirect, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import bcrypt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///C:/Users/Kavishka/Desktop/my project/library manegment/library-manegment-system/database/account.db'
app.secret_key ="hjghjdhjhuhgjbhj52"
db = SQLAlchemy(app)

class create_account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, email,username, password):
        self.name = username
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=['GET','POST'])
def login():
     if 'email' in session:
        return redirect(url_for('home'))

     if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        user = create_account.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['email'] = user.email
            flash('Logged in successfully!', category='success')
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid user')
   

     return render_template("login.html")


@app.route("/account" , methods=['GET', 'POST'])
def account():
    if request.method== 'POST':
        name= request.form['username']
        email= request.form['email']
        password= request.form['password']
        password2= request .form['password2']

        existing_user = create_account.query.filter_by(email=email).first()
        if existing_user:
            flash('Email is already used', category='error')
        elif password != password2:
            flash('Passwords do not match!', category='error')
        elif len(password) < 5:
            flash('Password must have a minimum of 5 characters', category='error')
        else:
            new_user = create_accoun(name=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully!', category='success')
            return redirect('/login')

    return render_template("account.html")

    

@app.route("/adminlogin")
def adminlogin():
    return render_template("adminlogin.html")  
      
@app.route("/admindashbord")
def admindashbord():
    return render_template("admindashbord.html")     

@app.route("/book")
def book():
    return render_template("book.html")

if __name__ == '__main__':
    app.run(debug=True)