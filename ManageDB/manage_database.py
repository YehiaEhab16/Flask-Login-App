'''
Manage Users database:
------------------------
*used to manage SQLlite3 database which consists of 4 tables:
 users: store user login and subscription info
 auth: store authenticated users that can access database
*preform all basic CRUD operations using flask APIs
 
$ Version: 2.0

@ Author: Yehia Ehab
'''

# Importing required Modules
import requests
import getpass
import argon2

# URL of flask server
BASE_URL = 'http://localhost:5000'
DECORATOR = 100
auth_token = None
username = None


# Get Input from terminal Method
def get_user_input(field_name):
    while True:
        if 'password' in field_name.lower() :
            user_input = getpass.getpass(prompt=f"Enter {field_name}: ")
        else:
            user_input = input(f"Enter {field_name}: ")

        if user_input.strip():
            return user_input.strip()
        else:
            print(f"{field_name} cannot be empty.")

# Display Menu Method
def display_menu(table):
    print("="*DECORATOR) 
    print("Choose an option:")
    print(f"1. Get {table}s")
    print(f"2. Get {table}")
    print(f"3. Create {table}")
    print(f"4. Update {table}")
    print(f"5. Update field")
    print(f"6. Delete {table}")
    print(f"7. Delete {table}s")
    print("0. Back")
    print("="*DECORATOR)

# Display Main Menu Method
def display_main_menu():
    print("="*DECORATOR) 
    print("Logged in as: ",username)
    print("="*DECORATOR) 
    print("1. Manage User Database")
    print("2. Manage Authentication Database")
    print("0. Exit")
    print("="*DECORATOR) 


def delete_table(table_name):
    try:
        headers = {'Authorization': f'Bearer {auth_token}'}
        response = requests.delete(f'{BASE_URL}/delete_table/{table_name}',headers=headers)
        if response.status_code == 200:
            print(response.json())
        else:
            print(f'Failed to delete table. Status code: {response.status_code}')
            print(response.json())
    except Exception as e:
        print(f'An error occurred: {e}')

def login():
    global auth_token, username
    try:
        username = get_user_input('username')
        password = get_user_input('password')
        login_data = {'username': username, 'password': password}
        response = requests.post(f'{BASE_URL}/auth/login', json=login_data)
        if response.status_code==200:
            auth_token = response.json().get('access_token')
            return True
        else:
            return False
        
    except Exception as e:
        print(f'An error occurred: {e}')
        return False
    
def get_auth_token():
    return auth_token
    
def get_password_hashed():
    password1 = get_user_input('password')
    password2 = get_user_input('password (for confirmation)')
    if password1 == password2:
        return True,hash_password(password1)
    else:
        return False, "Passwords don't match, Try again"
    
# Function to hash the password
def hash_password(password):
    return argon2.PasswordHasher().hash(password)
