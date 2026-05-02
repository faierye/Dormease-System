from flask import Flask, request, render_template, redirect, url_for, flash
from flask_mysqldb import MySQL
from config import Config
import MySQLdb.cursors
import os
import uuid
import datetime

app = Flask(__name__)
app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.secret_key = "secret123"

mysql = MySQL(app)

#Landing Page

@app.route('/')
def home():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT status, name, start_date, end_date
        FROM application_period
        ORDER BY period_id DESC LIMIT 1
    """)
    period = cur.fetchone()
    cur.close()

    if not period:
        return render_template(
            'index.html', 
            period_status = "No active application",
            show_apply = False
        )

    status, name, start_date, end_date = period
    
    if status == 'Open':
        period_status = f"{name} ({start_date} - {end_date})"
        show_apply = True
    elif status == 'Closed':
        period_status = "Application ended"
        show_apply = False
    else:  # UPCOMING
        period_status = f"Opens Soon: {name}  ({start_date} - {end_date})"
        show_apply = False

    return render_template(
        'index.html',
        period_status=period_status,
        show_apply=show_apply
    )

@app.errorhandler(405)
def method_not_allowed(error):
    return render_template('access_denied.html'), 405

#Application Form

@app.route('/application', methods = ['POST'])
def application():
    if request.method == 'POST':

        cur = mysql.connection.cursor()

        cur.execute("""
            SELECT period_id, name
            FROM application_period
            WHERE status = 'OPEN'
        """)

        period = cur.fetchone()

        if not period:
            return render_template(
                "application.html",
                success=False,
                error=True,
                message="No open application period. Please check back later.",
                period_name="No active application"
            )

        period_id = period[0]
        period_name = period[1]

        #GET DATA
        first_name = request.form['first_name']
        middle_name = request.form['middle_name']
        last_name = request.form['last_name']
        extension_name = request.form['extension_name']
        age = request.form['age']
        sex = request.form['sex']
        contact_number = request.form['contact_number']
        email = request.form['email']
        permanent_address= request.form['permanent_address']
        current_address = request.form['current_address']
        applicant_type = request.form['applicant_type']
        
        cur.execute("""
            SELECT * FROM applications_tb 
            WHERE contact_number=%s AND period_id=%s
        """, (contact_number, period_id))

        #ERROR
        existing = cur.fetchone()

        if existing:
            return render_template(
                "application.html",
                success=False,
                error=True,
                message="You already applied for this semester.",
                period_name=period_name
            )

        cur.execute("""
            INSERT INTO applications_tb 
            (first_name, middle_name, last_name, extension_name, age, sex, contact_number, email, permanent_address, current_address, applicant_type, period_id) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            first_name, middle_name, last_name, extension_name, age, sex,
            contact_number, email, permanent_address, current_address, applicant_type, period_id))

        mysql.connection.commit()

        # GET ID
        application_id = cur.lastrowid

        # GENERATE NUMBER
        
        year = datetime.datetime.now().year
        applicant_number = f"APP-{year}-{str(application_id).zfill(4)}"

        # UPDATE
        cur.execute("""
            UPDATE applications_tb
            SET applicant_number = %s
            WHERE application_id = %s
        """, (applicant_number, application_id))

        mysql.connection.commit()

        #STUDENT
        if applicant_type == "student":
            student_number = request.form['student_number']
            program = request.form['program']
            year_level = request.form['year_level']

            cur.execute("""
                INSERT INTO student_info 
                (application_id, student_number, program, year_level)
                VALUES (%s, %s, %s, %s)
            """, (application_id, student_number, program, year_level))

            # FILE
            file = request.files['enrollment_slip']
            if file and file.filename != "":
                unique_name = str(uuid.uuid4()) + "_" + file.filename
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
                file.save(filepath)

                cur.execute("""
                    INSERT INTO requirements_tb (application_id, file_name, file_type)
                    VALUES (%s, %s, %s)
                """, (application_id, unique_name, 'Enrollment'))

        #EMPLOYEE
        elif applicant_type == "employee":
            employee_number = request.form['employee_number']
            department = request.form['department']
            position = request.form['position']

            cur.execute("""
                INSERT INTO employee_info
                (application_id, employee_number, department, position)
                VALUES (%s, %s, %s, %s)
            """, (application_id, employee_number, department, position))

            # FILE
            file = request.files['certificate']
            if file and file.filename != "":
                unique_name = str(uuid.uuid4()) + "_" + file.filename
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
                file.save(filepath)

                cur.execute("""
                    INSERT INTO requirements_tb (application_id, file_name, file_type)
                    VALUES (%s, %s, %s)
                """, (application_id, unique_name, 'Employment'))     

        mysql.connection.commit()
        cur.close()

        #SUCCESS
        return render_template(
            "application.html",
            success=True,
            error=False,
            name=first_name,
            applicant_number=applicant_number,
            period_name=period_name
        )
        
    else:
        return redirect(url_for('home'))

#Direct to app form
@app.route('/apply', methods = ['GET'])
def apply_form():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT status, name, start_date, end_date
        FROM application_period ORDER BY period_id DESC LIMIT 1
    """)
    period = cur.fetchone()
    cur.close()
    
    if not period or period[0] != 'Open':
        return render_template(
            'application.html', 
            error = True, 
            message = "Applications not open yet!"
        )
    
    return render_template('application.html', success=False, error=False)

#Login Form
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return "Please fill in all fields!"

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM admin_tb WHERE username=%s AND password=%s",
                    (username, password))
        user = cur.fetchone()
        cur.close()
        
        if user:
            return redirect(url_for('dashboard')) # later: redirect
        else:
            flash("Invalid username or password!")
            return redirect(url_for('login'))  # go back to login page

    return render_template('login.html')

#Dashboard
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

#Application Period Management
@app.route('/manage_period', methods=['POST'])
def manage_period():
    if request.method == 'POST':
        name = request.form['name']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        status = request.form['status']

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO application_period (name, start_date, end_date, status)
            VALUES (%s, %s, %s, %s)
        """, (name, start_date, end_date, status))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('dashboard'))

#Residents
@app.route('/residents')
def residents():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("""
        SELECT a.applicant_number, a.first_name, a.last_name, s.student_number, s.program, s.year_level
        FROM applications_tb a
        JOIN student_info s ON a.application_id = s.application_id
        WHERE a.applicant_type = 'student'
    """)
    students = cur.fetchall()
    cur.close()

    return render_template('residents.html', students=students)


if __name__ == '__main__':
    app.run( debug=True) 