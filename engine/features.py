import os
import re
from playsound import playsound 

import eel 
from engine.command import speak
from engine.config import ASSISTANT_NAME
import pywhatkit as kit

#playing assistant sound function
@eel.expose
def playAssistantSound():
        music_dir = "www\\assets\\audio\\start_sound.mp3"
        playsound(music_dir)


def openCommand(query):
        query = query.replace(ASSISTANT_NAME , "")
        query = query.replace("open","")
        query.lower()

        if query!="":
                speak("Opening" +query)
                os.system('start '+query)
        
        else:
                speak("not found")


def PlayYoutube(query):
        search_term = extract_yt_term(query)
        speak("Playing "+search_term+" on Youtube")
        kit.playonyt(search_term)


def extract_yt_term(command):
    pattern = r'play\s+(.*)\s+(?:on|in)\s+youtube'# Define a regular expression pattern to capture the song name
    match = re.search(pattern, command, re.IGNORECASE)       # Use re.search to find the match in the command
    return match.group(1) if match else None          # If a match is found, return the extracted song name; otherwise, return None
