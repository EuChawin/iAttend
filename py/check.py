import sqlite3
from datetime import datetime

# Connect to SQLite database
conn = sqlite3.connect(r'C:\sqlite\gui\attendance')  # Adjust path as per your setup
cursor = conn.cursor()

def update_daily_attendance():
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Check if attendance records for today already exist
    cursor.execute("SELECT COUNT(*) FROM attendance_daily WHERE date = ?", (today,))
    existing_records = cursor.fetchone()[0]
    
    if existing_records == 0:
        # Fetch all student IDs
        cursor.execute("SELECT student_id FROM students")
        students = cursor.fetchall()
        
        # Insert records for all students with default values
        for student in students:
            cursor.execute(
                "INSERT INTO attendance_daily (student_id, date, entry_time, exit_time, late, attended) VALUES (?, ?, NULL, NULL, 0, 0)",
                (student[0], today)
            )
    
    conn.commit()
    print(f"Updated attendance for {today}")

# Run the function
update_daily_attendance()

# Close the database connection
conn.close()
