import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import date, datetime, timedelta
import mysql.connector

auth_manager = SpotifyClientCredentials('f3dc4f3802254be091c8d8576961bc9d', 'b51d135ad7104add8f71933197e9cc14')
sp = spotipy.Spotify(auth_manager=auth_manager)

cnx = mysql.connector.connect(user='root', password='1234',
                              host='35.222.92.143',
                              database='main')
cursor = cnx.cursor()

file1 = open('songs.txt', 'r')
Lines = file1.readlines()
 
for i in range(1, len(Lines)):
    track_id = Lines[i].strip()
    urn = 'spotify:track:{}'.format(track_id)
    track = sp.track(urn)
    for artist in track['artists']:

        add_album = ("INSERT IGNORE INTO SongsArtistsAlbums "
                 "(song_id, artist_id, album_id) "
                 "VALUES (%(song_id)s, %(artist_id)s, %(album_id)s) ")

        data_album = {
            'song_id': track_id,
            'artist_id': artist['id'],
            'album_id': track['album']['id'],
        }

        # Insert new employee
        cursor.execute(add_album, data_album)

        # Make sure data is committed to the database
        cnx.commit()

file1.close()

cursor.close()
cnx.close()