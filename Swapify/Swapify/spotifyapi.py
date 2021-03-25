import os
import spotipy
import sys
from spotipy.oauth2 import SpotifyClientCredentials

os.environ['SPOTIPY_CLIENT_ID'] = '8b9f85860db442c596871ea138aa4d60'
os.environ['SPOTIPY_CLIENT_SECRET'] = '399938641dbc4852941990d25ef110b4'
os.environ['SPOTIPY_REDIRECT_URI'] = 'http://localhost'

lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
results = spotify.artist_top_tracks(lz_uri)

for track in results['tracks'][:10]:
    print('track    : ' + track['name'])
    print('audio    : ' + track['preview_url'])
    print('cover art: ' + track['album']['images'][0]['url'])
    print()
# import os
# import spotipy

# os.environ['SPOTIPY_CLIENT_ID'] = '8b9f85860db442c596871ea138aa4d60'
# os.environ['SPOTIPY_CLIENT_SECRET'] = '399938641dbc4852941990d25ef110b4'
# os.environ['SPOTIPY_REDIRECT_URI'] = 'http://localhost'

# lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'

# spotify = spotipy.Spotify()
# results = spotify.artist_top_tracks(lz_uri)

# for track in results['tracks'][:10]:
#     print('track    : ' + track['name'])
#     print('audio    : ' + track['preview_url'])
#     print('cover art: ' + track['album']['images'][0]['url'])
#     print()
