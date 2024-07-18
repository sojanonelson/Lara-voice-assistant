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
            return "I'm sorry, I don't know your name yet."
    elif 'how are you' in command:
        return "I'm doing well, thank you!"
    elif 'open' in command:
        app_name = command.split('open ')[-1]
        open_application(app_name)
    elif 'play' in command and 'song' in command:
        favorite = fetch_user_data('favorite_song')
        play_audio(favorite)
    elif 'stop' in command and 'song' in command:
        return'Alright...'       
    elif 'lock my laptop' in command:
        lock_my_laptop()
    elif 'which version are you' in command:
        version = fetch_general_data('version')
        return f'I am version {version}'
    elif 'who creates you' in command:
        creator = fetch_general_data('creator')
        return f'I was created by {creator}'
    elif 'set alarm' in command:
        set_alarm()
    elif 'exit' in command:
        eel.close_window()
        speak("Goodbye!")
        os.system("exist")     
    elif 'reset' in command:
        speak("Are you sure want to reset..")
        response = listen()
        if 'yes i want to' in response:
            speak("Resetting on progress..")
            name = fetch_user_data('Nickname')
            os.system('python reset.py')
            speak(f"Reset completed sucessfuly. Goodbye {name}")
            eel.close_window()
            os.system('exit')

        else:
            speak("Okay, I won't reset.")
    elif 'where am i now' in command: 
        location_data = fetch_location()
        if location_data:
            city = location_data.get('city', 'Unknown city')
            region = location_data.get('region', 'Unknown region')
            country = location_data.get('country', 'Unknown country')
            print(location_data)
            return  f"You are in {city}, {region}, {country}."
            
        else:
            return "I'm sorry, I couldn't determine your location."
    elif 'clear my terminal' in command:
        clear_terminal()
    elif 'thank you' in command:
        return "You're welcome!"
    elif 'in which city are im now':
        location_data = fetch_location()
        if location_data:
            city = location_data.get('city', 'Unknown city')
            return f"You are in {city}."
        else:
            return "Somthing went wrong.."