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
    testFriends()
    print("friends tested")
    """Renders the home page."""
    # return render_template(
    #     'index.html',
    #     title='Home Page',
    #     year=datetime.now().year,
    # )

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
@app.route('/newUser', methods = ['POST'])
def addUser(form):
    # frontend, add form parsing here, you need to send first name, 
    # last name and email to create a new user
    u1 = User(first, last, email)
    db.session.add(u1)
    db.session.commit()
    return u1

@app.route('/addFriend', methods=['POST'])
def addFriend(form):
    # frontend add form parsing here, get the email of the current user (u1_email) and the 
    # user that they want to add as a friend (u2_email)
    u1 = User.query.filter_by(email=u1_email).first()
    u2 = User.query.filter_by(email=u2_email).first()
    u1.friended.append(u2)
    db.session.commit()


@app.route('/newSong', methods=['POST'])
def addSong(form):
    #frontend add form parsing here, you need a unique identifier from spotify (spotify_id)
    s1 = Song(spotify_id)
    db.session.add(s1)
    db.session.commit()
    return s1

@app.route('/newPlaylist', methods=['POST'])
def addPlaylist(form):
    #frontend add form parsing you need playlist name, length and user_id
    p1 = Playlist(name, length, user_id)
    db.session.add(p1)
    db.session.commit()
    return p1

@app.route('/addHappySong', methods=['POST'])
def addHappySong(form):
    #frontend add form parsing you need user email, and spotify_id for the song
    u1 = User.query.filter_by(email=email).first()
    s1 = Songs.query.filter_by(spotify_id=spotify_id).first()
    if s1 is None:
        s1 = Song(spotify_id)
        db.session.add(s1)
        db.session.commit()
    
    u1.happy_music.append(s1)
    db.session.commit()

@app.route('/addSadSong', methods=['POST'])
def addSadSong(form):
    #frontend add form parsing you need user email, and spotify_id for the song
    u1 = User.query.filter_by(email=email).first()
    s1 = Songs.query.filter_by(spotify_id=spotify_id).first()
    if s1 is None:
        s1 = Song(spotify_id)
        db.session.add(s1)
        db.session.commit()
    
    u1.sad_music.append(s1)
    db.session.commit()

@app.route('/addStudySong', methods=['POST'])
def addStudySong(form):
    #frontend add form parsing you need user email, and spotify_id for the song
    u1 = User.query.filter_by(email=email).first()
    s1 = Songs.query.filter_by(spotify_id=spotify_id).first()
    if s1 is None:
        s1 = Song(spotify_id)
        db.session.add(s1)
        db.session.commit()
    
    u1.study_music.append(s1)
    db.session.commit()

@app.route('/addPartySong', methods=['POST'])
def addPartySong(form):
    #frontend add form parsing you need user email, and spotify_id for the song
    u1 = User.query.filter_by(email=email).first()
    s1 = Songs.query.filter_by(spotify_id=spotify_id).first()
    if s1 is None:
        s1 = Song(spotify_id)
        db.session.add(s1)
        db.session.commit()
    
    u1.party_music.append(s1)
    db.session.commit()




if __name__ == '__main__':
    app.run()