from flask import Flask, redirect, session, render_template, request, flash
import sqlite3

conn = sqlite3.connect("QuizGame.db", check_same_thread=False)

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
            flash("Error one is field is missing")

        data = list(db.execute("SELECT * FROM Users WHERE username = ?", [username]))

        if data == []:
            flash("Invalid username")
            return render_template("login.html")
        
        if password == data[0][2]:
            session["username"] = username
            session["id"] = data[0][0]
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
        id = session["id"]
        data = db.execute("SELECT name FROM Questions, Users WHERE username = ?", [username])
        names_of_quizes = list(data)
        names = []
        for i in range(len(names_of_quizes)):
            names.append(names_of_quizes[i][0])

        if request.method == "POST":
        
            if "logout" in request.form:
                session.pop("username", None)
                return redirect("/login")
            
            if "createNew" in request.form:
                return redirect("/configQuiz")
            
            for j in names:
                if f"play{j}" in request.form:
                    session["selectedQuizName"] = j
                    return redirect("/selectGamemode")

                if f"delete{j}" in request.form:
                    db.execute("DELETE FROM Questions WHERE name = ?", [j])
                    conn.commit()
                    return redirect("/home")

        else:
            return render_template("home.html", username=username, names=names)
    else:
        return redirect("/login")
    
@app.route("/configQuiz", methods=["GET", "POST"])
def configQuiz():
    if "username" in session:
        if request.method == "POST":
            name = request.form.get("name")
            numOfQue = int(request.form.get("numOfQue"))

            if numOfQue > 50:
                flash("You cant have more than 50 questions!")
                return render_template("configQuiz.html")

            session["count"] = numOfQue
            session["name"] = name

            return redirect("/createQuiz")
        else:  
            return render_template("configQuiz.html")
    else:
        return redirect("/login")
    
@app.route("/createQuiz", methods=["GET", "POST"])
def createQuiz():
    if "username" in session:
        name = session["name"]
        id = session["id"]
        count = session["count"]
        if request.method == "POST":
            
            questions = []

            for i in range(count):
                question = request.form.get(f"question{i}")
                answer1 = request.form.get(f"answer1{i}")
                answer2 = request.form.get(f"answer2{i}")
                answer3 = request.form.get(f"answer3{i}")
                answer4 = request.form.get(f"answer4{i}")
                questions.append({"question": question, "correctAnswer1": answer1, "answer2": answer2, "answer3": answer3, "answer4": answer4})

           
            db.execute("INSERT INTO Questions(name, numOfQue, Question, person_id) VALUES (?, ?, ?, ?)", [name, count, str(questions), int(id)])
            conn.commit()
          
            session.pop("count", None)
            session.pop("name", None)
            
            return redirect("/home")

        else:
            return render_template("createQuiz.html", count=count)
    else:
        return redirect("/login")
    
@app.route("/selectGamemode", methods=["GET", "POST"])
def selectGamemode():
    if "username" in session:
        username = session["username"]
        quizName = session["selectedQuizName"]
        if request.method == "POST":
            gamemode = request.form.get("gamemode")
            session["gamemode"] = gamemode
            return redirect(f"/play/{gamemode}")
        else:
            return render_template("selectGamemode.html", quizName=quizName)
    else:
        return redirect("/login")

#not working
def data_to_list(data):
    datal = list(data)
    questionstr = datal[0][0]

    string = ""
    for i in questionstr:
        if i != "'" or i == "'":
            string += i

    question = string
    print(type(question))
    #return dict(question)


@app.route("/play/casual")
def playCasual():
    if "username" in session:
        name = session["selectedQuizName"]
        data = db.execute("SELECT Question FROM Questions WHERE name = ?", [name])

        question = data_to_list(data)

        #print(question)

        if request.method == "POST":
            pass
        else:
            return render_template("playCasual.html")
    else:
        return redirect("/login")

@app.route("/play/speedRun")
def playspeedRun():
    if "username" in session:
        username = session["username"]
        if request.method == "POST":
            pass
        else:
            return render_template("playSpeedRun.html")
    else:
        return redirect("/login")

@app.route("/play/hardcore")
def playhardcore():
    if "username" in session:
        username = session["username"]
        if request.method == "POST":
            pass
        else:
            return render_template("playhardcore.html")
    else:
        return redirect("/login")

@app.route("/play/master")
def playmaster():
    if "username" in session:
        username = session["username"]
        if request.method == "POST":
            pass
        else:
            return render_template("playMaster.html")
    else:
        return redirect("/login")


