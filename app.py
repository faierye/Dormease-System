from flask import Flask, request, render_template, redirect, url_for, flash
from flask_mysqldb import MySQL
from config import Config
import MySQLdb.cursors
import os
import uuid
import datetime
import smtplib
import requests as http_requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)
app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.secret_key = "secret123"

mysql = MySQL(app)

# ─── EMAIL HELPERS ────────────────────────────────────────────────────────────

def _send_email(to_email, subject, html):
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From']    = app.config['MAIL_FROM']
        msg['To']      = to_email
        msg.attach(MIMEText(html, 'html'))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(app.config['GMAIL_USER'], app.config['GMAIL_PASSWORD'])
            server.sendmail(app.config['GMAIL_USER'], to_email, msg.as_string())
        return True
    except Exception as e:
        print(f"[Email Error] {e}")
        return False


def _email_wrapper(title, accent, body_html):
    return f"""
    <div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;
                background:#f9f9f9;border-radius:12px;overflow:hidden;
                border:1px solid #e0e0e0;">
        <div style="background:#3b3b98;padding:28px 30px;text-align:center;">
            <h1 style="color:white;margin:0;font-size:22px;letter-spacing:1px;">DormEase</h1>
            <p style="color:rgba(255,255,255,0.75);margin:6px 0 0;font-size:13px;">
                Dormitory Management System
            </p>
        </div>
        <div style="padding:32px 30px;background:white;">
            <div style="background:{accent};border-radius:8px;padding:12px 18px;
                        margin-bottom:24px;font-weight:600;font-size:15px;color:white;">
                {title}
            </div>
            {body_html}
        </div>
        <div style="background:#f5f5f5;padding:14px 30px;text-align:center;
                    border-top:1px solid #e8e8e8;">
            <p style="color:#aaa;font-size:11px;margin:0;">
                This is an automated message from DormEase. Please do not reply.
            </p>
        </div>
    </div>
    """


def _fmt_date(date_str):
    try:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d").strftime("%B %d, %Y")
    except Exception:
        return date_str


def _fmt_time(time_str):
    try:
        return datetime.datetime.strptime(time_str, "%H:%M").strftime("%I:%M %p")
    except Exception:
        return time_str


def send_interview_email(applicant, interview_date, interview_time):
    name         = f"{applicant['first_name']} {applicant['last_name']}"
    date_display = _fmt_date(interview_date)
    time_display = _fmt_time(interview_time)

    body = f"""
        <p style="font-size:15px;color:#333;">Dear <strong>{name}</strong>,</p>
        <p style="color:#555;line-height:1.7;">
            We are pleased to inform you that your interview has been officially scheduled.
            Please see the details below and make sure to arrive on time.
        </p>
        <table style="width:100%;border-collapse:collapse;margin:20px 0;
                      font-size:14px;background:#f5f7ff;border-radius:8px;overflow:hidden;">
            <tr>
                <td style="padding:12px 16px;color:#888;font-weight:600;
                           width:40%;border-bottom:1px solid #e8e8e8;">Interview Date</td>
                <td style="padding:12px 16px;color:#333;
                           border-bottom:1px solid #e8e8e8;"><strong>{date_display}</strong></td>
            </tr>
            <tr>
                <td style="padding:12px 16px;color:#888;font-weight:600;">Interview Time</td>
                <td style="padding:12px 16px;color:#333;"><strong>{time_display}</strong></td>
            </tr>
            <tr>
                <td style="padding:12px 16px;color:#888;font-weight:600;">Interview Place</td>
                <td style="padding:12px 16px;color:#333;"><strong>LNU Dorm Office</strong></td>
            </tr>
        </table>
        <p style="color:#555;line-height:1.7;">
            <strong>Instructions:</strong><br>
            &bull; Arrive at least 10 minutes before your scheduled time.<br>
            &bull; Bring a valid school/company ID.<br>
            &bull; Dress appropriately and professionally.<br>
            &bull; If you cannot attend, please contact the dormitory office as soon as possible.
        </p>
        <p style="color:#555;line-height:1.7;">We look forward to meeting you. Good luck!</p>
        <p style="color:#3b3b98;font-weight:600;margin-top:24px;">— The DormEase Team</p>
    """
    html = _email_wrapper("Interview Scheduled", "#3b3b98", body)
    _send_email(applicant['email'], "Your Interview Has Been Scheduled – DormEase", html)


