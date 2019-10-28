import os
import sqlalchemy as db

from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from tempfile import mkdtemp
from sqlalchemy.orm import scoped_session, sessionmaker
from random import randint
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
# Configure session to use filesystem (instead of signed cookies)

#os.environ['SECRET_KEY'] = '3r6t_QQHDSCMtGGjbBYuQQ'
#os.environ['DATABASE_URL'] = 'postgres://sbcrjibpraivpg:cac3d5eaf635b550f67cf802268437d7f2dd6eccf84a13506ae52c5be32f53e4@ec2-107-21-200-103.compute-1.amazonaws.com:5432/d4keqqkhpmbhkn'
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# create session

# connect to the database
engine = db.create_engine(os.getenv("DATABASE_URL"), echo=True)
conn = engine.connect()
data = scoped_session(sessionmaker(bind=engine))


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        hash = generate_password_hash(request.form.get('password'))

        if not username:
            return render_template('register.html', message="Must provide a username")
        if not email:
            return render_template('register.html', message="Must provide email")
        if not request.form.get('password'):
            return render_template('register.html', message="Must proivde passsword")
        if request.form.get('password') != request.form.get('confirmation'):
            return render_template('register.html', message="Passwords must match")

        # query the database for username provided
        row = data.execute("SELECT * FROM users WHERE username=:username", {'username': username}).fetchone()

        if row:
            if row['username'] == username or not check_password_hash(row["hash"], request.form.get("password")):
                return render_template("register.html", message="Invalid username/password")

        data.execute("INSERT INTO users(user_id, hash, username, email) VALUES (default, :h, :u, :e)", {'h': hash, 'u': username, 'e': email})
        data.commit()

        return redirect('/')
    else:
        return render_template('register.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        username = request.form.get('username')
        # Ensure username was submitted
        if not username:
            return render_template("login.html", message="Must provide username")
        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("login.html", message="Must provide password")

        # Query database for username
        row = data.execute("SELECT * FROM users WHERE username = :username",
                           {'username': username}).fetchone()

        # Ensure username exists and password is correct
        if row:
            if row['username'] == username or not check_password_hash(row["hash"], request.form.get("password")):
                return render_template("login.html", message="Invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = row["user_id"]

        # Redirect user to home page
        return redirect('/')

    else:
        return render_template('login.html')


@app.route('/wodg')
def wodg():

    # get random int between 0 and num rows in workout database.
    num_rows = data.execute('SELECT count(*) FROM wods').fetchall()[0][0]
    workout_id = randint(1, num_rows)
    results = data.execute(
        'SELECT * FROM wods WHERE id=:workout_id', {'workout_id': workout_id})

    # fetch the workout
    row = results.fetchone()

    # creates a row with name as workout[1], type as [2], and the rest.
    workout = []
    workout.append(row[1])
    exercises = row[2].split(',')
    for exercise in exercises:
        workout.append(exercise)

    return render_template('wodg.html', workout=workout)


@app.route('/logout')
def logout():
    session.clear()
    return render_template("login.html", message="You have logged out!")


if __name__ == '__main__':
    app.run(debug=True)

# a comment
