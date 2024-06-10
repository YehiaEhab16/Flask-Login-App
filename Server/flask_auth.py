'''
Flask App to manage users database server
-------------------------------------------
*used to manage SQLlite3 database (auth users database):
 auth table: store authenticated users that can access database
*Flask App hanldes all CRUD operations and
 provides APIs for ecternal access
 
$ Version: 2.0

@ Author: Yehia Ehab
'''

# Importing Required Modules
from flask_jwt_extended import create_access_token
from flask import request, jsonify
from flask_database import *
import argon2

''' 
Auth APIs
'''
# Get Users Method
@app.route('/auth', methods=['GET'])
@jwt_required()
def get_auth_users():
    try:
        if verify_admin():
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT id, username FROM auth_users')  # Select both id and username
            users = cursor.fetchall()
            conn.close()
            return jsonify(users), 200  # Successful operation
        else:
            return jsonify({'error': 'Only admin can perform this operation'}), 404  # Unauthorized
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Error


# Get Specific User Method
@app.route('/auth/<string:username>', methods=['GET'])
@jwt_required()
def get_auth_user(username):
    try:
        if verify_admin():
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT id, username FROM auth_users WHERE username = ?', (username,))
            user = cursor.fetchone()
            conn.close()
            if user:
                return jsonify(user), 200  # Successful operation
            else:
                return jsonify({'error': 'User not found'}), 404  # Error
        else:
            return jsonify({'error': 'Only admin can perform this operation'}), 404  # Unauthorized
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Error


# Create User Method
@app.route('/auth', methods=['POST'])
@jwt_required()
def create_auth_user():
    try:
        if verify_admin():
            data = request.json
            username = data.get('username')
            password = data.get('password')

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO auth_users (username, password) VALUES (?, ?)',
                        (username, password))
            conn.commit()
            conn.close()
            return jsonify({'message': 'User created successfully'}), 201 # successful operation
        else:
            return jsonify({'error': 'Only admin can perform this operation'}), 404  # Unauthorized
    except Exception as e:
        return jsonify({'error': str(e)}), 500 # error

# Update User Method
@app.route('/auth/<string:username>', methods=['PUT'])
@jwt_required()
def update_auth_user(username):
    try:
        if verify_admin():
            data = request.json
            new_username = data.get('new_username')
            new_password = data.get('new_password')

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE auth_users SET username=?, password=? WHERE username=?',
                        (new_username, new_password, username))
            conn.commit()
            conn.close()
            return jsonify({'message': 'User updated successfully'}), 200 # successful operation
        else:
            return jsonify({'error': 'Only admin can perform this operation'}), 404  # Unauthorized
    except Exception as e:
        return jsonify({'error': str(e)}), 500 # error
    
# Update User Method (Specific Field)
@app.route('/auth/<string:username>', methods=['PATCH'])
@jwt_required()
def update_auth_user_by_field(username):
    try:
        if verify_admin():
            data = request.json
            field_name = data.get('field_name')
            new_value = data.get('new_value')

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(f'UPDATE auth_users SET {field_name}=? WHERE username=?', (new_value, username))
            conn.commit()
            conn.close()
            return jsonify({'message': f'{field_name} updated successfully'}), 200 # successful operation
        else:
            return jsonify({'error': 'Only admin can perform this operation'}), 404  # Unauthorized
    except Exception as e:
        return jsonify({'error': str(e)}), 500 # error
    
# Delete User Method
@app.route('/auth/<string:username>', methods=['DELETE'])
@jwt_required()
def delete_auth_user(username):
    try:
        if verify_admin():
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM auth_users WHERE username = ?', (username,))
            conn.commit()
            conn.close()
            return jsonify({'message': 'User deleted successfully'}), 200 # successful operation
        else:
            return jsonify({'error': 'Only admin can perform this operation'}), 404  # Unauthorized
    except Exception as e:
        return jsonify({'error': str(e)}), 500 # error

# Route for user login
@app.route('/auth/login', methods=['POST'])
def auth_login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT username, password FROM auth_users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return jsonify({"msg": "User not found"}), 404

    if not argon2.PasswordHasher().verify(user[1], password):
        return jsonify({"msg": "Invalid password"}), 401

    # Generate access token if authentication succeeds
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200