'''
Manage Users database:
------------------------
*used to manage SQLlite3 database (auth users database):
 auth table: store authenticated users that can access database
*preform all basic CRUD operations using flask APIs
 
$ Version: 2.0

@ Author: Yehia Ehab
'''

# Importing required Modules
from manage_database import *
import requests

''' 
Auth APIs
'''
# Get All Users Method
def get_auth():
    print("="*DECORATOR)
    try:
        headers = {'Authorization': f'Bearer {get_auth_token()}'}
        response = requests.get(f'{BASE_URL}/auth', headers=headers)
        print('GET /auth:')

        if response.status_code!=200:
            print(response.json())
            return

        users = response.json()

        if not users:
            print("No users found.")
            return

        print("{:<10} {:<30}".format("ID", "Username"))
        for user in users:
            print("{:<10} {:<30}".format(user[0], user[1]))
    except Exception as e:
        print(f'An error occurred: {e}')
    print("="*DECORATOR)

# Get User Method
def get_specific_auth(username):
    print("="*DECORATOR)
    try:
        headers = {'Authorization': f'Bearer {get_auth_token()}'}
        response = requests.get(f'{BASE_URL}/auth/{username}', headers=headers)
        print(f'GET /auth/{username}:')

        if response.status_code!=200:
            print(response.json())
            return

        user = response.json()
        
        if user:
            print("{:<10} {:<30}".format("Username:", user[0]))
        else:
            print("User not found.")
    except Exception as e:
        print(f'An error occurred: {e}')
    print("="*DECORATOR)

# Create User Method
def create_auth():
    print("="*DECORATOR)
    try:
        new_user_data = {}
        new_user_data['username'] = input("Enter username: ")
        success, password = get_password_hashed()
        if success:
            new_user_data['password'] = password
            headers = {'Authorization': f'Bearer {get_auth_token()}'}
            response = requests.post(f'{BASE_URL}/auth', json=new_user_data, headers=headers)
            print('POST /auth:')
            print(response.json())
        else:
            print(password)

    except Exception as e:
        print(f'An error occurred: {e}')
    print("="*DECORATOR)

# Update User Method
def update_auth(username):
    print("="*DECORATOR)
    try:
        new_username = input("Enter new username: ")
        success, password = get_password_hashed()

        if success:
            updated_user_data = {
                'new_username': new_username,
                'new_password': password
            }

            headers = {'Authorization': f'Bearer {get_auth_token()}'}
            response = requests.put(f'{BASE_URL}/auth/{username}', json=updated_user_data, headers=headers)
            print(f'PUT /auth/{username}:')
            print(response.json())
        else:
            print(password)
    except Exception as e:
        print(f'An error occurred: {e}')
    print("="*DECORATOR)

# Update User Method (Specific Field)
def update_auth_by_field(username):
    print("="*DECORATOR)    
    # Display the menu for field selection
    print("Choose the field to update:")
    print("1. Username")
    print("2. Password")
    choice = input("Enter the field number to update (1-2): ")

    # Map field number to field name
    fields = {
        '1': 'username',
        '2': 'password'
    }

    # Get the field name corresponding to the user's choice
    field_name = fields.get(choice)
    if not field_name:
        print("Invalid choice.")
        return

    # Prompt the user to enter the new value for the chosen field
    if field_name=='password':
        success, password = get_password_hashed()
        if success:
            new_value = password
        else:
            print(password)
            return
    else:
        new_value = get_user_input(f"new value for {field_name}: ")

    updated_user_data = {
        'field_name': field_name,
        'new_value': new_value
    }

    headers = {'Authorization': f'Bearer {get_auth_token()}'}
    response = requests.patch(f'{BASE_URL}/auth/{username}', json=updated_user_data, headers=headers)
    print(f'PATCH /auth/{username}:')
    print(response.json())
    
    print("="*DECORATOR)

# Delete User Method
def delete_auth(username):
    print("="*DECORATOR)
    try:
        headers = {'Authorization': f'Bearer {get_auth_token()}'}
        response = requests.delete(f'{BASE_URL}/auth/{username}', headers=headers)
        print(f'DELETE /auth/{username}:')
        print(response.json())
    except Exception as e:
        print(f'An error occurred: {e}')
    print("="*DECORATOR)