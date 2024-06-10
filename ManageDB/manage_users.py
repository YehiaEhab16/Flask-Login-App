'''
Manage Users database:
------------------------
*used to manage SQLlite3 database (users database):
 users table: store user login and subscription info
*preform all basic CRUD operations using flask APIs
 
$ Version: 2.0

@ Author: Yehia Ehab
'''

# Importing required Modules
from manage_database import *
import requests

# Get All Users Method
def get_users():
    print("="*DECORATOR)
    headers = {'Authorization': f'Bearer {get_auth_token()}'}
    response = requests.get(f'{BASE_URL}/users', headers=headers)
    print('GET /users:')

    if response.status_code!=200:
        print(response.json())
        return
    
    # Get Response
    users = response.json()
    if not users:
        print("No users found.")
        return
    
    # Print header
    print("{:<5} {:<10} {:<20} {:<15} {:<10} {:<10} {:<10}".format(
            "ID", "UID", "Email", "Name", "Age", "Gender", "Subscription Status"))
    
    try:
        # Print each user's details
        for user in users:
            print("{:<5} {:<10} {:<20} {:<15} {:<10} {:<10} {:<10}".format(
                user[0], user[1], user[2], user[3], user[4], user[5], user[7]))
    except:
        print('No Users Found')

    print("="*DECORATOR)

# Get User Method
def get_specific_user(user_id):
    print("="*DECORATOR) 
    headers = {'Authorization': f'Bearer {get_auth_token()}'}
    response = requests.get(f'{BASE_URL}/users/{user_id}', headers=headers)
    print(f'GET /users/{user_id}:')
    
    if response.status_code!=200:
        print(response.json())
        return

    # Get Response
    user = response.json()
    
    try:
        # Print user details
        print("{:<20} {:<10}".format("ID:", user[0]))
        print("{:<20} {:<10}".format("UID:", user[1]))
        print("{:<20} {:<30}".format("Email:", user[2]))
        print("{:<20} {:<20}".format("Name:", user[3]))
        print("{:<20} {:<20}".format("Age:", user[4]))
        print("{:<20} {:<20}".format("Gender:", user[5]))
        print("{:<20} {:<20}".format("Subscription Status:", user[7]))
        print("="*DECORATOR)

    except:
        print("User Not Found")

# Create User Method
def create_user():
    print("="*DECORATOR)

    # Create dictionary for new user
    new_user_data = {} 
    new_user_data['uid'] = get_user_input("uid")
    new_user_data['email'] = get_user_input("email")
    new_user_data['name'] = get_user_input("name")
    new_user_data['age'] = int(get_user_input("age"))
    new_user_data['gender'] = get_user_input("gender")
    success, password = get_password_hashed()
    if success:
        new_user_data['password_encrypt'] = password
        new_user_data['subscription_status'] = int(input("Enter subscription status (0 or 1): "))

        # Get Response
        headers = {'Authorization': f'Bearer {get_auth_token()}'}
        response = requests.post(f'{BASE_URL}/users', json=new_user_data, headers=headers)
        print('POST /users:')
        print(response.json())
        print("="*DECORATOR)
    else:
        print(password)

# Update User Method (All user data)
def update_user(user_id):
    print("="*DECORATOR) 

    # Create dictionary for updated user
    updated_user_data = {}
    updated_user_data['uid'] = get_user_input("uid")
    updated_user_data['email'] = get_user_input("email")
    updated_user_data['name'] = get_user_input("name")
    updated_user_data['age'] = int(get_user_input("age"))
    updated_user_data['gender'] = get_user_input("gender")
    success, password = get_password_hashed()
    if success:
        updated_user_data['password_encrypt'] = password
        updated_user_data['subscription_status'] = int(input("Enter subscription status (0 or 1): "))

        # Get Response
        headers = {'Authorization': f'Bearer {get_auth_token()}'}
        response = requests.put(f'{BASE_URL}/users/{user_id}', json=updated_user_data, headers=headers)
        print(f'PUT /users:')
        print(response.json())
        print("="*DECORATOR)
    else:
        print(password)

# Update User Method (Specific Field)
def update_user_by_field(user_id):
    print("="*DECORATOR) 
    
    # Display the menu for field selection
    print("Choose the field to update:")
    print("1. UID")
    print("2. Email")
    print("3. Name")
    print("4. Age")
    print("5. Gender")
    print("6. Password")
    print("7. Subscription Status")
    choice = input("Enter the field number to update (1-7): ")

    # Map field number to field name
    fields = {
        '1': 'uid',
        '2': 'email',
        '3': 'name',
        '4': 'age',
        '5': 'gender',
        '6': 'password_encrypt',
        '7': 'subscription_status'
    }

    # Get the field name corresponding to the user's choice
    field_name = fields.get(choice)
    if not field_name:
        print("Invalid choice.")
        return

    # Prompt the user to enter the new value for the chosen field
    if field_name == "password":
        success, password = get_password_hashed()
        if success:
            new_value = password
        else:
            print(password)
            return
    else:
        new_value = get_user_input(f"new value for {field_name}: ")

    try:
        # Prepare the data for the PATCH request
        updated_user_data = {
            'field_name': field_name,
            'new_value': new_value
        }

        # Send the PATCH request to update the user
        headers = {'Authorization': f'Bearer {get_auth_token()}'}
        response = requests.patch(f'{BASE_URL}/users/{user_id}', json=updated_user_data, headers=headers)
        
        if response.status_code == 200:
            print(f'User updated successfully.')
            print(response.json())
        else:
            print(f'Failed to update user. Status code: {response.status_code}')
            print(response.text)
    except Exception as e:
        print(f'An error occurred: {e}')

    print("="*DECORATOR)

# Delete User Method
def delete_user(user_id):
    print("="*DECORATOR) 
    headers = {'Authorization': f'Bearer {get_auth_token()}'}
    response = requests.delete(f'{BASE_URL}/users/{user_id}', headers=headers)
    print(f'DELETE /users/{user_id}:')
    print(response.json())
    print("="*DECORATOR)