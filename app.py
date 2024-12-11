from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import os

app = Flask(__name__)

# Use Heroku's environment variables to connect to the database
app.config['MYSQL_HOST'] = os.environ.get('CLEARDB_DATABASE_URL', 'localhost') 
app.config['MYSQL_USER'] = os.environ.get('CLEARDB_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.environ.get('CLEARDB_PASSWORD', 'your_password')
app.config['MYSQL_DB'] = os.environ.get('CLEARDB_DATABASE', 'social_media_usage_data')

mysql = MySQL(app)

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        # Retrieve data from form
        name = request.form['name']
        class_roll = request.form['class_roll']
        age = request.form['age']
        gender = request.form['gender']
        major = request.form['major']
        social_media_time = request.form['social_media_time']
        class_participation = request.form['class_participation']
        in_club = request.form['in_club']
        library_visits = request.form['library_visits']
        sleep_duration = request.form['sleep_duration']
        sleep_time = request.form['sleep_time']
        wake_time = request.form['wake_time']
        study_hours = request.form['study_hours']
        current_gpa = request.form['current_gpa']
        device_used = request.form['device_used']
        social_media_app = request.form['social_media_app']
        
        # Prepare SQL query to insert data into the database
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO student_profile (name, class_roll, age, gender, major, social_media_time, class_participation, 
                        in_club, library_visits, sleep_duration, sleep_time, wake_time, study_hours, current_gpa, device_used, social_media_app)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                        (name, class_roll, age, gender, major, social_media_time, class_participation, in_club, library_visits, 
                         sleep_duration, sleep_time, wake_time, study_hours, current_gpa, device_used, social_media_app))
        mysql.connection.commit()
        cursor.close()

        # Redirect to a confirmation page or back to home
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
