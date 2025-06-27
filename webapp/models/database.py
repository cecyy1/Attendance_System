import mysql.connector

def get_db_connection():
     return mysql.connector.connect(
        host="localhost",
        user="appuser",
        password="ceciliamartinez2301",
        database="attendance_system"
    )
