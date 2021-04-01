import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import mysql.connector

auth_manager = SpotifyClientCredentials('f3dc4f3802254be091c8d8576961bc9d', 'b51d135ad7104add8f71933197e9cc14')
sp = spotipy.Spotify(auth_manager=auth_manager)

cnx = mysql.connector.connect(user='root', password='1234',
                              host='35.222.92.143',
                              database='main')
cursor = cnx.cursor()

file1 = open('artists.txt', 'r')
Lines = file1.readlines()

for i in range(1, len(Lines)):
    artist_id = Lines[i].strip()
    urn = 'spotify:artist:{}'.format(artist_id)
    artist = sp.artist(urn)
    for genre in artist['genres']:
        query = ("SELECT genre_id FROM Genres "
                "WHERE name = %(genre_name)s; ")

        data_genre = {
            'genre_name': genre
        }

        cursor.execute(query, data_genre)
        for i in cursor:
            add_row = ("INSERT IGNORE INTO ArtistsGenres "
                    "(artist_id, artist_name, genre_id, genre_name) "
                    "VALUES (%(artist_id)s, %(artist_name)s, %(genre_id)s, %(genre_name)s) ")

            data_row = {
                'artist_id': artist_id,
                'artist_name': artist['name'],
                'genre_id': i[0],
                'genre_name': genre
            }

            # Insert new employee
            cursor.execute(add_row, data_row)

            # Make sure data is committed to the database
            cnx.commit()

cursor.close()
cnx.close()