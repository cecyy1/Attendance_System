from flask import Flask, render_template
from models.database import get_db_connection
from flask import request, redirect, url_for
import mysql.connector
<<<<<<< HEAD

=======
from datetime import datetime
>>>>>>> 157e5ca (Initial clean commit without passwords)
app=Flask(__name__)

@app.route('/')
def home():
    return """
    <h1>Welcome to Attendance System</h1>
    <p>Go to <a href='/employees'>Employees</a> to see the employee list.</p>
    <p>Go to <a href='/attendance'>Attendance</a> to see attendance records.</p>
    <p>Go to <a href='/events'>Events</a> to see events.</p>
<<<<<<< HEAD
=======
    <p>Go to <a href='/time_logs'>Clock In/Out Logs</a> to see clock in and clock out times.</p>
>>>>>>> 157e5ca (Initial clean commit without passwords)
    """



<<<<<<< HEAD
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
=======

#Employee List Page 
@app.route('/employees')
def employee_list():
    search_query=request.args.get('search', '').strip()
    conn=get_db_connection() #connects to the database which is database.py
    cursor=conn.cursor() 
    if search_query:
        query = """
            SELECT employee_id, first_name, last_name, department, email
            FROM employees
            WHERE first_name LIKE %s OR last_name LIKE %s OR department LIKE %s
        """
        like_query = f"%{search_query}%"
        cursor.execute(query, (like_query, like_query,like_query))
    else:
        cursor.execute("SELECT employee_id, first_name,last_name, department, email FROM employees ")#SQL query
    employees=cursor.fetchall() #fetch the results 
    cursor.close()
    conn.close() #connection close
    return render_template('employees.html', employees=employees, search_query=search_query)
>>>>>>> 157e5ca (Initial clean commit without passwords)


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
<<<<<<< HEAD
=======
    search_query=request.args.get('search', '').strip() #search 

>>>>>>> 157e5ca (Initial clean commit without passwords)

    # Validate inputs
    valid_columns = ['attendance_id', 'employee_id', 'event_id', 'attended', 'timestamp']
    if sort_by not in valid_columns:
        sort_by = 'timestamp'
    if order not in ['asc', 'desc']:
        order = 'desc'

<<<<<<< HEAD
    # Create SQL query safely
    query = f"SELECT attendance_id, employee_id, event_id, attended, timestamp FROM attendance ORDER BY {sort_by} {order.upper()}"

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    attendance_records = cursor.fetchall()
=======
    # build query with JOINs fo Employee and event name 
    query = """
       SELECT 
            a.attendance_id,
            CONCAT(e.first_name, ' ', e.last_name) AS employee_name,
            ev.event_name AS event_name,
            a.attended,
            a.timestamp
        FROM attendance a
        JOIN employees e ON a.employee_id = e.employee_id
        JOIN events ev ON a.event_id = ev.event_id
    """
    filters=[]
    params=[]

    #add search filter
    if search_query:
        filters.append("(CONCAT(e.first_name, ' ', e.last_name) LIKE %s OR ev.event_name LIKE %s)")
        params.extend([f"%{search_query}%", f"%{search_query}%"])

    if filters:
        query += " WHERE " + " AND ".join(filters)

    sort_columns_map = {
        'attendance_id': 'a.attendance_id',
        'employee_name': "employee_name",  # aliased, so we can sort by alias
        'event_name': 'ev.name',
        'attended': 'a.attended',
        'timestamp': 'a.timestamp'
    }

    query += f" ORDER BY {sort_columns_map.get(sort_by, 'a.timestamp')} {order.upper()}"


    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    attendance_records = cursor.fetchall()

     # Optional summary (e.g., how many events attended by each name)
    summary = None
    if search_query:  # Only generate summary if searching by something
        summary = {}
        for record in attendance_records:
            name = record[1]  # employee_name
            if name not in summary:
                summary[name] = {"total": 0, "present": 0}
            summary[name]["total"] += 1
            if record[3]:  # attended
                summary[name]["present"] += 1

>>>>>>> 157e5ca (Initial clean commit without passwords)
    cursor.close()
    conn.close()

    # Toggle order for next click
    next_order = 'asc' if order == 'desc' else 'desc'

    return render_template( 'attendance.html',
        attendance=attendance_records,
        sort_by=sort_by,
        order=order,
<<<<<<< HEAD
        next_order=next_order
=======
        next_order=next_order,
        search_query=search_query,
        summary=summary
>>>>>>> 157e5ca (Initial clean commit without passwords)
    )

#Event list Page 
@app.route("/events")
def events_list():
<<<<<<< HEAD
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
=======
    sort_by = request.args.get('sort', 'event_date')
    order = request.args.get('order', 'desc')
    search_query = request.args.get('search', '').strip()

    valid_columns = ['event_id', 'event_name', 'event_type', 'location', 'event_date']
    if sort_by not in valid_columns:
        sort_by = 'event_date'
    if order not in ['asc', 'desc']:
        order = 'asc'

    conn = get_db_connection()
    cursor = conn.cursor()

    if search_query:
        query = f"""
            SELECT event_id, event_name, event_type, location, event_date
            FROM events
            WHERE event_name LIKE %s OR event_type LIKE %s OR location LIKE %s OR event_date LIKE %s
            ORDER BY {sort_by} {order.upper()}
        """
        like_query = f"%{search_query}%"
        cursor.execute(query, (like_query, like_query, like_query, like_query))
    else:
        query = f"""
            SELECT event_id, event_name, event_type, location, event_date
            FROM events
            ORDER BY {sort_by} {order.upper()}
        """
        cursor.execute(query)

    event_records = cursor.fetchall()

    cursor.close()
    conn.close()

    next_order = 'asc' if order == 'desc' else 'desc'
    return render_template(
        'event.html',
        event=event_records,
        sort_by=sort_by,
        order=order,
        next_order=next_order,
        search_query=search_query
    )



