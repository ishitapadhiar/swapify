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
from flask import jsonify
from flask import Blueprint

os.environ["DBUSER"] = "usxuxwby"
os.environ["DBPASS"] = "sVUyUo4Z1aqH4MiKkLQtWlw8RNMhaq-H"
os.environ["DBHOST"] = "queenie.db.elephantsql.com"
os.environ["DBNAME"] = "usxuxwby"

database_uri = "postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}".format(
    dbuser=os.environ["DBUSER"],
    dbpass=os.environ["DBPASS"],
    dbhost=os.environ["DBHOST"],
    dbname=os.environ["DBNAME"],
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
from Swapify.playlistGenerator import PlaylistGenerator


migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command("db", MigrateCommand)


nav_bp = Blueprint("nav_bp", __name__)
music_bp = Blueprint("music_bp", __name__)
profile_bp = Blueprint("profile_bp", __name__)

# from Swapify.music import music_bp


@profile_bp.route("/")
@profile_bp.route("/login")
def log():
    scopes = "user-read-private user-read-email playlist-modify-public"
    my_client_id = "b167636c03db464bac2a9a61c6663685"
    my_redirect_uri = "http://localhost:5000/home"
    show_dialogs = "true"
    return redirect(
        "https://accounts.spotify.com/authorize"
        + "?client_id="
        + my_client_id
        + "&redirect_uri="
        + my_redirect_uri
        + "&response_type=token"
        + "&show_dialog="
        + show_dialogs
    )


# ==============================navbar main page routes==========================
@nav_bp.route("/home")
def home():
    # testFriends()
    # print("friends tested")
    """Renders the home page."""
    return render_template("index.html", title="Home Page", year=datetime.now().year)


# Genre routes
@nav_bp.route("/genre")
def genre():
    return render_template("genre.html")


@nav_bp.route("/mood")
def mood():
    """Renders the mood page."""

    return render_template(
        "mood.html",
        title="Mood Page",
        song_uri="1aEsTgCsv8nOjEgyEoRCpS",  # hardcoded track id,
        length=3,
    )


@nav_bp.route("/playlists")
def playlists():
    """Renders the playlist page."""
    return render_template(
        "playlists.html",
        title="Playlists Page",
        year=datetime.now().year,
        message="Your playlist page. This message is in views.py",
    )


@nav_bp.route("/profile")
def profile():
    """Renders the profile page."""
    return render_template(
        "profile.html",
        title="Profile Page",
        year=datetime.now().year,
        message="Settings",
    )


# ========================end top navbar routes===================================


@profile_bp.route("/user", methods=["POST", "GET", "PUT"])
def user():
    print("message recieved")
    print(request)
    # frontend, add form parsing here, you need to send first name,
    # last name and email to create a new user
    if request.method == "POST":
        rspotify_auth = request.json["token"]
        remail = request.json["email"]
        rname = request.json["display_name"]
        u1 = User.query.filter_by(email=remail).first()
        if u1 is None:  # user not in db
            u1 = User(rname, rname, remail, rspotify_auth)
            db.session.add(u1)
            db.session.commit()
        else:  # updating
            # overwrite the spotify auth
            u1.spotify_auth = rspotify_auth
            if "bio" in request.json:
                rbio = request.json["bio"]
                u1.bio = rbio
            db.session.commit()
        u1 = User.query.filter_by(email=remail).first()
        happysongs = []
        for song in u1.happy_music:
            happysongs.append(song.spotify_id)

        sadsongs = []
        for song in u1.sad_music:
            sadsongs.append(song.spotify_id)

        studysongs = []
        for song in u1.study_music:
            studysongs.append(song.spotify_id)

        partysongs = []
        for song in u1.party_music:
            partysongs.append(song.spotify_id)

        # should pass back an id for front end to make a cookie
        return jsonify(
            first_name=u1.first_name,
            last_name=u1.last_name,
            email=u1.email,
            spotify_auth=u1.spotify_auth,
            id=u1.id,
            bio=u1.bio,
            happysongs=happysongs,
            sadsongs=sadsongs,
            studysongs=studysongs,
            partysongs=partysongs,
        )
    elif request.method == "GET":
        # request the user row using id from cookie
        print(request.args)
        rid = request.args.get("id")
        u1 = User.query.filter_by(id=rid).first()
        happysongs = []
        for song in u1.happy_music:
            happysongs.append(song.spotify_id)
        sadsongs = []
        for song in u1.sad_music:
            sadsongs.append(song.spotify_id)

        studysongs = []
        for song in u1.study_music:
            studysongs.append(song.spotify_id)

        partysongs = []
        for song in u1.party_music:
            partysongs.append(song.spotify_id)
        return jsonify(
            first_name=u1.first_name,
            last_name=u1.last_name,
            email=u1.email,
            spotify_auth=u1.spotify_auth,
            id=u1.id,
            bio=u1.bio,
            happysongs=happysongs,
            sadsongs=sadsongs,
            studysongs=studysongs,
            partysongs=partysongs,
        )

    return u1


@music_bp.route("/getMoodPlaylist", methods=["GET"])
def getMoodPlaylist():
    rid = request.args.get("id")
    u1 = User.query.filter_by(id=rid).first()
    happysongs = []
    sadsongs = []
    studysongs = []
    partysongs = []

    allusers = [u1]
    for friendID in u1.friended:
        allUsers.append(db.session.query(User).get(friendID))
        print(friendID)

    for u in allusers:
        for song in u.happy_music:
            happysongs.append(song.spotify_id)
            print("added song")
        for song in u.sad_music:
            sadsongs.append(song.spotify_id)
        for song in u.study_music:
            studysongs.append(song.spotify_id)

    for song in u1.party_music:
        partysongs.append(song.spotify_id)
    return jsonify(
        first_name=u1.first_name,
        last_name=u1.last_name,
        email=u1.email,
        spotify_auth=u1.spotify_auth,
        id=u1.id,
        bio=u1.bio,
        happysongs=happysongs,
        sadsongs=sadsongs,
        studysongs=studysongs,
        partysongs=partysongs,
    )

    return u1


@profile_bp.route("/addFriend", methods=["POST"])
def addFriend():
    # frontend add form parsing here, get the email of the current user (u1_email) and the
    # user that they want to add as a friend (u2_email)
    if request.method == "POST":
        # gets friend's email; should check if it's valid
        u1_email = request.json["userEmail"]
        u2_email = request.json["friendEmail"]
    u1 = User.query.filter_by(email=u1_email).first()
    u2 = User.query.filter_by(email=u2_email).first()
    u1.friended.append(u2)
    db.session.commit()
    return jsonify(first_name=u1.first_name)


@music_bp.route("/newSong", methods=["POST"])
def addSong(form):
    # frontend add form parsing here, you need a unique identifier from spotify (spotify_id)
    # convert length to integer by rounding to the closest possible minute.
    s1 = Song(spotify_id, length)
    db.session.add(s1)
    db.session.commit()
    return s1


@music_bp.route("/generateNewPlaylist", methods=["POST"])
def generateNewPlaylist(form):
    # frontend add form parsing you need playlist name, length and user_id
    token = request.form["token"]
    email = request.form["email"]
    uri = request.form["uri"]
    name = request.form["name"]
    mood = request.form["mood"]
    friends = request.form["friends"]
    time = request.form["time"]
    numSongs = request.form["numSongs"]

    generator = PlaylistGenerator(email)
    generator.generate_user_playlist(name, mood, friends, time, numSongs)


@music_bp.route("/getPlaylist", methods=["GET"])
def getPlaylist(form):
    email = request.form["email"]
    playlistName = request.form["playlistName"]

    u1 = User.query.filter_by(email=email).first()
    allPlaylists = u1.playlists

    spotifySongId = []
    for p in allPlaylists:
        if p.name == playlistName:
            for song in p.songs:
                spotifySongId.append(song.spotify_id)

            return jsonify(
                error="No Errors", name=p.name, length=p.length, songs=spotifySongId
            )

    return jsonify(error="No matches", name=playlistName)


@music_bp.route("/addHappySong", methods=["POST"])
def addHappySong():
    # frontend add form parsing you need user email, and spotify_id for the song
    token = request.json["token"]
    email = request.json["email"]
    uri = request.json["uri"]
    length = request.json["length"]
    # print("email", email)
    u1 = User.query.filter_by(email=email).first()
    s1 = Song.query.filter_by(spotify_id=uri).first()
    print(s1)
    if s1 is None:
        s1 = Song(uri, length)
        print(s1)
        db.session.add(s1)
        db.session.commit()

    u1.happy_music.append(s1)
    db.session.commit()
    return jsonify(
        first_name=u1.first_name,
        last_name=u1.last_name,
        email=u1.email,
        spotify_auth=u1.spotify_auth,
        id=u1.id,
        bio=u1.bio,
    )


@music_bp.route("/addSadSong", methods=["POST"])
def addSadSong():
    # frontend add form parsing you need user email, and spotify_id for the song
    token = request.json["token"]
    email = request.json["email"]
    uri = request.json["uri"]
    length = request.json["length"]
    spotify_id = uri
    u1 = User.query.filter_by(email=email).first()
    s1 = Song.query.filter_by(spotify_id=uri).first()
    if s1 is None:
        s1 = Song(uri, length)
        db.session.add(s1)
        db.session.commit()

    u1.sad_music.append(s1)
    db.session.commit()
    return jsonify(
        first_name=u1.first_name,
        last_name=u1.last_name,
        email=u1.email,
        spotify_auth=u1.spotify_auth,
        id=u1.id,
        bio=u1.bio,
    )


@music_bp.route("/addStudySong", methods=["POST"])
def addStudySong():
    # frontend add form parsing you need user email, and spotify_id for the song
    token = request.json["token"]
    email = request.json["email"]
    uri = request.json["uri"]
    length = request.json["length"]
    spotify_id = uri
    u1 = User.query.filter_by(email=email).first()
    s1 = Song.query.filter_by(spotify_id=uri).first()
    if s1 is None:
        s1 = Song(uri, length)
        db.session.add(s1)
        db.session.commit()

    u1.study_music.append(s1)
    db.session.commit()
    return jsonify(
        first_name=u1.first_name,
        last_name=u1.last_name,
        email=u1.email,
        spotify_auth=u1.spotify_auth,
        id=u1.id,
        bio=u1.bio,
    )


@music_bp.route("/addPartySong", methods=["POST"])
def addPartySong():
    # frontend add form parsing you need user email, and spotify_id for the song
    token = request.json["token"]
    email = request.json["email"]
    uri = request.json["uri"]
    length = request.json["length"]
    spotify_id = uri
    u1 = User.query.filter_by(email=email).first()
    s1 = Song.query.filter_by(spotify_id=uri).first()
    if s1 is None:
        s1 = Song(uri, length)
        db.session.add(s1)
        db.session.commit()

    u1.party_music.append(s1)
    db.session.commit()

    return jsonify(
        first_name=u1.first_name,
        last_name=u1.last_name,
        email=u1.email,
        spotify_auth=u1.spotify_auth,
        id=u1.id,
        bio=u1.bio,
    )


app.register_blueprint(nav_bp)
app.register_blueprint(music_bp)
app.register_blueprint(profile_bp)

if __name__ == "__main__":
    app.debug = True
    app.run()
