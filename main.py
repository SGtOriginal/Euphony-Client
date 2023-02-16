"""
Euphony Client, for playing music from YouTube and other sources right from your desktop.
Copyright (C) 2023  SGtOriginal

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Contact SGtOriginal using the this email: sgtoriginal@gmail.com
"""


import time
import threading
import requests
from prettytable import PrettyTable
from zipfile import ZipFile
import os
import shutil
import win32con
import win32gui

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import sqlite3
import euphony
from pygame import mixer
import sys
import subprocess

def search(name):
    info = euphony.ytsearch(name)
    return info

def table_formatter(info):
    table = [['Serial Number', 'YTID', 'Title']]
    for i in range(0, len(info)):
        table.append([i+1, info[i][0], info[i][1]])
    tab = PrettyTable(table[0])
    tab.add_rows(table[1:])
    return tab

def play(id):
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
            os.system(f"ffmpeg.exe -y -loglevel quiet -i {os.path.join(os.path.join(os.getcwd(), 'music'), f'{id}.mp3')} {os.path.join(os.path.join(os.getcwd(), 'music'), f'{id}.wav')}")
            os.remove(f"music/{id}.mp3")
            mixer.music.load(song)
            mixer.music.play()
        
        elif len(check2) == 0:
            euphony.download(id)
            euphony.uploadtodb(id)
            song = f"{os.path.join(os.path.join(os.getcwd(), 'music'), f'{id}.wav')}"
            os.system(f"ffmpeg.exe -y -loglevel quiet -i {os.path.join(os.path.join(os.getcwd(), 'music'), f'{id}.mp3')} {os.path.join(os.path.join(os.getcwd(), 'music'), f'{id}.wav')}")
            os.remove(f"music/{id}.mp3")
            mixer.music.load(song)
            mixer.music.play()
    
    elif f"{id}.wav" in check1:
        conn = sqlite3.connect('euphonydb.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM musicdata WHERE id=?", (id,))
        check2 = cur.fetchall()
        if len(check2) != 0:
            song = f"{os.path.join(os.path.join(os.getcwd(), 'music'), f'{id}.wav')}"
            mixer.music.load(song)
            mixer.music.play()
        
        elif len(check2) == 0:
            euphony.uploadtodb(id)
            song = f"{os.path.join(os.path.join(os.getcwd(), 'music'), f'{id}.wav')}"
            os.system(f"ffmpeg.exe -y -loglevel quiet -i {os.path.join(os.path.join(os.getcwd(), 'music'), f'{id}.mp3')} {os.path.join(os.path.join(os.getcwd(), 'music'), f'{id}.wav')}")
            os.remove(f"music/{id}.mp3")
            mixer.music.load(song)
            mixer.music.play()

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
            "file"	BLOB NOT NULL
        )
    ''')
    conn.commit()

    if os.name == "nt":
        if os.path.exists("ffmpeg.exe"):
            print("Ffmpeg exists, OK.....")
        else:
            print("Ffmpeg not found, downloading latest version.....")
            response = requests.get("https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip")
            open("ffmpeg-master-latest-win64-gpl.zip", "wb").write(response.content)
            with ZipFile("ffmpeg-master-latest-win64-gpl.zip", 'r') as zip:
                zip.extract("ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe")
            os.remove("ffmpeg-master-latest-win64-gpl.zip")
            shutil.move("ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe", "ffmpeg.exe")
            shutil.rmtree("ffmpeg-master-latest-win64-gpl")
            print("Ffmpeg downloaded and extracted. All OK.....")
    else:
        check = subprocess.Popen(["test"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
        if len(check[0]) > 0:
            print("Ffmpeg exists, OK.....)
        else:
            print("Ffmpeg not found. Audio will not work without ffmpeg. See 'https://github.com/SGtOriginal/Euphony-Client/blob/main/README.md'.")

def main():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system("clear")

    print("""
Euphony Client  Copyright (C) 2023  SGtOriginal
This program comes with ABSOLUTELY NO WARRANTY; for details go to "https://github.com/SGtOriginal/Euphony-Client/blob/main/LICENSE".
This is free software, and you are welcome to redistribute it
under certain conditions; go to "https://github.com/SGtOriginal/Euphony-Client/blob/main/LICENSE" for details.
    """)
    
    print("""
-----------------------------------------------------------------------------------
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
    
    init = threading.Thread(target=initializer)
    init.daemon = True
    init.start()
    init.join()
    
    print("""
    [1] Search with song name
    [2] Play existing YouTube song
    [3] View your playlists (Not implemented yet)
    
    [0] Quit\n
    """)
    main_choice = int(input("Option :> "))
    if main_choice == 1:
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system("clear")
        
        name = input("Enter song name: ")
        info = search(name)
        print(table_formatter(info))
        num = int(input("Enter serial number of song you want to listen to :> "))
        if num > 0 and num <= len(info):
            num -= 1
            mixer.stop()
            play(info[num][0])
    
    elif main_choice == 2:
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system("clear")
        
        link = input("Enter YouTube link (something like https://www.youtube.com/watch?v=dQw4w9WgXcQ): ")
        id = ''.join(link.split("https://www.youtube.com/watch?v="))
        mixer.stop()
        play(id)
    
    elif main_choice == 3:
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system("clear")
    
    elif main_choice == 0:
        init.join()
        print("Stopping music.....")
        mixer.stop()
        mixer.music.unload()
        mixer.quit()
        print("Cleaning up music files.....")
        shutil.rmtree("music")
        os.mkdir("music")
        sys.exit("Quitting. G bye.....")

mixer.init()

while True:
    hwnd = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
    time.sleep(0.5)
    main()