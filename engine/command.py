import pyttsx3
import speech_recognition as sr
import eel
import time

# Text-to-Speech Function
def speak(text):
    engine = pyttsx3.init('sapi5') 
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # 0 = male, 1 = female
    engine.setProperty('rate', 150)  # Speech rate
    eel.DisplayMessage(text)
    engine.say(text)
    engine.runAndWait()

# Speech Recognition Function
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        eel.DisplayMessage('Listening...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)

        try:
            audio = r.listen(source, timeout=10, phrase_time_limit=50)
        except sr.WaitTimeoutError:
            print("Timeout: No speech detected.")
            eel.DisplayMessage("Timeout: No speech detected. Please try again.")
            eel.ShowHood()
            return ""

    try:
        print('Recognizing...')
        eel.DisplayMessage('Recognizing...')
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)
        return query.lower()

    except sr.UnknownValueError:
        print("Sorry, I could not understand your voice.")
        eel.DisplayMessage("Sorry, I could not understand your voice.")
        eel.ShowHood()
        return ""

    except sr.RequestError:
        print("Speech recognition service is unavailable.")
        eel.DisplayMessage("Speech recognition service is unavailable.")
        eel.ShowHood()
        return ""

    except Exception as e:
        print(f"Unexpected error: {e}")
        eel.DisplayMessage("An unexpected error occurred.")
        eel.ShowHood()
        return ""

@eel.expose
def allCommands(message=1):

    if message == 1:
        query = takecommand()
        print(query)
    else:
        query = message

    try:
        if "open" in query:
            from engine.features import openCommand
            openCommand(query)

        elif "on youtube" in query or "in youtube" in query:
            try:
                from engine.features import PlayYoutube
                PlayYoutube(query)
            except Exception as e:
                print(f"Error in PlayYoutube: {e}")
                eel.ShowHood()
                return

        elif "on spotify" in query or "in spotify" in query:
            try:
                from engine.features import PlaySpotify
                PlaySpotify(query)
            except Exception as e:
                print(f"Error in PlaySpotify: {e}")
                eel.ShowHood()
                return

        elif "search" in query and "on google" in query:
            try:
                from engine.features import GoogleSearch
                GoogleSearch(query)
            except Exception as e:
                print(f"Error in GoogleSearch: {e}")
                eel.ShowHood()
                return

        elif "send message" in query or "phone call" in query or "video call" in query:
            try:
                from engine.features import findContact, whatsApp
                contact_no, name = findContact(query)
                if contact_no != 0:
                    # Directly use WhatsApp without asking
                    message_type = ""
                    message_content = ""

                    if "send message" in query:
                        message_type = 'message'
                        speak("What message to send?")
                        message_content = takecommand()
                    elif "phone call" in query:
                        message_type = 'call'
                    else:
                        message_type = 'video call'

                    whatsApp(contact_no, message_content, message_type, name)

            except Exception as e:
                print(f"Error handling WhatsApp message/call: {e}")
                eel.DisplayMessage("Error while using WhatsApp.")
                eel.ShowHood()
                return

        else:
            print("Not Run")

    except Exception as e:
        print(f"Error in allCommands: {e}")
        eel.ShowHood()

    eel.ShowHood()
