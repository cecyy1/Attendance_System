from flask import Flask, render_template
from models.database import get_db_connection
from flask import request, redirect, url_for
import mysql.connector

app=Flask(__name__)

@app.route('/')
def home():
    return """
    <h1>Welcome to Attendance System</h1>
    <p>Go to <a href='/employees'>Employees</a> to see the employee list.</p>
    <p>Go to <a href='/attendance'>Attendance</a> to see attendance records.</p>
    <p>Go to <a href='/events'>Events</a> to see events.</p>
    """



#Employee List Page 
@app.route('/employees')
def employee_list():
    conn=get_db_connection() #connects to the database which is database.py
    cursor=conn.cursor() #makes a cursor(like a DB controller)
    cursor.execute("SELECT employee_id, first_name,last_name, department, email FROM employees ")#SQL query
    employees=cursor.fetchall() #fetch the results 
    cursor.close()
    conn.close() #connection close
    return render_template('employees.html', employees=employees)


#add employees
@app.route('/add-employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        first_name=request.form['first_name']
        last_name=request.form['last_name']
        department=request.form['department']
        email=request.form['email']
        hire_date=request.form['hire_date']

        conn = get_db_connection()
        cursor=conn.cursor()
        cursor.execute("INSERT INTO employees (first_name, last_name, department, email, hire_date) VALUES (%s, %s, %s, %s, %s)",
            (first_name, last_name, department, email, hire_date)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('employee_list'))

    return render_template('add_employee.html')

#edit employees 
@app.route('/edit-employee/<int:employee_id>', methods=['GET', 'POST'])
def edit_employee(employee_id):
     if request.method == 'POST':
        first_name=request.form['first_name']
        last_name=request.form['last_name']
        department=request.form['department']
        email=request.form['email']
        hire_date=request.form['hire_date']

        conn = get_db_connection()
        cursor=conn.cursor()
        cursor.execute("UPDATE employees SET first_name=%s, last_name=%s,"
        "department=%s, email=%s, hire_date=%s WHERE employee_id=%s",(first_name, last_name, department, email, hire_date, employee_id))
        conn.commit()
        conn.close()
        return redirect(url_for('employee_list'))
     #GET -get request to load the existing employee info
     conn=get_db_connection()
     cursor=conn.cursor()
     cursor.execute("SELECT * FROM employees WHERE employee_id = %s",(employee_id,))
     employee=cursor.fetchone()
     conn.close()
     return render_template('edit_employee.html', employee=employee)


#delete employees
@app.route('/delete-employee/<int:employee_id>', methods=['POST'])
def delete_employee(employee_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employees WHERE employee_id=%s", (employee_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('employee_list'))

#Attendance list Page 
@app.route("/attendance")
def attendance_list():
    sort_by = request.args.get('sort', 'timestamp')  # default sort column
    order = request.args.get('order', 'desc')        # default order

    # Validate inputs
    valid_columns = ['attendance_id', 'employee_id', 'event_id', 'attended', 'timestamp']
    if sort_by not in valid_columns:
        sort_by = 'timestamp'
    if order not in ['asc', 'desc']:
        order = 'desc'

    # Create SQL query safely
    query = f"SELECT attendance_id, employee_id, event_id, attended, timestamp FROM attendance ORDER BY {sort_by} {order.upper()}"

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    attendance_records = cursor.fetchall()
    cursor.close()
    conn.close()

    # Toggle order for next click
    next_order = 'asc' if order == 'desc' else 'desc'

    return render_template( 'attendance.html',
        attendance=attendance_records,
        sort_by=sort_by,
        order=order,
        next_order=next_order
    )

#Event list Page 
@app.route("/events")
def events_list():
    sort_by=request.args.get('sort','event_date' )
    order=request.args.get('order', 'desc')
    valid_columns=['event_id', 'event_name', 'event_type', 'location', 'event_date']
    if sort_by not in valid_columns:
        sort_by='event_date'
    if order not in ['asc', 'desc']:
        order='asc'
    query=f"SELECT event_id, event_name, event_type, event_date, location FROM events ORDER BY {sort_by} {order.upper()}"
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    event_records = cursor.fetchall()
    cursor.close()
    conn.close()

    next_order='asc' if order=='desc' else 'desc'
    return render_template('event.html', event=event_records, sort_by=sort_by, order=order, next_order=next_order)

if __name__=='__main__':
    app.run(debug=True)

