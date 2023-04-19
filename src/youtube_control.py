# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

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


def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "data/client_secret_id.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_local_server(port = 0)
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    create_playlist(youtube, "deezer_to_youtube", "Here is a copy of your deezer playlist")

if __name__ == "__main__":
    main()