from flask import render_template, request, jsonify, Flask, url_for, session, redirect
from app import app
from app import database as db_helper
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import time
import pandas as pd

"""

DELETE FUNCTIONS

"""
@app.route("/album/delete/<string:task_id>", methods=['POST'])
def delete_album(task_id):
    """ recieved post requests for entry delete """

    try:
        db_helper.remove_album(task_id)
        result = {'success': True, 'response': 'Removed task'}
    except:
        result = {'success': False, 'response': 'Something went wrong {}'.format(task_id)}        
    return jsonify(result)

@app.route("/artist/delete/<string:task_id>", methods=['POST'])
def delete_artist(task_id):
    """ recieved post requests for entry delete """

    try:
        db_helper.remove_artist(task_id)
        result = {'success': True, 'response': 'Removed task'}
    except:
        result = {'success': False, 'response': 'Something went wrong {}'.format(task_id)}        
    return jsonify(result)

@app.route("/song/delete/<string:task_id>", methods=['POST'])
def delete_song(task_id):
    """ recieved post requests for entry delete """

    try:
        db_helper.remove_song(task_id)
        result = {'success': True, 'response': 'Removed task'}
    except:
        result = {'success': False, 'response': 'Something went wrong {}'.format(task_id)}        
    return jsonify(result)



@app.route("/genre/delete/<int:song_id>", methods=['POST'])
def delete(song_id):
    """ recieved post requests for entry delete """

    try:
        db_helper.remove_genre_id(song_id)
        result = {'success': True, 'response': 'Removed task'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)

"""

UPDATE FUNCTIONS

"""
@app.route("/album/edit/<string:task_id>", methods=['POST'])
def update_album(task_id):
    """ recieved post requests for entry updates """
    print("In update Album")
    data = request.get_json()

    try:
        if "name" in data:
            db_helper.update_album_entry(task_id, data["name"], data["date"])
            result = {'success': True, 'response': 'Task Updated'}
        else:
            result = {'success': True, 'response': 'Nothing Updated'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)

@app.route("/artist/edit/<string:task_id>", methods=['POST'])
def update_artist(task_id):

    print("We are in update artist")
    """ recieved post requests for entry updates """
    print("In Update Artist")
    data = request.get_json()

    try:
        if "name" in data:
            db_helper.update_artist_entry(task_id, data["name"])
            result = {'success': True, 'response': 'Task Updated'}
        else:
            result = {'success': True, 'response': 'Nothing Updated'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)

@app.route("/song/edit/<string:task_id>", methods=['POST'])
def update_song(task_id):
    """ recieved post requests for entry updates """
    print("We are in update song")
    data = request.get_json()

    try:
        if "song_name" in data:
            print(task_id, data['song_name'])
            db_helper.update_song_entry(task_id, data['song_name'])
            result = {'success': True, 'response': 'Task Updated'}
        else:
            result = {'success': True, 'response': 'Nothing Updated'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)


@app.route("/genre/edit/<int:task_id>", methods=['POST'])
def update(task_id):
    """ recieved post requests for entry updates """

    data = request.get_json()

    try:
        if "name" in data:
            db_helper.update_name_genre(task_id, data["name"])
            result = {'success': True, 'response': 'Task Updated'}
        else:
            result = {'success': True, 'response': 'Nothing Updated'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)



""" 
CREATE FUNCTIONS 
 """
@app.route("/album/create", methods=['POST'])
def create_album():
    """ recieves post requests to add new task """
    data = request.get_json()
    db_helper.insert_new_album(data['id'], data['name'], data['date'])
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)

@app.route("/artist/create", methods=['POST'])
def create_artist():
    """ recieves post requests to add new task """
    data = request.get_json()
    print("IN ARTIST CREATE")
    print(data['id'], data['name'])
    db_helper.insert_new_artist(data['id'], data['name'])
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)

@app.route("/song/create", methods=['POST'])
def create_song():
    """ recieves post requests to add new task """
    print("We are in create song.")
    data = request.get_json()
    
    db_helper.insert_new_song(data['song_id'], data['song_name'], data['album_id'])
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)

