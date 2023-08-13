import os
import shutil
import sqlite3
import sys
import threading
import time
from zipfile import ZipFile

import pyautogui
import requests
from prettytable import PrettyTable
from pynput import keyboard
from pypresence import Presence

import euphony

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from pygame import mixer


def search(name):
    info = euphony.ytsearch(name)
    return info


def table_formatter(type, info):
    if type == "s":
        table = [['Serial Number', 'YTID', 'Title']]
        if len(info) != 0:
            for i in range(0, len(info)):
                table.append([i + 1, info[i][0], info[i][1]])
        tab = PrettyTable(table[0])
        if len(info) != 0:
            tab.add_rows(table[1:])
        tab.add_rows([['0', 'Return', 'Return To Menu']])
        return tab
    elif type == "p":
        table = [['Serial Number', 'Name']]
        if len(info) != 0:
            for i in range(0, len(info)):
                table.append([i + 4, info[i][1]])
        tab = PrettyTable(table[0])
        if len(info) != 0:
            tab.add_rows(table[1:])
        tab.add_rows([['1', 'Make New Playlist']])
        tab.add_rows([['2', 'Edit A Playlist']])
        tab.add_rows([['3', 'Delete A Playlist']])
        tab.add_rows([['0', 'Return To Menu']])
        return tab
    elif type == "pc":
        table = [['Serial Number', 'YTID', 'Title']]
        for i in range(0, len(info)):
            for j in range(len(info[i][2].split(", "))):
                table.append(
                    [len(table), info[i][2].split(", ")[j], f"{euphony.song_info(info[i][2].split(', ')[j])[0]}"
                                                            f" by {euphony.song_info(info[i][2].split(', ')[j])[1]}"])
        tab = PrettyTable(table[0])
        tab.add_rows(table[1:])
        tab.add_rows([['0', 'Return', 'Return To Menu']])
        return tab


