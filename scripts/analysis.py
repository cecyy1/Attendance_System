import mysql.connector

# Connect to MySQL
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="appuser",
        password="yourpassword",
        database="attendance_system"
    )

# Total Attended Events per Employee
def total_attended_events(cursor):
    query = """
    SELECT 
      e.employee_id, 
      e.first_name, 
      e.last_name, 
      COUNT(a.attendance_id) AS total_attended_events
    FROM employees e
    LEFT JOIN attendance a ON e.employee_id = a.employee_id AND a.attended = 1
    GROUP BY e.employee_id, e.first_name, e.last_name
    ORDER BY total_attended_events DESC;
    """
    cursor.execute(query)
    return cursor.fetchall()

# Total Absent Events per Employee
def total_absent_events(cursor):
    query = """
    SELECT 
      e.employee_id, 
      e.first_name, 
      e.last_name, 
      COUNT(a.attendance_id) AS total_absent_events
    FROM employees e
    LEFT JOIN attendance a ON e.employee_id = a.employee_id AND a.attended = 0
    GROUP BY e.employee_id, e.first_name, e.last_name
    ORDER BY total_absent_events DESC;
    """
    cursor.execute(query)
    return cursor.fetchall()

# Attendance Percentage per Employee
def percentage_per_employee(cursor):
    query= """
    SELECT 
      e.employee_id, 
      e.first_name, 
      e.last_name,
      COUNT(a.attendance_id) AS total_events,
      SUM(CASE WHEN a.attended = 1 THEN 1 ELSE 0 END) AS attended_events,
      ROUND( (SUM(CASE WHEN a.attended = 1 THEN 1 ELSE 0 END) / COUNT(a.attendance_id)) * 100, 2) AS attendance_percentage
    FROM employees e
    LEFT JOIN attendance a ON e.employee_id = a.employee_id
    GROUP BY e.employee_id, e.first_name, e.last_name
    ORDER BY attendance_percentage DESC;
    """
    cursor.execute(query)
    return cursor.fetchall()

# Employees with Perfect Attendance
def perfect_attendance(cursor):
    query = """
    SELECT 
      e.employee_id, 
      e.first_name, 
      e.last_name
    FROM employees e
    JOIN attendance a ON e.employee_id = a.employee_id
    GROUP BY e.employee_id, e.first_name, e.last_name
    HAVING SUM(CASE WHEN a.attended = 0 THEN 1 ELSE 0 END) = 0;
    """
    cursor.execute(query)
    return cursor.fetchall()

def main():
    conn = connect_db()
    cursor = conn.cursor()

    print("Total Attended Events per Employee:")
    results = total_attended_events(cursor)
    for row in results:
        print(row)

    print("\nTotal Absent Events per Employee:")
    absent_results = total_absent_events(cursor)
    for row in absent_results:
        print(row)

    print("\nAttendance Percentage per Employee:")
    percentage_results = percentage_per_employee(cursor)
    for row in percentage_results:
        print(row)

    print("\nEmployees with Perfect Attendance:")
    perfect_results = perfect_attendance(cursor)
    for row in perfect_results:
        print(row)

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
