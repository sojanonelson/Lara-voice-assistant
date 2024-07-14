import speech_recognition as sr
import pyttsx3
import os

# Initialize text-to-speech engine with female voice
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Index 1 is typically a female voice, adjust as needed

# Function to recognize speech
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    
    try:
        command = r.recognize_google(audio, language='en-US')
        print(f"User said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("Sorry, I didn't understand that.")
        return ""
    except sr.RequestError:
        print("Sorry, my speech service is down.")
        return ""

# Function to speak
def speak(text):
    engine.say(text)
    engine.runAndWait()


