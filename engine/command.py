import pyttsx3
import speech_recognition as sr

def speak(text):
    engine = pyttsx3.init('sapi5') 
    voices = engine.getProperty('voices')
    engine.setProperty('voice',voices[0].id)
    engine.setProperty('rate',150)  # the rate at which he talks
    print(voices)
    engine.say(text)
    engine.runAndWait()  #pauses and speaks

def takecommand():

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)

        audio = r.listen(source , 10 , 50)  # it waits for 10 sec before talking , it limits only for 50 seconds after when the user starts speaking

    try:
        print('Recognizing...')
        query = r.recognize_google(audio,language='en-in')
        print(f"user said: {query}")
    except Exception as e:
        return ""
    
    return query.lower()

text = takecommand()



speak(text) #speaks this content
