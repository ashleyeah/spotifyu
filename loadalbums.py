import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from credentials import SPOTIPY_CLIENT_ID
from credentials import SPOTIPY_CLIENT_SECRET
from datetime import date, datetime, timedelta
import mysql.connector

auth_manager = SpotifyClientCredentials('f3dc4f3802254be091c8d8576961bc9d', 'b51d135ad7104add8f71933197e9cc14')
sp = spotipy.Spotify(auth_manager=auth_manager)

cnx = mysql.connector.connect(user='root', password='1234',
                              host='104.197.65.16',
                              database='main')
cursor = cnx.cursor()

file1 = open('songs.txt', 'r')
Lines = file1.readlines()
 
for i in range(1, len(Lines)):
    track_id = Lines[i].strip()
    urn = 'spotify:track:{}'.format(track_id)

    track = sp.track(urn)

    add_album = ("INSERT IGNORE INTO Albums "
                 "(album_id, name, release_date) "
                 "VALUES (%(album_id)s, %(name)s, %(release_date)s) ")

    data_album = {
        'album_id': track['album']['id'],
        'name': track['album']['name'],
        'release_date': track['album']['release_date']
    }

    # Insert new employee
    cursor.execute(add_album, data_album)

    # Make sure data is committed to the database
    cnx.commit()

file1.close()

cursor.close()
cnx.close()