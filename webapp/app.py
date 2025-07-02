from flask import Flask, render_template, session,flash
from models.database import get_db_connection
from flask import request, redirect, url_for
from datetime import datetime, timedelta
import mysql.connector
from collections import defaultdict
from datetime import datetime, date
from flask_login import LoginManager
from flask_login import UserMixin
from flask_login import login_user
import hashlib 
from flask_login import logout_user, login_required
from flask_login import current_user
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from models.database import get_db_connection
import os


app = Flask(__name__)
# --- Security Settings ---
# Use an environment variable for the secret key (never hardcode in production!)
app.secret_key = os.environ.get('SECRET_KEY', 'dev_secret_key')
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=False,  # Set to True in production with HTTPS
    SESSION_COOKIE_SAMESITE='Lax'
)

# --- Extensions ---
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'
limiter = Limiter(key_func=get_remote_address)
limiter.init_app(app)

@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("admin_dashboard"))
    return render_template("index.html")



@app.route('/employees')
@login_required
def employee_list():
    search_query = request.args.get('search', '').strip()
    conn = get_db_connection()
    cursor = conn.cursor()
    if search_query:
        query = """
            SELECT employee_id, first_name, last_name, department, email
            FROM employees
            WHERE company_id=%s AND (first_name LIKE %s OR last_name LIKE %s OR department LIKE %s)
        """
        like_query = f"%{search_query}%"
        cursor.execute(query, (current_user.company_id, like_query, like_query, like_query))
    else:
        cursor.execute("SELECT employee_id, first_name, last_name, department, email FROM employees WHERE company_id = %s",
                       (current_user.company_id,))
    employees = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('employees.html', employees=employees, search_query=search_query)

@app.route('/add-employee', methods=['GET', 'POST'])
@login_required
def add_employee():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        department = request.form['department']
        email = request.form['email']
        hire_date = request.form['hire_date']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO employees (first_name, last_name, department, email, hire_date, company_id) VALUES (%s, %s, %s, %s, %s, %s)",
                       (first_name, last_name, department, email, hire_date, current_user.company_id))
        conn.commit()
        conn.close()
        return redirect(url_for('employee_list'))
    return render_template('add_employee.html')

@app.route('/edit-employee/<int:employee_id>', methods=['GET', 'POST'])
@login_required
def edit_employee(employee_id):
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        department = request.form['department']
        email = request.form['email']
        hire_date = request.form['hire_date']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE employees SET first_name=%s, last_name=%s, department=%s, email=%s, hire_date=%s WHERE employee_id=%s AND company_id = %s",
                       (first_name, last_name, department, email, hire_date, employee_id, current_user.company_id))
        conn.commit()
        conn.close()
        return redirect(url_for('employee_list'))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees WHERE employee_id = %s AND company_id = %s", (employee_id, current_user.company_id))
    employee = cursor.fetchone()
    conn.close()
    return render_template('edit_employee.html', employee=employee)

