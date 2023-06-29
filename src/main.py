import playlist_getter as pg
import os
import youtube_control

if __name__ == "__main__" :

    choice = 0
    print("1 - New user id")
    print("2 - Existing user")

    while choice not in (1, 2) :
        choice = input("Choice : ")
        if choice.isdigit():
            choice = int(choice)
        else :
            choice = 0
        if choice == 1 :
            user_id = input("user id : ")
        elif choice == 2 :
            if os.path.exists("data/user_id.txt"):
                with open("data/user_id.txt", "r") as fl :
                    user_id = fl.readline()
            else :
                print("No existing user\n")
                choice = 0

    choice = 0
    print("1 - New playlist")
    print("2 - Existing playlist")

    while choice not in (1, 2) :
        choice = input("Choice : ")
        if choice.isdigit():
            choice = int(choice)
        else :
            choice = 0

        if choice == 1 :
            list_title, list_id = pg.get_playlists(user_id)
            playlist_id, playlist_name = pg.deezer_menu(list_title, list_id)
            track_info = pg.get_track_info(playlist_id)
            print(len(track_info[0]), "tracks")
            pg.to_csv(track_info, playlist_name)
        elif choice == 2 :
            if os.path.exists("data/tracks.csv"):
                print("Playlist found")
            else :
                print("No existing playlist")
                print("Playlist must be saved in a csv file in tracks")
                print("csv separator mst be \',\'")
                print("csv format is : TITLE, ARTIST, ALBUM, DURATION (in s.)\n")
                choice = 0
    
        youtube_control.main()