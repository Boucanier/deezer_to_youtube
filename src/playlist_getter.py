import requests

def get_playlists(user_id : str) :

    title_list = []

    id_list = []

    url = "https://api.deezer.com/user/" + user_id + "/playlists"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        [title_list.append(playlist["title"]) for playlist in data["data"]]
        [id_list.append(playlist["id"]) for playlist in data["data"]]
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