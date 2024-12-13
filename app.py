from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os

app = Flask(__name__)

# Use environment variables to set PostgreSQL config
app.config['DB_HOST'] = os.getenv('DB_HOST', 'dpg-ctdsv6lumphs73988rm0-a')  # PostgreSQL host (Render will provide this)
app.config['DB_NAME'] = os.getenv('DB_NAME', 'social_media_usage_data')  # Database name
app.config['DB_USER'] = os.getenv('DB_USER', 'ronitbhowmick')  # PostgreSQL username
app.config['DB_PASSWORD'] = os.getenv('DB_PASSWORD', 'a9wRl3FU2krAeMWy9x5Jm4vcHU8AMJ5w')  # PostgreSQL password

# PostgreSQL connection
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=app.config['DB_HOST'],
            database=app.config['DB_NAME'],
            user=app.config['DB_USER'],
            password=app.config['DB_PASSWORD']
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

# Check if the 'student_profile' table exists in the database
def check_table_exists():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT to_regclass('public.student_profile');")
            result = cursor.fetchone()
            if result[0] is None:
                print("Table does not exist!")
            else:
                print("Table exists!")
        except Exception as e:
            print(f"Error checking table: {e}")
        finally:
            cursor.close()
            conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        # Retrieve data from form
        class_roll = request.form['class_roll']
        name = request.form['name']
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
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO student_profile (class_roll, name, age, gender, major, social_media_time, class_participation, 
                                               in_club, library_visits, sleep_duration, sleep_time, wake_time, study_hours, current_gpa, device_used, social_media_app)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''', (name, class_roll, age, gender, major, social_media_time, class_participation, in_club, library_visits, 
                      sleep_duration, sleep_time, wake_time, study_hours, current_gpa, device_used, social_media_app))
                conn.commit()
            except Exception as e:
                print(f"Error inserting data: {e}")
            finally:
                cursor.close()
                conn.close()
        
        # Redirect to a confirmation page or back to home
        return redirect(url_for('index'))

if __name__ == '__main__':
    check_table_exists()  # Ensure table exists before starting the app
    app.run(host='0.0.0.0', port=5000)
