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
   


if __name__ == '__main__':
    app.run(debug=True)