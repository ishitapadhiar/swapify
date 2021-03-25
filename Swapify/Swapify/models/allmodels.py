from ..app import db

playlistsongs = db.Table('playlistsongs',
	db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id'), primary_key = True),
	db.Column('song_id', db.Integer, db.ForeignKey('song.id'), primary_key = True)
)

friends = db.Table('friends',
	db.Column('user1_id', db.Integer, db.ForeignKey('user.id'), primary_key = True),
	db.Column('user2_id', db.Integer, db.ForeignKey('user.id'), primary_key = True)
)

happymusiclist = db.Table('happymusiclist',
	db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key = True),
	db.Column('song_id', db.Integer, db.ForeignKey('song.id'), primary_key = True)
)

sadmusiclist = db.Table('sadmusiclist',
	db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key = True),
	db.Column('song_id', db.Integer, db.ForeignKey('song.id'), primary_key = True)
)

studymusiclist = db.Table('studymusiclist',
	db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key = True),
	db.Column('song_id', db.Integer, db.ForeignKey('song.id'), primary_key = True)
)

partymusiclist = db.Table('partymusiclist',
	db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key = True),
	db.Column('song_id', db.Integer, db.ForeignKey('song.id'), primary_key = True)
)

class Song(db.Model):

	__tablename__ = 'song'
	id = db.Column(db.Integer, primary_key = True)
	spotify_id = db.Column(db.String)

	def __init__(self, name=None):
		self.spotify_id = spotify_id

class User(db.Model):

	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key = True)
	first_name = db.Column(db.String)
	last_name = db.Column(db.String)
	email = db.Column(db.String)
	playlists = db.relationship('Playlist', backref = 'user', lazy = True)

	def __init__(self, name=None):
		self.first_name = first_name
		self.last_name = last_name
		self.email = email

class Playlist(db.Model):

	__tablename__ = 'playlist'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String)
	creation_date = db.Column(db.DateTime)
	length = db.Column(db.Float)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

	def __init__(self, name=None):
		self.name = name
		self.creation_date = creation_date
		self.length = length