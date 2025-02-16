from flask import Flask, render_template, url_for, redirect, request, session, flash 
from flask_sqlalchemy import SQLAlchemy 
from werkzeug.utils import secure_filename 
from flask_migrate import Migrate
import bcrypt 
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/books'
app.config['UPLOAD_FOLDER2'] = 'static/cover_image'  # Folder for cover images
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///books.db'
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

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    copies = db.Column(db.Integer, nullable=False)
    pdf_path = db.Column(db.String(200), nullable=False)
    cover_image = db.Column(db.String(200), nullable=True)  # Relative path to cover image

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route("/")
def home():
    new_books = Book.query.order_by(Book.id.desc()).limit(10).all()  # Fetch the most recent books
    genres = ['Fiction', 'Science', 'Biography', 'Adventure', 'ICT', 'Novel']  # Define all genres
    genre_books = {genre: Book.query.filter_by(genre=genre).all() for genre in genres}
    return render_template('home.html', new_books=new_books, genre_books=genre_books)

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
    admin_email = "admin123@gmail.com"
    admin_pass = "admin123"

    if request.method == 'POST':
        email = request.form['username']
        password = request.form['password']

        if email == admin_email and password == admin_pass:
            session['admin'] = True
            flash('Welcome, Admin!', category='success')
            return redirect(url_for('admindashbord'))
        else:
            flash('Invalid admin credentials!', category='error')

    return render_template("adminlogin.html")

@app.route("/admindashbord")
def admindashbord():
    if 'admin' not in session:
        flash('Please log in as an admin first!', category='error')
        return redirect(url_for('adminlogin'))
    return render_template("admindashbord.html")

@app.route("/book")
def book():
    books = Book.query.all()  
    return render_template("book.html", books=books)

@app.route('/bookupload', methods=['GET', 'POST'])
def bookupload():  
    if request.method == 'POST': 
        title = request.form['title']    
        author = request.form['author']
        genre = request.form['genre']
        copies = int(request.form['copies'])  
        file = request.files['book_pdf']
        cover_image = request.files['cover_image'] 
            print(f"Received: {title}, {author}, {genre}, {copies}") 

        if file and allowed_file(file.filename) and cover_image:
            filename = secure_filename(file.filename)
            cover_filename = secure_filename(cover_image.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  
            cover_image.save(os.path.join(app.config['UPLOAD_FOLDER2'], cover_filename))

            new_book = Book(
                title=title,
                author=author,
                genre=genre,
                copies=copies,
                pdf_path=os.path.join(app.config['UPLOAD_FOLDER'], filename),
                cover_image=os.path.join('cover_image', cover_filename),  # Save only the relative path
            )
            db.session.add(new_book)
            db.session.commit()
            flash('Book added successfully!')
            return redirect(url_for('book'))  
        else:
            flash('Invalid file type. Please upload a PDF and an image.')
    return render_template('bookupload.html')

@app.route("/logout")
def logout():
    session.pop('email', None)
    flash('Logged out successfully!', category='success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)