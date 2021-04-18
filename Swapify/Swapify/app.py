import os

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


# @app.route('/')
# @app.route('/login')
# def log():
#     scopes = "user-read-private user-read-email"
#     my_client_id = "b167636c03db464bac2a9a61c6663685"
#     my_redirect_uri = "http://localhost:5000/home"
#     return redirect('https://accounts.spotify.com/authorize' +
#   '?client_id=' + my_client_id +
#   '&redirect_uri=' + my_redirect_uri +
#   '&response_type=token')

CLIENT_ID = "f38ef4e90a22440c85cc1e3333f3ef2e"
CLIENT_SECRET = "276a9e798a504e35aa5eac1683b0cbb4"

SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

# Server-side Parameters
CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 8080
REDIRECT_URI = "http://localhost:5000/callback/q"
SCOPE = "playlist-modify-public user-read-private user-read-email user-read-currently-playing user-read-playback-state"
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    # "state": STATE,
    # "show_dialog": SHOW_DIALOG_str,
    "client_id": CLIENT_ID
}

@app.route("/")
def index():
    # Auth Step 1: Authorization
    url_args = "&".join(["{}={}".format(key, quote(val)) for key, val in auth_query_parameters.items()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    return redirect(auth_url)

@app.route("/callback/q")
def callback():
    # Auth Step 4: Requests refresh and access tokens
    auth_token = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload)

    # Auth Step 5: Tokens are Returned to Application
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]
    refresh_token = response_data["refresh_token"]
    token_type = response_data["token_type"]
    expires_in = response_data["expires_in"]

    # Auth Step 6: Use the access token to access Spotify API
    authorization_header = {"Authorization": "Bearer {}".format(access_token)}

    # Get profile data
    user_profile_api_endpoint = "{}/me".format(SPOTIFY_API_URL)
    profile_response = requests.get(user_profile_api_endpoint, headers=authorization_header)
    profile_data = json.loads(profile_response.text)

    # Get user playlist data
    playlist_api_endpoint = "{}/playlists".format(profile_data["href"])
    playlists_response = requests.get(playlist_api_endpoint, headers=authorization_header)
    playlist_data = json.loads(playlists_response.text)

    # Combine profile and playlist data to display
    display_arr = [profile_data] + playlist_data["items"]
    playlist_id = playlist_data['items'][0]['uri'].split(':')[2]
    single_playlist_endpoint = "{}/{}/tracks".format(playlist_api_endpoint, playlist_id)
    single_playlist_response = requests.get(single_playlist_endpoint, headers=authorization_header)
    single_playlist_data = single_playlist_response.json()


    

    # #Get User Email and Song Info
    email = display_arr[0]['email']
    # single_info = single_playlist_data["items"][0]["track"]["album"]
    # song_name = (single_info["name"])
    # artist_name = (single_info["artists"][0]["name"])
    # image = (single_info["images"][2]["url"])
    # uri_link = (single_info["artists"][0]["uri"])
    # artist_id = uri_link.split(':')[2]
    # song_id = '1aEsTgCsv8nOjEgyEoRCpS' #hardcoded track id

    endpoint = "https://api.spotify.com/v1/recommendations?seed_genres=pop"
    response = requests.get(endpoint, headers={"Authorization": f"Bearer {access_token}"})
    resp_data = response.json()
    new_uri = (resp_data['tracks'][0]['uri'].split(":")[2])
    length = resp_data['tracks'][0]['duration_ms']  
    return render_template("about.html", auth=authorization_header, email=email, song_uri=new_uri, length= length)


    # return render_template("about.html", auth=authorization_header, email=email, song_uri=song_id)



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
def user(form):
    # frontend, add form parsing here, you need to send first name, 
    # last name and email to create a new user
    spotify_auth = None
    if request.method == 'POST':
        u1 = User.query.filter_by(email=email).first()
        if u1 is None:
            u1 = User(first, last, email, spotify_auth)
            db.session.add(u1)
            db.session.commit()

    if request.method == 'GET':
        u1 = User.query.filter_by(email=email).first()
        return jsonify(
            first_name=u1.first_name,
            last_name=u1.last_name,
            email=u1.email,
            spotify_auth= u1.spotify_auth,
            id= u1.id
        )

    if request.method == 'PUT':
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
def nextSong(token, email, uri):
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
    print("email", email)
    u1 = User.query.filter_by(email=email).first()
    s1 = Song.query.filter_by(spotify_id=uri).first()
    if s1 is None:
        s1 = Song(uri, length)
        db.session.add(s1)
        db.session.commit()
    
    u1.happy_music.append(s1)
    db.session.commit()

    return nextSong(token, email, uri)
    


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
    return nextSong(token, email, uri)

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
    return  (token, email, uri)

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

    return nextSong(token, email, uri)

if __name__ == '__main__':
    app.debug = True
    app.run()