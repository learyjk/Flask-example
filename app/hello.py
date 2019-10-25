import os

from flask import Flask, render_template
from sqlalchemy import create_engine

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")


engine = create_engine(os.getenv("DATABASE_URL"))


@app.route('/')
def home():
    return render_template('home.html', var=os.getenv('DATABASE_URL'))


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)

# a comment
