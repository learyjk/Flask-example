import os
import sqlalchemy as db

from flask import Flask, render_template
from sqlalchemy.orm import scoped_session, sessionmaker
from random import randint


app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")


engine = db.create_engine(os.getenv("DATABASE_URL"), echo=True)
data = scoped_session(sessionmaker(bind=engine))


@app.route('/')
def home():
    return render_template('home.html')


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


if __name__ == '__main__':
    app.run(debug=True)

# a comment
