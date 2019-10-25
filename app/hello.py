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

# get all rows
result = data.execute('SELECT * FROM first')


@app.route('/')
def home():
    return render_template('home.html', result=result)


@app.route('/wodg')
def wodg():
    return render_template('wodg.html')


if __name__ == '__main__':
    app.run(debug=True)

# a comment
