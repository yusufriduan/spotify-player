import os
import spotipy
import time
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from flask import Flask, request, redirect, session, url_for, send_from_directory, jsonify
from flask_cors import CORS

app = Flask(__name__, static_folder='.../')
CORS(app, supports_credentials=True)

app.secret_key = 'super secret key'
app.config['SESSION_COOKIE_NAME'] = 'spotify-login-session'

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
    token_info = sp_oauth.get_access_token(code)
    session[os.getenv('TOKEN_INFO')] = token_info
    return redirect(url_for('index'))

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
    try:
        sp = spotipy.Spotify(auth=get_token()["access_token"])
        playback_info = sp.current_playback()
        return jsonify(playback_info)
    except:
        print("Error: User is not logged in")

def create_spotify_oauth():
    return SpotifyOAuth(client_id=os.getenv('CLIENT_ID'),client_secret=os.getenv('CLIENT_SECRET'),redirect_uri=os.getenv('REDIRECT_URI'),scope='user-read-playback-state user-modify-playback-state')

if __name__ == '__main__':
    app.run(debug=True)