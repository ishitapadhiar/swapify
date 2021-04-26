import os
import spotipy
import sys
import math
import random
import requests
import json
import base64
from datetime import datetime
from spotipy.oauth2 import SpotifyClientCredentials


class RandomSongGenerator:
    # Spotify API credentials
    CLIENT_ID = "8b9f85860db442c596871ea138aa4d60"
    CLIENT_SECRET = "399938641dbc4852941990d25ef110b4"

    SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
    SPOTIFY_API_BASE_URL = "https://api.spotify.com"
    API_VERSION = "v1"
    SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

    def get_token(self):
        # Converts spotify api information into token
        client_token = base64.b64encode(
            "{}:{}".format(self.CLIENT_ID, self.CLIENT_SECRET).encode("UTF-8")
        ).decode("ascii")
        headers = {"Authorization": "Basic {}".format(client_token)}
        payload = {"grant_type": "client_credentials"}
        token_request = requests.post(
            self.SPOTIFY_TOKEN_URL, data=payload, headers=headers
        )
        access_token = json.loads(token_request.text)["access_token"]
        return access_token

    def getRandomSong(self, access_token, genre=None):
        # Creates a random Spotify API hash
        random_wildcards = [
            "%25a%25",
            "a%25",
            "%25a",
            "%25e%25",
            "e%25",
            "%25e",
            "%25i%25",
            "i%25",
            "%25i",
            "%25o%25",
            "o%25",
            "%25o",
            "%25u%25",
            "u%25",
            "%25u",
        ]
        wildcard = random.choice(random_wildcards)
        # Picks a random spotify song based on genre and hash
        authorization_header = {"Authorization": "Bearer {}".format(access_token)}
        song_request = requests.get(
            "{}/search?q={}{}&type=track&offset={}".format(
                self.SPOTIFY_API_URL,
                wildcard,
                "%20genre:%22{}%22".format(genre.replace(" ", "%20")),
                random.randint(0, 200),
            ),
            headers=authorization_header,
        )
        song_info = random.choice(json.loads(song_request.text)["tracks"]["items"])
        artist = song_info["artists"][0]["name"]
        song = song_info["name"]
        return "{} - {}".format(artist, song)


test = RandomSongGenerator()
token = test.get_token()
for i in range(15):
    print(test.getRandomSong(token, "pop"))
