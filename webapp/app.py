from flask import Flask, render_template
from models.database import get_db_connection
from flask import request, redirect, url_for
import mysql.connector

app=Flask(__name__)

@app.route('/')
def home():
    return "<h1>Welcome to Attendance System</h1><p>Go to <a href='/employees'>Employees</a> to see the employee list.</p>"



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


if __name__=='__main__':
    app.run(debug=True)

