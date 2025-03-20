import os, spotipy, time, json
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from flask import Flask, request, redirect, session, send_from_directory, jsonify
from flask_cors import CORS

app = Flask(__name__, static_folder='.../')
CORS(app, origins='http://localhost:5173', supports_credentials=True)

app.secret_key = 'super secret key'
app.config['SESSION_COOKIE_NAME'] = 'spotify-login-session'

load_dotenv()

client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')

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
    try:
        token_info = sp_oauth.get_access_token(code, as_dict=True)
    except Exception as e:
        print(f"Error getting access token: {e}")
        return jsonify({"error": "Failed to retrieve access token"}), 500

    if isinstance(token_info, str):
        try:
            token_info = json.loads(token_info)
        except json.JSONDecodeError as e:
            print(f"Error decoding token info: {e}")
            return jsonify({"error": "Failed to decode access token"}), 500

    if not token_info or 'access_token' not in token_info:
        return jsonify({"error": "Failed to retrieve access token"}), 400

    session['token_info'] = json.dumps(token_info)
    print("Token info stored in session:", session['token_info'])

    # Get user details
    sp = spotipy.Spotify(auth=token_info['access_token'])
    user_details = sp.current_user()

    # Debugging statements
    print("Token Info:", token_info)
    print("User Details:", user_details)

    # Redirect to React application with token info and user details
    react_redirect_url = (
        f"http://localhost:5173/callback?"
        f"access_token={token_info['access_token']}&"
        f"refresh_token={token_info['refresh_token']}&"
        f"expires_in={token_info['expires_in']}&"
        f"user_id={user_details['id']}&"
        f"user_name={user_details['display_name']}"
    )
    print("Redirect URL:", react_redirect_url)
    return redirect(react_redirect_url)

def get_token():
    token_info = session.get('token_info')
    if not token_info:
        print("Token info not found in session")
        raise Exception("No token info")
    token_info = json.loads(token_info)
    print("Token Info Retrieved:", token_info)  # Debugging statement
    now = int(time.time())

    expires_at = token_info.get('expires_at')
    if expires_at is None:
        raise Exception("Token expiration time is missing")

    is_expired = expires_at - now < 60
    if is_expired:
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
        session['token_info'] = json.dumps(token_info)
    return token_info['access_token']

@app.route('/currentPlaying')
def currentPlaying():
    try:
        token = request.headers.get('Authorization').split(' ')[1]
        sp = spotipy.Spotify(auth=token)
        current_playing = sp.current_playback()
        return jsonify(current_playing)
    except Exception as e:
        print(f"Error in currentPlaying: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/play', methods=['GET'])
def play():
    try:
        token = request.headers.get('Authorization').split(' ')[1]
        sp = spotipy.Spotify(auth=token)
        sp.start_playback()
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(f"Error in play: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/pause', methods=['GET'])
def pause():
    try:
        token = request.headers.get('Authorization').split(' ')[1]
        sp = spotipy.Spotify(auth=token)
        sp.pause_playback()
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(f"Error in pause: {e}")
        return jsonify({"error": str(e)}), 500
    
@app.route('/forward', methods=['GET'])
def next_track():
    try:
        token = request.headers.get('Authorization').split(' ')[1]
        sp = spotipy.Spotify(auth=token)
        sp.next_track()
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(f"Error in next_track: {e}")
        return jsonify({"error": str(e)}), 500
    
@app.route('/backward', methods=['GET'])
def previous_track():
    try:
        token = request.headers.get('Authorization').split(' ')[1]
        sp = spotipy.Spotify(auth=token)
        sp.previous_track()
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(f"Error in previous_track: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return jsonify({"status": "success"}), 200
    

def create_spotify_oauth():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(client_id=client_id,
                                              client_secret=client_secret,
                                              redirect_uri=redirect_uri,
                                              cache_handler=cache_handler,
                                              show_dialog=True,
                                              scope='user-read-playback-state user-read-currently-playing user-modify-playback-state')
    return auth_manager

@app.after_request
def add_cors_headers(response):
    if 'Access-Control-Allow-Origin' not in response.headers:
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
    if 'Access-Control-Allow-Credentials' not in response.headers:
        response.headers.add('Access-Control-Allow-Credentials', 'true')
    if 'Access-Control-Allow-Headers' not in response.headers:
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    if 'Access-Control-Allow-Methods' not in response.headers:
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS,DELETE,PUT')
    return response

@app.route('/forward', methods=['OPTIONS'])
def handle_forward_options():
    response = jsonify({"status": "success"})
    response.status_code = 200
    return response

@app.route('/backward', methods=['OPTIONS'])
def handle_backward_options():
    response = jsonify({"status": "success"})
    response.status_code = 200
    return response

if __name__ == '__main__':
    app.run(debug=True)