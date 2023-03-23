from flask import Flask, redirect, session, render_template, request
import sqlite3

conn = sqlite3.connect("QuizGame.db")

db = conn.cursor()

app = Flask(__name__)
 
#config
app.config['SECRET_KEY'] = 'SECRET'

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        if "login" in request.form:
            return redirect("/login")
        elif "signup" in request.form:
            return redirect("/signup")
    else:
        return render_template("index.html")
    
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            print("Error")

              
    else:
        return render_template("login.html")
    
@app.route("/signup", methods=["GET", "POST"])
def signup():
    return render_template("signup.html")

