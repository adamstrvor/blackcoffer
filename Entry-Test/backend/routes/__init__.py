from flask import Blueprint, jsonify, request, send_file
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import bcrypt
import pandas as pd
import numpy as np
import os
from  termcolor import colored
import sys
import requests
import re
import mysql.connector

api_bp = Blueprint('api', __name__)

print("\n| MYSQL Server Connexion...")
print("------------------------------------------")
host = input('|> Provide your MySQL server host: ').strip() or "localhost"
port = input('|> Provide your MySQL server port: ').strip() or "3306"
user = input('|> Provide your MySQL username: ').strip() or "root"
password = input('|> Provide your MySQL password: ').strip() or "Maliba2002"
database_name = input('|> Provide the MySQL database name: ').strip() or "global_outlooks"

db_config = {
    "host": host,
    "port": port,
    "user": user,
    "password": password, 
    "database": database_name
}

def get_db_connection():
    return mysql.connector.connect(**db_config)


def initialize_admin_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admin (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            password TEXT NOT NULL,
            fullname VARCHAR(255) NOT NULL,
            position VARCHAR(255),
            company VARCHAR(255),
            department VARCHAR(255) NOT NULL,
            access_level INT NOT NULL
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()

def is_admin_table_empty():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM admin;")
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count == 0


@api_bp.route('/', methods=['GET'])
def home():
	try:
		return jsonify({"message": "Welcome to the Flask API!"})
	except Exception as e:
	 	return jsonify({"message": "Internal Server Error", "error_details": str(e)}), 500


@api_bp.route('/admin/login', methods=['POST'])
def admin_login():
	try:
	    conn = get_db_connection()
	    cursor = conn.cursor(dictionary=True)

	    initialize_admin_table()

	    # Get JSON request data
	    data = request.get_json()
	    if not data or "email" not in data or "password" not in data:
	        return jsonify({"message": "Email and password are required"}), 400

	    email = data["email"].strip()
	    password = data["password"].strip()


	    # If no admin exists, first one becomes super admin
	    if is_admin_table_empty():
	        return jsonify({"message": "No admin found! Please create the first admin manually."}), 403

	    print("C")
	    # Fetch admin from DB
	    cursor.execute("SELECT * FROM admin WHERE email = %s", (email,))
	    admin = cursor.fetchone()

	    print("D")

	    if not admin or not bcrypt.checkpw(password.encode('utf-8'), admin["password_hash"].encode('utf-8')):
	        return jsonify({" ": "Invalid email or password"}), 401

	    print("E")

	    # Generate JWT token
	    access_token = create_access_token(identity=email)

	    print("F")

	    cursor.close()
	    conn.close()

	    return jsonify({
	        "message": "Login successful",
	        "access_token": access_token,
	        "admin": {
	            "fullname": admin["fullname"],
	            "position": admin["position"],
	            "department": admin["department"],
	            "access_level": admin["access_level"]
	        }
	    }), 200
	except Exception as e:
		return jsonify({"message": str(e)}), 500

@api_bp.route('/get/industry_trends', methods=['GET'])
@jwt_required()
def get_data():
	try:

		print('|> Fetching data...')

		conn = get_db_connection()
		cursor = conn.cursor(dictionary=True)  # Fetch rows as dictionaries
		cursor.execute("SELECT * FROM industry_trends")  # Replace with your table name
		data = cursor.fetchall()
		cursor.close()
		conn.close()
		return jsonify(data)
	except Exception as e:
		return jsonify({"message": str(e)}), 500