def send_approved_email(applicant):
    name = f"{applicant['first_name']} {applicant['last_name']}"
    body = f"""
        <p style="font-size:15px;color:#333;">Dear <strong>{name}</strong>,</p>
        <p style="color:#555;line-height:1.7;">
            We are delighted to inform you that your application to DormEase has been
            <strong style="color:#2e7d32;">APPROVED</strong>. Congratulations!
        </p>
        <p style="color:#555;line-height:1.7;">
            You will officially become a resident of the LNU Dormitory. Our team will be in
            touch with the next steps regarding your move-in schedule, room assignment,
            and other important details.
        </p>
        <p style="color:#555;line-height:1.7;">
            <strong>What to expect next:</strong><br>
            &bull; You will be assigned to a room and bed.<br>
            &bull; You will receive information about dormitory rules and payment schedules.<br>
            &bull; Please prepare the required documents for your move-in date.
        </p>
        <p style="color:#555;line-height:1.7;">
            Welcome to the DormEase community! We look forward to having you with us.
        </p>
        <p style="color:#3b3b98;font-weight:600;margin-top:24px;">— The DormEase Team</p>
    """
    html = _email_wrapper("Application Approved", "#2e7d32", body)
    _send_email(applicant['email'], "Congratulations! Your Application is Approved – DormEase", html)


def send_rejected_email(applicant):
    name = f"{applicant['first_name']} {applicant['last_name']}"
    body = f"""
        <p style="font-size:15px;color:#333;">Dear <strong>{name}</strong>,</p>
        <p style="color:#555;line-height:1.7;">
            Thank you for your interest in DormEase and for taking the time to go through
            our application process. After careful review, we regret to inform you that
            your application has <strong style="color:#c62828;">not been approved</strong>
            at this time.
        </p>
        <p style="color:#555;line-height:1.7;">
            This decision does not reflect negatively on you as a person. We encourage you
            to apply again in the next application period, as slots may become available.
        </p>
        <p style="color:#555;line-height:1.7;">
            If you have questions or would like further clarification, please feel free to
            contact the dormitory office directly.
        </p>
        <p style="color:#555;line-height:1.7;">
            Thank you again for your interest, and we wish you all the best.
        </p>
        <p style="color:#3b3b98;font-weight:600;margin-top:24px;">— The DormEase Team</p>
    """
    html = _email_wrapper("Application Not Approved", "#c62828", body)
    _send_email(applicant['email'], "Application Status Update – DormEase", html)


