from youtube_search import YoutubeSearch
from youtube_title_parse import get_artist_title
from pytube import YouTube
import lyricsgenius
import sqlite3
import json
import os
import re

GENIUS_TOKEN = ""


def song_info(id):
    yt = YouTube(f"https://www.youtube.com/watch?v={id}")
    conn = sqlite3.connect('euphonydb.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM musicdata WHERE id=?", (id,))
    stuff = cur.fetchall()
    if stuff[0][3] is not None and stuff[0][4] is not None:
        title, artist = stuff[0][3], stuff[0][4]
        conn.close()
        return title, artist
    else:
        genius = lyricsgenius.Genius(GENIUS_TOKEN,
                                     verbose=False, timeout=10, retries=5)
        song = genius.search_song(yt.title)
        if song is None:
            artist, title = get_artist_title(yt.title)
            if genius.search_artist(artist, max_songs=1, get_full_info=False) is None:
                title, artist = get_artist_title(yt.title)
        else:
            artist, title = song.artist, song.title
        title += " " + artist.split(re.split("\(.*?\)", artist)[0])[1]
        artist = re.split("\(.*?\)", artist)[0]
        cur.execute("UPDATE musicdata SET title=?, artist=? WHERE id=?", (title, artist, id,))
        conn.commit()
        conn.close()
        return title, artist


def download(id=None, name=None):
    if name is not None:
        yturl = yturlget(name)
        ytid = ytidget(name)
        yt = YouTube(yturl)
        audio = yt.streams.filter(only_audio=True).first()
        out_file = audio.download(output_path=f"{os.path.join(os.getcwd(), 'music')}")
        new_file = f'{ytid}.mp3'
        os.rename(f"{os.path.join(os.path.join(os.getcwd(), 'music'), out_file)}",
                  f"{os.path.join(os.path.join(os.getcwd(), 'music'), new_file)}")

    elif id is not None:
        yturl = yturlget(id)
        yt = YouTube(yturl)
        audio = yt.streams.filter(only_audio=True).first()
        out_file = audio.download(output_path=f"{os.path.join(os.getcwd(), 'music')}")
        new_file = f'{id}.mp3'
        os.rename(f"{os.path.join(os.path.join(os.getcwd(), 'music'), out_file)}",
                  f"{os.path.join(os.path.join(os.getcwd(), 'music'), new_file)}")


def yturlget(id=None, name=None):
    if name is not None:
        yturl = f"https://www.youtube.com/watch?v={json.loads(YoutubeSearch(name, max_results=1).to_json())['videos'][0]['id']}"
        return yturl

    elif id is not None:
        yturl = f"https://www.youtube.com/watch?v={id}"
        return yturl


def ctbd(filename):
    with open(filename, 'rb') as file:
        blobdata = file.read()

    return blobdata


def wtf(name, data):
    with open(f"{os.path.join(os.path.join(os.getcwd(), 'music'), f'{name}.mp3')}", 'wb') as file:
        file.write(data)


def uploadtodb(id=None, name=None):
    if name is not None:
        conn = sqlite3.connect('euphonydb.db')
        cur = conn.cursor()
        yturl = yturlget(name)
        ytid = ytidget(name)
        url = f"/play?id={ytid}"
        file = ctbd(f"{os.path.join(os.path.join(os.getcwd(), 'music'), f'{ytid}.mp3')}")
        title, artist = song_info(ytid)
        cur.execute("INSERT INTO musicdata (id, url, yturl, title, artist, file) VALUES (?, ?, ?, ?, ?, ?)",
                    (ytid, url, yturl, title, artist, file,))
        conn.commit()
        conn.close()

    elif id is not None:
        conn = sqlite3.connect('euphonydb.db')
        cur = conn.cursor()
        yturl = yturlget(id)
        url = f"/play?id={id}"
        file = ctbd(f"{os.path.join(os.path.join(os.getcwd(), 'music'), f'{id}.mp3')}")
        title, artist = song_info(id)
        cur.execute("INSERT INTO musicdata (id, url, yturl, title, artist, file) VALUES (?, ?, ?, ?, ?, ?)",
                    (id, url, yturl, title, artist, file,))
        conn.commit()
        conn.close()


def getfromdb(id=None, name=None):
    if name is not None:
        conn = sqlite3.connect('euphonydb.db')
        cur = conn.cursor()
        ytid = ytidget(name)
        cur.execute("SELECT * FROM musicdata WHERE id=?", (ytid,))
        stuff = cur.fetchall()
        for row in stuff:
            wtf(ytid, row[5])
        conn.close()

    elif id is not None:
        conn = sqlite3.connect('euphonydb.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM musicdata WHERE id=?", (id,))
        stuff = cur.fetchall()
        for row in stuff:
            wtf(id, row[5])
        conn.close()


def ytidget(name, i=1, j=0):
    ytid = json.loads(YoutubeSearch(name, max_results=i).to_json())["videos"][j]["id"]
    return ytid


def ytsearch(name):
    all = json.loads(YoutubeSearch(name, max_results=25).to_json())["videos"]
    info = []
    for i in range(0, len(all)):
        info.append([all[i]["id"], all[i]["title"]])

    return info
