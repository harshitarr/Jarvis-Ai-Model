import os
import re
import struct
import time
import webbrowser
from playsound import playsound
import sqlite3
import eel
import pvporcupine
import pyaudio
from engine.command import speak
from engine.config import ASSISTANT_NAME
import pywhatkit as kit
import urllib.parse

from engine.helper import extract_spotify_term, extract_yt_term,GoogleSearch

# Connect to SQLite database
con = sqlite3.connect("jarvis.db")
cursor = con.cursor()

# Play assistant startup sound
@eel.expose
def playAssistantSound():
    music_dir = "www\\assets\\audio\\start_sound.mp3"
    playsound(music_dir)

# Handle open commands for apps or websites
def openCommand(query):
    query = query.lower()
    query = query.replace(ASSISTANT_NAME.lower(), "")
    query = query.replace("open", "").strip()

    if query == "":
        speak("Please specify what to open.")
        return

    try:
        # Try opening a system command
        cursor.execute('SELECT path FROM sys_command WHERE name = ?', (query,))
        results = cursor.fetchall()

        if results:
            speak(f"Opening {query}")
            os.startfile(results[0][0])
            return

        # Try opening a web command
        cursor.execute('SELECT path FROM web_command WHERE name = ?', (query,))
        results = cursor.fetchall()

        if results:
            speak(f"Opening {query}")
            webbrowser.open(results[0][0])
            return

        # Try to open using the system default method
        speak(f"Trying to open {query}")
        try:
            os.system(f'start {query}')
        except Exception as e:
            speak("Unable to open. Not found.")
    except Exception as e:
        speak("Something went wrong.")
        print(f"Error: {e}")

# Play a song on YouTube
def PlayYoutube(query):
    search_term = extract_yt_term(query)
    if search_term:
        speak(f"Playing {search_term} on YouTube")
        kit.playonyt(search_term)
    else:
        speak("Sorry, I couldn't understand what to play on YouTube.")

# Play a song on Spotify (Web)
def PlaySpotify(query):
    search_term = extract_spotify_term(query)
    if search_term:
        speak(f"Playing {search_term} on Spotify")
        encoded = urllib.parse.quote(search_term)
        webbrowser.open(f"https://open.spotify.com/search/{encoded}")
    else:
        speak("Sorry, I couldn't understand what to play on Spotify.")


def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
       
        # pre trained keywords    
        porcupine=pvporcupine.create(keywords=["jarvis","alexa"]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")

                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
                
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()