import playlist_getter as pg
import os

if __name__ == "__main__" :

    if os.path.exists("data/user_id.txt"):
        with open("data/user_id.txt", "r") as fl :
            user_id = fl.readline()
    else :
        user_id = input("user id : ")

    list_title, list_id = pg.get_playlists(user_id)
    playlist_id = pg.deezer_menu(list_title, list_id)
    track_info = pg.get_track_info(playlist_id)

    print(len(track_info[0]))

    pg.to_csv(track_info)