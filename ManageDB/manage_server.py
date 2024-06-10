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
from manage_database import *
from manage_users import *
from manage_auth import *

# Choose Database to control
def get_user_choice(table):
    while True:
        display_menu(table)
        choice = input("Enter your choice (0-7): ")
        if choice == '1':
            get_users() if table == 'user'  else get_auth()
        elif choice == '2':
            index = input(f"Which {table}? ")
            get_specific_user(index) if table == 'user'  else get_specific_auth(index)
        elif choice == '3':
            create_user() if table == 'user' else create_auth()
        elif choice == '4':
            index = input(f"Which {table}? ")
            update_user(index) if table == 'user' else update_auth(index)
        elif choice == '5':
            index = input(f"Which {table}? ")
            update_user_by_field(index) if table == 'user' else update_auth_by_field(index)
        elif choice == '6':
            index = input(f"Which {table}? ")
            delete_user(index) if table == 'user' else delete_auth(index)
        elif choice == '7':
            sub_choice = input("Are you sure you want to delete the entire table? [y/n] ")
            if sub_choice == 'y' or sub_choice == 'Y':
                delete_table(f'{table}s')
        elif choice == '0':
            print("Back to Main Menu")
            break
        else:
            print("Invalid choice. Please enter a number from 0 to 7.")

# Main app
if __name__ == '__main__':
    trials = 3
    auth_user = False
    while True:
        if not auth_user:
            auth_user = login()
        if auth_user:
            display_main_menu()
            choice = input("Enter your choice (0-2): ")
            if choice == '1':
                get_user_choice('user')
            elif choice == '2':
                get_user_choice('auth_user')
            elif choice == '0':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please enter a number from 0 to 2.")
        else:
            if trials!=0:
                print("Incorrect Username or Password, Try Again")
                trials = trials -1
            else:
                print("Incorrect Username or Password, Exiting ... ")
                break