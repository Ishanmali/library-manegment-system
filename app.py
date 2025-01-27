# Updated app.py
from flask import Flask, render_template, url_for, redirect, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
import bcrypt
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/books'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
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
    uploaded_date = db.Column(db.DateTime, default=datetime.utcnow)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route("/")
def home():
    # Fetch books for "New" and "Famous" categories dynamically
    new_books = Book.query.filter(Book.uploaded_date >= datetime.utcnow() - timedelta(days=30)).all()
    famous_books = Book.query.filter(Book.genre == 'Fiction').limit(5).all()  # Example logic for "Famous"
    return render_template("home.html", new_books=new_books, famous_books=famous_books)

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

@app.route("/book")
def book():
    books = Book.query.all()  # Fetch all books
    genres = {book.genre for book in books}  # Extract unique genres dynamically
    return render_template("book.html", books=books, genres=genres)

@app.route('/bookupload', methods=['GET', 'POST'])
def bookupload():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        copies = int(request.form['copies'])
        file = request.files['book_pdf']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_book = Book(
                title=title,
                author=author,
                genre=genre,
                copies=copies,
                pdf_path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
            )
            db.session.add(new_book)
            db.session.commit()
            flash('Book added successfully!')
            return redirect(url_for('book'))
        else:
            flash('Invalid file type. Please upload a PDF.')
    return render_template('bookupload.html')

@app.route("/logout")
def logout():
    session.pop('email', None)
    flash('Logged out successfully!', category='success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
