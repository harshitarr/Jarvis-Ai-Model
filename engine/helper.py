# Extract YouTube search term
import re
import webbrowser

import urllib

from engine.command import speak


def extract_yt_term(command):
    pattern = r'play\s+(.*?)(?:\s+(?:on|in)\s+youtube)?$'
    match = re.search(pattern, command, re.IGNORECASE)
    return match.group(1).strip() if match else None

# Extract Spotify search term
def extract_spotify_term(command):
    pattern = r'play\s+(.*?)(?:\s+(?:on|in)\s+spotify)?$'
    match = re.search(pattern, command, re.IGNORECASE)
    return match.group(1).strip() if match else None

# Perform a Google search
def GoogleSearch(query):
    pattern = r'search\s+(.*?)(?:\s+on\s+google)?$'
    match = re.search(pattern, query, re.IGNORECASE)
    if match:
        search_term = match.group(1).strip()
        if search_term:
            speak(f"Searching for {search_term} on Google")
            encoded = urllib.parse.quote(search_term)
            webbrowser.open(f"https://www.google.com/search?q={encoded}")
        else:
            speak("Sorry, I couldn't understand what to search on Google.")
    else:
        speak("Sorry, I couldn't understand the search query.")


def remove_words(input_string, words_to_remove):
    # Split the input string into words
    words = input_string.split()

    # Remove unwanted words
    filtered_words = [word for word in words if word.lower() not in words_to_remove]

    # Join the remaining words back into a string
    result_string = ' '.join(filtered_words)

    return result_string


