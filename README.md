# deezer_to_youtube

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Deezer](https://img.shields.io/badge/Deezer-FEAA2D?style=for-the-badge&logo=deezer&logoColor=white)
![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?style=for-the-badge&logo=YouTube&logoColor=white)

This project create a youtube playlist that contain tracks that are in a deezer playlist.

## Requirements

- __Python 3.10__ or above (_```sudo apt install python3```_)
- __requests__ module (_```pip install requests```_)
- __google-api-python-client__ (_```pip install google-api-python-client```_)
- __google-auth-oauthlib__ (_```pip install google-auth-oauthlib```_)
- __google-auth-httplib2__ (_```pip install google-auth-httplib2```_)

To install all these requirements on a Debian based Linux distribution, you can run the script _installation.sh_

## Description

Run _src/main.py_ to start the program. Then you will have to enter a deezer user id or to chose an already registered one (you can paste your user id in _data/user_id.txt_).

Then you will have to chose between a new playlist or a saved playlist. If you chose a new playlist, you will have to chose among all the playlists related to you deezer account. Once you have chosen a playlist, its information will be saved in _data/tracks.csv_. Therefore, you will be able to chose this playlist later.

As soon as you have chosen a playlist, you will be redirected to a google authentication page. You will have to log in with your google account and to accept the permissions. The program will then create a youtube playlist named __deezer\_to\_youtube__ and will add all the tracks of the chosen playlist to it. It adds the most relevant video found for each track.

## Note

Since the google api has a requests quota per day, the program will not work with too long playlists. If you have a playlist with more than 100 tracks, you can split it in two playlists and then add them to the same youtube playlist.
