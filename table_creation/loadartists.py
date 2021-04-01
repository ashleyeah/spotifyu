import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import date, datetime, timedelta
import mysql.connector

auth_manager = SpotifyClientCredentials('f3dc4f3802254be091c8d8576961bc9d', 'b51d135ad7104add8f71933197e9cc14')
sp = spotipy.Spotify(auth_manager=auth_manager)

file1 = open('songs.txt', 'r')
Lines = file1.readlines()
 
# for i in range(1, 2):
#     track_id = Lines[i].strip()
#     urn = 'spotify:track:{}'.format(track_id)

#     track = sp.track(urn)

#     for artist in track['artists']:
#         # urn2 = 'spotify:artist:{}'.format('1z4g3DjTBBZKhvAroFlhOM')
#         # artist = sp.artist(urn2)
#         # print(artist)

urn2 = 'spotify:artist:{}'.format('1z4g3DjTBBZKhvAroFlhOM')
artist = sp.artist(urn2)
for genre in artist['genres']:
    print(genre)