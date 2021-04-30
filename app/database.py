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
            "img": album['images'][1]['url'],
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
    # sql='SELECT * FROM Albums WHERE name LIKE %s LIMIT 50'
    # args=['%'+name+'%']
    # conn.execute(sql,args)

    query = 'CALL `main`.`SearchAlbum`("{}");'.format(name)

    query_results = conn.execute(query).fetchall()
    search_res = []

    for result in query_results:
        urn = 'spotify:album:{}'.format(result[0].strip())
        album = sp.album(urn)
        # artists = album['artists'][0]['name']
        # for i in range(1, len(album['artists'])):
        #     artists += ", " + album['artists'][i]['name']
        item = {
            "img": album['images'][1]['url'],
            "album_id": result[0],
            "name": result[1],
            "artists": result[2],
            "songs": result[4],
            "type": result[3]
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

    auth_manager = SpotifyClientCredentials('f3dc4f3802254be091c8d8576961bc9d', 'b51d135ad7104add8f71933197e9cc14')
    sp = spotipy.Spotify(auth_manager=auth_manager)

    conn = db.connect()
    query_results = conn.execute("Select * From Artists ORDER BY artist_id DESC LIMIT 50;").fetchall()
    conn.close()
    todo_list = []
    for result in query_results:
        urn = 'spotify:artist:{}'.format(result[0].strip())
        artist = sp.artist(urn)
        img = ''
        if len(artist['images']) > 0:
            img = artist['images'][1]['url']
        else:
            img = "https://t4.ftcdn.net/jpg/00/64/67/63/360_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg"
        item = {
            "img": img,
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

def search_artist(name: str) -> dict:
    auth_manager = SpotifyClientCredentials('f3dc4f3802254be091c8d8576961bc9d', 'b51d135ad7104add8f71933197e9cc14')
    sp = spotipy.Spotify(auth_manager=auth_manager)

    conn = db.connect()
    sql='SELECT * FROM Artists WHERE artist_name LIKE %s'
    args=['%'+name+'%']
    conn.execute(sql,args)
    query_results = conn.execute(sql,args).fetchall()
    search_res = []
    for result in query_results:
        urn = 'spotify:artist:{}'.format(result[0].strip())
        artist = sp.artist(urn)
        img = ''
        if len(artist['images']) > 0:
            img = artist['images'][1]['url']
        else:
            img = "https://t4.ftcdn.net/jpg/00/64/67/63/360_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg"
        item = {
            "img": img,
            "artist_id": result[0],
            "name": result[1]
        }
        search_res.append(item)
    return search_res


""" --------------------------------------------------"""
""" -----------------SONGS FUNCTION -----------------"""
"""---------------------------------------------------"""
def fetch_songs() -> dict:
    """Reads all tasks listed in the todo table
    Returns:
        A list of dictionaries
    """

    auth_manager = SpotifyClientCredentials('f3dc4f3802254be091c8d8576961bc9d', 'b51d135ad7104add8f71933197e9cc14')
    sp = spotipy.Spotify(auth_manager=auth_manager)

    conn = db.connect()
    query_results = conn.execute("Select s.song_id, s.name, s.release_date, a.name From Songs s JOIN Albums a USING(album_id) LIMIT 30;").fetchall()
    conn.close()
    todo_list = []
    for result in query_results:
        urn = 'spotify:track:{}'.format(result[0].strip())
        song = sp.track(urn)
        item = {
            "img": song['album']['images'][1]['url'],
            "song_id": result[0],
            "song_name": result[1],
            "release_date": result[2],
            "album_name": result[3]
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

def insert_new_song(song_id: str, name: str) ->  None:
    """Insert new task to todo table.
    Args:
        text (str): Song name. Looks up the song name from SongsOld table, and
        gets the value of the attributes.
    Returns: The task ID for the inserted entry
    """
    auth_manager = SpotifyClientCredentials('f3dc4f3802254be091c8d8576961bc9d', 'b51d135ad7104add8f71933197e9cc14')
    sp = spotipy.Spotify(auth_manager=auth_manager)
    
    conn = db.connect()
    # today = date.today()
    output = 'spotify:track:{}'.format(song_id)

    track = sp.track(output)
    
    song_name = track['name']
    release_date = track['album']['release_date']
    album_id = track['album']['id']
    


    query = 'Insert Ignore Into Songs (song_id, name, release_date, album_id) VALUES ("{}", "{}", "{}", "{}");'.format(
        song_id, song_name, release_date, album_id)
    conn.execute(query)
    conn.close()

    return song_id

def search_song(name: str) -> dict:

    auth_manager = SpotifyClientCredentials('f3dc4f3802254be091c8d8576961bc9d', 'b51d135ad7104add8f71933197e9cc14')
    sp = spotipy.Spotify(auth_manager=auth_manager)

    conn = db.connect()
    sql='SELECT s.song_id, s.name, s.release_date, s.album_id FROM Songs s LEFT OUTER JOIN Albums a USING(album_id) WHERE s.name LIKE %s'
    args=['%'+name+'%']
    conn.execute(sql,args)
    query_results = conn.execute(sql,args).fetchall()
    search_res = []
    for result in query_results:
        urn = 'spotify:track:{}'.format(result[0].strip())
        song = sp.track(urn)
        item = {
            "img": song['album']['images'][1]['url'],
            "song_id": result[0],
            "song_name": result[1],
            "release_date": result[2],
            "album_name": song['album']['name']
        }
        search_res.append(item)
    return search_res
    

def remove_song(task_id: str) -> None:
    """ remove entries based on song ID """
    conn = db.connect()
    query = 'Delete From Songs Where song_id="{}";'.format(task_id) #task_id = song_id, also note- quotes around {}
    conn.execute(query)
    conn.close()


""" --------------------------------------------------"""
""" -----------------GENRE FUNCTION-------------------"""
"""---------------------------------------------------"""

def fetch_genres() -> dict:
    """Reads all tasks listed in the todo table

    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    query_results = conn.execute("Select * from Genres ORDER BY genre_id LIMIT 50;").fetchall()
    conn.close()
    todo_list = []
    for result in query_results:
        item = {
            "id": result[0],
            "name": result[1]
        }
        todo_list.append(item)

    return todo_list


def update_name_genre(task_id: int, text: str) -> None:
    """Updates task description based on given `task_id`

    Args:
        task_id (int): Targeted task_id
        text (str): Updated description

    Returns:
        None
    """
    conn = db.connect()
    query = 'Update Genres SET name = "{}" where genre_id = {};'.format(text, task_id)
    conn.execute(query)
    conn.close()

def insert_new_genre(name: str) ->  int:
    """Insert new task to todo table.

    Args:
        text (str): Task description

    Returns: The task ID for the inserted entry
    """

    conn = db.connect()
    min_id = conn.execute('SELECT MIN(genre_id) FROM Genres;').fetchall()[0][0]
    if min_id != 1:
        first_empty_id = 1
    else:
        query1 = 'SELECT a.genre_id+1 AS start FROM Genres AS a, Genres AS b WHERE a.genre_id < b.genre_id GROUP BY a.genre_id HAVING start < MIN(b.genre_id) LIMIT 1'
        conn.execute(query1)
        query_res = conn.execute(query1).fetchall()
        if not query_res:
            first_empty_id = conn.execute('SELECT MAX(genre_id) FROM Genres;').fetchall()[0][0] + 1
        else:
            first_empty_id = query_res[0][0]
    query = 'INSERT INTO Genres (genre_id, name) VALUES ("{}", "{}");'.format(first_empty_id, name)
    print(first_empty_id)
    conn.execute(query)
    conn.close()

    return first_empty_id


def remove_genre_id(id: int) -> None:
    """ remove entries based on task ID """

    conn = db.connect()
    query = 'DELETE From Genres where genre_id={};'.format(id)
    conn.execute(query)
    conn.close()


def genre_advanced_query():
    conn = db.connect()
    query = 'SELECT ag.genre_name, COUNT(sa.song_id) AS song_count FROM Artist_to_Genre ag JOIN SongsArtists as sa USING(artist_id) GROUP BY ag.genre_name ORDER BY song_count DESC LIMIT 15;'
    res = conn.execute(query).fetchall()
    conn.close()
    print(res)
    result = []
    for r in res:
        item = {
            "id": r[0],
            "name": r[1]
        }
        result.append(item)
    return result

def search_by_genre_name(name: str):
    conn = db.connect()
    query = "SELECT genre_name, group_concat(artist_name) FROM main.Artist_to_Genre NATURAL JOIN (SELECT genre_id FROM main.Genres WHERE name LIKE '%%{}%%') AS t GROUP BY genre_name;".format(name)
    res = conn.execute(query).fetchall()
    result = []
    for r in res:
        item = {
            "name": r[0],
            "artists": r[1]
        }
        result.append(item)
    conn.close()
    return result


def display_artists_by_genre(name: str):
    conn = db.connect()
    query = "SELECT * FROM Artist_to_Genre WHERE genre_name = '{genre_name}'".format(genre_name = name)
    res = conn.execute(query).fetchall()
    print(res)

    result = []
    auth_manager = SpotifyClientCredentials('f3dc4f3802254be091c8d8576961bc9d', 'b51d135ad7104add8f71933197e9cc14')
    sp = spotipy.Spotify(auth_manager=auth_manager)


    for r in res:
        urn = 'spotify:artist:{}'.format(r[0].strip())
        artist = sp.artist(urn)
        img = ''
        if len(artist['images']) > 0:
            img = artist['images'][1]['url']
        else:
            img = "https://t4.ftcdn.net/jpg/00/64/67/63/360_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg"
        item = {
            "img": img,
            "name": r[1],
            "genre": r[3]
        }
        result.append(item)
    return result, res[0][3]





""" --------------------------------------------------"""
""" -----------------USER CUSTOM FUNCTION-------------------"""
"""---------------------------------------------------"""

def user_top_tracks(access_token: str) -> dict:
    sp = spotipy.Spotify(auth=access_token)
    items = []
    while True:
        curGroup = sp.current_user_top_tracks(limit=25, offset=0, time_range='medium_term')['items']
        for res in curGroup:
            artist = res['artists'][0]['name']
            for i in range(1, len(res['artists'])):
                artist += ", " + res['artists'][i]['name']
            item = {
                "img": res['album']['images'][1]['url'],
                "song_name": res['name'],
                "artist_name": artist,
                "album_name": res['album']['name']
            }
            items.append(item)
        break
    return items

def user_top_artists(access_token: str) -> dict:
    sp = spotipy.Spotify(auth=access_token)
    items = []
    while True:
        curGroup = sp.current_user_top_artists(limit=25, offset=0, time_range='medium_term')['items']
        for res in curGroup:
            genres = res['genres'][0]
            for i in range(1, len(res['genres'])):
                genres += ", " + res['genres'][i]
            image = "https://t4.ftcdn.net/jpg/00/64/67/63/360_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg"
            if len(res['images']) > 0:
                image = res['images'][1]['url']
            item = {
                "img": image,
                "name": res['name'],
                "genres": genres,
            }
            items.append(item)
        break
    return items