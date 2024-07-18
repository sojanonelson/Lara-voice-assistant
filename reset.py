import os


user_data = "data/user_data.txt"
general_data = 'data/general_data.txt'

try:
    os.remove(user_data )
    print(f"{user_data } has been deleted successfully")
except FileNotFoundError:
    print(f"{user_data } does not exist")
except PermissionError:
    print(f"Permission denied: {user_data }")
except Exception as e:
    print(f"Error occurred: {e}")



def fetch_general_data(key):
    with open(general_data, 'r') as file:
        for line in file:
            if line.startswith(key):
                return line.split('=')[1].strip()
    return None

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

# Reset firsttimeuser to true
def reset_first_time_user():
    update_general_data('firsttimeuser', 'true')

# reset_first_time_user()
