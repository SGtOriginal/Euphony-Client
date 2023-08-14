# Euphony Client

READ LICENSE FIRST BEFORE ANYTHING ELSE

Euphony Client is a part of the bigger program called Euphony which aims to provide music right at your desktop without any pesky ads or loss of sound quality. All it requires is internet for downloading songs (depends on if you have listened to the song before using Euphony Client and if the database remains intact).

# Features
* Easy setup without any account system (and hence no backup system in place).
* Privacy based (We never have and never will collect any information on you. YouTube and pther sources may log your ip when the music is being downloaded but that can be solved with a good proxy/vpn/tor)
* Open source (so people can always improve the project)
* YouTube support (more yet to come)
* FREE (Most important point :) )

# Some (Probably) Important Info
Euphony Server is not required for this. It just has a very basic TUI (Terminal User Interface) with self-explaining buttons. For personal use, Euphony Client is recommended. For public use, like in your community, then this is good enough for you.

# How To Use
## I assume that you have Python 3 ##
If you don't have Python 3, then follow these steps:

* If you are using Windows, then download it from https://www.python.org/downloads/release/python-31010/ (and run it of course)
* If you are using Linux, then do 'apt-get install python3 python3-pip'
* If you are using Mac, then download it https://www.python.org/downloads/release/python-31010/ (and run it of course)

## I also assume that you have ffmpeg ##
If you don't have ffmpeg, then follow these steps:

* If you are using Windows, then Euphony automatically downloads it for you.
* If you are using Linux or Mac, go to https://www.hostinger.com/tutorials/how-to-install-ffmpeg/ (They write a better method of ffmpeg installation than me.)

### Steps ###

1. Click on the green `<> Code` button.
2. Click `Download zip`.
3. Extract the downloaded zip.
4. Open a terminal in the extracted folder.
5. Run `pip install -r requirements.txt`
6. Wait for the previous command to finish.
7. Make a Genius.com account and put your token in euphony.py (needed for Discord Rich Presence)
8. Run `python main.py`. If that does not work, run `python3 main.py`

# Credits #
* SGtOriginal (that's me! :> ) for doing the ENTIRE code.
* ShadowLp174 for ideas and code improvement suggestions.
* Blaze for asking me to make him a free alternative to Spotify and also for not making a website even though he's a good developer and literally does nothing the entire day
