Website is live!
http://flask-example-nunchuck.herokuapp.com/

This is my final project for CS50.  My idea was to build a WOD (Workout of the Day) Generator/Tracker that adhered to the following learning objectives:

1. Shall be developed on my local machine and deployed to the web via GitHub and Heroku.
2. Shall read/write from a remote database.
3. Shall look somewhat neat.

The web app shall:

1. Display a random workout and allow the user to click for a newly generated workout.
2. Keep track of user scores and display them chronologically.

Still to be desired:

1. Add more of the workouts (left at Murph https://www.crossfit.com/cf/faq).
2. Allow a user to add his/her own custom workout.
3. Allow user to explore WODs from a list/table rather than just get something random.
4. Allow sorting by date or by workout in /home.
5. More data validation:
  a. Minimum username/password requirements.
  b. Send an email welcoming the user upon registration.
  c. Score entry validation

Problems encountered, lessons learned, or things I had to study beyond CS50 content:
1. Deployment to Heroku worked at first but at some point my program would randomly return users to the login page after various amounts of clicking through the app.  Solution was to change from gunicorn v19.9.0 to v18.0.0 as discussed in the following thread: https://github.com/miguelgrinberg/flasky/issues/58
2. Had to get smart on the Procfile.  Inital deployent was difficult because I didn;t know I had to use --chdir flag since my app "hello.py" was nested in a folder called "app" and I wasn't telling Heroku that.
3. Still need to read up on environment variables esp. DATABASE_URL and SECRET_KEY.  Lots of online tutorials on this but a lot of them use different methods.  I imagine the CS50 web app course touches on this at some point.
4. Understanding virtual environments is key!  I imagine CS50 web app course touches on this too.
5. Take the CS50 web app course :)
6. Using .fetchall() or .fetchone() after my db.execute(SQL code) calls.  SQLAlchemy documentation eventually got me there.
