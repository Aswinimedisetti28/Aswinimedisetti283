import webbrowser
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from googleapiclient.discovery import build
import os

# API Keys (store securely in real projects)
from dotenv import load_dotenv

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")


# Spotify API setup
spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

# YouTube API setup
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

def get_spotify_tracks(mood, limit=10):
    query = f"{mood} music"
    results = spotify.search(q=query, type='track', limit=limit)
    tracks = []
    for item in results['tracks']['items']:
        name = item['name']
        artist = item['artists'][0]['name']
        url = item['external_urls']['spotify']
        tracks.append({"title": f"{name} - {artist}", "url": url})
    return tracks

def get_youtube_videos(mood, limit=10):
    query = f"{mood} music"
    request = youtube.search().list(
        q=query,
        part="snippet",
        type="video",
        maxResults=limit
    )
    response = request.execute()
    videos = []
    for item in response["items"]:
        title = item["snippet"]["title"]
        video_id = item["id"]["videoId"]
        url = f"https://www.youtube.com/watch?v={video_id}"
        videos.append({"title": title, "url": url})
    return videos

def get_recommendations(mood, preference="listen"):
    mood = mood.lower().strip()
    try:
        if preference == "watch":
            return get_youtube_videos(mood)
        else:
            return get_spotify_tracks(mood)
    except Exception as e:
        print(f"[ERROR] Failed to fetch songs: {e}")
        return [{"title": "Fallback Music", "url": "https://www.youtube.com/watch?v=5qap5aO4i9A"}]


# Optional helper to directly open a song in browser (not used in rendering)
def play_first(mood, preference="listen"):
    songs = get_recommendations(mood, preference)
    if songs:
        webbrowser.open(songs[0]['url'])
