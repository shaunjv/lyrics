from flask import Flask, jsonify, render_template, send_from_directory
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import lyricsgenius
import webbrowser
import threading
import os

# === CONFIG ===
SPOTIFY_CLIENT_ID = "dca25a8751fa48ff8859723fbabaf78a"
SPOTIFY_CLIENT_SECRET = "703b80952f41425095c98f793f93a216"
SPOTIFY_REDIRECT_URI = "http://127.0.0.1:8888/callback"
GENIUS_ACCESS_TOKEN = "AAnes0OAI3s3reAJyYvn90F2eXty7zbA5tT2h2kpzmMbxNv5gk582J3-usBLadEv"

# === APP SETUP ===
app = Flask(__name__, static_folder="static", template_folder="templates")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="user-read-playback-state",
    cache_path=".spotify_cache"
))

genius = lyricsgenius.Genius(GENIUS_ACCESS_TOKEN)
genius.skip_non_songs = True
genius.excluded_terms = ["(Remix)", "(Live)"]
genius.verbose = False

# === FUNCTIONS ===
def get_current_song():
    playback = sp.current_playback()
    if playback and playback.get("is_playing"):
        item = playback["item"]
        return item["name"], item["artists"][0]["name"]
    return None, None

# === ROUTES ===
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/lyrics")
def lyrics():
    track_name, artist_name = get_current_song()
    if track_name:
        song = genius.search_song(track_name, artist_name)
        lyrics_text = song.lyrics if (song and song.lyrics) else "Lyrics not found."
        return jsonify({
            "title": track_name,
            "artist": artist_name,
            "lyrics": lyrics_text
        })
    return jsonify({
        "title": "Nothing playing",
        "artist": "",
        "lyrics": ""
    })

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, "static"), "icon.png", mimetype="image/png")

# === BROWSER OPEN + SERVER RUN ===
def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")

if __name__ == "__main__":
    import os
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        threading.Timer(1, open_browser).start()
    app.run(debug=True, host="0.0.0.0", port=5000)
