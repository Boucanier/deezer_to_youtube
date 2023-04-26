import requests
import csv

def get_playlists(user_id : str) :

    title_list = []

    id_list = []

    url = "https://api.deezer.com/user/" + user_id + "/playlists"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        [title_list.append(playlist["title"]) for playlist in data["data"]]
        [id_list.append(str(playlist["id"])) for playlist in data["data"]]
    else:
        print('Error:', response.status_code, response.reason)
    
    return title_list, id_list


def deezer_menu(title_list, id_list):
    for i in range(len(title_list)) :
        print(i, title_list[i])
    
    choice = -1
    while choice not in range(len(id_list)) :
        choice = input("Choice : ")
        if choice.isdigit():
            choice = int(choice)
        else :
            choice = -1
    
    playlist_id = id_list[choice]
    
    return playlist_id


def get_track_info(playlist_id):
    url = "https://api.deezer.com/playlist/" + playlist_id + "/tracks"
    
    track_info = [],[],[],[]

    while url:
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            [track_info[0].append(track["title"]) for track in data["data"]]
            [track_info[1].append(track["artist"]["name"]) for track in data["data"]]
            [track_info[2].append(track["album"]["title"]) for track in data["data"]]
            [track_info[3].append(track["duration"]) for track in data["data"]]
            url = data.get('next')
        else:
            print('Error:', response.status_code, response.reason)
            break
    
    return track_info


def to_csv(track_info):
    with open('data/tracks.csv', 'w', newline='') as csvfile :
        writer = csv.writer(csvfile)
        for i in range(len(track_info[0])):
            writer.writerow([track_info[0][i], track_info[1][i], track_info[2][i], track_info[3][i]])