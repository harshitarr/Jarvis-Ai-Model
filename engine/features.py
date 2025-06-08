import os
import struct
import subprocess
import time
import webbrowser
import sqlite3
import eel
import pvporcupine
import pyaudio
import pyautogui
import pywhatkit as kit
import urllib.parse
from playsound import playsound

from engine.command import speak
from engine.config import ASSISTANT_NAME
from engine.helper import extract_spotify_term, extract_yt_term, remove_words,GoogleSearch

# Connect to SQLite database
con = sqlite3.connect("jarvis.db")
cursor = con.cursor()

# Play assistant startup sound
@eel.expose
def playAssistantSound():
    music_dir = "www\\assets\\audio\\start_sound.mp3"
    playsound(music_dir)

# Handle open commands

def openCommand(query):
    query = query.lower().replace(ASSISTANT_NAME.lower(), "").replace("open", "").strip()
    if query == "":
        speak("Please specify what to open.")
        return

    try:
        cursor.execute('SELECT path FROM sys_command WHERE name = ?', (query,))
        results = cursor.fetchall()
        if results:
            speak(f"Opening {query}")
            os.startfile(results[0][0])
            return

        cursor.execute('SELECT path FROM web_command WHERE name = ?', (query,))
        results = cursor.fetchall()
        if results:
            speak(f"Opening {query}")
            webbrowser.open(results[0][0])
            return

        speak(f"Trying to open {query}")
        os.system(f'start {query}')
    except Exception as e:
        speak("Something went wrong.")
        print(f"Error: {e}")

# YouTube Playback

def PlayYoutube(query):
    search_term = extract_yt_term(query)
    if search_term:
        speak(f"Playing {search_term} on YouTube")
        kit.playonyt(search_term)
    else:
        speak("Sorry, I couldn't understand what to play on YouTube.")

# Spotify Web Playback

def PlaySpotify(query):
    search_term = extract_spotify_term(query)
    if search_term:
        speak(f"Playing {search_term} on Spotify")
        encoded = urllib.parse.quote(search_term)
        webbrowser.open(f"https://open.spotify.com/search/{encoded}")
    else:
        speak("Sorry, I couldn't understand what to play on Spotify.")

# Wake word detection

def hotword():
    porcupine = None
    paud = None
    audio_stream = None
    try:
        porcupine = pvporcupine.create(keywords=["jarvis", "alexa"])
        paud = pyaudio.PyAudio()
        audio_stream = paud.open(rate=porcupine.sample_rate, channels=1,
                                 format=pyaudio.paInt16, input=True,
                                 frames_per_buffer=porcupine.frame_length)

        while True:
            keyword = audio_stream.read(porcupine.frame_length)
            keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)
            keyword_index = porcupine.process(keyword)
            if keyword_index >= 0:
                print("hotword detected")
                pyautogui.keyDown("win")
                pyautogui.press("j")
                time.sleep(2)
                pyautogui.keyUp("win")
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()

# Lookup contact

def findContact(query):
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'whatsapp', 'video']
    query = remove_words(query, words_to_remove).strip().lower()

    try:
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", 
                       ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        if not results:
            raise Exception("Contact not found")

        mobile_number_str = str(results[0][0])
        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('Not found in contacts.')
        return 0, 0

# Send WhatsApp message/call

def whatsApp(mobile_no, message, flag, name):
    if flag == 'message':
        target_tab = 13
        jarvis_message = "Message sent successfully to " + name

        encoded_message = urllib.parse.quote(message)
        whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"
        full_command = f'start "" "{whatsapp_url}"'

        subprocess.run(full_command, shell=True)
        time.sleep(5)
        pyautogui.hotkey('ctrl', 'f')
        for _ in range(1, target_tab):
            pyautogui.hotkey('tab')
        pyautogui.hotkey('enter')
        speak(jarvis_message)

    elif flag == 'call':
        # Open WhatsApp Web chat — user manually starts voice call
        target_tab = 7
        jarvis_message = "Starting Phone call with " + name

        encoded_message = urllib.parse.quote(message)
        whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"
        full_command = f'start "" "{whatsapp_url}"'

        subprocess.run(full_command, shell=True)
        time.sleep(5)
        pyautogui.hotkey('ctrl', 'f')
        for _ in range(1, target_tab):
            pyautogui.hotkey('tab')
        pyautogui.hotkey('enter')
        speak(jarvis_message)

    else:  # video call
        target_tab = 6
        jarvis_message = "Starting video call with " + name

        encoded_message = urllib.parse.quote(message)
        whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"
        full_command = f'start "" "{whatsapp_url}"'

        subprocess.run(full_command, shell=True)
        time.sleep(5)
        pyautogui.hotkey('ctrl', 'f')
        for _ in range(1, target_tab):
            pyautogui.hotkey('tab')
        pyautogui.hotkey('enter')
        speak(jarvis_message)

# Direct calling functions

def makeCall(name):
    mobile_no, contact_name = findContact(name)
    if mobile_no:
        whatsApp(mobile_no, message="", flag="call", name=contact_name)

def makeVideoCall(name):
    mobile_no, contact_name = findContact(name)
    if mobile_no:
        whatsApp(mobile_no, message="", flag="video", name=contact_name)

def sendMessage(name, message):
    mobile_no, contact_name = findContact(name)
    if mobile_no:
        whatsApp(mobile_no, message=message, flag="message", name=contact_name)
