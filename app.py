from flask import Flask, request, render_template, redirect, url_for, flash
from flask_mysqldb import MySQL
from config import Config
import MySQLdb.cursors

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = "secret123"

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')



@app.route('/application', methods = ['GET', 'POST'])
def application():
    if request.method == 'POST':
        first_name = request.form['first_name']
        middle_name = request.form['middle_name']
        last_name = request.form['last_name']
        extension_name = request.form['extension_name']
        age = request.form['age']
        sex = request.form['sex']
        contact_number = request.form['contact_number']
        permanent_address= request.form['permanent_address']
        current_address = request.form['current_address']
        applicant_type = request.form['applicant_type']
        
        cur = mysql.connection.cursor()

        cur.execute("""
            INSERT INTO application_tb 
            (first_name, middle_name, last_name, extension_name, age, sex, contact_number, permanent_address, current_address, applicant_type) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            first_name, middle_name, last_name, extension_name, age, sex,
            contact_number, permanent_address, current_address, applicant_type
        ))

        mysql.connection.commit()
        cur.close()

        return "Application submitted successfully!"
    
    return render_template('application.html')



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
            return f"Welcome back, {user['username']}!"  # later: redirect
        else:
            flash("Invalid username or password!")
            return redirect(url_for('login'))  # go back to login page

    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)