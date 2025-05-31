import mysql.connector

def get_db_connection():
     return mysql.connector.connect(
        host="localhost",
        user="appuser",
        password="yourpassword",
        database="attendance_system"
    )
