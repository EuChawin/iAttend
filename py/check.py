import sqlite3
from datetime import datetime

# Connect to SQLite database
conn = sqlite3.connect(r'C:\sqlite\gui\attendance')
cursor = conn.cursor()

def mark_absent_for_today():
    # Get the current date
    today = datetime.now().strftime('%Y-%m-%d')

    # Get the list of all student IDs
    cursor.execute("SELECT student_id FROM students")
    student_ids = [row[0] for row in cursor.fetchall()]

    # Get the list of students who tapped their cards today
    cursor.execute("SELECT DISTINCT student_id FROM attendance_daily WHERE date = ?", (today,))
    students_tapped = [row[0] for row in cursor.fetchall()]

    # Mark students who didn't tap their cards as absent
    for student_id in student_ids:
        if student_id not in students_tapped:
            cursor.execute(
                "INSERT INTO attendance_daily (student_id, date, attended) VALUES (?, ?, 0) "
                "ON CONFLICT(student_id, date) DO UPDATE SET attended=0", 
                (student_id, today)
            )
    
    conn.commit()
    print(f"Attendance for {today} has been updated.")

# Run the function
mark_absent_for_today()

# Close the connection
conn.close()
