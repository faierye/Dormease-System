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
    cur = mysql.connection.cursor()

    # your existing stats...
    cur.execute("SELECT COUNT(*) FROM residents_tb")
    total_residents = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM applications_tb WHERE status='Pending'")
    pending_applications = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM beds_tb WHERE status='Available'")
    available_beds = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM payment_tb WHERE status='Pending'")
    pending_payments = cur.fetchone()[0]

    # 🔥 GET CURRENT PERIOD (latest one)
    cur.execute("SELECT period_id, name, start_date, end_date, status FROM application_period ORDER BY period_id DESC LIMIT 1")
    period = cur.fetchone()

    cur.close()

    return render_template(
        'dashboard.html',
        total_residents=total_residents,
        pending_applications=pending_applications,
        available_beds=available_beds,
        pending_payments=pending_payments,
        period=period
    )

#Application Period Management
@app.route('/manage_period', methods=['POST'])
def manage_period():
    id = request.form.get('id')
    name = request.form['name']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    status = request.form['status']

    cur = mysql.connection.cursor()

    if id:  # 🔥 UPDATE
        cur.execute("""
            UPDATE application_period
            SET name=%s, start_date=%s, end_date=%s, status=%s
            WHERE id=%s
        """, (name, start_date, end_date, status, id))
    else:  # 🔥 INSERT
        cur.execute("""
            INSERT INTO application_period (name, start_date, end_date, status)
            VALUES (%s, %s, %s, %s)
        """, (name, start_date, end_date, status))

    mysql.connection.commit()
    cur.close()

    return redirect('/dashboard')

#Residents
@app.route('/residents')
def residents():

    applicant_type = request.args.get('applicant_type', 'all')
    sex = request.args.get('sex', 'all')

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    query = """
        SELECT a.applicant_number,
               CONCAT_WS(' ', a.first_name, a.middle_name, a.last_name, a.extension_name) AS full_name,
               a.contact_number,
               a.email,
               a.applicant_type,
               COALESCE(s.student_number, e.employee_number) AS id_number,
               COALESCE(s.program, e.department, 'N/A') AS assigned_room,
               a.sex
        FROM applications_tb a
        LEFT JOIN student_info s ON a.application_id = s.application_id
        LEFT JOIN employee_info e ON a.application_id = e.application_id
        WHERE a.status = 'Approved'
    """

    params = []

    if applicant_type != 'all':
        query += " AND a.applicant_type = %s"
        params.append(applicant_type)

    if sex != 'all':
        query += " AND a.sex = %s"
        params.append(sex)

    cur.execute(query, params)
    data = cur.fetchall()
    cur.close()

    return render_template('residents.html', residents=data, applicant_type=applicant_type, sex=sex)

#Application Details
@app.route('/applications')
def applications():
    applicant_type = request.args.get('applicant_type', 'all')
    sex = request.args.get('sex', 'all')

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    query = "SELECT * FROM applications_tb WHERE 1=1"
    params = []

    if applicant_type != 'all':
        query += " AND applicant_type = %s"
        params.append(applicant_type)

    if sex != 'all':
        query += " AND sex = %s"
        params.append(sex)

    cur.execute(query, params)
    data = cur.fetchall()
    cur.close()

    return render_template('applications.html', applications=data)

# Applicant Detail Page
@app.route('/application/<int:app_id>')
def application_detail(app_id):

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Get application details
    cur.execute("""
        SELECT * FROM applications_tb 
        WHERE application_id = %s
    """, (app_id,))

    application = cur.fetchone()
    
    if not application:
        cur.close()
        return redirect(url_for('applications'))
    
    # Get student or employee info
    if application['applicant_type'].lower() == 'Student':
        cur.execute("""
            SELECT * FROM student_info 
            WHERE application_id = %s
        """, (app_id,))

        info = cur.fetchone()

    else:
        cur.execute("""
            SELECT * FROM employee_info 
            WHERE application_id = %s
        """, (app_id,))

        info = cur.fetchone()
    
    # Get uploaded file
    cur.execute("""
        SELECT file_name FROM requirements_tb 
        WHERE application_id = %s 
        LIMIT 1
    """, (app_id,))

    file_data = cur.fetchone()
    
    # Get interview schedule data
    cur.execute("""
        SELECT status, interview_date, interview_time FROM interview_sched 
        WHERE application_id = %s 
    """, (app_id,))

    interview_data = cur.fetchone()
    
    cur.close()
    
    return render_template('application_detail.html', 
                           application=application, 
                           info=info,
                           file_data=file_data,
                           interview_data=interview_data)

