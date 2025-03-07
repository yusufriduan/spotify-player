import os
import spotipy
import time
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from flask import Flask, request, redirect, session, send_from_directory, jsonify
from flask_cors import CORS

app = Flask(__name__, static_folder='.../')
CORS(app, origins='http://localhost:5173', supports_credentials=True)

app.secret_key = 'super secret key'
app.config['SESSION_COOKIE_NAME'] = 'spotify-login-session'

client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')

load_dotenv()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.json
        # Process the data as needed
        return jsonify({"status": "success", "data": data})
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/login')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return jsonify({"url": auth_url})

@app.route('/callback')
def redirectPage():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code, as_dict=False)
    session[os.getenv('TOKEN_INFO')] = token_info

    # Redirect to React application with token info
    react_redirect_url = f"http://localhost:5173/callback?access_token={token_info['access_token']}"
    return redirect(react_redirect_url)

def get_token():
    token_info = session.get(os.getenv('TOKEN_INFO'), None)
    if not token_info:
        raise Exception("No token info")
    now = int(time.time())

    is_expired = token_info['expires_at'] - now < 60
    if (is_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
        session[os.getenv('TOKEN_INFO')] = token_info
    return token_info['access_token']

@app.route('/currentPlaying')
def currentPlaying():
    token = get_token()
    sp = spotipy.Spotify(auth=token)
    current_playing = sp.current_playback()
    return jsonify(current_playing)
    

def create_spotify_oauth():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(client_id=client_id,
                                              client_secret=client_secret,
                                              redirect_uri=redirect_uri,
                                              cache_handler=cache_handler,
                                              show_dialog=True,
                                              scope='user-read-playback-state user-read-currently-playing user-modify-playback-state')
    return auth_manager

if __name__ == '__main__':
    app.run(debug=True)