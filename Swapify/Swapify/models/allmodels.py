from ..app import db
import datetime


# Relation table between playlists and songs in the playlist
playlistsongs = db.Table(
    "playlistsongs",
    db.Column(
        "playlist_id", db.Integer, db.ForeignKey("playlist.id"), primary_key=True
    ),
    db.Column("song_id", db.Integer, db.ForeignKey("song.id"), primary_key=True),
)

# Relation table between two Users that we call friends
friends = db.Table(
    "friends",
    db.Column("user1_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("user2_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
)

# Relation table be users and the songs that they classify as happy
happymusiclist = db.Table(
    "happymusiclist",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("song_id", db.Integer, db.ForeignKey("song.id"), primary_key=True),
)

# Relation table be users and the songs that they classify as sad
sadmusiclist = db.Table(
    "sadmusiclist",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("song_id", db.Integer, db.ForeignKey("song.id"), primary_key=True),
)

# Relation table be users and the songs that they classify as study music
studymusiclist = db.Table(
    "studymusiclist",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("song_id", db.Integer, db.ForeignKey("song.id"), primary_key=True),
)

# Relation table be users and the songs that they classify as party music
partymusiclist = db.Table(
    "partymusiclist",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("song_id", db.Integer, db.ForeignKey("song.id"), primary_key=True),
)


# This contains the song database model, which has an id, spotify_id, and a song length in minutes
class Song(db.Model):

    __tablename__ = "song"
    id = db.Column(db.Integer, primary_key=True)
    spotify_id = db.Column(db.String)
    length = db.Column(db.Integer)

    def __init__(self, spotify_id=None, length=None):
        self.spotify_id = spotify_id
        self.length = length


# This contains the user model which has the first name, last name,
# email, spotify_auth, bio, and playlists of the user, and all of their
# music classifications
class User(db.Model):

    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)
    spotify_auth = db.Column(db.String)
    bio = db.Column(db.String)
    playlists = db.relationship("Playlist", backref="user", lazy=True)

    # these are connections to the relationship tables for users
    happy_music = db.relationship(
        "Song", backref="happyusers", lazy="dynamic", secondary=happymusiclist
    )
    sad_music = db.relationship(
        "Song", backref="sadusers", lazy="dynamic", secondary=sadmusiclist
    )
    study_music = db.relationship(
        "Song", backref="studyusers", lazy="dynamic", secondary=studymusiclist
    )
    party_music = db.relationship(
        "Song", backref="partyusers", lazy="dynamic", secondary=partymusiclist
    )

    # myFriends = db.relationship("User", backref=db.backref("users", remote_side= [id]), secondary=friends)
    friended = db.relationship(
        "User",
        secondary=friends,
        primaryjoin=(friends.c.user1_id == id),
        secondaryjoin=(friends.c.user2_id == id),
        backref=db.backref("friends", lazy="dynamic"),
        lazy="dynamic",
    )

    def __init__(
        self, first_name=None, last_name=None, email=None, spotify_auth=None, bio=None
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.spotify_auth = spotify_auth
        self.bio = bio


# The playlist class contains the different playlists that a user might have
class Playlist(db.Model):

    __tablename__ = "playlist"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    creation_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    length = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    songs = db.relationship(
        "Song", backref="playlists", lazy="dynamic", secondary=playlistsongs
    )

    def __init__(self, name=None, length=None, user_id=None):
        self.name = name
        self.length = length
        self.user_id = user_id
