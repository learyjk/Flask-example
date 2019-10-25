import os
import sqlalchemy as db

from flask import Flask, render_template
from sqlalchemy.orm import scoped_session, sessionmaker


app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")


engine = db.create_engine(os.getenv("DATABASE_URL"), echo=True)
data = scoped_session(sessionmaker(bind=engine))

#get row with id=MAKE IT RANDOM
results = data.execute('SELECT * FROM wods WHERE id=1')
row = results.fetchone()
workout = []
workout.append(row[1])
exercises = row[2].split(',')
for exercise in exercises:
    workout.append(exercise)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/wodg')
def wodg():
    return render_template('wodg.html', results=results, workout=workout)


if __name__ == '__main__':
    app.run(debug=True)

# a comment
