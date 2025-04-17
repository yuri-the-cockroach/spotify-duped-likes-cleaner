#!/usr/bin/env python

import datetime
import spotipy
from spotipy import SpotifyOAuth
import json
import os
from dotenv import load_dotenv

load_dotenv()
CLID: str = os.getenv("CLID")
SECRET: str = os.getenv("SECRET")
# I fucking hate python, this is abysmal.
# If I try to do it as a boolean, it's always true, so it is what it is...
DEBUG: bool = bool(int(os.getenv("DEBUG")))


def formJson(sp: spotipy.client.Spotify) -> list[dict]:
    """Make one big json out of all songs in your saved
    Spotify api only allow to get 50 songs at a time
    so you have to load them in a loop
    """
    total: list[dict] = list()
    sp.current_user_saved_tracks
    offset = 0
    limit = 50

    # Because python is shit and doesn't have a do-while loop
    results: list[dict] = sp.current_user_saved_tracks(limit=limit, offset=offset)[
        "items"
    ]
    total.extend(results)
    offset += limit
    while len(results):
        print(f"Current offset = {offset}")
        results = sp.current_user_saved_tracks(limit=limit, offset=offset)["items"]
        total.extend(results)
        offset += limit

    print(f"Got {len(total)} songs total")
    return total


def getAddedAtTimeStamp(song: dict) -> int:
    """A helper function to get unix timestamp as int straigt from the song's dict"""
    if type(song) != dict:
        print("Wrong type argument", type(song))
        exit(-1)

    return int(datetime.datetime.fromisoformat(song["added_at"]).timestamp())


def deleteDup(sp: spotipy.client.Spotify, dupes: list[list[dict]]):
    """Delete all the duplicated songs"""

    # Type checking, because python sucks
    if type(dupes) != list or type(dupes[0]) != list or type(dupes[0][0]) != dict:
        print(type(dupes))
        print(type(dupes[0]))
        print(type(dupes[0][0]))
        exit(69)
    to_delete: list[str] = list()

    for dupe in dupes:
        to_delete.append(
            # Prefer song that were added more recently to delete
            dupe[1]["track"]["id"]
            if (getAddedAtTimeStamp(dupe[0]) > getAddedAtTimeStamp(dupe[1]))
            else dupe[0]["track"]["id"]
        )

    # Still can't query for more than 50 songs at a time
    for i in range(0, len(to_delete), 50):
        if DEBUG:
            continue
        sp.current_user_saved_tracks_delete(to_delete[0 + i : 50 + i])


def main():
    # Create a session
    sp: spotipy.client.Spotify = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=CLID,
            client_secret=SECRET,
            redirect_uri="http://127.0.0.1:8888",
            scope="user-library-read,user-library-modify",
        )
    )

    track_list: list[dict] = list()
    isrc_dict: dict[list[dict]] = dict()
    dupes_list: list[list[dict]] = list()
    track_list: list[dict] = list()

    # Load songs from json; for debugging only
    if DEBUG:
        with open("dump.json", "r") as file:
            track_list = json.load(file)
    else:
        track_list: list[dict] = formJson(sp)

    for item in track_list:
        isrc = item["track"]["external_ids"][
            "isrc"
        ]  # Check the song by it's ISRC id, which is the same for a song and each it's permutation

        if not isrc_dict.get(isrc):
            isrc_dict[isrc] = list()

        isrc_dict[isrc].append(item)

    # Make a list of ISRC that have more than one match
    for i, isrc in enumerate(isrc_dict.keys()):
        if len(isrc_dict[isrc]) == 1:
            continue

        artists: str = ", ".join(
            [art["name"] for art in isrc_dict[isrc][0]["track"]["artists"]]
        )
        if (
            f"{artists} - {isrc_dict[isrc][0]['track']['name']}"
            == f"{artists} - {isrc_dict[isrc][1]['track']['name']}"
        ):
            print(
                f"{artists} - {isrc_dict[isrc][0]['track']['name']} == {artists} - {isrc_dict[isrc][1]['track']['name']}"
            )
            dupes_list.append(isrc_dict[isrc])

    if not len(dupes_list):
        print("found no duplicates... bye!")
        exit()

    ret: str = input(f"found {len(dupes_list)} dupes... Delete them? y/N\n")
    if ret != "y" and ret != "Y":
        print("Anything that is not y/Y is treated as no. Exiting now...")
        exit()

    print(f"Deleteing {len(dupes_list)} dupes...")

    deleteDup(sp, dupes_list)
    print("Done. Saving list of deleted songs just in case...")
    with open("deleted-songs.json", "w") as file:
        json.dump(dupes_list, file)

    return


if __name__ == "__main__":
    main()
