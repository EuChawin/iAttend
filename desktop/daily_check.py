import database
from datetime import datetime

def update_daily_attendance():
    conn = database.get_connection()
    cursor = conn.cursor()
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    try:
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
    finally:
        conn.close()

if __name__ == "__main__":
    # Run the function
    update_daily_attendance()
