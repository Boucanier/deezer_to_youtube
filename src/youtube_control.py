"""
    This script is used to create a youtube playlist and add tracks to it
"""
import os
import csv

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly", "https://www.googleapis.com/auth/youtube.force-ssl"]


def create_playlist(youtube, title, description):
    """
        Create a youtube playlist

        - Args :
            - youtube : youtube api object
            - title (str) : playlist title
            - description (str) : playlist description
            
        - Returns :
            - id (str) : playlist id
    """
    request = youtube.playlists().insert(
        part="snippet,status",
        body={
          "snippet": {
            "title": title,
            "description": description,
            "defaultLanguage": "en"
          },
          "status": {
            "privacyStatus": "public"
          }
        }
    )
    response = request.execute()
    print("Created playlist :", {response['snippet']['title']}, "- ID:", str({response['id']}))
    return response['id']


def search_tracks():
    """
        Read data/tracks.csv and return a dict of tracks
        Dict format : {TITLE : ARTIST}

        - Args :
            - None
        
        - Returns :
            - tracks (dict) : dict of tracks
    """
    tracks = {}
    with open("data/tracks.csv", "r") as track_file :
        spamreader = csv.reader(track_file, delimiter=',')
        for e in spamreader :
            tracks[e[0]] = e[1]
        tracks.pop("Title")
    return tracks


def add_tracks(id, playlist_name, tracks, youtube):
    """
        Search tracks on youtube and add them to the previously created playlist

        - Args :
            - id (str) : playlist id
            - tracks (dict) : dict of tracks
            - youtube : youtube api object

        - Returns :
            - None
    """
    save = {}
    create_check = False
    
    if os.path.exists("data/historic.csv") :
        with open("data/historic.csv", "r") as save_file :
            spamreader = csv.reader(save_file, delimiter=',')
            for e in spamreader :
                if e[0] != "PLAYLIST_NAME" :
                    save[e[0]] = (e[1], e[2])
            if not "PLAYLIST_NAME" in save or save["PLAYLIST_NAME"][0] != playlist_name :
                create_check = True

    if not os.path.exists("data/historic.csv") or create_check :
        with open("data/historic.csv", "w") as save_file :
            spamwriter = csv.writer(save_file, delimiter=',')
            spamwriter.writerow(["PLAYLIST_NAME", playlist_name])

    cpt = 0
    max = len(save)
    for e in tracks :
        if (e not in save or save[e] != tracks[e]) and e != "PLAYLIST_NAME" :
            search_response = youtube.search().list(part="id",q = e + " " + tracks[e],type="video",maxResults=1).execute()
            save[e] = (tracks[e], search_response["items"][0]["id"]["videoId"])
            print("get :", cpt+1, "/", len(tracks) - max)

            request = youtube.playlistItems().insert(part = 'snippet', body = {'snippet' : {'playlistId' : id, 'position' : 0, 'resourceId' : {'kind' : 'youtube#video', 'videoId' : save[e][1]}}})

            request.execute()
            print("add :", cpt+1, "/", len(tracks) - max)

            with open("data/historic.csv", "a") as save_file :
                spamwriter = csv.writer(save_file, delimiter=',')
                spamwriter.writerow([e, save[e][0], save[e][1]])

            cpt += 1


def main():
    
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    assert(os.path.exists("data/client_secret_id.json"), "No data/client_secret_id.json file found")

    client_secrets_file = "data/client_secret_id.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
    credentials = flow.run_local_server(port = 0)
    youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

    playlists = {}
    playlists_response = youtube.playlists().list(part = "snippet", mine=True).execute()

    for playlist in playlists_response["items"]:
        playlists[playlist["snippet"]["title"]] = playlist["id"]

    tracks = search_tracks()

    playlist_name = tracks["PLAYLIST_NAME"]

    if playlist_name in playlists :
        playlist_id = playlists[playlist_name]
        print("Playlist :", playlist_name, "- ID:", str(playlist_id))
    else :
        playlist_id = create_playlist(youtube, playlist_name, "Here is a copy of your deezer playlist")

    add_tracks(playlist_id, playlist_name, tracks, youtube)

if __name__ == "__main__":
    main()