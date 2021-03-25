import os

from flask import Flask, render_template, request
from datetime import datetime
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask import render_template
from flask import redirect

os.environ['DBUSER'] = 'usxuxwby' 
os.environ['DBPASS'] = 'sVUyUo4Z1aqH4MiKkLQtWlw8RNMhaq-H'
os.environ['DBHOST'] = 'queenie.db.elephantsql.com'
os.environ['DBNAME'] = 'usxuxwby'

database_uri = 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
    dbuser=os.environ['DBUSER'],
    dbpass=os.environ['DBPASS'],
    dbhost=os.environ['DBHOST'],
    dbname=os.environ['DBNAME']
)

app = Flask(__name__)

app.config.update(
    SQLALCHEMY_DATABASE_URI=database_uri,
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

# initialize the database connection
db = SQLAlchemy(app)

from Swapify.models.artist import Artist
from Swapify.models.allmodels import User
from Swapify.models.allmodels import Playlist
from Swapify.models.allmodels import Song



migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@app.route('/')
@app.route('/login')
def log():
    scopes = "user-read-private user-read-email";
    my_client_id = "b167636c03db464bac2a9a61c6663685"
    my_redirect_uri = "http://localhost:5000/home"
    return redirect('https://accounts.spotify.com/authorize' +
  '?client_id=' + my_client_id +
  '&redirect_uri=' + my_redirect_uri +
  '&response_type=token')



@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/about')
def about():
    """Renders the mood page."""
    return render_template(
        'about.html',
        title='Mood Page',
        year=datetime.now().year,
        message='Attach a mood to this song!'
    )

@app.route('/contact')
def contact():
    """Renders the playlist page."""
    return render_template(
        'contact.html',
        title='Playlists Page',
        year=datetime.now().year,
        message='Your playlist page. This message is in views.py'
    )

@app.route('/profile')
def profile():
    """Renders the profile page."""
    return render_template(
        'profile.html',
        title='Profile Page',
        year=datetime.now().year,
        message='Settings'
    )

# @app.route("/addartist", method = [Post])
# def addartist():
# 	return ourAddArtist(form.name)

# def ourAddArtist(name):
# 	a1 = Artist("Selena Gomez")
# 	db.session.add(a1)
# 	db.session.commit()
# 	return "done!"


if __name__ == '__main__':
    app.run()