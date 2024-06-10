'''
Flask App to manage users database server
-------------------------------------------
*used to manage SQLlite3 database which consists of 4 tables:
 users: store user login and subscription info
 auth: store authenticated users that can access database
*Flask App hanldes all CRUD operations and
 provides APIs for ecternal access
 
$ Version: 2.0

@ Author: Yehia Ehab
'''

# Importing Required Modules
from flask_database import *
from flask_users import *
from flask_auth import *
import os

# Run App
if __name__ == '__main__':
    if os.path.exists(DATABASE):
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        raise FileNotFoundError("Database not found")
