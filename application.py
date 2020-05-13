import os
import datetime

from flask import Flask, render_template, request, session, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
   return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():

    #Reached route through GET method
    if request.method == "GET":
        return render_template("register.html")
    
    #Reached route through POST method
    elif request.method == "POST":
        
        #Checks if email is already taken
        taken_email = db.execute("SELECT * FROM users WHERE username = :username",
                                {"username":request.form.get("username")}).fetchone()
        if taken_email:
            return render_template("error.html", message="Username already taken")

        #Check if password is matching confirmed password
        elif not request.form.get("psw") == request.form.get("psw2"):
            return render_template("error.html", message="Passwords do not match")
 
        #Sends submitted email and password to database
        db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
                    {"username":request.form.get("username"), "password":request.form.get("psw")})
        db.commit()

    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():

    #Reached route through GET method
    if request.method == "GET":
        return render_template("login.html")
    
    elif request.method == "POST":

        login = db.execute("SELECT * FROM users WHERE username = :username AND password = :password",
                    {"username":request.form.get("username"), "password":request.form.get("psw")}).fetchall()
        
        if not login:
            return render_template("error.html", message="Wrong username or password")
        else:
            return render_template("index.html")
            
        