#add Events
@app.route('/add-event', methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
        event_name = request.form['event_name']
        event_type = request.form['event_type']
        event_date = request.form['event_date']
        location = request.form['location']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO events (event_name, event_type, event_date, location) VALUES (%s, %s, %s, %s)",
            (event_name, event_type, event_date, location)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('events_list'))

    return render_template('add_event.html')


#edit Events 
@app.route('/edit-event/<int:event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
     if request.method == 'POST':
        event_name=request.form['event_name']
        event_type=request.form['event_type']
        event_date=request.form['event_date']
        location=request.form['location']

        conn = get_db_connection()
        cursor=conn.cursor()
        cursor.execute("UPDATE events SET event_name=%s, event_type=%s,"
        "event_date=%s, location=%s, WHERE event_id=%s",(event_name, event_type, event_date, location,event_id))
        conn.commit()
        conn.close()
        return redirect(url_for('events_list'))
     #GET -get request to load the existing employee info
     conn=get_db_connection()
     cursor=conn.cursor()
     cursor.execute("SELECT * FROM events WHERE event_id = %s",(event_id,))
     event=cursor.fetchone()
     conn.close()

     if event is None:
        return "Event not found", 404
     return render_template('edit_event.html', event=event)

#delete events
@app.route('/delete-event/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM events WHERE event_id=%s", (event_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('events_list'))

#show time logs 
@app.route("/time_logs")
def time_logs():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT tl.log_id, e.first_name, e.last_name, tl.clock_in, tl.clock_out
        FROM time_logs tl
        JOIN employees e ON tl.employee_id = e.employee_id
        ORDER BY tl.clock_in DESC
    """)
    logs = cursor.fetchall()

    # For dropdown list of employees
    cursor.execute("SELECT employee_id, first_name, last_name FROM employees")
    employees = cursor.fetchall()

    conn.close()
    return render_template("time_logs.html", logs=logs, employees=employees)


#clock in route 
@app.route("/clock_in/<int:employee_id>", methods=["POST"])
def clock_in(employee_id):
    now = datetime.now()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO time_logs (employee_id, clock_in) VALUES (%s, %s)", (employee_id, now))
    conn.commit()
    conn.close()
    return redirect(url_for('time_logs'))


# Clock Out route
@app.route("/clock_out/<int:employee_id>", methods=["POST"])
def clock_out(employee_id):
    now = datetime.now()
    conn = get_db_connection()
    cursor = conn.cursor()
    # Update the most recent entry without clock_out
    cursor.execute("""
        UPDATE time_logs
        SET clock_out = %s
        WHERE employee_id = %s AND clock_out IS NULL
        ORDER BY clock_in DESC
        LIMIT 1
    """, (now, employee_id))
    conn.commit()
    conn.close()
    return redirect(url_for('time_logs'))


@app.route("/handle_clock", methods=["POST"])
def handle_clock():
    employee_id = request.form.get("employee_id")
    now = datetime.now()

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if there's an open shift (clock_out IS NULL)
    cursor.execute("""
        SELECT log_id FROM time_logs
        WHERE employee_id = %s AND clock_out IS NULL
    """, (employee_id,))
    open_log = cursor.fetchone()

    if open_log:
        # If open shift exists, clock out (update clock_out)
        cursor.execute("""
            UPDATE time_logs
            SET clock_out = %s
            WHERE log_id = %s
        """, (now, open_log[0]))
        message = "Clocked out successfully."
    else:
        # If no open shift, clock in (insert new)
        cursor.execute("""
            INSERT INTO time_logs (employee_id, clock_in)
            VALUES (%s, %s)
        """, (employee_id, now))
        message = "Clocked in successfully."

    conn.commit()
    conn.close()

    return message

#Payroll-report- based on employee working hours 
@app.route("/payroll-report")
def payroll_report():
    start=request.args.get("start")
    end=request.args.get("end")
    employee_id=request.args.get("emplotee_id")

    conn=get_db_connection()
    cursor=conn.cursor()

    query="""
        SELECT ws.summary_id, e.first_name, e.last_name,
               ws.week_start, ws.week_end, ws.total_hours,
               p.gross_pay, p.tax_deduction, p.net_pay
        FROM weekly_summary ws
        JOIN employees e ON ws.employee_id = e.employee_id
        JOIN payroll p ON ws.summary_id = p.summary_id
        WHERE ws.week_start >= %s AND ws.week_end <= %s
    """
    params=[start, end]
    if employee_id:
        query+='AND e.employee_id=%s'
        params.append(employee_id)

        
    cursor.execute(query, tuple(params))
    payroll_data = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("payroll_report.html", payroll=payroll_data)
>>>>>>> 157e5ca (Initial clean commit without passwords)

if __name__=='__main__':
    app.run(debug=True)

