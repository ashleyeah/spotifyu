"""Defines all the functions related to the database"""
from app import db
from datetime import date
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

""" --------------------------------------------------"""
""" -----------------ALBUM FUNCTION ------------------"""
"""---------------------------------------------------"""
def fetch_albums() -> dict:
    """Reads all tasks listed in the todo table
    Returns:
        A list of dictionaries
    """

    auth_manager = SpotifyClientCredentials('f3dc4f3802254be091c8d8576961bc9d', 'b51d135ad7104add8f71933197e9cc14')
    sp = spotipy.Spotify(auth_manager=auth_manager)

    conn = db.connect()
    query_results = conn.execute("Select * From Albums ORDER BY release_date DESC LIMIT 30;").fetchall()
    conn.close()
    albums = []
    for result in query_results:
        urn = 'spotify:album:{}'.format(result[0].strip())
        album = sp.album(urn)
        artists = album['artists'][0]['name']
        for i in range(1, len(album['artists'])):
            artists += ", " + album['artists'][i]['name']
        item = {
            "img": album['images'][0]['url'],
            "artists": artists,
            "album_id": result[0],
            "name": result[1],
            "date": result[2]
        }
        albums.append(item)

    return albums

def update_album_entry(task_id: str, text: str, date: str) -> None:
    """Updates task description based on given `task_id`
    Args:
        task_id (int): Targeted task_id
        text (str): Updated description
    Returns:
        None
    """

    conn = db.connect()
    query = 'UPDATE Albums SET name = "{}", release_date = "{}" where album_id="{}";'.format(text, date, task_id)
    conn.execute(query)
    conn.close()


def insert_new_album(album_id: str, name: str, date: str) ->  None:
    """Insert new task to todo table.
    Args:
        text (str): Song name. Looks up the song name from SongsOld table, and
        gets the value of the attributes.
    Returns: The task ID for the inserted entry
    """

    conn = db.connect()
    query = 'Insert Ignore Into Albums (album_id, name, release_date) VALUES ("{}", "{}", "{}");'.format(
        album_id, name, date)
    conn.execute(query)
    conn.close()

    return album_id


def remove_album(task_id: str) -> None:
    """ remove entries based on song ID """
    conn = db.connect()
    query = 'Delete From Albums Where album_id="{}";'.format(task_id) #task_id = song_id, also note- quotes around {}
    conn.execute(query)
    conn.close()

def advanced_query_album() -> dict:
    conn = db.connect()
    query_results = conn.execute("SELECT ag.artist_name, GROUP_CONCAT(ag.genre_name) AS genres, pa.song_count "
                                 "FROM Artist_to_Genre ag JOIN (SELECT artist_id, COUNT(song_id) as song_count "
                                                "FROM SongsArtistsAlbums "
                                                "GROUP BY artist_id) AS pa USING(artist_id) "
                                 "GROUP BY ag.artist_name, pa.song_count "
                                 "ORDER BY pa.song_count DESC "
                                 "LIMIT 30;").fetchall()
    query_res = []
    for result in query_results:
        item = {
            "name": result[0],
            "genres": result[1]
        }
        query_res.append(item)
    return query_res

def search_album(name: str) -> dict:
    auth_manager = SpotifyClientCredentials('f3dc4f3802254be091c8d8576961bc9d', 'b51d135ad7104add8f71933197e9cc14')
    sp = spotipy.Spotify(auth_manager=auth_manager)

    conn = db.connect()
    sql='SELECT * FROM Albums WHERE name LIKE %s LIMIT 50'
    args=['%'+name+'%']
    conn.execute(sql,args)

    query_results = conn.execute(sql,args).fetchall()
    search_res = []

    for result in query_results:
        urn = 'spotify:album:{}'.format(result[0].strip())
        album = sp.album(urn)
        artists = album['artists'][0]['name']
        for i in range(1, len(album['artists'])):
            artists += ", " + album['artists'][i]['name']
        item = {
            "img": album['images'][0]['url'],
            "artists": artists,
            "album_id": result[0],
            "name": result[1],
            "date": result[2]
        }
        search_res.append(item)
    return search_res



""" --------------------------------------------------"""
""" -----------------ARTIST FUNCTION -----------------"""
"""---------------------------------------------------"""
def fetch_artists() -> dict:
    """Reads all tasks listed in the todo table
    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    query_results = conn.execute("Select * From Artists ORDER BY artist_id DESC LIMIT 30;").fetchall()
    conn.close()
    todo_list = []
    for result in query_results:
        item = {
            "artist_id": result[0],
            "name": result[1]
        }
        todo_list.append(item)

    return todo_list

def update_artist_entry(task_id: str, text: str) -> None:
    conn = db.connect()
    query = 'UPDATE Artists SET artist_name = "{}" where artist_id = "{}";'.format(text, task_id)
    conn.execute(query)
    conn.close()

def insert_new_artist(artist_id: str, name: str) ->  None:
    conn = db.connect()
    today = date.today()
    print(artist_id)
    print(name)
    query = 'Insert Ignore Into Artists (artist_id, artist_name) VALUES ("{}", "{}");'.format(
        artist_id, name)
    conn.execute(query)
    conn.close()

    return artist_id

def remove_artist(task_id: str) -> None:
    """ remove entries based on artist ID """
    conn = db.connect()
    query = 'Delete From Artists Where artist_id="{}";'.format(task_id) #task_id = song_id, also note- quotes around {}
    conn.execute(query)
    conn.close()


""" --------------------------------------------------"""
""" -----------------SONGS FUNCTION -----------------"""
"""---------------------------------------------------"""
def fetch_songs() -> dict:
    """Reads all tasks listed in the todo table
    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    query_results = conn.execute("Select * From Songs LIMIT 30;").fetchall()
    conn.close()
    todo_list = []
    for result in query_results:
        item = {
            "song_id": result[0],
            "name": result[1],
            "release_date": result[2],
            "album_id": result[3]
        }
        todo_list.append(item)

    return todo_list

def update_song_entry(task_id: str, text: str) -> None:
    """Updates task description based on given `task_id`
    Args:
        task_id (int): Targeted song_id
        text (str): Updated name of song
    Returns:
        None
    """

    conn = db.connect()
    query = 'UPDATE Songs SET name = "{}" where song_id = "{}";'.format(text, task_id)
    conn.execute(query)
    conn.close()

def insert_new_song(song_id: str, name: str, album_id: str) ->  None:
    """Insert new task to todo table.
    Args:
        text (str): Song name. Looks up the song name from SongsOld table, and
        gets the value of the attributes.
    Returns: The task ID for the inserted entry
    """

    conn = db.connect()
    today = date.today()
    query = 'Insert Ignore Into Songs (song_id, name, release_date, album_id) VALUES ("{}", "{}", "{}", "{}");'.format(
        song_id, name, today, album_id)
    conn.execute(query)
    conn.close()

    return song_id