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
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask import Flask, jsonify
import sqlite3

JWT_SECRET_KEY = 'Secret-Key'
ADMIN_NAME     = 'admin' 
DATABASE       = 'users.db'


# Database Declaration
app = Flask(__name__)

app.config['JWT_SECRET_KEY'] =  JWT_SECRET_KEY
jwt = JWTManager(app)


# Database Connection
def get_db_connection():
    return sqlite3.connect(DATABASE)
    
# Delete Entire Table Method (for both users and animations tables)
@app.route('/delete_table/<string:table_name>', methods=['DELETE'])
@jwt_required()
def delete_table_contents(table_name):
    try:
        if verify_admin():        
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(f'DELETE FROM {table_name};')
            conn.commit()
            conn.close()
            return jsonify({'message': f'Contents of table {table_name} deleted successfully'}), 200 # Successful Operation
        else:
            return jsonify({'error': 'Only admin can perform this operation'}), 404  # Unauthorized
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Protected route
@app.route('/protected', methods=['GET'])
@jwt_required()  # Requires a valid JWT token
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

def verify_admin():
    current_user = get_jwt_identity()
    if current_user == ADMIN_NAME:
        return True
    else: 
        return False