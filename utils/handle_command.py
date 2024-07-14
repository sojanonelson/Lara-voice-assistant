from utils.general_action import *




def handle_command(command):
    if 'your name' in command:
        return "My name is Lara version 1"
        
    elif 'my name' in command:
        name = fetch_user_data('Name')
        if name:
            # speak(f"Your name is {name}.")
            response = f"Your name is {name}."
            return response
        else:
            speak("I'm sorry, I don't know your name yet.")
    elif 'how are you' in command:
        speak("I'm doing well, thank you!")
    elif 'open' in command:
        app_name = command.split('open ')[-1]
        open_application(app_name)
    elif 'play' in command and 'song' in command:
        favorite = fetch_user_data('favorite_song')
        play_audio(favorite)
    elif 'stop' in command and 'song' in command:
        speak('Alright...')
        stop_audio()
    elif 'lock my laptop' in command:
        lock_my_laptop()
    elif 'which version are you' in command:
        version = fetch_general_data('version')
        speak(f'I am version {version}')
    elif 'who creates you' in command:
        creator = fetch_general_data('creator')
        speak(f'I was created by {creator}')
    elif 'set alarm' in command:
        set_alarm()
    elif 'exit' in command:
        
        speak("Goodbye!")
        eel.close_window()
        exit()

    elif 'clear my terminal' in command:
        clear_terminal()