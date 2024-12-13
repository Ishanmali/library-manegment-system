from flask import Flask, render_template, url_for, redirect, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import bcrypt


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///CreateAccount.db' 
app.secret_key = "hjghjdhjhuhgjbhj52" 
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class CreateAccount(db.Model):
    __tablename__ = 'create_account'  
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, email, username, password):
        self.name = username
        self.email = email
        
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
       
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if 'email' in session:
        return redirect(url_for('home'))  

    if request.method == 'POST':
        email = request.form['username']  
        password = request.form['password']
        user = CreateAccount.query.filter_by(email=email).first()  
        if user and user.check_password(password):
            session['email'] = user.email  
            flash('Logged in successfully!', category='success')
            return redirect(url_for('home')) 
        else:
            flash('Invalid username or password!', category='error')
            return render_template('login.html')  

    return render_template("login.html")


@app.route("/account", methods=['GET', 'POST'])
def account():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password2 = request.form['password2']

        existing_user = CreateAccount.query.filter_by(email=email).first()
        if existing_user:
            flash('Email is already registered', category='error')
        elif password != password2:  
            flash('Passwords do not match!', category='error')
        elif len(password) < 5: 
            flash('Password must have at least 5 characters', category='error')
        else:
            
            new_user = CreateAccount(email=email, username=username, password=password)
            db.session.add(new_user)  
            db.session.commit()  
            flash('Account created successfully!', category='success')
            return redirect(url_for('login'))  

    return render_template("account.html")

@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    
    admin_email = "admin@librify.com"
    admin_password = "admin123"

    if request.method == 'POST':
        email = request.form['username']
        password = request.form['password']

    
        if email == admin_email and password == admin_password:
            session['admin'] = True 
            flash('Welcome, Admin!', category='success')
            return redirect(url_for('admindashbord'))
        else:
            flash('Invalid admin credentials!', category='error')

    return render_template("adminlogin.html")

@app.route("/admindashbord")
def admindashbord():
    if 'admin' not in session:  # Check if admin is logged in
        flash('Please log in as an admin first!', category='error')
        return redirect(url_for('adminlogin'))
    return render_template("admindashbord.html")

@app.route("/book")
def book():
    return render_template("book.html")


@app.route("/logout")
def logout():
    session.pop('email', None)  
    flash('Logged out successfully!', category='success')
    return redirect(url_for('home'))  


if __name__ == '__main__':
    app.run(debug=True)
