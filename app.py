from flask import Flask, render_template 

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def register():
    return render_template("register.html")

@app.route("/account")
def account():
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