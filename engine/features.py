import os
import re
import webbrowser
from playsound import playsound
import sqlite3
import eel
from engine.command import speak
from engine.config import ASSISTANT_NAME
import pywhatkit as kit

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

# Extract the YouTube search term from command
def extract_yt_term(command):
    pattern = r'play\s+(.*?)(?:\s+(?:on|in)\s+youtube)?$'
    match = re.search(pattern, command, re.IGNORECASE)
    return match.group(1).strip() if match else None
