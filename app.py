from flask import Flask, redirect, session, render_template, request, flash
import sqlite3

conn = sqlite3.connect("QuizGame.db", check_same_thread=False)

db = conn.cursor()

#x = db.execute("SELECT * FROM Users")
#print(list(x))

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
            flash("Error one is field is missing")

        data = list(db.execute("SELECT * FROM Users WHERE username = ?", [username]))

        if data == []:
            flash("Invalid username")
            return render_template("login.html")
        
        if password == data[0][2]:
            session["username"] = username
            return redirect("/home")
        
        flash("Wrong password")
        return render_template("login.html")
    else:
        return render_template("login.html")
    
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmPassword = request.form.get("confirmPassword")

        if not username or not password or not confirmPassword:
            flash("Error one is field is missing")
            return render_template("signup.html")
        
        if password != confirmPassword:
            flash("Error, passwords do not match")
            return render_template("signup.html")

        data = list(db.execute("SELECT * FROM Users WHERE username = ?", [username]))

        if not data == []:
            flash("Error, a user with this username already exists")
            return render_template("signup.html")

        db.execute("INSERT INTO Users (username, password) VALUES (?,?)", [username, password])
        conn.commit()

        return redirect("/login")
    else:
        return render_template("signup.html")
    
@app.route("/home", methods=["GET", "POST"])
def home():
    if "username" in session:
        username = session["username"]
        if request.method == "POST":

            if "logout" in request.form:
                session.pop("username", None)
                return redirect("/login")
           
        else:
            return render_template("home.html", username=username)
    else:
        return redirect("/login")

