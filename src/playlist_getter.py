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
        print(title_list)
        print(id_list)
    else:
        print('Error:', response.status_code, response.reason)
    
    return title_list, id_list