# Get Applicant Info (Student/Employee Details) MODAL
@app.route('/get_applicant_info/<int:app_id>')
def get_applicant_info(app_id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Get application details FIRST (including status)
    cur.execute("""
        SELECT applicant_type, status FROM applications_tb 
        WHERE application_id = %s
    """, (app_id,))
    application = cur.fetchone()
    
    if not application:
        cur.close()
        return {'success': False, 'message': 'Application not found'}
    
    # Get student or employee info
    if application['applicant_type'].lower() == 'student':
        cur.execute("""
            SELECT student_number, program, year_level 
            FROM student_info 
            WHERE application_id = %s
        """, (app_id,))
    else:
        cur.execute("""
            SELECT employee_number, department, position 
            FROM employee_info 
            WHERE application_id = %s
        """, (app_id,))
    
    info = cur.fetchone()
    cur.close()
    
    if info:
        info['success'] = True
        info['status'] = application['status']  # ADD THIS LINE
        return info
    else:
        return {'success': True, 'status': application['status']}

#SCHEDULE INTERVIEW
@app.route('/schedule_interview', methods=['POST'])
def schedule_interview():
    data = request.get_json()
    app_id = data.get('application_id')
    interview_date = data.get('interview_date')
    interview_time = data.get('interview_time')
    
    cur = mysql.connection.cursor()
    
    # MAGIC: Updates OR inserts - NO DUPLICATES EVER!
    cur.execute("""
        INSERT INTO interview_sched (application_id, interview_date, interview_time, status)
        VALUES (%s, %s, %s, 'scheduled')
        ON DUPLICATE KEY UPDATE 
            interview_date = VALUES(interview_date),
            interview_time = VALUES(interview_time),
            status = 'scheduled',
            updated_at = CURRENT_TIMESTAMP
    """, (app_id, interview_date, interview_time))
    
    rows_affected = cur.rowcount  # 1=insert, 2=update
    print(f"Interview updated: {rows_affected} rows affected")
    
    # Update application status
    cur.execute("UPDATE applications_tb SET status = 'For_Interview' WHERE application_id = %s", (app_id,))
    
    mysql.connection.commit()
    cur.close()
    
    return {'success': True, 'message' :f'Interview {"created" if rows_affected == 1 else "updated"}!'}

# Update Interview Status
@app.route('/update_interview_status', methods=['POST'])
def update_interview_status():
    data = request.get_json()
    app_id = data.get('application_id')
    interview_status = data.get('interview_status')  # 'scheduled', 'completed', or 'no show'
    
    cur = mysql.connection.cursor()
    
    cur.execute("""
        UPDATE interview_sched 
        SET status = %s
        WHERE application_id = %s
    """, (interview_status, app_id))
    
    mysql.connection.commit()
    cur.close()
    
    return {'success': True, 'message': f'Interview status updated to {interview_status}'}

# Update Application Status
@app.route('/update_application_status', methods=['POST'])
def update_application_status():
    data = request.get_json()
    app_id = data.get('application_id')
    status = data.get('status')  # 'approved' or 'rejected'
    
    cur = mysql.connection.cursor()
    
    cur.execute("""
        UPDATE applications_tb 
        SET application_status = %s
        WHERE application_id = %s
    """, (status, app_id))
    
    mysql.connection.commit()
    cur.close()
    
    return {'success': True, 'message': f'Application {status} successfully'}

if __name__ == '__main__':
    app.run( debug=True) 