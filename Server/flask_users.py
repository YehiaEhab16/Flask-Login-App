'''
Flask App to manage users database server
-------------------------------------------
*used to manage SQLlite3 database (users database):
 users table: store user login and subscription info
*Flask App hanldes all CRUD operations and
 provides APIs for ecternal access
 
$ Version: 2.0

@ Author: Yehia Ehab
'''

# Importing Required Modules
from flask import request, jsonify
from flask_database import *

''' 
Users APIs
'''
# Get Users Method
@app.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users') # get all users
        users = cursor.fetchall()
        conn.close()
        return jsonify(users), 200  # successful operation
    except Exception as e:
        return jsonify({'error': str(e)}), 500 # error

# Get Specific User Method
@app.route('/users/<string:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE uid = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        if user:
            return jsonify(user), 200 # successful operation
        else:
            return jsonify({'error': 'User not found'}), 404 # error
    except Exception as e:
        return jsonify({'error': str(e)}), 500 # error

# Create User Method
@app.route('/users', methods=['POST'])
@jwt_required()
def create_user():
    try:
        data = request.json
        uid = data.get('uid')
        email = data.get('email')
        name = data.get('name')
        age = data.get('age')
        gender = data.get('gender')
        password_encrypt = data.get('password_encrypt')
        subscription_status = data.get('subscription_status', 0)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (uid, email, name, age, gender, password_encrypt, subscription_status) VALUES (?, ?, ?, ?, ?, ?, ?)',
                       (uid, email, name, age, gender, password_encrypt, subscription_status))
        conn.commit()
        conn.close()
        return jsonify({'message': 'User created successfully'}), 201 # successful operation
    except Exception as e:
        return jsonify({'error': str(e)}), 500 # error

# Update User Method (All user data)
@app.route('/users/<string:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    try:
        data = request.json
        uid = data.get('uid')
        email = data.get('email')
        name = data.get('name')
        age = data.get('age')
        gender = data.get('gender')
        password_encrypt = data.get('password_encrypt')
        subscription_status = data.get('subscription_status', 0)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET uid=?, email=?, name=?, age=?, gender=?, password_encrypt=?, subscription_status=? WHERE uid=?',
                       (uid, email, name, age, gender, password_encrypt, subscription_status, user_id))
        conn.commit()
        conn.close()
        return jsonify({'message': 'User updated successfully'}), 200 # successful operation
    except Exception as e:
        return jsonify({'error': str(e)}), 500 # error
    
# Update User Method (Specfic Field)
@app.route('/users/<string:user_id>', methods=['PATCH'])
@jwt_required()
def update_user_specific_field(user_id):
    try:
        data = request.json
        field_name = data.get('field_name')
        new_value = data.get('new_value')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f'UPDATE users SET {field_name}=? WHERE uid=?', (new_value, user_id))
        conn.commit()
        conn.close()
        
        return jsonify({'message': f'{field_name} updated successfully'}), 200 # successful operation
    except Exception as e:
        return jsonify({'error': str(e)}), 500 # error

# Delete User Method
@app.route('/users/<string:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE uid = ?', (user_id,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'User deleted successfully'}), 200 # successful operation
    except Exception as e:
        return jsonify({'error': str(e)}), 500 # error
