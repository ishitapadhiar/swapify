import random
from Swapify.app import db
from Swapify.models.allmodels import User

#This class handles playlist generation
class PlaylistGenerator():
	def __init__(self, email):
		self.user = User.query.filter_by(email=email).first()

	# This function genrerate different playlists for a user. It does so using the following parameters
	#   name: name of the playlist
	#   mood: the mood that the playlist should be based on
	#   friends: whether or not you want friends to contribute to it
	#   time: the length of the plalist
	#   numSongs: the number of songs in the playlist
	# The last two parameters are optional, you only need one, either a time limit on the 
	# playlist or the number of songs in the playlist
	# Returns the generated playlist
	def generate_user_playlist(self, name, mood, friends= False, time = None, numSongs = None):
		fullSongList = self.get_all_mood_songs(mood)
		random.shuffle(fullSongList)

		songList = []
		# If we are generating the playlist based on the number of songs
		if numSongs:
			songList = fullSongList[0:numSongs]

		# If we are generating the playlist based on a time limit
		else:
			subset =([[False for i in range(time + 1)] for i in range(len(fullSongList) + 1)])

			subset[0][0] = (True, [])
			for i in range(len(fullSongList) + 1):
				subset[i][0] = (True, [fullSongList[i-1]])
			for i in range(1, time + 1):
				subset[0][i]= (False,[])

			for i in range(1, len(fullSongList) + 1):
				for j in range(1, time + 1):
					if j<fullSongList[i-1].length:
						subset[i][j] = (subset[i-1][j][0], subset[i-1][j][1])
					songLength = fullSongList[i-1].length
					if j>= songLength:
						if subset[i-1][j][0]:
							subset[i][j] = (subset[i-1][j][0], subset[i-1][j][1])
						elif subset[i-1][j-songLength][0]:
							subset[i][j] = (subset[i-1][j-songLength][0], subset[i-1][j-songLength][1].append(fullSongList[i-1]))
						else:
							subset[i][j] = (False, 0)

			subsetExists = [False, None]
			for i in range(time, 0):
				if subset[len(fullSongList)][i][0]:
					subsetExists = [True, subset[len(fullSongList)][i][1]]
					break

			if subsetExists[0]:
				songList = subsetExists[1]
			else:
				print("Error, no generateable playlist")


		#creating the playlist
		playlistLength = self.get_length(songList)
		p1 = Playlist(name, playlistLength, self.user.id)
		db.session.add(p1)
		for song in songList:
			p1.songs.append(song.id)
		db.session.commit()

		return p1


	# Generates all the songs for a user
	#   mood: The specified mood for which we want to create the song
	#   friends: boolean that represents whether or not you want friends to contribute to it
	# Returns all the songs matching a mood that you have classified, and songs that friends
	# have also classifed
	def get_all_mood_songs(self, mood, friends):

		songList = self.get_user_mood_songs(self.user, mood)

		if friends:
			for friendID in self.user.friended:
				friend = db.session.query(User).get(friendID)
				songList += self.get_user_mood_songs(friend, mood)

		songList = list(set(songList))
		songList = [db.session.query(Song).get(id) for id in songList] 

		return songList
		
	# Given a user and a mood gets all the songs that they have classified for that mood
	def get_user_mood_songs(self,user, mood):
		songList = []
		if mood == "happy":
			songList = user.happy_music
		if mood == "sad":
			songList = user.sad_music
		if mood == "study":
			songList = user.study_music
		if mood == "party":
			songList =  user.party_music
		return songList

	#given a list of songs return that total length of the list of songs
	def get_length(self, songList):
		length= 0
		for song in songList:
			length += song.length
		return length
