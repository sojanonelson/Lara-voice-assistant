import os
import speech_recognition as sr
import pyttsx3
from utils.general_action import *
from playsound import playsound
from utils.voice import speak
import shutil
import sys

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


# Function to setup assistant and save data to file
def setup_assistant():
    # Ask for name
    os.system("cls")
    speak("Hello! I'm Lara. , It seems like you are starting Lara for the first time. Let's set things up.")
    speak("please enter your name?")
    name = input("Enter you name:")
    if name:
        # Ask for nickname
        speak(f"Nice to meet you, {name}. What should I call you?")
        # nickname = listen()
        nickname = input("Enter you nickname: ")
        if nickname:
            # Save data to file
            with open('data/user_data.txt', 'w') as f:
                f.write(f"Name: {name}\n")
                f.write(f"Nickname: {nickname}\n")
            speak(f"Great, I'll call you {nickname} from now on.")
            name = fetch_user_data('Nickname')
            speak(f"Welcome back {name} !, Starting Lara assistant.")
            playsound("resources/sounds/start_sound.mp3")
            update_general_data('firsttimeuser', 'false')
            os.system('python assistant.py')
            add_to_startup('assistant.py')
            return name, nickname
    speak("I'm sorry, I didn't catch that. Let's try again.")
    return setup_assistant()

# Function to check if it's the first time user
def is_first_time():
    try:
        with open('data/general_data.txt', 'r') as f:
            data = f.read()
            if data.strip() == "firsttimeuser=true":
                return True
            else:
                return False
    except FileNotFoundError:
        return True

# Main function to run setup or assistant
def main():
    if is_first_time():
        speak("It seems like you are starting Lara for the first time. Let's set things up.")
        setup_assistant()
        with open('data/general_data.txt', 'w') as f:
            f.write("firsttimeuser=false")
    else:
        name = fetch_user_data('Nickname')
        speak(f"Welcome back {name} !, Starting Lara assistant.")
        playsound("resources/sounds/start_sound.mp3")
        os.system('python assistant.py')
        add_to_startup('assistant.py')
     
def add_to_startup(file_path=None):
    if file_path is None:
        file_path = os.path.realpath(__file__)
    
    # Startup folder path
    startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    
    # Script name to be added in the startup folder
    script_name = os.path.basename(file_path)
    
    # Shortcut path
    shortcut_path = os.path.join(startup_folder, script_name + ".lnk")

    # If the shortcut already exists, no need to create again
    if not os.path.exists(shortcut_path):
        # Create a shortcut
        import win32com.client
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortcut(shortcut_path)
        shortcut.TargetPath = sys.executable
        shortcut.Arguments = f'"{file_path}"'
        shortcut.WorkingDirectory = os.path.dirname(file_path)
        shortcut.IconLocation = sys.executable
        shortcut.save()
        
        print(f"Shortcut created at: {shortcut_path}")
    else:
        print(f"Shortcut already exists at: {shortcut_path}")

# Usage
# Specify the path of the Python script you want to run at startup
# If you want to add this current script to startup, pass no arguments to the function
add_to_startup("C:\\Users\\sojan\\OneDrive\\Desktop\\Projects\\Lara Assistant\\Lara v1\\assistant.py")       

# Entry point
if __name__ == "__main__":
    main()
