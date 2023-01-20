import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
import pandas as pd
import re
import utils

# load credentials from .env file
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID", "")
CLIENT_SECRET = os.getenv("CLIENT_SECRET", "")
REDIRECT_URI = os.getenv("REDIRECT_URI", "")

def setScope(inputScope: str) -> spotipy.Spotify:
    output = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                       client_secret=CLIENT_SECRET,
                                                       redirect_uri=REDIRECT_URI,
                                                       scope=inputScope))
    return output


def extract_id(PLAYLIST_LINK: str) -> str:
    if match := re.match(r"https://open.spotify.com/playlist/(.*)\?", PLAYLIST_LINK):
        playlist_uri = match.groups()[0]
    else:
        raise ValueError(
            "Expected format: https://open.spotify.com/playlist/...")
    return str(playlist_uri)

sp = setScope('user-library-read')
