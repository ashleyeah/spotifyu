from flask import render_template, request, jsonify, Flask, url_for, session, redirect
from app import app
from app import database as db_helper
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask_session import Session
import json
import time
import pandas as pd
import os
import uuid

os.environ['SPOTIPY_CLIENT_ID']='f3dc4f3802254be091c8d8576961bc9d'
os.environ['SPOTIPY_CLIENT_SECRET']='b51d135ad7104add8f71933197e9cc14'
os.environ['SPOTIPY_REDIRECT_URI']='https://spotifyu.uc.r.appspot.com/'

app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
Session(app)

caches_folder = './.spotify_caches/'
if not os.path.exists(caches_folder):
    os.makedirs(caches_folder)

def session_cache_path():
    return caches_folder + session.get('uuid')

@app.route('/')
def index():
    # if not session.get('uuid'):
    #     # Step 1. Visitor is unknown, give random ID
    #     session['uuid'] = str(uuid.uuid4())

    # cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    # auth_manager = spotipy.oauth2.SpotifyOAuth(scope='user-library-read user-read-recently-played user-top-read',
    #                                             cache_handler=cache_handler, 
    #                                             show_dialog=True)

    # if request.args.get("code"):
    #     # Step 3. Being redirected from Spotify auth page
    #     auth_manager.get_access_token(request.args.get("code"))
    #     return redirect('/')

    # if not auth_manager.validate_token(cache_handler.get_cached_token()):
    #     # Step 2. Display sign in link when no token
    #     auth_url = auth_manager.get_authorize_url()
    #     return render_template("sign_in.html", url=auth_url)

    #     # return f'<h2><a href="{auth_url}">Sign in</a></h2>'


    # # Step 4. Signed in, display data
    # sp = spotipy.Spotify(auth_manager=auth_manager)
    # items = []
    # while True:
    #     curGroup = sp.current_user_top_tracks(limit=25, offset=0, time_range='medium_term')['items']
    #     for res in curGroup:
    #         artist = res['artists'][0]['name']
    #         for i in range(1, len(res['artists'])):
    #             artist += ", " + res['artists'][i]['name']
    #         item = {
    #             "img": res['album']['images'][1]['url'],
    #             "song_name": res['name'],
    #             "artist_name": artist,
    #             "album_name": res['album']['name']
    #         }
    #         items.append(item)
    #     break
    # artists = []
    # while True:
    #     curGroup2 = sp.current_user_top_artists(limit=25, offset=0, time_range='medium_term')['items']
    #     for res in curGroup2:
    #         genres = res['genres'][0]
    #         for i in range(1, len(res['genres'])):
    #             genres += ", " + res['genres'][i]
    #         image = "https://t4.ftcdn.net/jpg/00/64/67/63/360_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg"
    #         if len(res['images']) > 0:
    #             image = res['images'][1]['url']
    #         item = {
    #             "img": image,
    #             "name": res['name'],
    #             "genres": genres,
    #         }
    #         artists.append(item)
    #     break
    # items = db_helper.user_top_tracks(session.get('token_info').get('access_token'))
    # artists = db_helper.user_top_artists(session.get('token_info').get('access_token'))
    return render_template("index.html")


@app.route('/sign_out')
def sign_out():
    try:
        # Remove the CACHE file (.cache-test) so that a new user can authorize.
        os.remove(session_cache_path())
        session.clear()
    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))
    return redirect('/')


'''
Following lines allow application to be run more conveniently with
`python app.py` (Make sure you're using python3)
(Also includes directive to leverage pythons threading capacity.)
'''
if __name__ == '__main__':
    app.run(threaded=True, port=int(os.environ.get("PORT",
                                                   os.environ.get("SPOTIPY_REDIRECT_URI", 5000).split(":")[-1])))

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
    
    db_helper.insert_new_song(data['song_id'], data['song_name'])
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)

@app.route("/genre/create", methods=['POST'])
def create():
    """ recieves post requests to add new task """
    data = request.get_json()
    db_helper.insert_new_genre(data["name"])
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)

"""

Routing to different tables 

"""
@app.route("/album", methods=['GET', 'POST'])
def album():
    items = db_helper.fetch_albums()
    return render_template("album.html", items=items)

@app.route("/artist", methods=['GET', 'POST'])
def artist():
    items = db_helper.fetch_artists()
    return render_template("artist.html", items=items)

@app.route("/song", methods=['GET', 'POST'])
def song():
    items = db_helper.fetch_songs()
    return render_template("song.html", items=items)

@app.route("/genre", methods=['GET', 'POST'])
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
    print('search')
    res = db_helper.search_by_genre_name(request.form['search_name'])
    return render_template('searchGenre.html', items = res)

    

# special functions 

@app.route("/genre/search/<string:genre_name>", methods=['GET', 'POST'])
def genre_artists(genre_name):
    """ recieved post requests for entry updates """
    print('here?')
    data = request.get_json()
    res, genre = db_helper.display_artists_by_genre(genre_name)

    return render_template('genre_artists.html', items = res, genre = genre.upper())


# @app.route('/login')
# def login():
#     sp_oauth = create_spotify_oauth()
#     auth_url = sp_oauth.get_authorize_url()
#     print(auth_url)
#     return redirect(auth_url)

# @app.route('/authorize')
# def authorize():
#     sp_oauth = create_spotify_oauth()
#     session.clear()
#     code = request.args.get('code')
#     token_info = sp_oauth.get_access_token(code)
#     session["token_info"] = token_info
#     return redirect("/")

# @app.route('/logout')
# def logout():
#     for key in list(session.keys()):
#         session.pop(key)
#     return redirect('/')

# @app.route('/getTracks')
# def get_all_tracks():
#     session['token_info'], authorized = get_token()
#     session.modified = True
#     if not authorized:
#         return redirect('/login')
#     sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
#     results = []
#     iter = 0
#     while True:
#         offset = iter * 50
#         iter += 1
#         curGroup = sp.current_user_saved_tracks(limit=50, offset=offset)['items']
#         for idx, item in enumerate(curGroup):
#             track = item['track']
#             val = track['name'] + "," + track['id'] + "," + track['artists'][0]['name'] + "," + track['artists'][0]['id'] 
#             results += [val]
#         if (len(curGroup) < 50):
#             break
    
#     df = pd.DataFrame(results, columns=["song names"]) 
#     df.to_csv('songs.csv', index=False)
#     return redirect('/')


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
            scope="user-library-read user-read-recently-played user-top-read")