def _get_applicant_for_email(app_id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("""
        SELECT first_name, last_name, email
        FROM applications_tb WHERE application_id = %s
    """, (app_id,))
    applicant = cur.fetchone()
    cur.close()
    return applicant


# ─── SMS HELPERS ──────────────────────────────────────────────────────────────

def _normalize_ph_number(number):
    n = ''.join(filter(str.isdigit, str(number)))
    if n.startswith('0'):
        n = '63' + n[1:]
    if not n.startswith('63'):
        n = '63' + n
    return '+' + n

def _send_sms(to_number, message):
    try:
        number = _normalize_ph_number(to_number)
        response = http_requests.post(
            app.config['SMS_API_URL'],
            headers={
                'x-api-key':    app.config['SMS_API_KEY'],
                'Content-Type': 'application/json',
            },
            json={
                'recipient': number,
                'message':   message,
            },
            timeout=15
        )
        print(f"[SMS] to={number} status={response.status_code} body={response.text[:200]}")
        return response.status_code in (200, 201)
    except Exception as e:
        print(f"[SMS Error] {e}")
        return False

@app.template_filter('format_time')
def format_time(t):
    if t is None:
        return ''
    if isinstance(t, datetime.timedelta):
        total = int(t.total_seconds())
        hours, remainder = divmod(total, 3600)
        minutes = remainder // 60
        ampm = 'AM' if hours < 12 else 'PM'
        hours12 = hours % 12 or 12
        return f'{hours12}:{minutes:02d} {ampm}'
    if hasattr(t, 'strftime'):
        return t.strftime('%I:%M %p')
    return str(t)

# ─── ACTIVITY LOG ─────────────────────────────────────────────────────────────

def _log_activity(action):
    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO activity_log (action) VALUES (%s)", (action,))
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        print(f"[Activity Log Error] {e}")

# Canonical status values — normalises old lowercase DB entries on read
_STATUS_MAP = {
    'approved and done': 'Approved',
    'approved':          'Approved',
    'rejected':          'Rejected',
    'pending':           'Pending',
    'for_interview':     'For_Interview',
    'for interview':     'For_Interview',
    'for_approval':      'For_Approval',
    'for approval':      'For_Approval',
}

def normalize_status(row):
    raw = (row.get('status') or 'Pending').strip()
    row['status'] = _STATUS_MAP.get(raw.lower(), raw)
    return row

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
        first_name        = request.form['first_name'].strip().title()
        middle_name       = request.form['middle_name'].strip().title()
        last_name         = request.form['last_name'].strip().title()
        extension_name    = request.form['extension_name'].strip().title()
        age               = request.form['age']
        sex               = request.form['sex']
        contact_number    = request.form['contact_number'].strip()
        email             = request.form['email'].strip().lower()
        permanent_address = request.form['permanent_address'].strip().title()
        current_address   = request.form['current_address'].strip().title()
        applicant_type    = request.form['applicant_type']
        
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
            try:
                student_number = request.form['student_number'].strip().upper()
                program = request.form['program'].strip().title()
                year_level = request.form['year_level'].strip()

                cur.execute("""
                    INSERT INTO student_info 
                    (application_id, student_number, program, year_level)
                    VALUES (%s, %s, %s, %s)
                """, (application_id, student_number, program, year_level))

                # FILE
                file = request.files.get('enrollment_slip')
                if file and file.filename != "":
                    unique_name = str(uuid.uuid4()) + "_" + file.filename
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
                    file.save(filepath)

                    cur.execute("""
                        INSERT INTO requirements_tb (application_id, file_name, file_type)
                        VALUES (%s, %s, %s)
                    """, (application_id, unique_name, 'Enrollment'))
            except KeyError as e:
                mysql.connection.rollback()
                cur.close()
                return render_template(
                    "application.html",
                    success=False,
                    error=True,
                    message=f"Missing required student information: {str(e).replace('\'', '')}",
                    period_name=period_name
                )

        #EMPLOYEE
        elif applicant_type == "employee":
            try:
                employee_number = request.form['employee_number'].strip().upper()
                department = request.form['department'].strip().title()
                position = request.form['position'].strip().title()

                cur.execute("""
                    INSERT INTO employee_info
                    (application_id, employee_number, department, position)
                    VALUES (%s, %s, %s, %s)
                """, (application_id, employee_number, department, position))

                # FILE
                file = request.files.get('certificate')
                if file and file.filename != "":
                    unique_name = str(uuid.uuid4()) + "_" + file.filename
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
                    file.save(filepath)

                    cur.execute("""
                        INSERT INTO requirements_tb (application_id, file_name, file_type)
                        VALUES (%s, %s, %s)
                    """, (application_id, unique_name, 'Employment'))
            except KeyError as e:
                mysql.connection.rollback()
                cur.close()
                return render_template(
                    "application.html",
                    success=False,
                    error=True,
                    message=f"Missing required employee information: {str(e).replace('\'', '')}",
                    period_name=period_name
                )     

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
    cur.execute("SELECT COUNT(*) FROM residents_tb WHERE is_archived = 0 AND (status = 'Active' OR status IS NULL) AND end_date IS NULL")
    total_residents = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM applications_tb WHERE status='Pending'")
    pending_applications = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM beds_tb WHERE status='Available'")
    available_beds = cur.fetchone()[0]

    cur.execute("""
        SELECT COUNT(*) FROM residents_tb
        LEFT JOIN payment_tb ON residents_tb.resident_id = payment_tb.resident_id
        WHERE (payment_tb.status = 'Pending' OR payment_tb.status IS NULL)
        AND residents_tb.is_archived = 0
        AND (residents_tb.status = 'Active' OR residents_tb.status IS NULL)
        AND residents_tb.end_date IS NULL
    """)
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
        SELECT
            residents_tb.resident_id,
            residents_tb.bed_id,
            residents_tb.start_date,
            residents_tb.end_date,
            residents_tb.is_archived,
            CONCAT(applications_tb.first_name, ' ', applications_tb.last_name) AS full_name,
            applications_tb.email,
            applications_tb.contact_number,
            applications_tb.applicant_type,
            applications_tb.sex,
            COALESCE(student_info.student_number, employee_info.employee_number) AS id_number,
            CASE
                WHEN beds_tb.bed_id IS NOT NULL
                THEN CONCAT('Room ', rooms_tb.room_number, ' - Bed ', beds_tb.bed_number)
                ELSE NULL
            END AS assigned_room
        FROM residents_tb
        LEFT JOIN applications_tb ON residents_tb.application_id = applications_tb.application_id
        LEFT JOIN student_info ON residents_tb.application_id = student_info.application_id
        LEFT JOIN employee_info ON residents_tb.application_id = employee_info.application_id
        LEFT JOIN beds_tb ON residents_tb.bed_id = beds_tb.bed_id
        LEFT JOIN rooms_tb ON beds_tb.room_id = rooms_tb.room_id
        WHERE residents_tb.is_archived = 0
    """
    params = []

    if applicant_type != 'all':
        query += " AND applications_tb.applicant_type = %s"
        params.append(applicant_type)

    if sex != 'all':
        query += " AND applications_tb.sex = %s"
        params.append(sex)

    query += " ORDER BY applications_tb.first_name ASC"

    cur.execute(query, params)
    residents = cur.fetchall()

    # Approved applicants not yet added as residents
    cur.execute("""
        SELECT
            application_id,
            CONCAT(first_name, ' ', last_name) AS full_name,
            applicant_type
        FROM applications_tb
        WHERE status = 'Approved'
        AND application_id NOT IN (
            SELECT application_id FROM residents_tb
            WHERE application_id IS NOT NULL
        )
        ORDER BY first_name ASC
    """)
    applicants = cur.fetchall()

    cur.close()

    return render_template('residents.html', residents=residents, applicants=applicants)

# Resident Info (JSON for View Info modal)
@app.route('/get_resident_info/<int:resident_id>')
def get_resident_info(resident_id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cur.execute("""
        SELECT
            residents_tb.resident_id,
            residents_tb.start_date,
            residents_tb.end_date,
            applications_tb.application_id,
            applications_tb.applicant_number,
            applications_tb.first_name,
            applications_tb.middle_name,
            applications_tb.last_name,
            applications_tb.extension_name,
            applications_tb.age,
            applications_tb.sex,
            applications_tb.email,
            applications_tb.contact_number,
            applications_tb.permanent_address,
            applications_tb.current_address,
            applications_tb.applicant_type,
            applications_tb.created_at,
            CASE
                WHEN beds_tb.bed_id IS NOT NULL
                THEN CONCAT('Room ', rooms_tb.room_number, ' - Bed ', beds_tb.bed_number)
                ELSE NULL
            END AS assigned_room
        FROM residents_tb
        JOIN applications_tb ON residents_tb.application_id = applications_tb.application_id
        LEFT JOIN beds_tb ON residents_tb.bed_id = beds_tb.bed_id
        LEFT JOIN rooms_tb ON beds_tb.room_id = rooms_tb.room_id
        WHERE residents_tb.resident_id = %s
    """, (resident_id,))

    data = cur.fetchone()

    if not data:
        cur.close()
        return {'success': False}

    # Convert dates to strings for JSON
    if data.get('start_date'):
        data['start_date'] = data['start_date'].strftime('%B %d, %Y')
    if data.get('end_date'):
        data['end_date'] = data['end_date'].strftime('%B %d, %Y')
    if data.get('created_at'):
        data['created_at'] = data['created_at'].strftime('%B %d, %Y')

    # Get student or employee info
    app_id = data['application_id']
    if data['applicant_type'].lower() == 'student':
        cur.execute("""
            SELECT student_number, program, year_level
            FROM student_info WHERE application_id = %s
        """, (app_id,))
        extra = cur.fetchone()
        data['extra'] = extra or {}
    else:
        cur.execute("""
            SELECT employee_number, department, position
            FROM employee_info WHERE application_id = %s
        """, (app_id,))
        extra = cur.fetchone()
        data['extra'] = extra or {}

    cur.close()
    data['success'] = True
    return data

#Application Details
@app.route('/applications')
def applications():
    applicant_type = request.args.get('applicant_type', 'all')
    status = request.args.get('status', 'all')

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    query = """
        SELECT
            applications_tb.*,
            interview_sched.status AS interview_status,
            interview_sched.interview_date,
            interview_sched.interview_time
        FROM applications_tb
        LEFT JOIN interview_sched
            ON applications_tb.application_id = interview_sched.application_id
        WHERE 1=1
    """
    params = []

    if applicant_type != 'all':
        query += " AND applications_tb.applicant_type = %s"
        params.append(applicant_type)

    if status != 'all':
        if status == 'Approved':
            query += " AND applications_tb.status IN ('Approved', 'Approved and Done')"
        elif status == 'For_Approval':
            query += " AND applications_tb.status IN ('For_Approval', 'For Approval')"
        else:
            query += " AND applications_tb.status = %s"
            params.append(status)

    cur.execute(query, params)
    data = [normalize_status(row) for row in cur.fetchall()]
    cur.close()

    return render_template('applications.html', applications=data)

@app.route('/add_resident', methods=['POST'])
def add_resident():
    application_id = request.form['application_id']
    start_date = request.form['start_date']

    cur = mysql.connection.cursor()

    cur.execute("""
        INSERT INTO residents_tb (application_id, start_date)
        VALUES (%s, %s)
    """, (application_id, start_date))

    resident_id = cur.lastrowid

    cur.execute("""
        INSERT INTO payment_tb (resident_id, status)
        VALUES (%s, 'Pending')
    """, (resident_id,))

    mysql.connection.commit()

    cur.execute("""
        SELECT CONCAT(first_name, ' ', last_name) AS full_name
        FROM applications_tb WHERE application_id = %s
    """, (application_id,))
    row = cur.fetchone()
    cur.close()

    if row:
        _log_activity(f"New resident added: {row[0]}")

    return redirect('/residents')


@app.route('/set_end_date', methods=['POST'])
def set_end_date():
    data = request.get_json()
    resident_id = data.get('resident_id')
    end_date = data.get('end_date')

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Get bed_id before clearing it
    cur.execute("SELECT bed_id, residents_tb.resident_id, CONCAT(a.first_name,' ',a.last_name) AS full_name FROM residents_tb JOIN applications_tb a ON residents_tb.application_id = a.application_id WHERE resident_id = %s", (resident_id,))
    resident = cur.fetchone()

    # Set end_date and mark inactive
    cur.execute("UPDATE residents_tb SET end_date = %s, bed_id = NULL, status = 'Inactive' WHERE resident_id = %s", (end_date, resident_id))

    # Free the bed
    if resident and resident['bed_id']:
        cur.execute("UPDATE beds_tb SET status = 'Available' WHERE bed_id = %s", (resident['bed_id'],))

    mysql.connection.commit()
    cur.close()

    if resident:
        _log_activity(f"Resident stay ended: {resident['full_name']} (End date: {end_date})")

    return {'success': True}


@app.route('/archive_resident', methods=['POST'])
def archive_resident():
    data = request.get_json()
    resident_id = data.get('resident_id')

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Only archive if end_date is set
    cur.execute("SELECT end_date, CONCAT(a.first_name,' ',a.last_name) AS full_name FROM residents_tb JOIN applications_tb a ON residents_tb.application_id = a.application_id WHERE resident_id = %s", (resident_id,))
    resident = cur.fetchone()

    if not resident or not resident['end_date']:
        cur.close()
        return {'success': False, 'message': 'Cannot archive a resident without an end date.'}

    cur.execute("UPDATE residents_tb SET is_archived = 1, status = 'Inactive' WHERE resident_id = %s", (resident_id,))
    mysql.connection.commit()
    cur.close()

    _log_activity(f"Resident archived: {resident['full_name']}")
    return {'success': True}


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

    normalize_status(application)
    
    # Get student or employee info
    if application['applicant_type'].lower() == 'student':
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

    applicant = _get_applicant_for_email(app_id)
    if applicant:
        send_interview_email(applicant, interview_date, interview_time)
        _log_activity(f"Interview scheduled for {applicant['full_name']} on {interview_date}")

    return {'success': True, 'message': f'Interview {"created" if rows_affected == 1 else "updated"}!'}

# Update Interview Status
@app.route('/update_interview_status', methods=['POST'])
def update_interview_status():
    data = request.get_json()
    app_id = data.get('application_id')
    interview_status = data.get('interview_status')

    cur = mysql.connection.cursor()

    cur.execute("""
        UPDATE interview_sched
        SET status = %s
        WHERE application_id = %s
    """, (interview_status, app_id))

    # Drive application status based on interview outcome
    if interview_status == 'no_show':
        cur.execute("""
            UPDATE applications_tb SET status = 'Rejected'
            WHERE application_id = %s
        """, (app_id,))
    elif interview_status == 'completed':
        cur.execute("""
            UPDATE applications_tb SET status = 'For_Approval'
            WHERE application_id = %s
        """, (app_id,))

    mysql.connection.commit()
    cur.close()

    applicant = _get_applicant_for_email(app_id)
    if interview_status == 'no_show':
        if applicant:
            send_rejected_email(applicant)
            _log_activity(f"Application rejected (no-show): {applicant['full_name']}")
    elif interview_status == 'completed':
        if applicant:
            _log_activity(f"Interview completed: {applicant['full_name']}")

    return {'success': True, 'message': f'Interview status updated to {interview_status}'}

# Update Application Status
@app.route('/update_application_status', methods=['POST'])
def update_application_status():

    data = request.get_json()

    app_id = data.get('application_id')
    status = data.get('status')

    cur = mysql.connection.cursor()

    cur.execute("""
        UPDATE applications_tb
        SET status = %s
        WHERE application_id = %s
    """, (status, app_id))

    mysql.connection.commit()
    cur.close()

    applicant = _get_applicant_for_email(app_id)
    if applicant:
        if status == 'Approved':
            send_approved_email(applicant)
            _log_activity(f"Application approved: {applicant['full_name']}")
        elif status == 'Rejected':
            send_rejected_email(applicant)
            _log_activity(f"Application rejected: {applicant['full_name']}")

    return {'success': True}

# =========================
# ROOMS & BEDS PAGE
# =========================
@app.route('/rooms_bed')
def rooms_bed():

    applicant_type_filter = request.args.get('applicant_type', 'all')

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # ROOMS — filter by building's applicant_type
    room_query = """
        SELECT rooms_tb.*, building_tb.building_name, building_tb.applicant_type
        FROM rooms_tb
        JOIN building_tb ON rooms_tb.building_id = building_tb.building_id
    """
    room_params = []
    if applicant_type_filter != 'all':
        room_query += " WHERE building_tb.applicant_type = %s"
        room_params.append(applicant_type_filter)
    room_query += " ORDER BY building_tb.building_name ASC, rooms_tb.room_number ASC"

    cur.execute(room_query, room_params)
    rooms = cur.fetchall()

    room_data = []
    available_beds = 0

    for room in rooms:

        cur.execute("""
            SELECT
                beds_tb.*,
                applications_tb.first_name,
                applications_tb.last_name

            FROM beds_tb

            LEFT JOIN residents_tb
            ON beds_tb.bed_id = residents_tb.bed_id

            LEFT JOIN applications_tb
            ON residents_tb.application_id = applications_tb.application_id

            WHERE beds_tb.room_id = %s

            ORDER BY beds_tb.bed_number ASC
        """, (room['room_id'],))

        beds = cur.fetchall()

        for bed in beds:
            if bed['status'] == 'Available':
                available_beds += 1

        room_data.append({
            "room_id": room['room_id'],
            "room_number": room['room_number'],
            "capacity": room['capacity'],
            "building_name": room['building_name'],
            "applicant_type": room['applicant_type'],
            "beds": beds
        })

    cur.execute("SELECT * FROM building_tb")
    buildings = cur.fetchall()

    cur.execute("""
        SELECT
            residents_tb.resident_id,
            CONCAT(applications_tb.first_name, ' ', applications_tb.last_name) AS full_name
        FROM residents_tb
        JOIN applications_tb
            ON residents_tb.application_id = applications_tb.application_id
        WHERE residents_tb.bed_id IS NULL
        AND residents_tb.is_archived = 0
        AND residents_tb.end_date IS NULL
        ORDER BY applications_tb.first_name ASC
    """)
    residents = cur.fetchall()

    cur.close()

    return render_template(
        'rooms_bed.html',
        rooms=room_data,
        residents=residents,
        available_beds=available_beds,
        buildings=buildings
    )

@app.route('/add_building', methods=['POST'])
def add_building():

    building_name = request.form['building_name']
    applicant_type = request.form['applicant_type']

    cur = mysql.connection.cursor()

    cur.execute("""

        INSERT INTO building_tb
        (
            building_name,
            applicant_type
        )

        VALUES (%s,%s)

    """, (

        building_name,
        applicant_type

    ))

    mysql.connection.commit()
    cur.close()

    _log_activity(f"New building added: {building_name} ({applicant_type})")
    return redirect('/rooms_bed')

@app.route('/add_room', methods=['POST'])
def add_room():

    building_id = request.form['building_id']
    room_number = request.form['room_number']
    capacity = int(request.form['capacity'])

    cur = mysql.connection.cursor()

    # INSERT ROOM
    cur.execute("""
        INSERT INTO rooms_tb
        (building_id, room_number, capacity)
        VALUES (%s, %s, %s)
    """, (building_id, room_number, capacity))

    mysql.connection.commit()

    room_id = cur.lastrowid

    # CREATE BEDS
    for i in range(1, capacity + 1):

        cur.execute("""
            INSERT INTO beds_tb
            (room_id, bed_number, status)
            VALUES (%s, %s, %s)
        """, (room_id, i, 'Available'))

    mysql.connection.commit()
    cur.close()

    return redirect('/rooms_bed')

@app.route('/add_bed', methods=['POST'])
def add_bed():

    room_id = request.form['room_id']
    bed_number = request.form['bed_number']
    status = request.form['status']

    cur = mysql.connection.cursor()

    cur.execute("""

        INSERT INTO beds_tb
        (
            room_id,
            bed_number,
            status
        )

        VALUES (%s, %s, %s)

    """, (

        room_id,
        bed_number,
        status

    ))

    mysql.connection.commit()

    cur.close()

    return redirect('/rooms_bed')

# =========================
# ASSIGN BED
# =========================

@app.route('/assign_bed', methods=['POST'])
def assign_bed():

    resident_id = request.form['resident_id']
    bed_id = request.form['bed_id']

    cur = mysql.connection.cursor()

    # =========================
    # ASSIGN BED TO RESIDENT
    # =========================

    cur.execute("""

        UPDATE residents_tb

        SET bed_id = %s

        WHERE resident_id = %s

    """, (bed_id, resident_id))

    # =========================
    # UPDATE BED STATUS
    # =========================

    cur.execute("""

        UPDATE beds_tb

        SET status = 'Occupied'

        WHERE bed_id = %s

    """, (bed_id,))

    mysql.connection.commit()
    cur.close()

    try:
        cur2 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur2.execute("""
            SELECT CONCAT(a.first_name,' ',a.last_name) AS full_name,
                   r.room_number, b.bed_number
            FROM residents_tb rt
            JOIN applications_tb a ON rt.application_id = a.application_id
            JOIN beds_tb b ON b.bed_id = %s
            JOIN rooms_tb r ON b.room_id = r.room_id
            WHERE rt.resident_id = %s
        """, (bed_id, resident_id))
        info = cur2.fetchone()
        cur2.close()
        if info:
            _log_activity(f"Bed assigned: {info['full_name']} → Room {info['room_number']} Bed {info['bed_number']}")
    except Exception as e:
        print(f"[Assign log error] {e}")

    next_url = request.form.get('next', '/rooms_bed')
    return redirect(next_url)

@app.route('/api/dashboard_stats')
def dashboard_stats():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cur.execute("""
        SELECT COUNT(*) AS total FROM residents_tb
        JOIN applications_tb ON residents_tb.application_id = applications_tb.application_id
        WHERE LOWER(applications_tb.applicant_type) IN ('student', 'employee')
        AND residents_tb.is_archived = 0
        AND (residents_tb.status = 'Active' OR residents_tb.status IS NULL)
        AND residents_tb.end_date IS NULL
    """)
    total_residents = cur.fetchone()['total']

    cur.execute("""
        SELECT COUNT(*) AS total FROM residents_tb
        JOIN applications_tb ON residents_tb.application_id = applications_tb.application_id
        WHERE LOWER(applications_tb.applicant_type) = 'student'
        AND residents_tb.is_archived = 0
        AND (residents_tb.status = 'Active' OR residents_tb.status IS NULL)
        AND residents_tb.end_date IS NULL
    """)
    student_count = cur.fetchone()['total']

    cur.execute("""
        SELECT COUNT(*) AS total FROM residents_tb
        JOIN applications_tb ON residents_tb.application_id = applications_tb.application_id
        WHERE LOWER(applications_tb.applicant_type) = 'employee'
        AND residents_tb.is_archived = 0
        AND (residents_tb.status = 'Active' OR residents_tb.status IS NULL)
        AND residents_tb.end_date IS NULL
    """)
    employee_count = cur.fetchone()['total']

    cur.close()

    return {
        'total_residents': total_residents,
        'student_count':   student_count,
        'employee_count':  employee_count
    }


@app.route('/api/new_applications_count')
def new_applications_count():
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM applications_tb WHERE status = 'Pending'")
    count = cur.fetchone()[0]
    cur.close()
    return {'count': count}

@app.route('/api/pending_applications')
def pending_applications_api():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("""
        SELECT application_id,
               applicant_number,
               CONCAT(first_name, ' ', last_name) AS full_name,
               applicant_type,
               created_at
        FROM applications_tb
        WHERE status = 'Pending'
        ORDER BY created_at DESC
        LIMIT 15
    """)
    rows = cur.fetchall()
    cur.close()
    return {'applications': [
        {
            'id': r['application_id'],
            'number': r['applicant_number'],
            'name': r['full_name'],
            'type': r['applicant_type'],
            'date': r['created_at'].strftime('%b %d, %Y')
        }
        for r in rows
    ]}

@app.route('/api/recent_activities')
def recent_activities():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("""
        SELECT action, created_at
        FROM activity_log
        WHERE DATE(created_at) = CURDATE()
        ORDER BY created_at DESC
        LIMIT 10
    """)
    rows = cur.fetchall()
    cur.close()
    return {
        'activities': [
            {'action': r['action'], 'time': r['created_at'].strftime('%b %d, %Y %I:%M %p')}
            for r in rows
        ]
    }


@app.route('/payments')
def payments():
    applicant_type = request.args.get('applicant_type', 'all')
    pay_status = request.args.get('status', 'all')

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    query = """
        SELECT
            residents_tb.resident_id,
            CONCAT(applications_tb.first_name, ' ', applications_tb.last_name) AS full_name,
            applications_tb.applicant_type,
            CASE
                WHEN beds_tb.bed_id IS NOT NULL
                THEN CONCAT('Room ', rooms_tb.room_number, ' — Bed ', beds_tb.bed_number)
                ELSE 'Unassigned'
            END AS assigned_room,
            COALESCE(payment_tb.status, 'Pending') AS payment_status,
            payment_tb.payment_date
        FROM residents_tb
        JOIN applications_tb ON residents_tb.application_id = applications_tb.application_id
        LEFT JOIN beds_tb ON residents_tb.bed_id = beds_tb.bed_id
        LEFT JOIN rooms_tb ON beds_tb.room_id = rooms_tb.room_id
        LEFT JOIN payment_tb ON residents_tb.resident_id = payment_tb.resident_id
        WHERE applications_tb.applicant_type IN ('student', 'Student', 'employee', 'Employee')
        AND residents_tb.is_archived = 0
        AND (residents_tb.status = 'Active' OR residents_tb.status IS NULL)
        AND residents_tb.end_date IS NULL
    """
    params = []

    if applicant_type != 'all':
        query += " AND applications_tb.applicant_type = %s"
        params.append(applicant_type)

    if pay_status != 'all':
        if pay_status == 'Pending':
            query += " AND (payment_tb.status = 'Pending' OR payment_tb.status IS NULL)"
        else:
            query += " AND payment_tb.status = %s"
            params.append(pay_status)

    query += " ORDER BY applications_tb.first_name ASC"

    cur.execute(query, params)
    payments_data = cur.fetchall()
    cur.close()

    return render_template('payments.html', payments=payments_data)


@app.route('/mark_paid', methods=['POST'])
def mark_paid():
    data = request.get_json()
    resident_id = data.get('resident_id')
    payment_date = data.get('payment_date')

    cur = mysql.connection.cursor()

    cur.execute("SELECT payment_id FROM payment_tb WHERE resident_id = %s", (resident_id,))
    existing = cur.fetchone()

    if existing:
        cur.execute("""
            UPDATE payment_tb SET status = 'Paid', payment_date = %s
            WHERE resident_id = %s
        """, (payment_date, resident_id))
    else:
        cur.execute("""
            INSERT INTO payment_tb (resident_id, status, payment_date)
            VALUES (%s, 'Paid', %s)
        """, (resident_id, payment_date))

    cur.execute("""
        SELECT CONCAT(a.first_name,' ',a.last_name) AS full_name
        FROM residents_tb rt
        JOIN applications_tb a ON rt.application_id = a.application_id
        WHERE rt.resident_id = %s
    """, (resident_id,))
    row = cur.fetchone()

    mysql.connection.commit()
    cur.close()

    if row:
        _log_activity(f"Payment marked as Paid: {row[0]}")

    return {'success': True}

@app.route('/send_payment_reminder', methods=['POST'])
def send_payment_reminder():
    data        = request.get_json()
    resident_id = data.get('resident_id')

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("""
        SELECT
            CONCAT(applications_tb.first_name, ' ', applications_tb.last_name) AS full_name,
            applications_tb.contact_number
        FROM residents_tb
        JOIN applications_tb ON residents_tb.application_id = applications_tb.application_id
        WHERE residents_tb.resident_id = %s
    """, (resident_id,))
    resident = cur.fetchone()
    cur.close()

    if not resident or not resident.get('contact_number'):
        return {'success': False, 'message': 'Resident or contact number not found'}, 404

    name   = resident['full_name']
    number = resident['contact_number']

    message = f"Hi {name}, your DormEase dorm payment is PENDING. Please settle it at your earliest convenience. Thank you!"

    ok = _send_sms(number, message)

    if ok:
        return {'success': True,  'message': f'Reminder sent to {number}'}
    else:
        return {'success': False, 'message': 'SMS gateway error — please try again later'}


@app.route('/test_email')
def test_email():
    to = request.args.get('to', '')
    if not to:
        return {
            'success': False,
            'message': 'Provide a recipient: /test_email?to=you@example.com'
        }, 400

    html = _email_wrapper(
        "🔧 Test Email",
        "#3b3b98",
        """
        <p style="font-size:15px;color:#333;">Hello from <strong>DormEase</strong>!</p>
        <p style="color:#555;line-height:1.7;">
            This is a test email to confirm that the Resend API is connected
            and working correctly. If you received this, the email system is live.
        </p>
        <p style="color:#3b3b98;font-weight:600;margin-top:24px;">— The DormEase Team</p>
        """
    )

    ok = _send_email(to, "DormEase – Email Test", html)

    if ok:
        return {'success': True,  'message': f'Test email sent to {to}'}
    else:
        return {'success': False, 'message': 'Resend API call failed — check server logs'}, 500


@app.route('/settings')
def settings():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Fetch all archived residents with their info, including the period they applied in
    cur.execute("""
        SELECT
            residents_tb.resident_id,
            residents_tb.start_date,
            residents_tb.end_date,
            CONCAT(applications_tb.first_name, ' ', applications_tb.last_name) AS full_name,
            applications_tb.applicant_type,
            COALESCE(student_info.student_number, employee_info.employee_number) AS id_number,
            COALESCE(application_period.name, 'Unassigned Period') AS period_name,
            CASE
                WHEN beds_tb.bed_id IS NOT NULL
                THEN CONCAT('Room ', rooms_tb.room_number, ' - Bed ', beds_tb.bed_number)
                ELSE NULL
            END AS assigned_room
        FROM residents_tb
        LEFT JOIN applications_tb ON residents_tb.application_id = applications_tb.application_id
        LEFT JOIN application_period ON applications_tb.period_id = application_period.period_id
        LEFT JOIN student_info ON residents_tb.application_id = student_info.application_id
        LEFT JOIN employee_info ON residents_tb.application_id = employee_info.application_id
        LEFT JOIN beds_tb ON residents_tb.bed_id = beds_tb.bed_id
        LEFT JOIN rooms_tb ON beds_tb.room_id = rooms_tb.room_id
        WHERE residents_tb.is_archived = 1
        ORDER BY application_period.start_date ASC, residents_tb.start_date ASC
    """)
    archived = cur.fetchall()

    cur.close()

    # Group archived residents by their application period
    grouped = {}
    for resident in archived:
        period_name = resident['period_name']
        if period_name not in grouped:
            grouped[period_name] = []
        grouped[period_name].append(resident)

    # Format dates for display
    for resident in archived:
        if resident.get('start_date'):
            resident['start_date_display'] = resident['start_date'].strftime('%b %d, %Y')
        else:
            resident['start_date_display'] = '—'
        if resident.get('end_date'):
            resident['end_date_display'] = resident['end_date'].strftime('%b %d, %Y')
        else:
            resident['end_date_display'] = '—'

    return render_template('settings.html', grouped=grouped)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)