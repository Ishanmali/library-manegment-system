from flask import Flask, render_template, url_for, redirect, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
from werkzeug.utils import secure_filename
import bcrypt
import os
import requests

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/books'
app.config['UPLOAD_FOLDER2'] = 'static/cover_image'
app.config['ALLOWED_EXTENSIONS_PDF'] = {'pdf'}
app.config['ALLOWED_EXTENSIONS_IMAGE'] = {'png', 'jpg', 'jpeg', 'gif'}
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///books.db'
app.secret_key = "hjghjdhjhuhgjbhj52"

# Create upload directories if they don't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['UPLOAD_FOLDER2'], exist_ok=True)

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
    cover_image = db.Column(db.String(200), nullable=True)

def allowed_pdf(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS_PDF']

def allowed_image(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS_IMAGE']

@app.route("/")
def home():
    new_books = Book.query.order_by(Book.id.desc()).limit(10).all()
    genres = ['Fiction', 'Science', 'Biography', 'Adventure', 'ICT', 'Novel']
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

        if (file and allowed_pdf(file.filename) and 
            cover_image and allowed_image(cover_image.filename)):
            
            pdf_filename = secure_filename(file.filename)
            cover_filename = secure_filename(cover_image.filename)
            
            # Save files
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename))
            cover_image.save(os.path.join(app.config['UPLOAD_FOLDER2'], cover_filename))

            new_book = Book(
                title=title,
                author=author,
                genre=genre,
                copies=copies,
                pdf_path=f"books/{pdf_filename}",
                cover_image=f"cover_image/{cover_filename}"
            )
            
            db.session.add(new_book)
            db.session.commit()
            flash('Book added successfully!')
            return redirect(url_for('book'))
        else:
            flash('Invalid file types. PDF for book and image (PNG, JPG, JPEG, GIF) for cover required.')

    return render_template('bookupload.html')

@app.route("/edit_book/<int:book_id>",methods=['GET','POST'])
def edit_book(book_id):
    book= Book.query.get_or_404(book_id)

    if request.method == 'POST':
        book.titlee = request.form['title']
        book.author = request.form['author']
        book.genre = request.form['genre']
        book.copies = int( request.form['copies'])
        db.session.commit()
        flash("book update successfully..." ,"success")
        return redirect(url_for('book'))
    
    return render_template('edit_book.html',book=book)
  

@app.route("/deleted_book/<int:book_id>",methods=['POST'])
def delete_book(book_id):
    book= Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash("book deleted successfully..." ,"success")
    return redirect(url_for('book'))

@app.route('/book/<book_id>')
def book_details(book_id):
    
    api_key = 'YOUR_GOOGLE_BOOKS_API_KEY'
    url = f'https://www.googleapis.com/books/v1/volumes/{book_id}?key={'AIzaSyBXAzmRYtYaq2bBgdMKS3-aUMKt-6uwwJg'}'
    response = requests.get(url)
    
    if response.status_code == 200:
        book = response.json()
        return render_template('book_details.html', book=book)
    else:
        return "Book not found", 404

@app.route("/member")  
def member():
    return render_template('member.html')
    

@app.route("/logout")
def logout():
    session.pop('email', None)
    flash('Logged out successfully!', category='success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