@app.route("/genre/create", methods=['POST'])
def create():
    """ recieves post requests to add new task """
    data = request.get_json()
    db_helper.insert_new_genre(data["name"])
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)






@app.route("/")
def homepage():
    """ returns rendered homepage """
    session['token_info'], authorized = get_token()
    session.modified = True
    print(authorized)
    if not authorized:
        return redirect('/login')
    else:
        return render_template("index.html")


"""

Routing to different tables 

"""
@app.route("/album", methods=['POST'])
def album():
    items = db_helper.fetch_albums()
    return render_template("album.html", items=items)

@app.route("/artist", methods=['POST'])
def artist():
    items = db_helper.fetch_artists()
    return render_template("artist.html", items=items)

@app.route("/song", methods=['POST'])
def song():
    items = db_helper.fetch_songs()
    return render_template("song.html", items=items)

@app.route("/genre", methods=['POST'])
def genre():
    items = db_helper.fetch_genres()
    return render_template("genre.html", items=items)

# @app.route("/user-info", methods=['POST'])
# def userInfo():
#     items = db_helper.fetch_userInfo()
#     return render_template("userInfo.html", items=items)




""" 

@app.route("/album/advance", methods=['POST'])
def advanced():
    items = db_helper.advanced_query_album()
    return render_template("advanced_query.html", items=items) 
"""


@app.route("/album/search", methods=['POST'])
def search_album():
    data = request.get_json()
    items = db_helper.search_album(request.form['search_name'])
    return render_template("searchAlbum.html", items=items)

@app.route("/artist/search", methods=['POST'])
def search_artist():
    data = request.get_json()
    items = db_helper.search_artist(request.form['search_name'])
    return render_template("searchArtist.html", items=items)

@app.route("/song/search", methods=['POST'])
def search_song():
    data = request.get_json()
    items = db_helper.search_song(request.form['search_name'])
    return render_template("searchSong.html", items=items)

@app.route("/genre/search", methods=['POST'])
def search_by_name():
    res = db_helper.search_by_genre_name(request.form['search_name'])
    return render_template('searchGenre.html', items = res)

    

@app.route('/login')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    print(auth_url)
    return redirect(auth_url)

@app.route('/authorize')
def authorize():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session["token_info"] = token_info
    return redirect("/getTracks")

@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')

@app.route('/getTracks')
def get_all_tracks():
    session['token_info'], authorized = get_token()
    session.modified = True
    if not authorized:
        return redirect('/login')
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    results = []
    iter = 0
    while True:
        offset = iter * 50
        iter += 1
        curGroup = sp.current_user_saved_tracks(limit=50, offset=offset)['items']
        for idx, item in enumerate(curGroup):
            track = item['track']
            val = track['name'] + "," + track['id'] + "," + track['artists'][0]['name'] + "," + track['artists'][0]['id'] 
            results += [val]
        if (len(curGroup) < 50):
            break
    
    df = pd.DataFrame(results, columns=["song names"]) 
    df.to_csv('songs.csv', index=False)
    return redirect('/')


# Checks to see if token is valid and gets a new token if not
def get_token():
    token_valid = False
    token_info = session.get("token_info", {})

    # Checking if the session already has a token stored
    if not (session.get('token_info', False)):
        token_valid = False
        return token_info, token_valid

    # Checking if token has expired
    now = int(time.time())
    is_token_expired = session.get('token_info').get('expires_at') - now < 60

    # Refreshing token if it has expired
    if (is_token_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(session.get('token_info').get('refresh_token'))

    token_valid = True
    return token_info, token_valid


# CLIENT_ID = 'f3dc4f3802254be091c8d8576961bc9d'
# CLIENT_SECRET = 'b51d135ad7104add8f71933197e9cc14'

def create_spotify_oauth():
    return SpotifyOAuth(
            client_id="f3dc4f3802254be091c8d8576961bc9d",
            client_secret="b51d135ad7104add8f71933197e9cc14",
            redirect_uri=url_for('authorize', _external=True),
            scope="user-library-read")