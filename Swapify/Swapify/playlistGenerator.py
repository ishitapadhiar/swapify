import random
from ..app import db

class PlaylistGenerator():
	def __init__(self, userID):
		self.user = db.session.query(User).get(userID)

	def generate_user_playlist(self, name, mood, friends= False, time = None, numSongs = None):
		fullSongList = self.get_all_mood_songs(mood)
		random.shuffle(fullSongList)

		songList = []
		if numSongs:
			songList = fullSongList[0:numSongs]
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

		playlistLength = self.get_length(songList)
		p1 = Playlist(name, playlistLength, self.user.id)
		db.session.add(p1)
		for song in songList:
			p1.songs.append(song.id)
		db.session.commit()



	def generate_genre(self,genre):
		pass

	def get_all_mood_songs(self, mood, friends):

		songList = self.get_user_mood_songs(self.user, mood)

		if friends:
			for friendID in self.user.friended:
				friend = db.session.query(User).get(friendID)
				songList += self.get_user_mood_songs(friend, mood)

		songList = list(set(songList))
		songList = [db.session.query(Song).get(id) for id in songList] 

		return songList
		

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

	def get_length(self, songList):
		length= 0
		for song in songList:
			length += song.length
		return length
