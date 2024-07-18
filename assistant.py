import eel
import os
import speech_recognition as sr
import pyttsx3
import pyautogui
import threading
from utils.general_action import *
from setup import setup_assistant
from colorama import init, Fore, Style
from utils.handle_command import handle_command

# Initialize colorama
init()

# Check if user_data.txt exists
user_data_file = "data/user_data.txt"

if not os.path.exists(user_data_file):
    setup_assistant()

pyautogui.FAILSAFE = False

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Female voice





def speak(text):
    print(Fore.MAGENTA + f"Speaking: {text}" + Style.RESET_ALL)
    engine.say(text)
    engine.runAndWait()


@eel.expose
def update_ui_command(command):
    return command  # Just return command if needed


@eel.expose
def update_ui_response(response):
    return response


@eel.expose
def assistant_logic():
    os.system('cls' if os.name == 'nt' else 'clear')
    internet = is_connected()
    user = is_first_time_user()
    start_sound()
    print(f'First time user: {user}')
    print(f"Device connected to internet: {internet}")
    name = fetch_user_data('Nickname')
    print(Fore.CYAN + f'Welcome back {name}' + Style.RESET_ALL)
    greet = get_greeting()
    print(Fore.CYAN + f'Greeting: {greet}' + Style.RESET_ALL)
    speak(greet)
    speak("What can I do for you today?")

    while True:
        command = listen()
        if command:
            if 'stop' in command:
                print("Stopping the assistant...")
                break
            else:
                print(f"Processing command: {command}")
                time.sleep(1)
                response = handle_command(command)
                speak(response)
                # print(f"Command is: {command}")
                # eel.update_ui_command(command)
                # eel.update_ui_response(response)
            # speak(response)


@eel.expose
def start_assistant():
    eel.init("www")
    
    # eel_thread = threading.Thread(
    #     target=lambda: eel.start('index.html', mode='chrome', host='localhost', port=8000, block=True,
    #                              size=(1920, 1080)))
    eel_thread = threading.Thread(
        target=lambda: eel.start('index.html', mode='chrome', host='localhost', port=8000, block=True,
                                 size=(550, 500)))
    eel_thread.daemon = True
    eel_thread.start()

    assistant_logic()


@eel.expose
def close_program():
    eel.close_window()
    print("Closing the program...")
    os._exit(0)  # Forcefully exit the Python program


if __name__ == "__main__":
    start_assistant()
