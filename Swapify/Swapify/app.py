import os
import json

from flask import Flask, render_template, request
import requests
from datetime import datetime
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask import render_template
from flask import redirect
from urllib.parse import quote
import json
import spotipy
from flask import jsonify

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
    scopes = "user-read-private user-read-email"
    my_client_id = "b167636c03db464bac2a9a61c6663685"
    my_redirect_uri = "http://localhost:5000/home"
    show_dialogs = 'true'
    return redirect('https://accounts.spotify.com/authorize' +
  '?client_id=' + my_client_id +
  '&redirect_uri=' + my_redirect_uri +
  '&response_type=token' +
  '&show_dialog='+show_dialogs)


@app.route('/home')
def home():
    # testFriends()
    # print("friends tested")
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year
    )

#Genre routes
@app.route('/genre')
def genre():
    return render_template('genre.html')

@app.route('/about')
def about():
    """Renders the mood page."""
    return render_template(
        'about.html',
        title='Mood Page',
        song_uri = '1aEsTgCsv8nOjEgyEoRCpS' #hardcoded track id,
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

@app.route('/user', methods = ['POST', 'GET', 'PUT'])
def user():
    print("message recieved")
    print(request)

    # frontend, add form parsing here, you need to send first name, 
    # last name and email to create a new user
    if request.method == 'POST':
        rspotify_auth = request.json['token']
        remail = request.json['email']
        rname = request.json['display_name']
        u1 = User.query.filter_by(email=remail).first()
        if u1 is None:
            u1 = User(rname, rname, remail, rspotify_auth)
            db.session.add(u1)
            db.session.commit()
        else:
            #overwrite the spotify auth
            u1.spotify_auth = rspotify_auth
            db.session.commit()
        u1 = User.query.filter_by(email=remail).first()    
        #should pass back an id for front end to make a cookie
        return jsonify(
            first_name=u1.first_name,
            last_name=u1.last_name,
            email=u1.email,
            spotify_auth= u1.spotify_auth,
            id= u1.id
        )
    elif request.method == 'GET':
        print(request.args)
        rid = request.args.get('id')
        u1 = User.query.filter_by(id=rid).first()
        return jsonify(
            first_name=u1.first_name,
            last_name=u1.last_name,
            email=u1.email,
            spotify_auth= u1.spotify_auth,
            id= u1.id
        )
    #for edit profile
    elif request.method == 'PUT':
        u1 = User.query.filter_by(email=email).first()
        # add the changedFields dictionary by parsing the object from the function
        if 'first' in changedFields.keys():
            u1.first_name = changedFields['first']
        if 'last' in changedFields.keys():
            u1.last_name = changedFields['last']
        if 'auth' in changedFields.keys():
            u1.spotify_auth = changedFields['auth']
            
        db.session.commit()

    return u1

@app.route('/addFriend', methods=['POST'])
def addFriend():
    # frontend add form parsing here, get the email of the current user (u1_email) and the 
    # user that they want to add as a friend (u2_email)
    if request.method == 'POST':
        #gets friend's email; should check if it's valid
        friend = request.form['friendName']
    u1 = User.query.filter_by(email=u1_email).first()
    u2 = User.query.filter_by(email=u2_email).first()
    u1.friended.append(u2)
    db.session.commit()

# removing this function, and it is incorrect, this is done through the PUT method, I 
# have included one for users in the user route/function (line 100)     

# @app.route('/editProfile', methods=['POST'])
# def editProfile():
#     #If user updates name, email, or bio in profile settings
#     if request.method == 'POST':
#         first = request.form['first']
#         last = request.form['last']
#         bio = request.form['bio']
#         return render_template(
#             'profile.html',
#             bio = bio
#         )


@app.route('/newSong', methods=['POST'])
def addSong(form):
    #frontend add form parsing here, you need a unique identifier from spotify (spotify_id)
    #convert length to integer by rounding to the closest possible minute.
    s1 = Song(spotify_id, length)
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

@app.route('/nextSong', methods=['GET'])
def nextSong():
    token = request.form['token']
    email = request.form['email']
    uri = request.form['uri']

    access_token = token.split('Bearer ')
    access_token = (access_token[1][:len(access_token)-4])
    headers = {"Authorization": f"Bearer {access_token}"}
    endpoint = "https://api.spotify.com/v1/recommendations?seed_genres=pop"
    response = requests.get(endpoint, headers={"Authorization": f"Bearer {access_token}"})
    resp_data = response.json()
    new_uri = (resp_data['tracks'][0]['uri'].split(":")[2])
    length = resp_data['tracks'][0]['duration_ms']  
    return render_template("about.html", auth=headers, email=email, song_uri=new_uri, length= length)


@app.route('/addHappySong', methods=['POST'])
def addHappySong():
    
    #frontend add form parsing you need user email, and spotify_id for the song
    token = request.form['token']
    email = request.form['email']
    uri = request.form['uri']
    length = request.form['length']
    # print("email", email)
    u1 = User.query.filter_by(email=email).first()
    s1 = Song.query.filter_by(spotify_id=uri).first()
    if s1 is None:
        s1 = Song(uri, length)
        db.session.add(s1)
        db.session.commit()
    
    u1.happy_music.append(s1)
    db.session.commit()

    return nextSong()
    


@app.route('/addSadSong', methods=['POST'])
def addSadSong():
    #frontend add form parsing you need user email, and spotify_id for the song
    token = request.form['token']
    email = request.form['email']
    uri = request.form['uri']
    length = request.form['durationms']
    
    u1 = User.query.filter_by(email=email).first()
    s1 = Song.query.filter_by(spotify_id=uri).first()
    if s1 is None:
        s1 = Song(spotify_id, length)
        db.session.add(s1)
        db.session.commit()
    
    u1.happy_music.append(s1)
    db.session.commit()    
    return nextSong()

@app.route('/addStudySong', methods=['POST'])
def addStudySong():
    #frontend add form parsing you need user email, and spotify_id for the song
    token = request.form['token']
    email = request.form['email']
    uri = request.form['uri']
    length = request.form['durationms']
    u1 = User.query.filter_by(email=email).first()
    s1 = Song.query.filter_by(spotify_id=uri).first()
    if s1 is None:
        s1 = Song(spotify_id, length)
        db.session.add(s1)
        db.session.commit()
    
    u1.happy_music.append(s1)
    db.session.commit()
    return  nextSong()

@app.route('/addPartySong', methods=['POST'])
def addPartySong():
    #frontend add form parsing you need user email, and spotify_id for the song
    token = request.form['token']
    email = request.form['email']
    uri = request.form['uri']
    length = request.form['durationms']
    u1 = User.query.filter_by(email=email).first()
    s1 = Song.query.filter_by(spotify_id=uri).first()
    if s1 is None:
        s1 = Song(spotify_id, length)
        db.session.add(s1)
        db.session.commit()
    
    u1.happy_music.append(s1)
    db.session.commit()

    return nextSong()

if __name__ == '__main__':
    app.debug = True
    app.run()