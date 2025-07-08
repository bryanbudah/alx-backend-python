import mysql.connector
from mysql.connector import errorcode
import csv
import uuid

# 1. Connect to MySQL server (not database)
def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_mysql_password"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# 2. Create database if not exists
def create_database(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        connection.commit()
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
    cursor.close()

# 3. Connect to the `ALX_prodev` database
def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_mysql_password",
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# 4. Create `user_data` table
def create_table(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL,
                INDEX(user_id)
            )
        """)
        connection.commit()
        print("Table user_data created successfully")
    except mysql.connector.Error as err:
        print(f"Failed creating table: {err}")
    cursor.close()

# 5. Insert data from CSV
def insert_data(connection, csv_file):
    cursor = connection.cursor()

    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Check if user_id exists
            cursor.execute("SELECT user_id FROM user_data WHERE user_id = %s", (row['user_id'],))
            exists = cursor.fetchone()
            if not exists:
                cursor.execute("""
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                """, (
                    row['user_id'],
                    row['name'],
                    row['email'],
                    row['age']
                ))
    connection.commit()
    cursor.close()