@app.route('/delete-employee/<int:employee_id>', methods=['POST'])
@login_required
def delete_employee(employee_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employees WHERE employee_id=%s AND company_id=%s", (employee_id,current_user.company_id))
    conn.commit()
    conn.close()
    return redirect(url_for('employee_list'))

@app.route("/attendance")
@login_required
def attendance_list():
    sort_by = request.args.get('sort', 'timestamp')
    order = request.args.get('order', 'desc')
    search_query = request.args.get('search', '').strip()
    valid_columns = ['attendance_id', 'employee_id', 'event_id', 'attended', 'timestamp']
    if sort_by not in valid_columns:
        sort_by = 'timestamp'
    if order not in ['asc', 'desc']:
        order = 'desc'
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
    WHERE e.company_id = %s
"""
    filters = []
    params = [current_user.company_id]
    if search_query:
        filters.append("(CONCAT(e.first_name, ' ', e.last_name) LIKE %s OR ev.event_name LIKE %s)")
        params.extend([f"%{search_query}%", f"%{search_query}%"])
    if filters:
        query += " WHERE " + " AND ".join(filters)
    sort_columns_map = {
        'attendance_id': 'a.attendance_id',
        'employee_name': "employee_name",
        'event_name': 'ev.event_name',
        'attended': 'a.attended',
        'timestamp': 'a.timestamp'
    }
    query += f" ORDER BY {sort_columns_map.get(sort_by, 'a.timestamp')} {order.upper()}"
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    attendance_records = cursor.fetchall()
    summary = None
    if search_query:
        summary = {}
        for record in attendance_records:
            name = record[1]
            if name not in summary:
                summary[name] = {"total": 0, "present": 0}
            summary[name]["total"] += 1
            if record[3]:
                summary[name]["present"] += 1
    cursor.close()
    conn.close()
    next_order = 'asc' if order == 'desc' else 'desc'
    return render_template('attendance.html',
                           attendance=attendance_records,
                           sort_by=sort_by,
                           order=order,
                           next_order=next_order,
                           search_query=search_query,
                           summary=summary
                           )

@app.route("/events")
@login_required
def events_list():
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
            WHERE company_id = %s AND (event_name LIKE %s OR event_type LIKE %s OR location LIKE %s OR event_date LIKE %s)
            ORDER BY {sort_by} {order.upper()}
        """
        like_query = f"%{search_query}%"
        cursor.execute(query, (current_user.company_id, like_query, like_query, like_query, like_query))

    else:
        query = f"""
            SELECT event_id, event_name, event_type, location, event_date
            FROM events
            WHERE company_id = %s
            ORDER BY {sort_by} {order.upper()}
        """
        cursor.execute(query,  (current_user.company_id,))
    event_records = cursor.fetchall()
    cursor.close()
    conn.close()
    next_order = 'asc' if order == 'desc' else 'desc'
    return render_template('event.html',
                           event=event_records,
                           sort_by=sort_by,
                           order=order,
                           next_order=next_order,
                           search_query=search_query
                           )

@app.route('/add-event', methods=['GET', 'POST'])
@login_required
def add_event():
    if request.method == 'POST':
        event_name = request.form['event_name']
        event_type = request.form['event_type']
        event_date = request.form['event_date']
        location = request.form['location']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO events (event_name, event_type, event_date, location, company_id) VALUES (%s, %s, %s, %s, %s)",
            (event_name, event_type, event_date, location, current_user.company_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('events_list'))
    return render_template('add_event.html')

@app.route('/edit-event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    if request.method == 'POST':
        event_name = request.form['event_name']
        event_type = request.form['event_type']
        event_date = request.form['event_date']
        location = request.form['location']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE events SET event_name=%s, event_type=%s, event_date=%s, location=%s WHERE event_id=%s AND company_id=%s",
                       (event_name, event_type, event_date, location, event_id, current_user.company_id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('events_list'))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events WHERE event_id = %s AND company_id = %s", (event_id, current_user.company_id))
    event = cursor.fetchone()
    cursor.close()
    conn.close()
    if event is None:
        return "Event not found", 404
    return render_template('edit_event.html', event=event)

@app.route('/delete-event/<int:event_id>', methods=['POST'])
@login_required
def delete_event(event_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM events WHERE event_id=%s AND company_id=%s", (event_id,current_user.company_id))
    conn.commit()
    conn.close()
    return redirect(url_for('events_list'))

@app.route("/time_logs")
@login_required
def time_logs():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT tl.log_id, e.first_name, e.last_name, tl.clock_in, tl.clock_out
    FROM time_logs tl
    JOIN employees e ON tl.employee_id = e.employee_id
    WHERE e.company_id = %s
    ORDER BY tl.clock_in DESC
""", (current_user.company_id,))

    logs = cursor.fetchall()
    cursor.execute("SELECT employee_id, first_name, last_name FROM employees WHERE company_id = %s", (current_user.company_id,))
    employees = cursor.fetchall()
    conn.close()
    return render_template("time_logs.html", logs=logs, employees=employees)

@app.route("/clock_in/<int:employee_id>", methods=["POST"])
@login_required
def clock_in(employee_id):
    now = datetime.now()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO time_logs (employee_id, clock_in) VALUES (%s, %s)", (employee_id, now))
    conn.commit()
    conn.close()
    return redirect(url_for('time_logs'))

@app.route("/clock_out/<int:employee_id>", methods=["POST"])
@login_required
def clock_out(employee_id):
    now = datetime.now()
    conn = get_db_connection()
    cursor = conn.cursor()
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
@login_required
def handle_clock():
    employee_id = int(request.form.get("employee_id"))
    now = datetime.now()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT log_id FROM time_logs
        WHERE employee_id = %s AND clock_out IS NULL
    """, (employee_id,))
    open_log = cursor.fetchone()
    if open_log:
        cursor.execute("""
            UPDATE time_logs
            SET clock_out = %s
            WHERE log_id = %s
        """, (now, open_log[0]))
        message = "Clocked out successfully."
    else:
        cursor.execute("""
            INSERT INTO time_logs (employee_id, clock_in)
            VALUES (%s, %s)
        """, (employee_id, now))
        message = "Clocked in successfully."
    conn.commit()
    conn.close()
    return message

# @app.route("/payroll-report")
# def payroll_report():
#     start = request.args.get("start")
#     end = request.args.get("end")
#     employee_id = request.args.get("employee_id")

#     conn = get_db_connection()
#     cursor = conn.cursor()

#     base_query = """SELECT ws.employee_id, CONCAT(e.first_name, ' ', e.last_name) AS full_name,
#                     ws.week_start, ws.week_end, ws.total_hours, ws.gross_pay, ws.tax, ws.net_pay
#                     FROM weekly_summary ws
#                     JOIN employees e ON ws.employee_id = e.employee_id
#                  """
#     conditions = []
#     params = []

#     if start and end:
#         conditions.append("ws.week_start >= %s AND ws.week_end <= %s")
#         params.extend([start, end])

#     if employee_id:
#         conditions.append("ws.employee_id = %s")
#         params.append(employee_id)

#     if conditions:
#         base_query += " WHERE " + " AND ".join(conditions)

#     cursor.execute(base_query, tuple(params))
#     payroll_data = cursor.fetchall()
#     cursor.close()
#     conn.close()

#     # group by month-year
#     grouped_payroll = defaultdict(list)
#     for row in payroll_data:
#         week_start = row[2]
#         if isinstance(week_start, str):
#             week_start = datetime.strptime(week_start, '%Y-%m-%d')
#         elif isinstance(week_start, date):
#             week_start = datetime.combine(week_start, datetime.min.time())
#         month_year = week_start.strftime('%B %Y')
#         grouped_payroll[month_year].append(row)

#     return render_template("payroll_report.html", grouped_payroll=grouped_payroll)

# # calculate payroll for a given week 
# def calculate_weekly_payroll(week_start_date):
#     # Calculate week_end_date as 6 days after week_start_date
#     week_end_date = week_start_date + timedelta(days=6)
    
#     conn = get_db_connection()
#     cursor = conn.cursor()
    
#     # Get all employees
#     cursor.execute("SELECT employee_id FROM employees")
#     employees = cursor.fetchall()
    
#     for (employee_id,) in employees:
#         # Sum total hours worked by this employee between week_start and week_end
#         cursor.execute("""
#             SELECT clock_in, clock_out FROM time_logs
#             WHERE employee_id = %s
#               AND clock_in >= %s AND clock_in <= %s
#               AND clock_out IS NOT NULL
#         """, (employee_id, week_start_date, week_end_date))
        
#         logs = cursor.fetchall()
        
#         total_seconds = 0
#         for clock_in, clock_out in logs:
#             # Calculate seconds worked this shift
#             delta = clock_out - clock_in
#             total_seconds += delta.total_seconds()
        
#         total_hours = total_seconds / 3600
        
#         # Example pay calculation:
#         hourly_rate = 20.25
#         gross_pay = total_hours * hourly_rate
#         tax = gross_pay * 0.1  # 10% tax example
#         net_pay = gross_pay - tax
        
#         # Check if record exists for this week & employee
#         cursor.execute("""
#             SELECT summary_id FROM weekly_summary
#             WHERE employee_id = %s AND week_start = %s AND week_end = %s
#         """, (employee_id, week_start_date, week_end_date))
        
#         record = cursor.fetchone()
#         if record:
#             # Update existing
#             cursor.execute("""
#                 UPDATE weekly_summary
#                 SET total_hours=%s, gross_pay=%s, tax=%s, net_pay=%s
#                 WHERE summary_id=%s
#             """, (total_hours, gross_pay, tax, net_pay, record[0]))
#         else:
#             # Insert new record
#             cursor.execute("""
#                 INSERT INTO weekly_summary (employee_id, week_start, week_end, total_hours, gross_pay, tax, net_pay)
#                 VALUES (%s, %s, %s, %s, %s, %s, %s)
#             """, (employee_id, week_start_date, week_end_date, total_hours, gross_pay, tax, net_pay))
    
#     conn.commit()
#     cursor.close()
#     conn.close()

@app.route("/work-hours-summary")
@login_required
def work_hours_summary():
    start = request.args.get("start")
    end = request.args.get("end")
    employee_id = request.args.get("employee_id")

    conn = get_db_connection()
    cursor = conn.cursor()

    base_query = """SELECT ws.employee_id, CONCAT(e.first_name, ' ', e.last_name) AS full_name,
                ws.week_start, ws.week_end, ws.total_hours
                FROM weekly_summary ws
                JOIN employees e ON ws.employee_id = e.employee_id
                WHERE e.company_id = %s
             """
    params = [current_user.company_id]
    
    if start and end and start.strip() != "" and end.strip() != "":
        base_query += " AND ws.week_start >= %s AND ws.week_end <= %s"
        params.extend([start, end])
    if employee_id:
        base_query += " AND ws.employee_id = %s"
        params.append(employee_id)


    cursor.execute(base_query, tuple(params))
    summary_data = cursor.fetchall()
    cursor.close()
    conn.close()

    # Group by month-year
    grouped_summary = defaultdict(list)
    for row in summary_data:
        week_start = row[2]
        if isinstance(week_start, str):
            week_start = datetime.strptime(week_start, '%Y-%m-%d')
        elif isinstance(week_start, date):
            week_start = datetime.combine(week_start, datetime.min.time())
        month_year = week_start.strftime('%B %Y')
        grouped_summary[month_year].append(row)

    return render_template("work_hours_summary.html", grouped_summary=grouped_summary)

#admin-sign up 
@app.route("/admin-register", methods=["GET", "POST"])
def admin_register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        company_name = request.form["company_name"].strip().lower()

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if username is taken
        cursor.execute("SELECT * FROM admins WHERE username = %s", (username,))
        if cursor.fetchone():
            flash("Username already taken.", "danger")
            conn.close()
            return render_template("admin_register.html")

        # Check if company exists, else create it
        cursor.execute("SELECT company_id FROM companies WHERE company_name = %s", (company_name,))
        company = cursor.fetchone()
        if company:
            company_id = company[0]
        else:
            cursor.execute("INSERT INTO companies (company_name) VALUES (%s)", (company_name,))
            company_id = cursor.lastrowid

        # Hash password with bcrypt
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

        cursor.execute(
            "INSERT INTO admins (username, password_hash, company_id) VALUES (%s, %s, %s)",
            (username, password_hash, company_id)
        )

        conn.commit()
        conn.close()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("admin_login"))

    return render_template("admin_register.html")

#flask-login 
class Admin(UserMixin):
    def __init__(self, id, username, password_hash, company_id):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.company_id = company_id

#admin loader function 
@login_manager.user_loader
def load_user(admin_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admins WHERE id = %s", (admin_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Admin(id=row[0], username=row[1], password_hash=row[2], company_id=row[3])
    return None

@app.route("/admin-login", methods=["GET", "POST"])
@limiter.limit("5 per minute")  # 5 login attempts per minute per IP
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admins WHERE username = %s", (username,))
        row = cursor.fetchone()
        conn.close()

        if row and bcrypt.check_password_hash(row[2], password):
            admin = Admin(id=row[0], username=row[1], password_hash=row[2], company_id=row[3])
            login_user(admin)
            return redirect(url_for("admin_dashboard"))

        flash("Invalid username or password.", "danger")

    return render_template("admin_login.html")

#logging out -sign out 
@app.route("/logout")
@login_required
def logout():
    logout_user()  # from flask_login
    return redirect(url_for('home'))  # or the name of your homepage route

@app.route("/admin-dashboard")
@login_required
def admin_dashboard():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT company_name FROM companies WHERE company_id = %s", (current_user.company_id,))
    row = cursor.fetchone()
    conn.close()

    company_name = row[0] if row else "Unknown Company"
    return render_template("admin_dashboard.html", company_name=company_name)


if __name__ == '__main__':
    app.run(debug=True)
