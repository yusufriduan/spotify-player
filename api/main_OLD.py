from flask import Flask, request, redirect, jsonify, session
from dotenv import load_dotenv
import os, base64, requests, json

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')

def get_token():
  auth_string = client_id + ':' + client_secret
  auth_bytes = auth_string.encode('utf-8')
  auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

  url = "https://accounts.spotify.com/api/token"
  headers = {
    "Authorization": "Basic " + auth_base64,
    "Content-Type": "application/x-www-form-urlencoded"
  }
  data = {"grant_type": "client_credentials"}
  result = requests.post(url, headers=headers, data=data)
  json_result = json.loads(result.content)
  token = json_result['access_token']
  return token

def get_auth_header(token):
  return {"Authorization": "Bearer " + token}

@app.route('/login')
def login():
  scopes = "user-read-playback-state user-modify-playback-state"
  auth_url = f"https://accounts.spotify.com/authorize?response_type=code&client_id={client_id}&scopes={scopes}&redirect_uri={REDIRECT_URI}"
  return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": client_id,
        "client_secret": client_secret
    }
    response = requests.post(url, headers=headers, data=data)
    session['token_info'] = response.json()
    return redirect('/')

@app.route('/refresh_token')
def refresh_token():
    refresh_token = session['token_info']['refresh_token']
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret
    }
    response = requests.post(url, headers=headers, data=data)
    session['token_info'] = response.json()
    return jsonify(session['token_info'])

@app.route('/api/playback-state')
def get_playback_state():
    token = session['token_info']['access_token']
    url = "https://api.spotify.com/v1/me/player"
    headers = get_auth_header(token)
    response = requests.get(url, headers=headers)
    return jsonify(response.json())


if __name__ == '__main__':
    app.run(debug=True)