def play(id):
    global event
    if event is not None:
        event.set()
    check1 = os.listdir(os.path.join(os.getcwd(), 'music'))
    if f"{id}.wav" not in check1:
        conn = sqlite3.connect('euphonydb.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM musicdata WHERE id=?", (id,))
        check2 = cur.fetchall()
        conn.close()
        if len(check2) != 0:
            euphony.getfromdb(id)
            song = f"{os.path.join(os.path.join(os.getcwd(), 'music'), f'{id}.wav')}"
            os.system(
                f"ffmpeg.exe -y -loglevel quiet -i {os.path.join(os.path.join(os.getcwd(), 'music'), f'{id}.mp3')} "
                f"{os.path.join(os.path.join(os.getcwd(), 'music'), f'{id}.wav')}")
            os.remove(f"music/{id}.mp3")
            mixer.music.load(song)
            mixer.music.play()
            title, artist = euphony.song_info(id)
            event = threading.Event()
            th1 = threading.Thread(target=rpc, args=(title, artist, event))
            th1.daemon = True
            th1.start()

        elif len(check2) == 0:
            euphony.download(id)
            euphony.uploadtodb(id)
            song = f"{os.path.join(os.path.join(os.getcwd(), 'music'), f'{id}.wav')}"
            os.system(
                f"ffmpeg.exe -y -loglevel quiet -i {os.path.join(os.path.join(os.getcwd(), 'music'), f'{id}.mp3')} "
                f"{os.path.join(os.path.join(os.getcwd(), 'music'), f'{id}.wav')}")
            os.remove(f"music/{id}.mp3")
            mixer.music.load(song)
            mixer.music.play()
            title, artist = euphony.song_info(id)
            event = threading.Event()
            th1 = threading.Thread(target=rpc, args=(title, artist, event))
            th1.daemon = True
            th1.start()

    elif f"{id}.wav" in check1:
        conn = sqlite3.connect('euphonydb.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM musicdata WHERE id=?", (id,))
        check2 = cur.fetchall()
        if len(check2) != 0:
            song = f"{os.path.join(os.path.join(os.getcwd(), 'music'), f'{id}.wav')}"
            mixer.music.load(song)
            mixer.music.play()
            title, artist = euphony.song_info(id)
            event = threading.Event()
            th1 = threading.Thread(target=rpc, args=(title, artist, event))
            th1.daemon = True
            th1.start()

        elif len(check2) == 0:
            euphony.uploadtodb(id)
            song = f"{os.path.join(os.path.join(os.getcwd(), 'music'), f'{id}.wav')}"
            os.system(
                f"ffmpeg.exe -y -loglevel quiet -i {os.path.join(os.path.join(os.getcwd(), 'music'), f'{id}.mp3')} "
                f"{os.path.join(os.path.join(os.getcwd(), 'music'), f'{id}.wav')}")
            os.remove(f"music/{id}.mp3")
            mixer.music.load(song)
            mixer.music.play()
            title, artist = euphony.song_info(id)
            event = threading.Event()
            th1 = threading.Thread(target=rpc, args=(title, artist, event))
            th1.daemon = True
            th1.start()


def playlist():
    while True:
        conn = sqlite3.connect('euphonydb.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM playlists")
        check = cur.fetchall()
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
        table = table_formatter("p", check)
        print(table)
        choice1 = int(input("Option :> "))
        if ((len(check)) + 4) >= choice1 > 3:
            print("Please wait while we load your playlist.....")
            while True:
                plist = [check[choice1 - 4]]
                table = table_formatter("pc", plist)
                if os.name == 'nt':
                    os.system('cls')
                else:
                    os.system('clear')
                print(table)
                choice2 = int(input("Option :> "))
                if len(check[choice1 - 4][2].split(", ")) >= choice2 > 0:
                    play(check[choice1 - 4][2].split(", ")[choice2 - 1])
                elif choice2 == 0:
                    conn.close()
                    break
        elif choice1 == 1:
            while True:
                name = input("Enter name of new playlist (0 to return):> ")
                if name == '0':
                    conn.close()
                    break
                muids = input(
                    "Enter list of comma-separated youtube ids (like this dQw4w9WgXcQ, rTga41r3a4s, aSk9ZyY5Ww0) (0 "
                    "to return) :> ")
                if muids == '0':
                    conn.close()
                    break
                cur.execute("INSERT INTO playlists VALUES (?, ?, ?)", (None, name, muids,))
                conn.commit()
        elif choice1 == 2:
            while True:
                name = input("Enter name of playlist to edit (0 to return) :> ")
                if name == '0':
                    conn.close()
                    break
                cur.execute("SELECT * FROM playlists WHERE name=?", (name,))
                choice2 = cur.fetchall()
                if len(choice2) != 0:
                    table = table_formatter("pc", choice2)
                    print(table)
                    choice3 = int(input("Option :> "))
                    if len(choice2) >= choice3 > 0:
                        choice2.pop(choice3 - 1)
                        cur.execute("UPDATE playlists SET muids=? WHERE name=?", (choice2, name,))
                        conn.commit()
                    elif choice3 == 0:
                        conn.close()
                        break
                elif len(choice2) == 0:
                    print("Invalid playlist name")
        elif choice1 == 3:
            while True:
                name = input("Enter name of playlist to delete (0 to return) :> ")
                if name == '0':
                    conn.close()
                    break
                cur.execute("SELECT * FROM playlists WHERE name=?", (name,))
                choice2 = cur.fetchall()
                if len(choice2) != 0:
                    cur.execute("DELETE FROM playlists WHERE name=?", (name,))
                    conn.commit()
                    break
                elif len(choice2) == 0:
                    print("Invalid playlist name")
        elif choice1 == 0:
            conn.close()
            break


def rpc(title, artist, event):
    client_id = "1073202968096149504"
    RPC = Presence(client_id)
    RPC.connect()
    while True:
        RPC.update(
            large_image="euphony-logo-discord",
            large_text="Euphony",
            details=title,
            state=f"by {artist}",
            buttons=[
                {"label": "Euphony Developer", "url": "https://github.com/SGtOriginal"},
                {"label": "Euphony Repository", "url": "https://github.com/SGtOriginal/Euphony-Client"}
            ],
        )
        time.sleep(10)
        if event.is_set():
            break
    RPC.close()
    event = None


def on_press(key):
    if key == keyboard.Key.media_play_pause:
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
    elif key == keyboard.Key.media_next:
        pygame.mixer.music.stop()
    elif key == keyboard.Key.media_previous:
        pygame.mixer.music.rewind()
    elif key == keyboard.Key.media_volume_up:
        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.1)
    elif key == keyboard.Key.media_volume_down:
        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.1)
    elif key == keyboard.Key.media_volume_mute:
        pygame.mixer.music.set_volume(0)
    elif key == keyboard.Key.esc:
        if pyautogui.getActiveWindow().title == "Euphony":
            print("\nStopping music.....")
            mixer.stop()
            mixer.music.unload()
            mixer.quit()
            print("Cleaning up music files.....")
            shutil.rmtree("music")
            os.mkdir("music")
            print("Stopping RPC.....")
            global event
            if event is not None:
                event.set()
            print("Quitting. G bye.....")
            os._exit(0)
        else:
            pass


def initializer():
    if os.path.exists("music"):
        pass
    else:
        os.mkdir("music")

    conn = sqlite3.connect("euphonydb.db")
    cur = conn.cursor()
    cur.executescript('''
        CREATE TABLE IF NOT EXISTS "musicdata" (
            "id"	TEXT NOT NULL,
            "url"	TEXT NOT NULL,
            "yturl"	TEXT NOT NULL,
            "title"	TEXT NOT NULL,
            "artist"	TEXT NOT NULL,
            "file"	BLOB NOT NULL
        )
    ''')
    conn.commit()
    cur.executescript('''
        CREATE TABLE IF NOT EXISTS "playlists" (
            "id"	INTEGER NOT NULL,
            "name"	TEXT NOT NULL UNIQUE,
            "muids"	TEXT,
            PRIMARY KEY("id" AUTOINCREMENT)
        )
    ''')
    conn.commit()

    if os.path.exists("ffmpeg.exe"):
        print("Ffmpeg exists, OK.....")
    else:
        print("Ffmpeg not found, downloading latest version.....")
        response = requests.get(
            "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip")
        open("ffmpeg-master-latest-win64-gpl.zip", "wb").write(response.content)
        with ZipFile("ffmpeg-master-latest-win64-gpl.zip", 'r') as zip:
            zip.extract("ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe")
        os.remove("ffmpeg-master-latest-win64-gpl.zip")
        shutil.move("ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe", "ffmpeg.exe")
        shutil.rmtree("ffmpeg-master-latest-win64-gpl")
        print("Ffmpeg downloaded and extracted. All OK.....")
    conn.close()


def main():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system("clear")

    os.system("title Euphony")

    print("""-----------------------------------------------------------------------------------
#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#
-----------------------------------------------------------------------------------
   ▄████████ ███    █▄     ▄███████▄    ▄█    █▄     ▄██████▄  ███▄▄▄▄   ▄██   ▄   
  ███    ███ ███    ███   ███    ███   ███    ███   ███    ███ ███▀▀▀██▄ ███   ██▄ 
  ███    █▀  ███    ███   ███    ███   ███    ███   ███    ███ ███   ███ ███▄▄▄███ 
 ▄███▄▄▄     ███    ███   ███    ███  ▄███▄▄▄▄███▄▄ ███    ███ ███   ███ ▀▀▀▀▀▀███ 
▀▀███▀▀▀     ███    ███ ▀█████████▀  ▀▀███▀▀▀▀███▀  ███    ███ ███   ███ ▄██   ███ 
  ███    █▄  ███    ███   ███          ███    ███   ███    ███ ███   ███ ███   ███ 
  ███    ███ ███    ███   ███          ███    ███   ███    ███ ███   ███ ███   ███ 
  ██████████ ████████▀   ▄████▀        ███    █▀     ▀██████▀   ▀█   █▀   ▀█████▀
-----------------------------------------------------------------------------------
X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X
-----------------------------------------------------------------------------------
""")

    print(f"""[1] Search with song name
[2] Play existing YouTube song
[3] View your playlists

[0] Quit
""")

    main_choice = int(input("Enter your choice :> "))
    if main_choice == 1:
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system("clear")

        while True:
            name = input("Enter song name (0 to return) :> ")
            if name == "0":
                break
            else:
                info = search(name)
                print(table_formatter("s", info))
                num = int(input("Enter serial number of song you want to listen to :> "))
                if 0 < num <= len(info):
                    mixer.stop()
                    play(info[num - 1][0])
                elif num == 0:
                    break

    elif main_choice == 2:
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system("clear")

        while True:
            link = input(
                "Enter YouTube link or id \n(something like https://www.youtube.com/watch?v=dQw4w9WgXcQ or "
                "dQw4w9WgXcQ) \n(0 to return) :> ")
            if link == "0":
                break
            else:
                if "https://www.youtube.com/watch?v=" in link:
                    id = ''.join(link.split("https://www.youtube.com/watch?v="))
                else:
                    id = link
                mixer.stop()
                play(id)

    elif main_choice == 3:
        playlist()

    elif main_choice == 0:
        init.join()
        print("Stopping music.....")
        mixer.stop()
        mixer.music.unload()
        mixer.quit()
        print("Cleaning up music files.....")
        shutil.rmtree("music")
        os.mkdir("music")
        print("Stopping RPC..... (takes upto 10 seconds)")
        global event
        if event is not None:
            event.set()
        sys.exit("Quitting. G bye.....")


mixer.init()

if os.name == 'nt':
    os.system('cls')
else:
    os.system("clear")

init = threading.Thread(target=initializer)
init.daemon = True
init.start()
init.join()

time.sleep(1.5)

event = None

listener = keyboard.Listener(on_press=on_press)
listener.start()

while True:
    main()
