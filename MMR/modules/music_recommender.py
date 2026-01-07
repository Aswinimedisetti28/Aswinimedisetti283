import webbrowser
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

# -------------------- LOAD ENV --------------------
load_dotenv()
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# -------------------- SPOTIFY SETUP --------------------
spotify = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET
    )
)

# -------------------- YOUTUBE SETUP --------------------
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

# -------------------- SPOTIFY TRACKS (EN + TE) --------------------
def get_spotify_tracks(mood, limit=10):
    queries = [
        f"{mood} english music",
        f"{mood} telugu songs",
        f"telugu {mood} melody"
    ]

    tracks = []

    for q in queries:
        results = spotify.search(q=q, type="track", limit=limit // len(queries))
        for item in results["tracks"]["items"]:
            tracks.append({
                "title": f"{item['name']} - {item['artists'][0]['name']}",
                "url": item["external_urls"]["spotify"]
            })

    return tracks


# -------------------- YOUTUBE TRACKS (EN + TE) --------------------
def get_youtube_tracks(mood, limit=10):
    queries = [
        f"{mood} english songs",
        f"{mood} telugu songs",
        f"telugu {mood} music"
    ]

    tracks = []

    for q in queries:
        request = youtube.search().list(
            q=q,
            part="snippet",
            type="video",
            maxResults=limit // len(queries)
        )
        response = request.execute()

        for item in response.get("items", []):
            tracks.append({
                "title": item["snippet"]["title"],
                "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}"
            })

    return tracks


# -------------------- RECOMMENDATIONS --------------------
def get_recommendations(mood, preference="listen"):
    mood = mood.lower().strip()
    preference = preference.lower().strip()

    try:
        if preference == "watch":
            return get_youtube_tracks(mood)

        else:
            return get_spotify_tracks(mood)

    except Exception as e:
        print(f"[ERROR] Music fetch failed: {e}")
        return []


# -------------------- OPTIONAL AUTO PLAY --------------------
def play_first(mood, preference="listen"):
    tracks = get_recommendations(mood, preference)
    if tracks:
        webbrowser.open(tracks[0]["url"])
    else:
        print("No tracks found for this mood.")


# -------------------- TEST --------------------
if __name__ == "__main__":
    mood_input = input("Enter your mood: ")
    pref_input = input("Listen or Watch? (listen/watch): ")

    recommendations = get_recommendations(mood_input, pref_input)

    for idx, track in enumerate(recommendations, start=1):
        print(f"{idx}. {track['title']} → {track['url']}")

    play_first(mood_input, pref_input)
