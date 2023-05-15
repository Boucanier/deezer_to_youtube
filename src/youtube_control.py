import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import csv

scopes = ["https://www.googleapis.com/auth/youtube.readonly", "https://www.googleapis.com/auth/youtube.force-ssl"]


def create_playlist(youtube, title, description):
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
    print("Created playlist : ", {response['snippet']['title']}, " - ID: " + str({response['id']}))
    return response['id']


def search_tracks():
    tracks = {}
    with open("data/tracks.csv", "r") as track_file :
        spamreader = csv.reader(track_file, delimiter=',')
        for e in spamreader :
            tracks[e[0]] = e[1]
    return tracks


def add_tracks(id, tracks, youtube):
    ids = []
    for e in tracks :
        search_response = youtube.search().list(part="id",q = e + " " + tracks[e],type="video",maxResults=1).execute()
        ids.append(search_response["items"][0]["id"]["videoId"])
    for i in range(len(ids)) :
        request = youtube.playlistItems().insert(
            part='snippet',
            body={
                'snippet': {
                    'playlistId': id,
                    'position': 0,
                    'resourceId': {
                        'kind': 'youtube#video',
                        'videoId': ids[i]
                    }
                }
            }
        )
        print(i+1, "/", len(ids))
        request.execute()


def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "data/client_secret_id.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
    credentials = flow.run_local_server(port = 0)
    youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

    playlist_id = create_playlist(youtube, "deezer_to_youtube", "Here is a copy of your deezer playlist")
    tracks = search_tracks()
    add_tracks(playlist_id, tracks, youtube)

if __name__ == "__main__":
    main()