import os
import speech_recognition as sr
import pyttsx3
from playsound import playsound
from utils.voice import speak
import sys
import time
from datetime import datetime, timedelta
import subprocess
import requests
import eel
import psutil

current_song_process = None
general_data = 'data/general_data.txt'
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


def is_connected():
    url = "http://www.google.com"
    timeout = 5
    try:
        response = requests.get(url, timeout=timeout)
        # If the request was successful, the device is connected to the internet
        return True
    except (requests.ConnectionError, requests.Timeout):
        # If the request failed, the device is not connected to the internet
        return False
# Function to fetch user data from user_data.txt
@eel.expose
def fetch_user_data(key):
    try:
        with open('data/user_data.txt', 'r') as f:
            for line in f:
                parts = line.strip().split(':')
                if len(parts) == 2:
                    k, v = parts[0].strip(), parts[1].strip()
                    if k.lower() == key.lower():
                        return v
    except FileNotFoundError:
        print("User data file not found.")
    return None

def fetch_general_data(key):
    try:

        with open('data/general_data.txt', 'r') as f:
            for line in f:
                parts = line.strip().split(':')
                if len(parts) == 2:
                    k, v = parts[0].strip(), parts[1].strip()
                    if k.lower() == key.lower():
                        return v
    except FileNotFoundError:
        print("General data file not found.")
    return None


def save_user_data(key, value):
    try:
        # Read existing data
        with open('data/user_data.txt', 'r') as f:
            lines = f.readlines()

        # Update or append new data
        with open('data/user_data.txt', 'w') as f:
            updated = False
            for line in lines:
                if line.startswith(f"{key}:"):
                    f.write(f"{key}: {value}\n")
                    updated = True
                else:
                    f.write(line)
            if not updated:
                f.write(f"{key}: {value}\n")
        
        print(f"Data saved: {key} = {value}")
    except FileNotFoundError:
        # If file doesn't exist, create new
        with open('data/user_data.txt', 'w') as f:
            f.write(f"{key}: {value}\n")
        print(f"Data saved: {key} = {value}")
    except Exception as e:
        print(f"Error saving data: {e}")

# Function to open applications based on app_name
def open_application(app_name):
    try:
        if 'chrome' in app_name:
            os.system('start chrome')
        elif 'notepad' in app_name:
            os.system('start notepad')
        elif 'calculator' in app_name:
            os.system('start calc')
        else:
            speak(f"Sorry, I don't know how to open {app_name}.")
    except Exception as e:
        print(f"Error opening application: {e}")
        speak("Sorry, I couldn't open that application.")

# Function to play favorite song
def play_audio(favorite):
    if favorite:
        music_dir = r"C:\Users\sojan\Music\My Fav"
        song_path = os.path.join(music_dir, favorite + ".mp3")
        
        if os.path.exists(song_path):
            speak(f"Playing {favorite} for you.")
            os.startfile(song_path)  # Use os.startfile to open the file with the default application
        else:
            speak(f"Sorry, I couldn't find {favorite} in your music directory.")
    else:
        speak("I'm sorry, I don't know your favorite song yet.")
        speak("What is your favorite song?")
        favorite = listen()
        if favorite:
            save_user_data('favorite_song', favorite)
            play_audio(favorite)
        else:
            speak("I couldn't understand your favorite song. Please try again later.")


# Function to stop playing song
def stop_audio():
    global current_song_process
    if current_song_process:
        current_song_process.terminate()
        speak("The song has been stopped.")
        current_song_process = None
    else:
        speak("No song is currently playing.")

def lock_my_laptop():
    try:
        os.system("rundll32.exe user32.dll,LockWorkStation")  # Lock the screen using system command
        speak("Your laptop has been locked.")
       
    except Exception as e:
        print(f"Error locking laptop: {e}")
        speak("Sorry, I couldn't lock your laptop at the moment.")

def set_alarm():
    speak("What time do you want to set the alarm for? Please say the time with AM or PM.")
    alarm_time_str = listen()
    if alarm_time_str:
        try:
            # Parse the time input from the user
            alarm_time = datetime.strptime(alarm_time_str, "%I:%M %p")
            now = datetime.now()
            alarm_time = now.replace(hour=alarm_time.hour, minute=alarm_time.minute, second=0, microsecond=0)
            if alarm_time < now:
                alarm_time += timedelta(days=1)

            speak("Do you want to add a note to the alarm?")
            note_response = listen()
            alarm_note = ""
            if "yes" in note_response:
                speak("Please say your note.")
                alarm_note = listen()

            # Calculate time difference
            time_diff = (alarm_time - now).total_seconds()
            speak(f"Alarm set for {alarm_time.strftime('%I:%M %p')}.")
            if alarm_note:
                speak(f"Note added: {alarm_note}")

            time.sleep(time_diff)
            speak(f"Alarm ringing! {alarm_note}")
            playsound("resources/sounds/alarm_sound.mp3")
        except ValueError:
            speak("I didn't understand the time format. Please try again.")
            set_alarm()
    else:
        speak("I didn't catch the time. Please try again.")
        set_alarm()
        
def clear_terminal():
    start_sound()
    os.system('cls')




def get_greeting():
 
    current_time = datetime.now().time()

   
    morning_start = datetime.strptime('05:00:00', '%H:%M:%S').time()
    afternoon_start = datetime.strptime('12:00:00', '%H:%M:%S').time()
    evening_start = datetime.strptime('18:00:00', '%H:%M:%S').time()
    night_start = datetime.strptime('21:00:00', '%H:%M:%S').time()

    
    if morning_start <= current_time < afternoon_start:
        return "Good morning"
    elif afternoon_start <= current_time < evening_start:
        return "Good afternoon"
    elif evening_start <= current_time < night_start:
        return "Good evening"
    else:
        return "Good night"

@eel.expose
def start_sound():
    playsound("resources/sounds/start_sound.mp3")

@eel.expose
def exit_sound():
    playsound("resources/sounds/exit.mp3")




def is_first_time_user(file_path="data/general_user.txt"):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith("firsttimeuser"):
                    key, value = line.split('=')
                    if value.strip().lower() == 'false':
                        return False
                    else:
                        return True
        # If the key is not found, assume it is the first time user
        return True
    except FileNotFoundError:
        # If the file does not exist, assume it is the first time user
        return True



def check_battery_percentage():
    battery = psutil.sensors_battery()
    if battery is not None:
        percentage = battery.percent
        is_plugged = battery.power_plugged
        return percentage, is_plugged
    else:
        return None, None
       
def update_general_data(key, value):
    lines = []
    with open(general_data, 'r') as file:
        lines = file.readlines()
    with open(general_data, 'w') as file:
        for line in lines:
            if line.startswith(key):
                file.write(f"{key}={value}\n")
            else:
                file.write(line)

# @eel.expose
# def close_program():
#     global listening
#     print("Closing the program...")
#     listening = False
#     exit_sound()
#     eel.close()
#     os._exit(0)