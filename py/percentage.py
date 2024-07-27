import sqlite3
from datetime import datetime

# Connect to SQLite database
conn = sqlite3.connect(r'C:\sqlite\gui\attendance')
cursor = conn.cursor()

def calculate_attendance_statistics():
    today = datetime.now().date()

    # Get the total number of school days (excluding weekends and holidays)
    cursor.execute("SELECT DISTINCT date FROM attendance_daily")
    school_days = {row[0] for row in cursor.fetchall()}

    # Get all students
    cursor.execute("SELECT student_id, name FROM students")
    students = cursor.fetchall()

    stats = []

    for student_id, name in students:
        # Get attendance records for the student
        cursor.execute("SELECT date, attended FROM attendance_daily WHERE student_id = ?", (student_id,))
        records = cursor.fetchall()

        total_days_attended = sum(1 for date, attended in records if attended)
        total_days_recorded = len(records)

        if total_days_recorded == 0:
            attendance_percentage = 0
        else:
            attendance_percentage = (total_days_attended / len(school_days)) * 100
        
        stats.append({
            'student_id': student_id,
            'name': name,
            'attendance_percentage': round(attendance_percentage, 2),
            'total_days_recorded': total_days_recorded,
            'total_days_attended': total_days_attended
        })

    return stats

# Example usage
attendance_stats = calculate_attendance_statistics()
for stat in attendance_stats:
    print(stat)

# Close the connection
conn.close()
