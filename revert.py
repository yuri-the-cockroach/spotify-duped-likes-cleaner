#!/usr/bin/env python3
from dotenv import load_dotenv
import os
import spotipy
import json
from spotipy import SpotifyOAuth

load_dotenv()
CLID: str = os.getenv("CLID")
SECRET: str = os.getenv("SECRET")
DEBUG: bool = os.getenv("DEBUG")

sp: spotipy.client.Spotify = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLID,
        client_secret=SECRET,
        redirect_uri="http://127.0.0.1:8888",
        scope="user-library-read,user-library-modify",
    )
)

songs = list()
with open("deleted-songs.json", "r") as file:
    songs = json.load(file)
    ids = list()
    for num, i in enumerate(songs):
        if num >= 50:
            break
        print(i[0]["track"]["artists"][0]["name"], "-", i[0]["track"]["name"])
        ids.append(i[0]["track"]["id"])
        print(ids)

    sp.current_user_saved_tracks_add(ids)
